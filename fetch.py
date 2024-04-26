import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_and_save_scripts(url):
    try:
        # Parse the domain from the URL to use as a folder name
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace('.', '_')

        # Define the path to save files
        download_path = os.path.join('/mnt/c/Users/newpu/Downloads', domain_name)

        # Create the directory if it does not exist
        os.makedirs(download_path, exist_ok=True)

        # Send HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Download JavaScript files
        scripts = soup.find_all('script')
        for script in scripts:
            if 'src' in script.attrs:
                src = script.attrs['src']
                download_file(src, download_path, 'js')

        # Download CSS files
        links = soup.find_all('link', attrs={'rel': 'stylesheet'})
        for link in links:
            if 'href' in link.attrs:
                href = link.attrs['href']
                download_file(href, download_path, 'css')

    except requests.RequestException as e:
        print(f"Error fetching or saving scripts: {e}")

def download_file(url, path, file_type):
    # Handle absolute and relative URLs
    if not url.startswith(('http:', 'https:')):
        if url.startswith('//'):
            url = 'http:' + url
        else:
            print(f"Skipping non-absolute URL for {file_type}: {url}")
            return

    try:
        # Extract filename from URL
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            raise ValueError("URL does not contain a valid filename")

        # Define the full path for the file
        full_path = os.path.join(path, filename)

        # Download and save the file
        response = requests.get(url)
        response.raise_for_status()
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f"Saved {file_type} file: {full_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Example usage:
fetch_and_save_scripts('https://www.example.com')  # Replace with your target URL
