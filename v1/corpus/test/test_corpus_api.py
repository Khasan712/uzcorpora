import pytest
import requests
from v1.commons.base import BASE_URL


@pytest.mark.parametrize('id', [(1), (2)])
def test_corpus_get_api(id):
    api = f'{BASE_URL}/v1/corpus/?parent_id={id}'
    res = requests.get(api)
    assert res.status_code == 200
