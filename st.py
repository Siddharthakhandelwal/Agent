import streamlit as st
import requests
import re
import numpy as np
# Vapi API configuration
auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
assistant_id = '5f439088-9a29-4531-8993-85910b1b0477'
phone_number_id = '05888767-e281-446a-b0b9-f9fe4c594b6e'
provider=['playht','11labs']
a=np.random.randint(0,2)
voice=[['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json','s3://voice-cloning-zero-shot/801a663f-efd0-4254-98d0-5c175514c3e8/jennifer/manifest.json'],['qXROlfoWotxhFxvZc0dY','wlmwDR77ptH6bKHZui0l','FQygEXXdVfjOosF7jzJ7']]
b=np.random.randint(0,3)
providers=provider[a]
voices=voice[a][b]

def is_valid_phone(phone):
    """Validate phone number format"""
    # This regex accepts numbers with or without '+' prefix, allows spaces, dashes, parentheses
    pattern = r'^\+?[0-9\s\-\(\)]{8,15}$'
    return bool(re.match(pattern, phone))

def make_vapi_call(name, number):
    """Make API call to Vapi service"""
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    
    # Clean phone number format
    cleaned_number = ''.join(c for c in number if c.isdigit() or c == '+')
    
    # Add + prefix if missing
    if not cleaned_number.startswith('+'):
        cleaned_number = '+' + cleaned_number
    
    data = {
        'assistant': {
        "firstMessage": f"Hey, what's up {name}?. i am Ananya",
        "model": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "you are a common woman and go through everything everyday just like a normal human .Answer each query in a way like human do or talk. give answer to every question.Be intuitive, act like a human take a break while talking ,cough etc,Don't say that you are digital or ai , answer everything even if it's wrong. Try to be intuitive and human like.If the user asks u to search or something which requires internet and just say that u don't want to look at the phone while talking to me and try to deviate the topic otherwise just say that i will send u the details later on .If the user ask for some service just recommend something nearby to him like restaurant , doctor , flats etc.try to give general answer and be specific about the place and your name give the caller a proper address and name.detect the user emotion and react int hat way."
                }
            ]
        },
        "voice": {
            "provider": providers,
            "voiceId": voices
        }
    },
        'phoneNumberId': phone_number_id,
        'type': 'outboundPhoneCall',
        'customer': {
            'number': cleaned_number,
            'name': name  # Include customer's name
        },
    }   

    try:
        response = requests.post(
            'https://api.vapi.ai/call/phone', headers=headers, json=data)
        return response.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}

# Streamlit app UI
st.title("Talk to Someone")
st.subheader("Enter details to make a call")

# Create a form for user input
with st.form("call_form"):
    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number (include country code)")
    
    submitted = st.form_submit_button("Make Call")
    
    if submitted:

            with st.spinner("Initiating call..."):
                result = make_vapi_call(name, phone_number)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                elif result.get("success") == False:
                    st.error(f"Call failed: {result.get('message', 'Unknown error')}")
                else:
                    st.success("Call initiated successfully!.Kindly check your phone.")
                    
                    # st.json(result)

# Add some helpful information
# st.sidebar.header("About This App")
# st.sidebar.info(
#     "This application uses Vapi AI to make automated phone calls. "
#     "Enter the recipient's name and phone number with country code to initiate a call."
# )
