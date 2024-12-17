# Upload params class

import requests
import json


class UploadParams:

    def __init__(self, token_address, upload_address, username, password, data):
        self.token_address = token_address
        self.upload_address = upload_address
        self.username = username
        self.password = password
        self.data = data

    def upload(self):
        token = self.get_token()
        if token == "":
            print("get token failed!")
            return False

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        json_data = json.loads(self.data)

        response = requests.post(self.upload_address, headers=headers, json=json_data, verify=False)

        if response.status_code == 200:
            json_data = response.json()
            print(json_data)  # 打印响应的 JSON 数据
            if json_data.get('success'):
                return True
            else:
                print(f"Failed. msg: {json_data['error']['message']}")
                return False
        else:
            print(f"Failed. Status code: {response.status_code}")
            return False

    def get_token(self):
        headers = {
            "Content-Type": "application/json"
        }

        json_data = {
            "userName": self.username,
            "userPassword": self.password
        }

        response = requests.post(self.token_address, headers=headers, json=json_data, verify=False)

        if response.status_code == 200:
            json_data = response.json()
            # print(json_data)  # 打印响应的 JSON 数据
            if json_data.get("code") == 200:
                return json_data["data"]["token"]
            else:
                print("get token err")
                return ''

        else:
            print(f"Failed. Status code: {response.status_code}")
            return ''
