import requests

auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
def querry_search(callid):
    url = f"https://api.vapi.ai/call/{callid}"
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    querry = response.json()
    print(querry['status'])
querry_search("d379f518-4a5d-477d-b229-d2e1204dfdf2")

# ['analysis']['structuredData']['query']