import pytest
import requests
from v1.commons.base import BASE_URL, AUTH_HEADER_ADMIN, AUTH_HEADER_MANAGER, AUTH_HEADER_CUSTOMER


@pytest.mark.parametrize('source_type, header', [('abc', AUTH_HEADER_ADMIN), ('def', AUTH_HEADER_MANAGER)])
def test_text_meta_data_api_403(source_type, header):
    url = f"{BASE_URL}/v1/core/text/?source_type={source_type}/"
    res = requests.post(url=url, headers=header)
    assert res.status_code == 400


@pytest.mark.parametrize('source_type', [('newspaper')])
def test_text_meta_data_api_200(source_type):
    url = f"{BASE_URL}/v1/core/text/?source_type={source_type}/"
    res = requests.post(url=url, headers=AUTH_HEADER_CUSTOMER)
    assert res.status_code == 403


@pytest.mark.parametrize('source_type, header', [('newspaper', AUTH_HEADER_ADMIN), ('newspaper', AUTH_HEADER_MANAGER)])
def test_text_meta_data_api_201(source_type, header):
    url = f"{BASE_URL}/v1/core/text/?source_type={source_type}/"
    res = requests.post(url=url, headers=header)
    assert res.status_code == 201
