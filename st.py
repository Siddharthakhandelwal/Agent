import streamlit as st
import requests
import re
import numpy as np
# Vapi API configuration
auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
assistant_id = '5f439088-9a29-4531-8993-85910b1b0477'
phone_number_id = 'cd74c85c-7cb3-4120-aceb-94fba4b1f0c8'
provider=['playht','11labs']
a=np.random.randint(0,2)
voice=[['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json','s3://voice-cloning-zero-shot/801a663f-efd0-4254-98d0-5c175514c3e8/jennifer/manifest.json','s3://voice-cloning-zero-shot/b2f5441d-354f-4c2f-8f32-390aaaabf42d/charlottesaad/manifest.json','s3://peregrine-voices/charlotte ads parrot saad/manifest.json','s3://voice-cloning-zero-shot/5b81dc4c-bf98-469d-96b4-8f09836fb500/aurorasaad/manifest.json','s3://voice-cloning-zero-shot/f43cc4b4-b193-4a13-a903-e6b125c3d572/original/manifest.json','s3://voice-cloning-zero-shot/34eaa933-62cb-4e32-adb8-c1723ef85097/original/manifest.json','s3://voice-cloning-zero-shot/f741f871-63ad-4207-8278-907aec4e9e50/aylameditationsaad/manifest.json','s3://voice-cloning-zero-shot/b709b944-9256-4578-b9d8-a1ce4d729022/eileensaad/manifest.json','s3://voice-cloning-zero-shot/e5df2eb3-5153-40fa-9f6e-6e27bbb7a38e/original/manifest.json'],['qXROlfoWotxhFxvZc0dY','wlmwDR77ptH6bKHZui0l','FQygEXXdVfjOosF7jzJ7','ftDdhfYtmfGP0tFlBYA1','Oq0cIHWGcnbOGozOQv0t','MGaY6WIx4nO5dhOtYlvw','NlykoD7D8eVGPHL3HAze','90ipbRoKi4CpHXvKVtl0','tzoR7arDwmW2nN2tuFJy','KRCS4PnIIvwc4cjKLAz5','ZeK6O9RfGNGj0cJT2HoJ']]
b=np.random.randint(0,11)
providers=provider[a]
voices=voice[a][b]
name=['Ananya','Anushka','nidhi','ridhi','rose','anita','harishree','ankita','ruchi','tanisha','nishi','saumya','parul','tanu']
c=np.random.randint(0,13)
ai_name=name[c]
def is_valid_phone(phone):
    """Validate phone number format"""
    # This regex accepts numbers with or without '+' prefix, allows spaces, dashes, parentheses
    pattern = r'^\+?[0-9\s\-\(\)]{8,15}$'
    return bool(re.match(pattern, phone))

def make_vapi_call(name, number,ai_name):
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
        "firstMessage": f"Hey, what's up {name}?. i am {ai_name}",
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "you are a common woman and go through everything everyday just like a normal human.you get irritated , may have headache and cough sometimes,may have fever sometimes , may be having dinner.Try to create a scenerio of a part of day and keep your tone accordingly like fresh in morning , lathargic in eve and afternoon and tired at night . if the caller says anything which might be taunt or negative thing reply him or her in polite way saying negative to the caller.Answer each query in a way like human do or talk. give answer to every question.Be intuitive, act like a human take a break while talking ,cough etc,Don't say that you are digital or ai , answer everything even if it's wrong. Try to be intuitive and human like.If the user asks u to search or something which requires internet and just say that u don't want to look at the phone while talking to me and try to deviate the topic otherwise just say that i will send u the details later on .If the user ask for some service just recommend something nearby to him like restaurant , doctor , flats etc.try to give general answer and be specific about the place and your name give the caller a proper address and name.detect the user emotion and react int hat way.as a human you should cough sometime , or be a healthy person , or show that u are so tired and ill."
                }
            ]
        },
        "voice": {
            "provider": providers,
            "voiceId": voices
        },
        "backgroundSound":'office',
         "analysisPlan": {
            "summaryPlan": {
                "messages": [
                    {
                    "role": "assistant",
                    "content": "you need to suumarize the transcript so that i can understand the conversation"
                    }
                ],
                "enabled": True,
                "timeoutSeconds": 1.1
                },
                "structuredDataPlan": {
                "messages": [
                    {
                    "role": "assistant",
                    "content": "you need to extract the querry if user asked some question which requires internet connectivity to answer"
                    }
                ],
                "enabled": True,
                "schema": {
                    "type": "string",
                },
                "timeoutSeconds": 1.1
                    }
                },
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
                result = make_vapi_call(name, phone_number,ai_name)
                print(result)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                elif result.get("success") == False:
                    st.error(f"Call failed: {result.get('message', 'Unknown error')}")
                else:
                    st.success("Call initiated successfully!.Kindly check your phone.")
                    print(result)
