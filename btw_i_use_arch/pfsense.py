import os
import json
import requests
from dotenv import load_dotenv


"""
This is a script for toggling firewall rules on a pfSense appliance.

From the documentation re: auth:

curl -X POST -H "Content-Type: application/json" -u admin:pfsense https://pfsense.example.com/api/v2/auth/jwt
{"code":200,"status":"ok","response_id":"SUCCESS","message":"","data":{"token":"xxxxxxxxxxxxxxxxxxx"}}

curl -H "Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxx" https://pfsense.example.com/api/v2/firewall/rules

which in Python translates to:
response = requests.post(
    'https://{SERVER}/api/v2/auth/jwt',
    headers=headers,
    verify=CERT_PATH,
    auth=('admin', 'whatever_the_pw_is_2024'),
)

if response.status_code == 200:
    token = response.json()["data"]["token"]
    headers['Authorization'] = f'Bearer {token}'
print(response.json())

However, using API keys is easier and more secure. Will be doing that instead.
"""


load_dotenv()
SERVER = os.environ.get('SERVER')
CERT_PATH = os.environ.get('CERT_PATH')
headers = {
    'Content-Type': 'application/json',
}

"""
"""

def disabled_or_enabled(disabled: bool):
    if disabled:
        return "DISABLED"
    else:
        return "ENABLED"


def toggle_access_rule(id: int):
    """Toggles access rule

    Returns:
        _type_: _description_
    """
    headers["X-API-Key"] = os.environ.get('API_KEY')
    data = {"id": id}
    def get_current_status():
        return requests.get(f"{SERVER}/api/v2/firewall/rule", headers=headers, verify=CERT_PATH, data=json.dumps(data)).json()["data"]["disabled"]
    
    disabled = get_current_status()
    print(f"Firewall Rule {id} is presently {disabled_or_enabled(disabled)}")
    data["disabled"] = not disabled

    return requests.patch(f"{SERVER}/api/v2/firewall/rule", headers=headers, verify=CERT_PATH, data=json.dumps(data))

response = toggle_access_rule(2)

if response.status_code == 200:
    print(f"""Firewall Rule {response.json()["data"]["id"]} is now {disabled_or_enabled(response.json()["data"]["disabled"])}""")
