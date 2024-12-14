from libcove2.common import get_orgids_prefixes


# Note: This test will fail if no internet access or if org-id server is down
def test_get_orgids_prefixes():

    orgids_prefixes = get_orgids_prefixes()

    assert len(orgids_prefixes) > 500
    assert "GB-COH" in orgids_prefixes
    assert "XI-LEI" in orgids_prefixes
