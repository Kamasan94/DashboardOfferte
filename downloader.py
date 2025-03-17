import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Open Data URL
URL = "https://www.ilportaleofferte.it/portaleOfferte/it/open-data.page"

#Destination folder
DOWNLOAD_FOLDER = "offerte"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_file_list():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    #Find all CSV/XML
    links = soup.findAll("a", href=True)
    
    file_links = [link["href"] for link in links if link["href"].endswith(".csv") or link["href"].endswith(".xml")]
    
    return file_links

def download_file(url):
    
    Segments = url.rpartition('/')
    filename = os.path.join(DOWNLOAD_FOLDER, Segments[-1])
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(filename, "wb") as file:
        file.write(response.content)
        
    print(f"✅ File scaricato: {filename}")


file_list = get_file_list()
if file_list:
    for file in file_list:
        full_url = f"https://www.ilportaleofferte.it{file}"  
        download_file(full_url)
else:
    print("⚠ Nessun file trovato.")

    
    