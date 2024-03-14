import requests
from bs4 import BeautifulSoup
import time

def rating_review_check(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(2)
        
        product_title_tag = soup.find('h1', class_='yhB1nd')
        product_title = product_title_tag.text.strip() if product_title_tag else None

        product_div = soup.find('div', class_='_3_L3jD')

        if product_div:
            rating_div = product_div.find('div', class_='_3LWZlK')
            rating = rating_div.text.strip() if rating_div else None

            rating_count_span = product_div.find('span', class_='_2_R_DZ')
            if rating_count_span:
                rating_count_text = rating_count_span.text.strip()
                rating_count = rating_count_text.split('&')[0].strip()
                review_count = rating_count_text.split('&')[1].split()[0].strip()
            else:
                rating_count = None
                review_count = None

            return {
                'product_title': product_title,
                'rating': rating,
                'rating_count': rating_count,
                'review_count': review_count
            }
        else:
            return {'product_title':product_title,'result': "This product has not yet been reviewed or rated by any verified customers"}
    except Exception as e:
        return {'error': str(e)}
