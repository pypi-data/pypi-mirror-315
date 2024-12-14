import json

import pytest

from libcove2.common import get_fields_present_with_examples


@pytest.fixture
def bods_data_0_4():
    """Data for BODS 0.4"""
    with open("tests/fixtures/bods-data-0-4-0.json", "r") as read_file:
        return json.load(read_file)


def test_get_fields_present_with_examples(bods_data_0_4):

    fields_present = get_fields_present_with_examples(bods_data_0_4)

    assert len(fields_present) == 46

    assert fields_present["/statementId"]["count"] == 3
    assert (
        "1dc0e987-5c57-4a1c-b3ad-61353b66a9b7"
        in fields_present["/statementId"]["examples"]
    )
    assert (
        "019a93f1-e470-42e9-957b-03559861b2e2"
        in fields_present["/statementId"]["examples"]
    )
    assert (
        "fbfd0547-d0c6-4a00-b559-5c5e91c34f5c"
        in fields_present["/statementId"]["examples"]
    )

    assert fields_present["/recordDetails/personType"]["count"] == 1
    assert fields_present["/recordDetails/personType"]["examples"] == ["knownPerson"]
