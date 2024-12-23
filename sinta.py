import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk mendapatkan data artikel dari satu halaman
def get_articles_from_page(url):
    # Mengambil halaman HTML
    response = requests.get(url)
    response.raise_for_status()  # Jika gagal, raise error
    
    # Parse HTML dengan BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Mencari data artikel
    articles = soup.find_all('div', class_='ar-list-item')
    
    # Menyimpan hasil scraping dalam format list
    data = []
    for article in articles:
        title = article.find('div', class_='ar-title').get_text(strip=True)
        leader = article.find('a', href="#!").get_text(strip=True)  # Nama penulis
        year = article.find('a', class_='ar-year').get_text(strip=True)  # Tahun publikasi
        
        data.append([title, leader, year])
    
    return data

# Fungsi untuk mengambil data dari beberapa halaman
def scrape_sinta_data(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages + 1):
        print(f"Scraping halaman {page}...")
        
        # Membentuk URL untuk setiap halaman
        url = f"{base_url}?page={page}"
        
        # Ambil artikel dari halaman
        articles_data = get_articles_from_page(url)
        all_data.extend(articles_data)  # Menambahkan data artikel ke list total
    
    return all_data

# URL dasar dari situs SINTA
base_url = 'https://sinta.kemdikbud.go.id/researches'

# Meminta input dari pengguna untuk jumlah halaman yang ingin diambil
num_pages = int(input("Masukkan jumlah halaman yang ingin di-scrape: "))

# Scraping data dari beberapa halaman
data = scrape_sinta_data(base_url, num_pages)

# Membuat DataFrame dengan pandas
df = pd.DataFrame(data, columns=['Judul Artikel', 'Penulis', 'Tahun Publikasi'])

# Menyimpan data ke dalam file CSV
df.to_csv('sinta_articles.csv', index=False)

# Menampilkan data dalam format tabel di terminal
print(df)

# Analisis Data: Visualisasi jumlah artikel per tahun
year_counts = df['Tahun Publikasi'].value_counts()

# Plotting jumlah artikel per tahun
year_counts.plot(kind='bar', color='skyblue')
plt.title('Jumlah Artikel per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Artikel')
plt.show()
