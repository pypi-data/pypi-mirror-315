import datetime
import json
import os
import re
import shutil
from tempfile import NamedTemporaryFile

import requests

LANGUAGE_RE = re.compile(
    "^(.*_(((([A-Za-z]{2,3}(-([A-Za-z]{3}(-[A-Za-z]{3}){0,2}))?)|[A-Za-z]{4}|[A-Za-z]{5,8})(-([A-Za-z]{4}))?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*(-([0-9A-WY-Za-wy-z](-[A-Za-z0-9]{2,8})+))*(-(x(-[A-Za-z0-9]{1,8})+))?)|(x(-[A-Za-z0-9]{1,8})+)))$"  # noqa
)


def _resolve_ref(value, defs, registry=None):
    if value["$ref"].startswith("urn:"):
        subschema = registry.contents(value["$ref"].split("#")[0])
        if "#/$defs/" in value["$ref"]:
            name = value["$ref"].split("$defs/")[-1]
            defs = subschema["$defs"]
            subschema = defs[name]
        return subschema
    elif value["$ref"].startswith("#/$defs/"):
        name = value["$ref"].split("$defs/")[-1]
        return defs[name]


def _process_items(schema_dict, registry=None, defs=None):
    items_schema_dicts = []
    if "oneOf" in schema_dict["items"] and isinstance(
        schema_dict["items"]["oneOf"], list
    ):
        for oneOf in schema_dict["items"]["oneOf"]:
            items_schema_dicts.append(oneOf)
    elif "$ref" in schema_dict["items"]:
        if schema_dict["items"]["$ref"].startswith("urn:"):
            subschema = registry.contents(schema_dict["items"]["$ref"].split("#")[0])
            if "#/$defs/" in schema_dict["items"]["$ref"]:
                name = schema_dict["items"]["$ref"].split("$defs/")[-1]
                defs = subschema["$defs"]
                subschema = defs[name]
            items_schema_dicts.append(subschema)
        elif schema_dict["items"]["$ref"].startswith("#/$defs/"):
            name = schema_dict["items"]["$ref"].split("$defs/")[-1]
            items_schema_dicts.append(defs[name])
    elif "properties" in schema_dict["items"] and isinstance(
        schema_dict["items"]["properties"], dict
    ):
        items_schema_dicts.append(schema_dict["items"])
    return items_schema_dicts


def schema_dict_fields_generator(schema_dict, registry=None, defs=None):
    """
    Iterate over fields in the input schema (with recursion):

    Parameters:

    * schema_dict (dict): Current input schema or subset thereof.
    * registry (int, optional): Registry object from referencing package.
                    See https://referencing.readthedocs.io/ for details.
                    Contains all schema files that might be referenced.
                    Currently only urn: references are supported.
    * defs (dict, optional): Contents of "$defs" schema property.
                    This will usually only be used internally when function is
                    calling itself.

    Yields:

    * str: Contains path of field
    """
    if "$defs" in schema_dict:
        defs = schema_dict["$defs"]
    if "properties" in schema_dict and isinstance(schema_dict["properties"], dict):
        for property_name, value in schema_dict["properties"].items():
            if "$ref" in value:
                if value["$ref"].startswith("urn:"):
                    property_schema_dicts = registry.contents(
                        value["$ref"].split("#")[0]
                    )
                    if "$defs/" in value["$ref"]:
                        name = value["$ref"].split("$defs/")[-1]
                        property_schema_dicts = property_schema_dicts["$defs"][name]
                else:
                    name = value["$ref"].split("$defs/")[-1]
                    property_schema_dicts = defs[name]
                property_schema_dicts = [property_schema_dicts]
            elif (
                "items" in value
                and isinstance(value["items"], dict)
                and ("type" not in value["items"] or value["items"]["type"] == "object")
            ):
                property_schema_dicts = _process_items(
                    value, registry=registry, defs=defs
                )
            elif "oneOf" in value:
                property_schema_dicts = value["oneOf"]
            else:
                property_schema_dicts = [value]
            for property_schema_dict in property_schema_dicts:
                if not isinstance(property_schema_dict, dict):
                    continue
                if "properties" in property_schema_dict:
                    for field in schema_dict_fields_generator(
                        property_schema_dict, registry=registry, defs=defs
                    ):
                        yield f"/{property_name}{field}"
                elif "items" in property_schema_dict:
                    for field in schema_dict_fields_generator(
                        property_schema_dict["items"], registry=registry, defs=defs
                    ):
                        yield f"/{property_name}{field}"
                elif "$ref" in property_schema_dict:
                    item_schema_dict = _resolve_ref(
                        property_schema_dict, defs, registry=registry
                    )
                    for field in schema_dict_fields_generator(
                        item_schema_dict, registry=registry, defs=defs
                    ):
                        yield f"/{property_name}{field}"
                yield f"/{property_name}"
    if "allOf" in schema_dict and isinstance(schema_dict["allOf"], list):
        for clause in schema_dict["allOf"]:
            if "then" in clause and isinstance(clause["then"], dict):
                for field in schema_dict_fields_generator(
                    clause["then"], registry=registry, defs=defs
                ):
                    yield field
    if (
        "items" in schema_dict
        and isinstance(schema_dict["items"], dict)
        and (
            "type" not in schema_dict["items"]
            or schema_dict["items"]["type"] == "object"
        )
    ):
        items_schema_dicts = _process_items(schema_dict, registry=registry, defs=defs)
        for items_schema_dict in items_schema_dicts:
            for field in schema_dict_fields_generator(
                items_schema_dict, registry=registry, defs=defs
            ):
                yield field


def get_additional_fields_info(json_data, schema_fields, fields_regex=False):
    """Returns information on any additional fields that are
    in the passed data but which are NOT defined in the schema."""
    fields_present = get_fields_present_with_examples(json_data)

    additional_fields = {}
    root_additional_fields = set()

    for field, field_info in fields_present.items():
        if field in schema_fields:
            continue
        if fields_regex and LANGUAGE_RE.search(field.split("/")[-1]):
            continue

        for root_additional_field in root_additional_fields:
            if field.startswith(root_additional_field):
                field_info["root_additional_field"] = False
                additional_fields[root_additional_field][
                    "additional_field_descendance"
                ][field] = field_info
                break
        else:
            field_info["root_additional_field"] = True
            field_info["additional_field_descendance"] = {}
            root_additional_fields.add(field)

        field_info["path"] = "/".join(field.split("/")[:-1])
        field_info["field_name"] = field.split("/")[-1]
        additional_fields[field] = field_info

    return additional_fields


def get_fields_present_with_examples(*args, **kwargs):
    """Returns list of fields present in some data,
    with a count of how many times they exist and some examples of their values."""
    counter = {}
    for key, value in fields_present_generator(*args, **kwargs):
        if key not in counter:
            counter[key] = {"count": 1, "examples": []}
        else:
            counter[key]["count"] += 1
        if len(counter[key]["examples"]) < 3:
            if not isinstance(value, (list, dict)):
                counter[key]["examples"].append(value)

    return counter


def fields_present_generator(json_data, prefix=""):
    """Returns list of fields present in some data."""
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = f"{prefix}/{key}"
            yield new_key, value
            if isinstance(value, (dict, list)):
                yield from fields_present_generator(value, new_key)
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict):
                yield from fields_present_generator(item, prefix)


def _org_id_file_fresh(org_id_file_contents, check_date):
    """Unless the file was downloaded on greater than or equal to 'check_date'
    it is considered stale."""
    org_id_file_date_downloaded_date = datetime.datetime.strptime(
        org_id_file_contents.get("downloaded", "2000-1-1"), "%Y-%m-%d"
    ).date()
    return org_id_file_date_downloaded_date >= check_date


def get_orgids_prefixes(orgids_url=None):
    """Get org-ids.json file from file system
    (or fetch remotely if it doesn't exist)"""
    local_org_ids_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "org-ids.json"
    )
    today = datetime.date.today()
    if orgids_url is None:
        orgids_url = "http://org-id.guide/download.json"
    org_id_file_contents = None

    # Try to grab the data from the local filesystem
    try:
        with open(local_org_ids_file) as fp:
            org_id_file_contents = json.load(fp)
    except FileNotFoundError:
        pass

    if org_id_file_contents is None or not _org_id_file_fresh(
        org_id_file_contents, today
    ):
        # Refresh the file
        try:
            org_id_file_contents = requests.get(orgids_url).json()
        except requests.exceptions.RequestException as e:
            # We have tried locally and remotely with no luck. We have to raise.
            raise e

        org_id_file_contents["downloaded"] = "%s" % today
        # Use a tempfile and move to create new file here for atomicity
        with NamedTemporaryFile(mode="w", delete=False) as tmp:
            json.dump(org_id_file_contents, tmp, indent=2)
        shutil.move(tmp.name, local_org_ids_file)
    # Return either the original file data, if it was found to be fresh,
    # or the new data, if we were able to retrieve it.
    return [org_list["code"] for org_list in org_id_file_contents["lists"]]
