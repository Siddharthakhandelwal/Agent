import requests

auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'

def to_call(number):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'assistantId': '5f439088-9a29-4531-8993-85910b1b0477',
        'phoneNumberId': 'cd74c85c-7cb3-4120-aceb-94fba4b1f0c8',
        'type': 'outboundPhoneCall',
        'customer': {
            'number': number,
        },
    }   

    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data)
    print(response.json())

to_call("+917300608902")

