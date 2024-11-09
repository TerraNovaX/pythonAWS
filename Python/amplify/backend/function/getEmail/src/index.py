import json
import re
import uuid
import boto3
from boto3.dynamodb.conditions import Key
from http import HTTPStatus
import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

HEADERS = {
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def handler(event, context):
    try: 
        response = {
            'statusCode': HTTPStatus.OK,
            'headers': HEADERS,
            'body': ''
        }
        
        if event['httpMethod'] != 'POST':
            response['statusCode'] = HTTPStatus.METHOD_NOT_ALLOWED
            response['body'] = 'Method Not Allowed'
            return response

        try:
            body = json.loads(event['body'])
            email = body.get('email')
        except json.JSONDecodeError:
            response['statusCode'] = HTTPStatus.BAD_REQUEST
            response['body'] = 'Invalid JSON format'
            return response

        if not email:
            response['statusCode'] = HTTPStatus.BAD_REQUEST
            response['body'] = 'Email is required'
            return response

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            response['statusCode'] = HTTPStatus.BAD_REQUEST
            response['body'] = 'Invalid email format'
            return response
        
        table_name = os.environ.get('STORAGE_USERS_NAME')
        if not table_name:
            logging.error("STORAGE_DB_NAME environment variable is not set.")
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
            response['body'] = 'Server configuration error'
            return response

        db = boto3.resource('dynamodb', region_name='eu-west-1')  
        table = db.Table(table_name)

        try:
            entities = table.query(
                IndexName='emails',  
                KeyConditionExpression=Key('email').eq(email)
            )
            
            if 'Items' in entities and len(entities['Items']) > 0:  
                user = entities['Items'][0]
                response['body'] = json.dumps({ 'api_key': user['api_key'] })
                return response
        except Exception as e:
            logging.error(f"Error retrieving user: {e}")
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
            response['body'] = f'Error retrieving user: {str(e)}'
            return response

        user_id = str(uuid.uuid4())
        api_key = hashlib.sha256((email).encode()).hexdigest()

        try:
            table.put_item(Item={'id': user_id, 'email': email, 'api_key': api_key})
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
            response['body'] = f'Error creating user: {str(e)}'
            return response
        
        response['body'] = json.dumps({ 'api_key': api_key })
        return response
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        response['body'] = f'Error: {str(e)}'
        return response
