from flask import render_template, redirect, url_for, request, send_file, flash, session
from app import app
import pandas as pd
from ifc_scraper import execute_search
from tqdm import tqdm

# export FLASK_APP=app/__init__.py;

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/searchterms', methods=['GET', 'POST'])
def searchterms():
    # TODO: optional: validate search_terms
    # TODO: optional: offer selector for DFI site, default to 'all'
    if request.method == 'POST':
        f = request.files['file']
        df = pd.read_csv(f, header=None)
        df.columns = ['Terms']
        session['search_terms'] = [i.strip() for i in df.Terms]
        table_html = df.to_html(classes=['table','tableformat'])
        table_html = table_html.replace('style="text-align: right;"','')

        return render_template('searchterms.html', title='Search Terms', table=table_html)


@app.route('/run', methods=['GET','POST'])
def run_scraper():
    error = None
    master_df = None

    for idx, t in enumerate(tqdm(session['search_terms'])):
        print(t)
        results = execute_search(t)
        if idx == 0:
            master_df = results
        else:
            master_df = master_df.append(results)
        master_df = master_df.reset_index(drop=True)

    if len(master_df) > 0:
        grpd_df = (master_df[['Project Name', 'url', 'Search Term']]
                            .groupby(['Project Name', 'url'])
                            .agg(lambda z: tuple(z))
                            .reset_index()
                   )
        grpd_df['Search Term'] = [','.join(i) for i in grpd_df['Search Term']]

        # Add Reference Columns
        grpd_df['Reviewed'] = None
        grpd_df['DFI'] = 'IFC'

        # TODO: Add informative headers

        # Save
        # TODO: Give unique filename
        grpd_df.to_csv('app/output_data/ifc_scrape.csv',index=False)

        # TODO: optional: to_excel, with urls converted to live links

        # Prep HTML
        table_html = grpd_df.to_html(classes=['table','tableformat'])
        table_html = table_html.replace('style="text-align: right;"', '')

        return render_template('table.html', title='Ran', table=table_html)
    else:
        flash('No Search Results Found')
        return render_template('index.html', error=error)


@app.route('/table_page_actions' , methods=['GET','POST'])
def table_page_actions():

    if request.method == 'POST':
        if 'Home' in request.form:
            return render_template('index.html', title='Home')
        elif 'Download' in request.form:
            return send_file('output_data/ifc_scrape.csv', attachment_filename='ifc_scrape.csv', as_attachment=True)
        else:
            pass # unknown
    else:
        print('not a post')
