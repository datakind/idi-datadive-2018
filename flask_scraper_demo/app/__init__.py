from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app._static_folder = 'static'
app.secret_key = 'many random bytes'

from app import routes


