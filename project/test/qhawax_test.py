import requests
import json

url='https://qairamapnapi-dev-opensource.qairadrones.com'

"""
Test QHAWAX Endpoints

"""
def test_get_inca_qhawax_inca():
    params = {'name':'qH004'}
    response = requests.get(url+'/api/get_qhawax_inca/',params=params)
    assert response.status_code == 200
    assert json.loads(response.text) == "green"

def test_get_inca_qhawax_inca_not_valid():
    params = {'no_name':'qH004'}
    response = requests.get(url+'/api/get_qhawax_inca/',params=params)
    assert response.status_code == 400
    assert json.loads(response.text) == {"error":"'qHAWAX name None should be string'"}

def test_post_inca_qhawax_inca_not_valid():
    params = {'no_name':'qH001'}
    response = requests.post(url+'/api/get_qhawax_inca/',params=params)
    assert response.status_code == 405

def test_get_qhawaxs_active_mode_customer():
    response = requests.get(url+'/api/get_qhawaxs_active_mode_customer/')
    assert response.status_code == 200

def test_get_qhawaxs_active_mode_customer_parameters():
    params = {'no_name':'qH001'}
    response = requests.get(url+'/api/get_qhawaxs_active_mode_customer/',params=params)
    assert response.status_code == 200

def test_post_qhawaxs_active_mode_customer_not_valid():
    params = {'no_name':'qH001'}
    response = requests.post(url+'/api/get_qhawaxs_active_mode_customer/',params=params)
    assert response.status_code == 405
