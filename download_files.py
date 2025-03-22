import requests
import os
import json
from urllib.parse import unquote, urlparse
import time

def read_urls_from_json(json_file):
    """Read URLs from JSON file"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data["urls"]
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {str(e)}")
        return []
    except FileNotFoundError:
        print(f"File {json_file} not found")
        return []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def download_pdfs(urls, output_folder, max_downloads=3):
    """
    Download PDFs from given URLs and save them to specified folder
    
    Args:
    urls (list): List of URLs to download
    output_folder (str): Folder path to save PDFs
    max_downloads (int): Maximum number of PDFs to download
    """
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Remove duplicates while preserving order
    unique_urls = list(dict.fromkeys(url for url in urls if url.lower().endswith('.pdf')))
    
    # Limit number of downloads
    #urls_to_process = unique_urls[:max_downloads]
    urls_to_process = unique_urls
    
    print(f"Found {len(unique_urls)} unique PDF URLs, will download {len(urls_to_process)}")
    
    successful_downloads = 0
    
    for url in urls_to_process:
        try:
            # Extract filename from URL
            parsed_url = urlparse(url)
            filename = unquote(os.path.basename(parsed_url.path))
            
            # Ensure filename is not empty and ends with .pdf
            if not filename:
                filename = f"document_{int(time.time())}.pdf"
            elif not filename.lower().endswith('.pdf'):
                filename += '.pdf'
            
            output_path = os.path.join(output_folder, filename)
            
            # Check if file already exists
            if os.path.exists(output_path):
                print(f"Skipping {filename} - already exists")
                continue
            
            print(f"Downloading {url} -> {filename}")
            
            # Make GET request with stream=True to handle large files
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check if content type is PDF
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' not in content_type and 'application/octet-stream' not in content_type:
                print(f"Warning: {url} may not be a PDF (Content-Type: {content_type})")
            
            # Save the file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            successful_downloads += 1
            print(f"Successfully downloaded {filename}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error processing {url}: {str(e)}")
            
        # Add small delay between downloads
        time.sleep(1)
    
    print(f"\nDownload Summary:")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed downloads: {len(urls_to_process) - successful_downloads}")

if __name__ == "__main__":
    # Path to JSON file (in same directory as script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, 'list_downloads.json')
    output_folder = "downloaded_pdfs"
    
    try:
        # Read URLs from JSON file
        pdf_urls = read_urls_from_json(json_file)
        
        if pdf_urls:
            download_pdfs(pdf_urls, output_folder)
        else:
            print("No URLs found in JSON file")
            
    except Exception as e:
        print(f"Script execution failed: {str(e)}")
    