from flask_wtf import FlaskForm
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired

SCRAPERS = [
    ('IFC', 'IFC'),
    ('World Bank', 'World Bank'),
]

class SearchForm(FlaskForm):
    scrapers = SelectMultipleField('Choose Sites', choices=SCRAPERS)
