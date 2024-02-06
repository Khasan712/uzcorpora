import pytest
import requests
from v1.commons.base import BASE_URL


@pytest.mark.parametrize('id', [(1), (2)])
def test_level_of_audit(id):
    url = f"{BASE_URL}/v1/core/?parent_id={id}"
    res = requests.get(url)
    assert res.status_code == 200
