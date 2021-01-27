#!/usr/bin/env python3


from app import app
import pytest
import json
import requests
import re



regex = re.compile('[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]')
headers = {'Content-type': 'application/json'}
app_url = 'http://127.0.0.1:5000'

def test_post():
    test_data = {
        'key error': [
            { 
                'adsa': 'test',
                'value': 'test'
            },
            { 
                'key': 'test',
                'aasda': 'test'
            },
            { 
                'key': 'test',
                'aasda': 'test'
            },
            { 
                'key': 'test',
            },
            { 
                'value': 'test',
            },
            { 
                'key': 'test',
                'value': 'test',
                'foo': 'test',
            },
        ],
        'value error': [
            { 
                'key': '',
                'value': 'test'
            },
            { 
                'key': '',
                'value': ''
            },
            { 
                'key': 'test',
                'value': ''
            },
            { 
                'key': None,
                'value': ''
            },
            { 
                'key': 'test',
                'value': None
            },
        ],
        'Success': [
            { 
                'key': 'test',
                'value': 'test'
            },
            { 
                'key': 111,
                'value': 222
            },
        ],
        'key exists': [
            { 
                'key': 'test',
                'value': 'test'
            },
            { 
                'key': 111,
                'value': 222
            },
        ],
    }
    for result in test_data:
        for post_body in test_data[result]:
            res = requests.post(app_url + '/dictionary', data = json.dumps(post_body), headers = headers)
            if result == 'Success':
                assert res.status_code == 200
            elif result == 'key exists':
                assert res.status_code == 409
            else:
                assert res.status_code == 400
            data = res.json()
            assert data['result'] == result
            assert re.match(regex, data['time'])
    for test_data in test_data['Success']:
        key = str(test_data['key'])
        requests.delete(app_url + '/dictionary' + f'/{key}',  headers = headers)


def test_get():
    test_data = json.dumps({ 
            'key': 'key_get',
            'value': 'value_get'
            })

    res = requests.get(app_url + '/dictionary/empty')
    data = res.json()
    assert res.status_code == 404
    assert data['result'] == None
    assert re.match(regex, data['time'])


    requests.post(app_url + '/dictionary', data = test_data, headers=headers )
    res = requests.get(app_url + '/dictionary/key_get', headers=headers )
    assert res.status_code == 200
    data = res.json()
    assert data['result'] == 'value_get'
    assert re.match(regex, data['time'])
    requests.delete(app_url + '/dictionary' + f'/key_get', headers=headers )


def test_put():
    test_data1 = json.dumps({ 
            'key': 'key_put',
            'value': 'value_put'
            })
    test_data2 = json.dumps({ 
            'key': 'key_put',
            'value': 'value_put2'
            })
    test_data3 = json.dumps({ 
            'key': 'key_put3',
            'value': 'value_put3'
            })

    requests.post(app_url + '/dictionary', data = test_data1, headers=headers )
    # for i in range(2):
    res = requests.put(app_url + '/dictionary/key_put', data = test_data2, headers=headers )
    assert res.status_code == 200
    data = res.json()
    assert data['result'] == 'Success'
    assert re.match(regex, data['time'])
    res = requests.get(app_url + '/dictionary/key_put', headers=headers )
    assert res.status_code == 200
    data = res.json()
    assert data['result'] == 'value_put2'
    assert re.match(regex, data['time'])

    res = requests.put(app_url + '/dictionary/put_key3', data = test_data3, headers=headers )
    assert res.status_code == 404
    data = res.json()
    assert data['result'] == 'key not found'
    assert re.match(regex, data['time'])

    requests.delete(app_url + '/dictionary' + f'/key_put',  headers=headers )



def test_delete():
    test_data = json.dumps({ 
            'key': 'key_delete',
            'value': 'value_delete'
            })
    requests.post(app_url + '/dictionary', data = test_data, headers=headers )
    res = requests.delete(app_url + '/dictionary/key_delete', headers=headers )
    assert res.status_code == 200
    data = res.json()
    assert data['result'] == None
    assert re.match(regex, data['time'])
    res = requests.delete(app_url + '/dictionary/empty', headers=headers )
    assert res.status_code == 200
    assert data['result'] == None
    assert re.match(regex, data['time'])













# def test_get_empty_key():
#     response = app.test_client().get( '/dictionary/empty', content_type = 'application/json')
#     time = now()
#     data = json.loads(response.get_data(as_text=True))
#     assert response.status_code == 404
#     assert data == {'result': None, 'time': time}

# def test_get_exist_key():
#     app.test_client().post( 
#             '/dictionary/', 
#             data= json.dumps({ "key": "testkey", "value": "testvalue" }), 
#             content_type = 'application/json')
#     response = app.test_client().get( '/dictionary/testkey', content_type = 'application/json')
#     time = now()
#     data = json.loads(response.get_data(as_text=True))
#     assert data == {'result': 'testvalue', 'time': time }
#     assert response.status_code == 200

# def post_key():
#     response = app.test_client().post( '/dictionary/', data=json.dumps(
#         content_type = 'application/json')
#     data = json.loads(response.get_data(as_text=True))
#     assert response.status_code == 404
