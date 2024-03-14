from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from discount import discount_check
from ratingStatus import rating_review_check
from review import review_check
from timer import time_check
from urgency import urgency_check
import os



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
relative_json_file_path = '../src/reviewresult/reviews_with_sentiment.json'
absolute_json_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_json_file_path))

@app.route('/discount', methods=['POST'])
def get_discount():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    result = discount_check(url)
    return jsonify(result)

@app.route('/rating-review', methods=['POST'])
def get_rating_review():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    result = rating_review_check(url)
    return jsonify(result)

@app.route('/review', methods=['POST'])
def get_review():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    result = review_check(url)
    return jsonify(result)

@app.route('/delivery-time', methods=['POST'])
def get_delivery_time():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    result = time_check(url)
    return jsonify(result)

@app.route('/urgency', methods=['POST'])
def get_urgency():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    result = urgency_check(url)
    return jsonify(result)

# Define the route to delete the JSON file
import os
from flask import jsonify

@app.route('/deletejson', methods=['DELETE'])
def delete_json_file():
    try:
        # Define the content to add to the JSON file
        new_content = [
            {
                "id": None,
                "User Name": "No Data Found",
                "Title": "No Data Found",
                "Review": "No Data Found",
                "Upvote": "No Data Found",
                "Downvote": "No Data Found",
                "Sentiment": "No Data Found",
                "Response": "No Data Found"
            }
        ]

        # Write the new content to the JSON file
        with open(relative_json_file_path, 'w') as f:
            json.dump(new_content, f, indent=2)

        return jsonify(message='JSON file content cleared successfully'), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
