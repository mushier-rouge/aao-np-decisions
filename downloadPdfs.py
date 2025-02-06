import os
import requests
from bs4 import BeautifulSoup

def download_pdfs_from_page(page_num, download_dir):
    url = f"https://www.uscis.gov/administrative-appeals/aao-decisions/aao-non-precedent-decisions?uri_1=19&m=All&y=6&items_per_page=100&page={page_num}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to access page {page_num}, stopping...")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    
    if not pdf_links:
        print(f"No PDFs found on page {page_num}, stopping...")
        return False
    
    os.makedirs(download_dir, exist_ok=True)
    
    for pdf_link in pdf_links:
        pdf_url = pdf_link if pdf_link.startswith('http') else f"https://www.uscis.gov{pdf_link}"
        pdf_name = pdf_url.split('/')[-1]
        pdf_path = os.path.join(download_dir, pdf_name)
        
        if os.path.exists(pdf_path):
            print(f"Skipping {pdf_name}, already downloaded.")
            continue
        
        print(f"Downloading {pdf_name}...")
        pdf_response = requests.get(pdf_url, headers=headers)
        if pdf_response.status_code == 200:
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
        else:
            print(f"Failed to download {pdf_name}")
    
    return True

def main():
    download_dir = "uscis_pdfs"
    page_num = 0
    
    while True:
        success = download_pdfs_from_page(page_num, download_dir)
        if not success:
            break
        page_num += 1
    
    print("Download process complete.")

if __name__ == "__main__":
    main()
