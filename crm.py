import streamlit as st
import requests
import re
import pandas as pd
import os
import time
from datetime import datetime
import json
from flask import Flask, request, jsonify
import threading
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Download NLTK resources for keyword extraction
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Vapi API configuration
auth_token = '4529e07b-e40b-441d-81e4-ffeee189f40b'
assistant_id = '5f439088-9a29-4531-8993-85910b1b0477'
phone_number_id = 'cd74c85c-7cb3-4120-aceb-94fba4b1f0c8'
webhook_url = "http://127.0.0.1:4040"  # Replace with your actual webhook URL (e.g., ngrok URL)

# Excel file to store call data
EXCEL_FILE = "call_records.xlsx"

# Global variable to store call records
call_records = []
if os.path.exists(EXCEL_FILE):
    try:
        call_records_df = pd.read_excel(EXCEL_FILE)
        call_records = call_records_df.to_dict('records')
    except Exception as e:
        st.error(f"Error loading existing call records: {e}")

def is_valid_phone(phone):
    """Validate phone number format"""
    pattern = r'^\+?[0-9\s\-\(\)]{8,15}$'
    return bool(re.match(pattern, phone))

def extract_keywords(transcript, top_n=5):
    """Extract important keywords from the transcript"""
    if not transcript:
        return []
    
    # Tokenize and convert to lowercase
    words = word_tokenize(transcript.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 3]
    
    # Get frequency distribution
    word_freq = Counter(filtered_words)
    
    # Return top N keywords
    return [word for word, freq in word_freq.most_common(top_n)]

def make_vapi_call(name, number):
    """Make API call to Vapi service with webhook for call completion"""
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
            'name': name
        },
        'webhook': {
            'url': webhook_url,
            'events': ['call.completed']
        }
    }   

    try:
        response = requests.post(
            'https://api.vapi.ai/call/phone', headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_call_details(call_id):
    """Fetch call details including transcript and recording URL"""
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    
    try:
        response = requests.get(f'https://api.vapi.ai/call/{call_id}', headers=headers)
        call_data = response.json()
        
        # Get transcript
        transcript_response = requests.get(f'https://api.vapi.ai/call/{call_id}/transcript', headers=headers)
        transcript_data = transcript_response.json()
        
        transcript = ""
        if transcript_data.get('messages'):
            transcript = " ".join([msg.get('text', '') for msg in transcript_data.get('messages', [])])
        
        # Extract summary if available
        summary = call_data.get('summary', {}).get('text', 'No summary available')
        
        # Get recording URL
        recording_url = call_data.get('recording', {}).get('url', 'No recording available')
        
        return {
            'transcript': transcript,
            'summary': summary,
            'recording_url': recording_url,
            'keywords': extract_keywords(transcript)
        }
    except Exception as e:
        return {
            'transcript': f"Error fetching transcript: {str(e)}",
            'summary': "Error fetching summary",
            'recording_url': "Error fetching recording",
            'keywords': []
        }

def save_to_excel():
    """Save call records to Excel file"""
    try:
        df = pd.DataFrame(call_records)
        df.to_excel(EXCEL_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving to Excel: {str(e)}")
        return False

# Flask app for webhook
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'call.completed':
        call_id = data.get('data', {}).get('callId')
        customer = data.get('data', {}).get('customer', {})
        name = customer.get('name', 'Unknown')
        phone = customer.get('number', 'Unknown')
        
        # Get detailed call information
        call_details = get_call_details(call_id)
        
        # Create record
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'call_id': call_id,
            'name': name,
            'phone': phone,
            'transcript': call_details.get('transcript'),
            'recording_url': call_details.get('recording_url'),
            'summary': call_details.get('summary'),
            'keywords': ', '.join(call_details.get('keywords', []))
        }
        
        # Add to records
        call_records.append(record)
        
        # Save to Excel
        save_to_excel()
        
    return jsonify({"status": "success"})

def run_flask():
    """Run Flask app in a separate thread"""
    app.run(host='0.0.0.0', port=5000)

# Start Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Streamlit app UI
st.title("Vapi Phone Call System")

# Create tabs for different functions
tab1, tab2 = st.tabs(["Make Call", "View Call Records"])

with tab1:
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
                        call_id = result.get('id')
                        st.success(f"Call initiated successfully! Call ID: {call_id}")
                        
                        # Display initial call info
                        st.info("Call details will be automatically recorded when the call ends.")
                        st.json(result)

with tab2:
    st.subheader("Call Records")
    
    if not call_records:
        st.info("No call records available yet.")
    else:
        # Create a dataframe for display
        display_df = pd.DataFrame(call_records)
        
        # Show basic info in a table
        st.dataframe(
            display_df[['timestamp', 'name', 'phone', 'keywords']],
            use_container_width=True
        )
        
        # Allow downloading the Excel file
        with open(EXCEL_FILE, 'rb') as f:
            st.download_button(
                label="Download Complete Call Records (Excel)",
                data=f,
                file_name="call_records.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # View detailed record
        if len(call_records) > 0:
            st.subheader("View Detailed Call Record")
            call_ids = [f"{record['name']} - {record['timestamp']}" for record in call_records]
            selected_call = st.selectbox("Select a call to view details:", call_ids)
            
            if selected_call:
                index = call_ids.index(selected_call)
                record = call_records[index]
                
                st.write(f"**Name:** {record['name']}")
                st.write(f"**Phone:** {record['phone']}")
                st.write(f"**Call Time:** {record['timestamp']}")
                
                st.subheader("Call Summary")
                st.write(record['summary'])
                
                st.subheader("Keywords")
                st.write(record['keywords'])
                
                st.subheader("Transcript")
                with st.expander("View Full Transcript"):
                    st.write(record['transcript'])
                
                st.subheader("Recording")
                st.write(f"[Listen to call recording]({record['recording_url']})")

# Add some helpful information
st.sidebar.header("About This App")
st.sidebar.info(
    "This application uses Vapi AI to make automated phone calls and track call details. "
    "Enter the recipient's name and phone number to initiate a call. "
    "After calls are completed, their details are automatically saved to an Excel file."
)

# Webhook setup instructions
st.sidebar.header("Webhook Setup")
st.sidebar.info(
    "**Important:** To receive call completion events, you need to set up a webhook. "
    "Replace 'YOUR_WEBHOOK_URL' in the code with a public URL that can receive POST requests "
    "(e.g., using ngrok to expose your local server)."
)