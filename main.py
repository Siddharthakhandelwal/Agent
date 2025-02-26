import streamlit as st
import os
from vapi_caller import is_valid_phone, make_vapi_call
from web_search import needs_web_search, search_web, extract_answer_from_search, extract_file_links
from file_utils import download_file

# Create downloads directory if it doesn't exist
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Streamlit app UI
def main():
    st.title("AI Agent with Web Search")
    
    tabs = st.tabs(["Make a Call", "Ask a Question"])
    
    with tabs[0]:
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
                            st.success("Call initiated successfully! Kindly check your phone.")
    
    with tabs[1]:
        st.subheader("Ask me anything")
        
        query = st.text_input("Your question")
        search_button = st.button("Get Answer")
        
        if search_button and query:
            with st.spinner("Processing your question..."):
                # Determine if the query needs web search
                if needs_web_search(query):
                    st.info("Searching the web for the latest information...")
                    
                    # Perform web search
                    search_results = search_web(query)
                    
                    # Extract and display answer
                    answer = extract_answer_from_search(search_results, query)
                    st.markdown(answer)
                    
                    # Check for file downloads
                    file_links = extract_file_links(search_results)
                    if file_links and len(file_links) > 0:
                        st.subheader("Download Relevant Files")
                        for file in file_links[:3]:  # Limit to 3 files
                            if st.button(f"Download {file['title']} ({file['type']})"):
                                with st.spinner(f"Downloading {file['type']} file..."):
                                    download_result = download_file(file['url'], DOWNLOADS_DIR)
                                    if download_result["success"]:
                                        st.success(f"Downloaded to {download_result['path']}")
                                    else:
                                        st.error(f"Download failed: {download_result['error']}")
                else:
                    st.info("I can answer this without searching the web.")
                    # Here you would call your AI's standard answering function
                    st.write("This is where your AI would provide an answer from its knowledge base.")

if __name__ == "__main__":
    main()