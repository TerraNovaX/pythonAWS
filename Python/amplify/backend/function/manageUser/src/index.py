import json
from functools import wraps
from http import HTTPStatus
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
                response['body'] = json.dumps(res)
            response['statusCode'] = HTTPStatus.OK
        except HTTPError as error:
            response['statusCode'] = error.response.status_code
        except PermissionError as error:
            response['error'] = str(error)
            response['statusCode'] = HTTPStatus.FORBIDDEN
        except Exception as error: 
            response['error'] = str(error)
            print('An error occurred:', error)
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        return response

    return wrapper

@exception_handler
def handler(event, context):
  
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    dynamoDB = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamoDB.Table(user_table_name)

    
    api_key = event['headers'].get('x-api-key')
    
    
    response = table.scan(
        FilterExpression='api_key = :api_key',
        ExpressionAttributeValues={':api_key': api_key}
    )
    
    if response['Items']:
        email = response['Items'][0].get('email')
        return {
            'message': f'Email associated with API key: {email}'
        }
    else:
        return {
            'error': 'No user found with the provided API key'
        }