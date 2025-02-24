import requests

auth_token = 'b04c706e-1624-4bff-b47c-be85ffe618de'

def to_call(number):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'assistantId': '5fbd8b20-fd79-4fc5-85d8-2d5243875bff',
        'phoneNumberId': '31b853ab-753e-422e-9492-0ea4360850e8',
        'customer': {
            'number': number,
        },
    }

    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data)
    print(response.json())

to_call("+917300608902")

