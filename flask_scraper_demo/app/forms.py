from wtforms import Form
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired

from .scrapers.execute_search import SCRAPER_MAP, SELECT_ALL_NAME

SCRAPER_NAMES = [
    (name, name) for name in [SELECT_ALL_NAME] + sorted(SCRAPER_MAP.keys())
]

class SearchForm(Form):
    scrapers = SelectMultipleField('Choose Sites', choices=SCRAPER_NAMES)
