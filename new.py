import requests
import numpy as np
# Your Vapi API Authorization token
auth_token = '<YOUR AUTH TOKEN>'
# The Phone Number ID, and the Customer details for the call
phone_number_id = '<PHONE NUMBER ID FROM DASHBOARD>'
customer_number = "+14151231234"
provider=['playht','11labs']
a=np.random.randint(0,2)
voice=[['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json','s3://voice-cloning-zero-shot/801a663f-efd0-4254-98d0-5c175514c3e8/jennifer/manifest.json'],['qXROlfoWotxhFxvZc0dY','wlmwDR77ptH6bKHZui0l','FQygEXXdVfjOosF7jzJ7']]
b=np.random.randint(0,3)
providers=provider[a]
voices=voice[a][b]

# Create the header with Authorization token
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

# Create the data payload for the API request
data = {
    'assistant': {
        "firstMessage": "Hey, what's up?. i am Ananya",
        "model": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant."
                }
            ]
        },
        "voice": {
            "provider": providers,
            "voice": voices
        }
    },
    'phoneNumberId': phone_number_id,
    'customer': {
        'number': customer_number,
    },
}

# Make the POST request to Vapi to create the phone call
response = requests.post(
    'https://api.vapi.ai/call/phone', headers=headers, json=data)

# Check if the request was successful and print the response
if response.status_code == 201:
    print('Call created successfully')
    print(response.json())
else:
    print('Failed to create call')
    print(response.text)
