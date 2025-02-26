import os
import re
import requests
from datetime import datetime

def download_file(url, download_dir, filename=None):
    """Download a file from a URL and save it to the downloads directory"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # If filename not provided, extract from URL or generate a timestamp-based name
        if not filename:
            if "Content-Disposition" in response.headers:
                content_disposition = response.headers["Content-Disposition"]
                filename_match = re.search(r'filename="?([^"]+)"?', content_disposition)
                if filename_match:
                    filename = filename_match.group(1)
            
            if not filename:
                # Extract filename from URL or generate based on timestamp
                url_filename = url.split("/")[-1].split("?")[0]
                if url_filename and "." in url_filename:
                    filename = url_filename
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    extension = guess_extension_from_content_type(response.headers.get("Content-Type", ""))
                    filename = f"download_{timestamp}{extension}"
        
        file_path = os.path.join(download_dir, filename)
        
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return {
            "success": True,
            "path": file_path,
            "filename": filename
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def guess_extension_from_content_type(content_type):
    """Guess file extension based on content type"""
    content_type = content_type.lower()
    extensions = {
        "application/pdf": ".pdf",
        "application/msword": ".doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "application/vnd.ms-powerpoint": ".ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "text/plain": ".txt",
        "text/html": ".html",
        "text/csv": ".csv"
    }
    
    return extensions.get(content_type, ".bin")  # Default to .bin if unknown