import requests
from bs4 import BeautifulSoup
import time

def urgency_check(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(2)
        urgency_div = soup.find('div', class_='_2JC05C')
        if urgency_div:
            return {'result': f"Urgency found for this product by mentioning \"{urgency_div.text.strip()}\""}
        else:
            return {'result': 'No urgency found for this product'}
    except Exception as e:
        return {'error': str(e)}