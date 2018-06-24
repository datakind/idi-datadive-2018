import logging
import pandas as pd
from flask import render_template, request, send_file, flash, session
from tqdm import tqdm

from . import app

from .forms import SearchForm
from .scrapers.execute_search import execute_search, SELECT_ALL_NAME
from .helpers import TableBuilder


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/search_terms', methods=['POST'])
def search_terms():
    if request.method == 'POST':
        f = request.files['file']

        # clean input, remove space paddings, drop duplicates
        terms = pd.read_csv(f, header=None)[0].str.strip()
        duplicated_terms = [term for term in terms[terms.duplicated()]]
        if duplicated_terms:
            flash('{} term(s) were dropped for being duplicates: {}'.format(
                len(duplicated_terms), duplicated_terms
            ))
            terms.drop_duplicates(inplace=True)
            terms.reset_index(inplace=True, drop=True)

        # flag words smaller than a certain length
        min_word_length = 4
        terms_too_small = terms[terms.str.len() < min_word_length]
        if terms_too_small.size:
            flash('{} term(s) have less than {} characters: {}'.format(
                terms_too_small.size, min_word_length, [term for term in terms_too_small],
            ))

        df = pd.DataFrame(terms)
        df.columns = ['Terms']
        table_html = df.to_html(classes=['table', 'tableformat'])
        table_html = table_html.replace('style="text-align: right;"', '')
        form = SearchForm()

        session['search_terms'] = [term for term in df.Terms] # for reuse in next request

        return render_template(
            'search_terms.html',
            form=form,
            title='Search Terms',
            table=table_html,
        )


@app.route('/run', methods=['POST'])
def run_scraper():
    error = None
    master_df = None

    scraper_names = request.form.getlist('scrapers')
    if not scraper_names:
        scraper_names.append(SELECT_ALL_NAME)

    for idx, term in enumerate(tqdm(session.get('search_terms'))):
        try:
            results = execute_search(term, scraper_names)
        except Exception as e:
            logger.exception("The scraper {scraper_names} failed on the search {term}"
                             .format(scraper_names=scraper_names, term=term))
            failed_data = [['Error', 'Error', 'Error', scraper_names, term]]
            results = pd.DataFrame(failed_data, columns=['Project Name', 'URL', 'Status', 'DFI', 'Search Term'])

        if idx == 0:
            master_df = results
        else:
            master_df = master_df.append(results)
        # reset index numbering
        master_df = master_df.reset_index(drop=True)

    if len(master_df) > 0:
        table_builder = TableBuilder(master_df)
        table_builder.save_df()
        table_html = table_builder.get_table_html()

        return render_template('table.html', title='Ran', table=table_html)
    else:
        flash('No Search Results Found')
        return render_template('index.html', error=error)


@app.route('/table-page-actions', methods=['GET', 'POST'])
def table_page_actions():

    if request.method == 'POST':
        if 'Home' in request.form:
            return render_template('index.html', title='Home')
        elif 'Download' in request.form:
            return send_file('output_data/ifc_scrape.csv', attachment_filename='ifc_scrape.csv', as_attachment=True)
        else:
            pass  # unknown
    else:
        print('not a post')
