import streamlit as st
import requests
import re

# Vapi API configuration
auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
assistant_id = '5f439088-9a29-4531-8993-85910b1b0477'
phone_number_id = 'cd74c85c-7cb3-4120-aceb-94fba4b1f0c8'

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
        'assistantId': assistant_id,
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
        if not name:
            st.error("Please enter a name")
        elif not is_valid_phone(phone_number):
            st.error("Please enter a valid phone number with country code (e.g., +917300608902)")
        else:
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