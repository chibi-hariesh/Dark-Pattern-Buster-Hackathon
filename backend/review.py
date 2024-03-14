import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from textblob import TextBlob

def scrape_usernames(soup, username_class):
    try:
        username_elements = soup.find_all('p', class_=username_class)
        usernames = [element.text.strip() for element in username_elements]
        return usernames
    except Exception as e:
        print(f"Error occurred while scraping usernames: {str(e)}")
        return []

def scrape_titles(soup, title_class):
    try:
        title_elements = soup.find_all('p', class_=title_class)
        titles = [element.text.strip() for element in title_elements]
        return titles
    except Exception as e:
        print(f"Error occurred while scraping titles: {str(e)}")
        return []

def scrape_reviews(soup, review_class):
    try:
        review_elements = soup.find_all('div', class_=review_class)
        reviews = [element.text.strip().replace("READ MORE", "") for element in review_elements]
        return reviews
    except Exception as e:
        print(f"Error occurred while scraping reviews: {str(e)}")
        return []

def scrape_upvotes_downvotes(soup, upvote_downvote_class):
    try:
        upvote_downvote_elements = soup.find_all('div', class_=upvote_downvote_class)
        upvotes_downvotes = [element.find('span', class_='_3c3Px5').text.strip() for element in upvote_downvote_elements]
        return upvotes_downvotes
    except Exception as e:
        print(f"Error occurred while scraping upvotes/downvotes: {str(e)}")
        return []

def scrape_review_data(base_url, review_class, star_class, title_class, upvote_downvote_class, username_class, total_pages):
    all_review_data = []
    count_reviews = {'Positive Legitimate Review': 0,  'Negative Legitimate Review': 0, 'Positive Misleading Review': 0, 'Negative Misleading Review': 0, 'Neutral Review': 0}

    review_id = 1  # Initialize review ID counter

    try:
        for page in range(1, total_pages + 1):
            response = requests.get(f"{base_url}&page={page}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                usernames = scrape_usernames(soup, username_class)
                titles = scrape_titles(soup, title_class)
                reviews = scrape_reviews(soup, review_class)
                upvotes_downvotes = scrape_upvotes_downvotes(soup, upvote_downvote_class)

                for i in range(len(usernames)):
                    review = {
                        "id": review_id,  # Assign the review ID
                        "User Name": usernames[i],
                        "Title": titles[i],
                        "Review": reviews[i],
                        "Upvote": upvotes_downvotes[i*2],
                        "Downvote": upvotes_downvotes[i*2 + 1]
                    }
                    review['Sentiment'] = analyze_sentiment(review['Title'], review['Review'])
                    review['Response'] = get_response(review['Sentiment'], review['Upvote'], review['Downvote'])

                    # Update count_reviews dictionary
                    if review['Response'].startswith("Negative"):
                        count_reviews[review['Response']] += 1
                    elif review['Response'].startswith("Positive"):
                        count_reviews[review['Response']] += 1
                    else:
                        count_reviews['Neutral Review'] += 1  # Increment neutral review count
                    all_review_data.append(review)

                    review_id += 1  # Increment the review ID counter
            else:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred during review data scraping: {str(e)}")

    return all_review_data, count_reviews


def review_check(product_url):
    try:
        predefined_url = get_review_page_url(product_url)
        review_class_to_find = 't-ZTKy'
        star_class_to_find = '_3LWZlK _1BLPMq'
        title_class_to_find = '_2-N8zT'
        upvote_downvote_class_to_find = '_1LmwT9'
        username_class_to_find = '_2sc7ZR _2V5EHH'

        total_pages = get_total_pages(predefined_url)

        if total_pages == 0:
            print("No review pages found.")
            return {"result":"No Reviews Found"}

        review_data, count_reviews = scrape_review_data(predefined_url, review_class_to_find, star_class_to_find, title_class_to_find, upvote_downvote_class_to_find, username_class_to_find, total_pages)

        with open('../src/reviewresult/reviews_with_sentiment.json', 'w') as f:
            json.dump(review_data, f, indent=2)

        return count_reviews
    except Exception as e:
        print(f"Error occurred during review check: {str(e)}")
        return {"result":"No Review Found"}


def get_review_page_url(url):
    try:
        response = requests.get(url)
        full_url = None

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            target_div = soup.find('div', class_='col JOpGWq')

            if target_div:
                anchor_element = target_div.find('a', recursive=False)

                if anchor_element:
                    anchor_href = anchor_element.get('href')
                    full_url = urljoin(url, anchor_href)
                    if not full_url.endswith("&page=1"):
                        full_url += "&page=1"

        return full_url
    except Exception as e:
        print(f"Error occurred while getting review page URL: {str(e)}")
        return None


def get_total_pages(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_info = soup.find('div', class_='_2MImiq _1Qnn1K')

            if page_info:
                total_pages = int(page_info.find('span').text.split()[-1])
                return total_pages
    except Exception as e:
        print(f"Error occurred while getting total pages: {str(e)}")
    return 0


def analyze_sentiment(title, review_text):
    try:
        combined_text = title + " " + review_text
        analysis = TextBlob(combined_text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        else:
            return 'Negative'
    except Exception as e:
        print(f"Error occurred during sentiment analysis: {str(e)}")
        return 'Neutral'

def get_response(sentiment, upvotes, downvotes):
    try:
        if sentiment == 'Positive' and int(upvotes) > int(downvotes):
            return "Positive Legitimate Review"
        elif sentiment == 'Negative' and int(upvotes) > int(downvotes):
            return "Negative Legitimate Review"
        elif sentiment == 'Positive' and int(upvotes) < int(downvotes):
            return "Positive Misleading Review"
        elif sentiment == 'Negative' and int(upvotes) < int(downvotes):
            return "Negative Misleading Review"
        else:
            return "Neutral Review"
    except Exception as e:
        print(f"Error occurred while getting response: {str(e)}")
        return "Neutral Review"
