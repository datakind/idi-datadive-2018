import pandas as pd
from flask import render_template, request, send_file, flash, session
from tqdm import tqdm

from . import app

from .forms import SearchForm
from .scrapers.execute_search import execute_search
from .helpers import TableBuilder


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/search_terms', methods=['GET', 'POST'])
def search_terms():
    # TODO: optional: validate search_terms
    # TODO: optional: offer selector for DFI site, default to 'all'
    if request.method == 'POST':
        f = request.files['file']
        df = pd.read_csv(f, header=None)
        df.columns = ['Terms']
        session['search_terms'] = [i.strip() for i in df.Terms]
        table_html = df.to_html(classes=['table', 'tableformat'])
        table_html = table_html.replace('style="text-align: right;"', '')
        form = SearchForm()

        return render_template('search_terms.html', form=form, title='Search Terms', table=table_html)


@app.route('/run', methods=['GET', 'POST'])
def run_scraper():
    error = None
    master_df = None

    for idx, term in enumerate(tqdm(session.get('search_terms'))):
        results = execute_search(term)
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
