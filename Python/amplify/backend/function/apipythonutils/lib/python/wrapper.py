import json
from functools import wraps
from http import HTTPStatus
from requests import HTTPError
import os
import boto3

def exception_handler(func):
    @wraps(func)
    def wrapper(event, context):
        print(event)
        
        response = {}
        try:
            if not event['headers'].get('x-api-key'):
                raise PermissionError('x-api-key missing')
            
            res = func(event, context)
            if res:
                response['body']= json.dumps(res)
            response['statusCode'] = HTTPStatus.OK
        except HTTPError as error:
            response['statusCode'] = error.response.status_code
        except PermissionError as error:
            response['error']=str(error)
            response['statusCode'] = HTTPStatus.FORBIDDEN
        except Exception as error: 
            response['error']=str(error)
            print('hi')
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        return response

    return wrapper