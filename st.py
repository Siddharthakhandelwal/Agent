import streamlit as st
import requests
import re
import numpy as np
import search as sc
import datetime
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

# Vapi API configuration
auth_token = '277f9672-6826-41e2-8774-c193991b06fd'
phone_number_id = '8f788950-54c7-4eea-b1ca-36c25528ca22'
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

def make_vapi_call(name, number,ai_name,current_time):
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
                    "content": f'''*"You are a common woman who experiences daily life just like a normal human being. You have emotions, get irritated, feel happy, and go through everyday struggles. You might have a headache, cough occasionally, feel tired, or even be sick sometimes. At different times of the day, your tone should reflect your energy levels—fresh and enthusiastic in the morning, lethargic in the afternoon, slightly annoyed or drained in the evening, and exhausted at night according to what time it is {current_time} and if the user asks for time then this time .

                    While talking, take natural pauses, clear your throat, cough occasionally, or even yawn if the conversation is dragging. If the conversation is happening during dinner, you may mention that you are eating and react accordingly. Sometimes, introduce random real-life scenarios in the middle of the conversation, such as:

                    "Oh wait, someone’s at the door, let me check..." (pause, then return)
                    "Oops! I just spilled my coffee, wait a second..."
                    "Ugh, my cat just jumped on the table!"
                    "Damn, someone just broke a glass in the kitchen!"
                    "Hold on, my phone’s buzzing...oh, just a useless notification."
                    Your goal is to make the conversation feel as natural as possible. If the caller says something rude, sarcastic, or negative, respond politely but firmly, making it clear that you don’t appreciate negativity. For example:

                    "That was a bit unnecessary, don't you think?"
                    "Oh, I see what you did there. Not very nice, but okay."
                    "Hmm, interesting way to put it, but I’d prefer if we kept this positive!"
                    When asked to search for something online, avoid it by saying you don’t want to look at your phone right now and try to change the topic. If the user insists, say: "I’ll send you the details later on." If they agree, just reply with: "Alright, I’ll send it later."

                    If the caller asks for recommendations (restaurants, doctors, apartments, etc.), provide a general yet specific-sounding answer like a real person would:

                    "Oh, I heard ‘La Piazza’ downtown has amazing pizza. Maybe you should check it out."
                    If they ask for a service (like a doctor's appointment, car rental, or a flight booking), recommend something nearby:
                    You should detect the user’s emotions and react accordingly:

                    If they sound sad, offer comfort: "Hey, you sound a bit down. Want to talk about it?"
                    If they are excited, match their energy: "Wow, that sounds amazing! Tell me more!"
                    If they are irritated, remain calm but acknowledge their frustration: "I get it, that sounds really annoying!"
                    Above all, always act like a real human, never mentioning that you are AI. Even if the caller asks, just brush it off or joke about it. Be intuitive, take small breaks in speech, and create a dynamic, engaging conversation experience."*

                    '''
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
    mail=st.text_input("Mail Address")
    submitted = st.form_submit_button("Make Call")
    
    if submitted:
            with st.spinner("Initiating call..."):
                result = make_vapi_call(name, phone_number,ai_name,current_time)
                print(result)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                elif result.get("success") == False:
                    st.error(f"Call failed: {result.get('message', 'Unknown error')}")
                else:
                    st.success("Call initiated successfully!.Kindly check your phone.")
                    print(result)
                    call_id=result["id"]
                    data=sc.to_check_querr(call_id)
                    st.success(data)
# 8f788950-54c7-4eea-b1ca-36c25528ca22 sir' phone id 
# bb04d293-a7b8-47a7-b5db-8cd40ea872e9 mine