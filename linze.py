import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from collections import Counter
import re

def crawl_lao_dong(url, output_file='crawl_lao_dong.xlsx'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lấy tất cả các bài viết
        articles = soup.select('h2 a')  # Tìm tất cả thẻ a trong thẻ h2
        data = []
        titles = []
        
        # Lặp qua từng liên kết để lấy tiêu đề và URL
        for article in articles:
            title = article.text.strip()
            href = article['href']
            data.append({'Tiêu đề': title, 'Liên kết': href})
            titles.append(title)
        
        # Lưu dữ liệu vào file Excel
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Dữ liệu đã được lưu vào file {output_file}.")
        
        # Tìm từ khóa phổ biến nhất
        words = re.findall(r'\b\w+\b', ' '.join(titles).lower())
        word_counts = Counter(words)
        if word_counts:
            most_common_word, most_common_count = word_counts.most_common(1)[0]
            print(f'Từ khóa phổ biến nhất là "{most_common_word}" với {most_common_count} lần xuất hiện.')
        
        # Mở tệp Excel
        os.startfile(output_file)
    else:
        print(f'Lỗi: Không thể truy cập trang {url} (Mã lỗi: {response.status_code})')

# Ví dụ sử dụng
url_to_crawl = 'https://laodong.vn/'
crawl_lao_dong(url_to_crawl)
