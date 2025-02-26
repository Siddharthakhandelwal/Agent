import os
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WhatsAppSender:
    def __init__(self, headless=False):
        """Initialize the WhatsApp Sender with browser settings."""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user-agent to avoid detection
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Enable file downloads in headless mode
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        # Initialize Chrome driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        self.wait = WebDriverWait(self.driver, 60)
        
    def start(self):
        """Start the WhatsApp Web session."""
        print("Starting WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com/")
        
        # Wait for QR code scan
        print("Please scan the QR code to log in to WhatsApp Web...")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._1G3Wr")))
        print("Successfully logged in to WhatsApp Web")
        
    def find_contact(self, phone_number):
        """Find a contact by phone number."""
        print(f"Finding contact: {phone_number}")
        
        # Use direct message link with phone number
        self.driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
        
        # Wait for the chat to load
        try:
            chat_loaded = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div._1UWac._1LbR4")
            ))
            print(f"Contact {phone_number} found and chat loaded.")
            return True
        except Exception as e:
            print(f"Error finding contact: {e}")
            return False
    
    def send_message(self, message):
        """Send a text message."""
        try:
            message_box = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='conversation-compose-box-input']")
            ))
            
            # Type the message with line breaks
            for line in message.split('\n'):
                message_box.send_keys(line)
                # Add shift+enter for new line
                message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            # Remove the last line break and send
            message_box.send_keys(Keys.BACKSPACE)
            send_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='compose-btn-send']")
            ))
            send_button.click()
            
            print("Message sent successfully")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def send_attachment(self, file_path):
        """Send an attachment (image, document, etc.)."""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False
                
            # Click the attachment button
            attachment_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[data-testid='clip']")
            ))
            attachment_button.click()
            
            # Wait for attach menu to appear and click on document option
            document_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[accept='*']")
            ))
            
            # Send the file path to the file input
            document_button.send_keys(os.path.abspath(file_path))
            
            # Wait for file to upload and click send
            send_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span[data-icon='send']")
            ))
            send_button.click()
            
            # Wait for attachment to send
            time.sleep(3)  # Give some time for the attachment to be sent
            
            print(f"Attachment sent successfully: {file_path}")
            return True
        except Exception as e:
            print(f"Error sending attachment: {e}")
            return False
    
    def close(self):
        """Close the browser session."""
        print("Closing WhatsApp Web session...")
        if self.driver:
            self.driver.quit()
            
def main():
    parser = argparse.ArgumentParser(description="Send WhatsApp messages and attachments")
    parser.add_argument("--phone", type=str, required=True, help="Recipient phone number with country code (no + or spaces)")
    parser.add_argument("--message", type=str, help="Message text to send")
    parser.add_argument("--attachment", type=str, help="Path to file attachment")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (no browser UI)")
    
    args = parser.parse_args()
    
    if not args.message and not args.attachment:
        print("Error: Either message or attachment is required")
        return
    
    # Initialize WhatsApp sender
    sender = WhatsAppSender(headless=args.headless)
    
    try:
        # Start WhatsApp Web
        sender.start()
        
        # Find contact
        if sender.find_contact(args.phone):
            # Send message if provided
            if args.message:
                sender.send_message(args.message)
                
            # Send attachment if provided
            if args.attachment:
                sender.send_attachment(args.attachment)
                
        else:
            print(f"Could not find contact with number: {args.phone}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Give some time to see what happened
        time.sleep(5)
        sender.close()

if __name__ == "__main__":
    main()