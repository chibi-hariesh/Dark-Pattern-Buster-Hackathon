import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def open_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def tap_price_info_icon(driver):
    price_info_icon = driver.find_element(By.ID, "price-info-icon")
    price_info_icon.click()
    time.sleep(1)
    price_info_icon.click()
    time.sleep(1)

def extract_prices(driver):
    mrp = None
    selling_price = None
    special_price = None
    
    try:
        mrp_element = driver.find_element(By.XPATH, '//div[contains(text(), "Maximum Retail Price")]/following-sibling::div')
        mrp = mrp_element.text.strip()
    except NoSuchElementException:
        pass
    
    try:
        selling_price_element = driver.find_element(By.XPATH, '//div[contains(text(), "Selling Price")]/following-sibling::div')
        selling_price = selling_price_element.text.strip()
    except NoSuchElementException:
        pass
    
    try:
        special_price_element = driver.find_element(By.XPATH, '//div[contains(text(), "Special Price")]/following-sibling::div')
        special_price = special_price_element.text.strip()
    except NoSuchElementException:
        pass
    
    return mrp, selling_price, special_price


def calculate_discount(mrp, selling_price, special_price):

    original_price = float(mrp.replace('₹', '').replace(',', '').strip())
    sell_price = float(selling_price.replace('₹', '').replace(',', '').strip())

    if special_price:
        discounted_price = float(special_price.replace('₹', '').replace(',', '').strip())
        discount_amount = int(sell_price - discounted_price)
    else:
        discounted_price = float(selling_price.replace('₹', '').replace(',', '').strip())
        discount_amount = int(original_price - selling_price)
    
    
    discount_percentage = int((discount_amount / original_price) * 100)
    return discount_amount, discount_percentage

def extract_actual_discount_percentage(html_content):
    actual_discount_percentage_match = re.search(r'(\d+)% off', html_content)
    if actual_discount_percentage_match:
        actual_discount_percentage = int(actual_discount_percentage_match.group(1))
    else:
        actual_discount_percentage = None
    return actual_discount_percentage

def compare_discounts(actual_discount_percentage, calculated_discount_percentage):
    if actual_discount_percentage is not None:
        if abs(actual_discount_percentage - calculated_discount_percentage) <= 1:
            return "No dark pattern found in Discount.", calculated_discount_percentage, actual_discount_percentage
        else:
            return "Dark pattern detected in Discount.", calculated_discount_percentage, actual_discount_percentage
    else:
        return "Actual discount percentage not found in HTML.", calculated_discount_percentage, None

def discount_check(url):
    result_dict = {}
    
    # Step 1: Open Chrome
    driver = open_chrome()
    
    # Step 2: Navigate to the URL
    driver.get(url)
    
    # Step 3: Tap on the price info icon twice with a 1-second interval
    tap_price_info_icon(driver)
    
    # Step 4: Extract prices
    mrp, selling_price, special_price = extract_prices(driver)
    
    result_dict['MRP'] = mrp
    result_dict['Selling Price'] = selling_price
    result_dict['Special Price'] = special_price
    
    # Step 5: Calculate discount
    discount_amount, discount_percentage = calculate_discount(mrp, selling_price, special_price)
    
    result_dict['Discount Amount'] = discount_amount
    result_dict['Discount Percentage'] = discount_percentage
    
    # Step 6: Extract actual discount percentage from HTML content
    html_content = driver.page_source
    actual_discount_percentage = extract_actual_discount_percentage(html_content)
    
    # Step 7: Compare discounts
    result, real_discount_percentage, given_discount_percentage = compare_discounts(actual_discount_percentage, discount_percentage)
    
    result_dict['Result'] = result
    result_dict['Real Discount Percentage'] = real_discount_percentage
    result_dict['Given Discount Percentage'] = given_discount_percentage
    
    # Close the browser
    driver.quit()
    
    return result_dict