import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
