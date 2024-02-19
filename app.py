from flask import Flask, request, jsonify, redirect, abort, Response
from database.db import DatabaseConnection
from services.UrlService import UrlService
from database.dbmodels import Url
from dotenv import load_dotenv
import os
import json
from pprint import pprint

def init_database():
    database_client.init_app(app)
    database_client.create_database(app)

load_dotenv()
app = Flask(__name__)
database_client = DatabaseConnection(
    os.getenv("DATABASE_NAME"), 
    os.getenv("DATABASE_URI")
)

shortener = UrlService()

init_database()

@app.route('/')
def home():
    return 'Service is up!'

@app.route('/api/create', methods=['POST'])
def shortenUrl():
    if not request.is_json:
        return Response('Request must be JSON', 400)
    data = request.get_json()

    if "url" not in data:
        return Response('Url parameter is missing', 422)

    result = shortener.create_short_url(data['url'])
    return result, 201

@app.route('/api/view_all')
def view_all_urls():
    urls = shortener.view_all()
    return jsonify(data=[url.serialize for url in urls])

@app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = shortener.view(short_url)

    if original_url:
        return redirect(original_url)
    else:
        return 'Not found'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
