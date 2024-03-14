import time
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

def check_timer(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        delivery_info_div = soup.find("div", class_="_20XEBf")
        if delivery_info_div:
            timer_element = delivery_info_div.find("div", class_="_1dXn7l")
            if timer_element:
                return timer_element.get_text().strip()
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def check_delivery_date(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        delivery_info_div = soup.find("div", class_="_3XINqE")
        if delivery_info_div:
            date_element = delivery_info_div.find("span", class_="_1TPvTK")
            if date_element:
                return date_element.get_text().strip()
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def time_check(url):
    try:
        html = fetch_page(url)
        if html is None:
            return {"result": "Error occurred: Unable to fetch the webpage", "res": 0}

        initial_timer = check_timer(html)
        delivery_date = check_delivery_date(html)

        if initial_timer is None:
            return {"result": "There is no delivery timer found", "initial_timer": None, "updated_timer": None, "delivery_date": delivery_date, "res": 0}

        print(f"Initial Timer: {initial_timer}")

        start_time = time.time()
        while time.time() - start_time <= 60:
            html = fetch_page(url)
            if html is None:
                return {"result": "Error occurred: Unable to fetch the webpage", "initial_timer": initial_timer, "updated_timer": None, "delivery_date": delivery_date, "res": 0}
            
            current_timer = check_timer(html)
            if current_timer is None:
                return {"result": "There is no delivery timer found", "initial_timer": initial_timer, "updated_timer": None, "delivery_date": delivery_date, "res": 0}
            elif current_timer != initial_timer:
                print(f"Updated Timer: {current_timer}")
                return {"result": "Potential Dark Pattern Found in the timer.....", "initial_timer": initial_timer, "updated_timer": current_timer, "delivery_date": delivery_date, "res": 1}
            
            time.sleep(2)
        
        return {"result": "The timer is likely real.....", "initial_timer": initial_timer, "updated_timer": initial_timer, "delivery_date": delivery_date, "res": 0}

    except Exception as e:
        return {"result": f"Error occurred: {str(e)}", "initial_timer": None, "updated_timer": None, "delivery_date": None, "res": 0}
