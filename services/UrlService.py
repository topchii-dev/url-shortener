import string
import random
from database.dbmodels import Url
from database import db
from flask import jsonify
import os

class UrlService:

    STRING_LENGTH = 6
    APPLICATION_URL = os.getenv("APPLICATION_URL")

    def generate_short_url(self) -> str:
        """
        Create short url by generating
        random string and appending it to
        the app's domain name
        """
        shortenedUrl = f'{self.APPLICATION_URL}/{self.generate_random_string()}'
        return shortenedUrl

    def generate_random_string(self) -> str:
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(self.STRING_LENGTH))
    
    def view_all(self):
        records = Url.view_all()
        return records
    
    def create_short_url(self, url: str):
        generatedUrl = self.generate_short_url()
        newModel = Url.create(original_url=url, shorten_url=generatedUrl)
        return newModel.serialize
    
    def view(self, shortened_url):
        # Search only by shorten url
        entry = Url.view('shorten_url', shortened_url)
        return entry.serialize