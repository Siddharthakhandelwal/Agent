import requests

# Replace with your actual VAPI API token
VAPI_API_TOKEN = "b04c706e-1624-4bff-b47c-be85ffe618de"
CALL_ID = "642c16c3-9955-449e-a3bc-6705f5bb6141"  # Replace with the actual call ID
OUTPUT_FILE = "call_audio.wav"  # Change filename if needed

def get_call_details(call_id):
    """Fetch call details including the stereo recording URL."""
    url = f"https://api.vapi.ai/call/{call_id}"
    headers = {"Authorization": f"Bearer {VAPI_API_TOKEN}"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
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

# Fetch call details and download audio
call_data = get_call_details(CALL_ID)
if call_data and "stereoRecordingUrl" in call_data:
    audio_url = call_data["stereoRecordingUrl"]
    print(f"Audio URL: {audio_url}")
    download_audio(audio_url, OUTPUT_FILE)
else:
    print("No audio URL found for this call.")
