import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/tech-stock-dashboard')
load_dotenv(os.path.join(project_folder,'.env'))

class Config:
    API_KEY = os.environ['API_KEY']