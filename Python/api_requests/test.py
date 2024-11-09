import requests
import json
from requests import HTTPError
from requests import Session

class Test():
    def __init__ (self):
        self.session = Session()
        self.session.headers = {
            'x-api-key':"ae2116a6fe723f593c97eb02864b315cf049f005c4993ca61eeaf6636113f7d4"
        }
        self.base_url = "https://woqx7nwit4.execute-api.eu-west-1.amazonaws.com/dev"
        
    def get_user (self):
        res = self.session.get(
            url=f"{self.base_url}/manageUser" 
        )
        print(res.text)
        res.raise_for_status()
    def get_email(self, email):
        payload = json.dumps({
            "email": email,
        })
        res = self.session.post(
            url=f"{self.base_url}/getEmail",
            data=payload 
        )
        print("Response from getEmail:", res.text)
        res.raise_for_status()


test = Test()
test.get_user()