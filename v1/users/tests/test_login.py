import pytest
import requests
from v1.commons.base import BASE_URL


def test_admin_and_manager_login_200():
    api = f'{BASE_URL}/v1/user/admin-manager/login/'
    data = {
        'phone_number': '0000',
        'password': '1'
    }
    res = requests.post(api, json=data)
    assert res.status_code == 200


def test_admin_and_manager_login_400():
    api = f'{BASE_URL}/v1/user/admin-manager/login/'
    data = {
        'phone_number': '3333',
        'password': '1'
    }
    res = requests.post(api, json=data)
    assert res.status_code == 400


def test_admin_and_manager_login_401():
    api = f'{BASE_URL}/v1/user/admin-manager/login/'
    data = {
        'phone_number': '1111',
        'password': '1'
    }
    res = requests.post(api, json=data)
    assert res.status_code == 401
