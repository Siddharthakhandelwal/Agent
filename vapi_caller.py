import re
import requests

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