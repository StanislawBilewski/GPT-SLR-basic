import bibtexparser
import fitz
import os
import requests

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def extract_papers(bibtex_file_path):
    with open(bibtex_file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    papers = []
    for entry in bib_database.entries:
        paper = {
            'ID': entry.get('ID', "no-id"),
            'title': entry.get('title', 'No title available').strip('{}'),
            'abstract': entry.get('abstract', None),
            'doi': entry.get('doi', None),
            'author': entry.get('author', None),
            'year': entry.get('year', None),
            'journal': entry.get('journal', None),
            'keywords': entry.get('keywords', None),
            'url': entry.get('url', None),
            'pages': entry.get('pages', None),
            # Add more fields if needed
        }
        papers.append(paper)
    
    return papers


def save_papers_to_bibtex(papers, output_file_path):
    bib_database = BibDatabase()
    bib_database.entries = []

    for paper in papers:
        entry = {
            'ID': paper.get('ID', "no-id"),
            'ENTRYTYPE': 'article',  # Assuming all are articles; adjust as necessary
            'title': f"{{{paper['title']}}}",
            'abstract': paper.get('abstract', None),
            'doi': paper.get('doi', None),
            'author': paper.get('author', None),
            'year': paper.get('year', None),
            'journal': paper.get('journal', None),
            'keywords': paper.get('keywords', None),
            'url': paper.get('url', None),
            'pages': paper.get('pages', None),
            # Add more fields as necessary
        }
        # Remove None entries
        entry = {k: v for k, v in entry.items() if v is not None}
        bib_database.entries.append(entry)
    
    writer = BibTexWriter()
    with open(output_file_path, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

def get_pdf_url(doi, user_email):
    if not doi:
        return None
    
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(f"https://api.unpaywall.org/v2/{doi}?email={user_email}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['is_oa']:
            return data['best_oa_location']['url_for_pdf']
    
    return None

def download_pdf(url, save_path):
    try:
        # Send a request to the initial URL
        response = requests.get(url, allow_redirects=True)
        
        # Check the final URL and Content-Type
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'application/pdf' in content_type:
            # If the final content is a PDF, save it
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF successfully downloaded and saved to {save_path}")
        else:
            download_pdf_with_headers(url, save_path)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def download_pdf_with_headers(url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/pdf' in content_type:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"PDF successfully downloaded and saved to {save_path}")
        else:
            print(f"The final URL did not lead to a PDF file. Content-Type received: {content_type}")
            print(f"Final URL: {response.url}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def write_summary_to_file(summary, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing summary to file: {e}")