import os
from dotenv import load_dotenv
load_dotenv()



class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///api.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    BASE_API_URL = os.getenv('API_URL')