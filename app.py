#!/usr/bin/env python3

from flask import Flask, request, jsonify, Response
from datetime import datetime
from functools import wraps


app = Flask(__name__)

keys = ['key', 'value']

data = {}

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def response(result):
    return jsonify({ 'result': result, 'time': now() })

def validate():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            app.logger.debug(f'data: {data}')
            app.logger.debug(f'json_request: {_json}')
            # missing = [r for r in required.keys() if r not in _json]
            if list(_json.keys()) != keys:
                return response("key error"), 400
            for key in _json.keys():
                if _json[key] in [ None, "" ]:
                    return response("value error"), 400
            app.logger.debug(f'request method {request.method}')
            if request.method == 'POST':
                if str(_json['key']) in data:
                    return response("key exists"), 409
            elif request.method == 'PUT':
                if str(_json['key']) not in data:
                    return response("key not found"), 404
            return fn(*args, **kwargs)
        return wrapper
    return decorator
        

@app.route('/dictionary/<key>')
def get_dict(key):
    if key in data:
        app.logger.debug(key)
        app.logger.debug(data[key])
        return response(data[key]), 200
    return response(None), 404


@app.route('/dictionary', methods=['POST'])
@validate()
def create_dict():
    _json = request.get_json()
    data[str(_json['key'])] = str(_json['value'])
    return response('Success'), 200


@app.route('/dictionary/<key>', methods=['PUT'])
@validate()
def update_dict(key):
    _json = request.get_json()
    if key in data.keys():
        data[str(_json['key'])] = str(_json['value'])
        return response('Success'), 200
    return response('key not found'), 404



@app.route('/dictionary/<key>', methods=['DELETE'])
def delete_dict(key):
    if key in data:
        del(data[key])
        return response(None), 200
    return response('key not found'), 200


if __name__ == "__main__":
    app.run()

