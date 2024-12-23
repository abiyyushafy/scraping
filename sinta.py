import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def get_articles_from_page(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('div', class_='ar-list-item')
    
    data = []
    for article in articles:
        title = article.find('div', class_='ar-title').get_text(strip=True)
        leader = article.find('a', href="#!").get_text(strip=True) 
        year = article.find('a', class_='ar-year').get_text(strip=True) 
        
        data.append([title, leader, year])
    
    return data

def scrape_sinta_data(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages + 1):
        print(f"Scraping halaman {page}...")
        url = f"{base_url}?page={page}"
        articles_data = get_articles_from_page(url)
        all_data.extend(articles_data)
    
    return all_data

base_url = 'https://sinta.kemdikbud.go.id/researches'

num_pages = int(input("Masukkan jumlah halaman yang ingin di-scrape: "))
data = scrape_sinta_data(base_url, num_pages)
df = pd.DataFrame(data, columns=['Judul Artikel', 'Penulis', 'Tahun Publikasi'])
df.to_csv('sinta_articles.csv', index=False)
print(df)

year_counts = df['Tahun Publikasi'].value_counts()
year_counts.plot(kind='bar', color='skyblue')
plt.title('Jumlah Artikel per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Artikel')
plt.show()
