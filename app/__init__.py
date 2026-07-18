import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)

from app import routes
