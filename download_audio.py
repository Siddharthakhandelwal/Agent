import requests

# Replace with your actual VAPI API token
VAPI_API_TOKEN = "4529e07b-e40b-441d-81e4-ffeee189f40b"
CALL_ID = "8de15983-44ee-4c47-8d1d-a125002574e2"  # Replace with the actual call ID
OUTPUT_FILE = f"{CALL_ID}.wav"  # Change filename if needed

def get_call_details():
    """Fetch call details including the stereo recording URL."""
    url = f"https://api.vapi.ai/call/{CALL_ID}"
    headers = {"Authorization": f"Bearer {VAPI_API_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(len(data)) #
        print(data.keys()) #
        return data
    else:
        print(f"Failed to get call details: {response.text}")
        return None

def download_audio(audio_url, output_file):
    """Download and save the call audio file."""
    response = requests.get(audio_url, stream=True)
    
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Audio downloaded successfully: {output_file}")
    else:
        print(f"Failed to download audio: {response.text}")

# # Fetch call details and download audio
call_data = get_call_details()
if call_data and "stereoRecordingUrl" in call_data:
    audio_url = call_data["stereoRecordingUrl"]
    print(f"Audio URL: {audio_url}")
    download_audio(audio_url, OUTPUT_FILE)
else:
    print("No audio URL found for this call.")
