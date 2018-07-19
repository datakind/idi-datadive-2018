from datetime import datetime
from pathlib import Path
import pandas as pd

class TableBuilder(object):
    def __init__(self, master_df, scraper_names, search_terms):
        self.master_df = master_df
        self.scraper_names = scraper_names
        self.search_terms = search_terms
        self.grpd_df = self._process_df()
        self.abs_filepath = self._make_absolute_filepath()
        self.filename = self.abs_filepath.name

    def save_df(self):
        # Save
        writer = pd.ExcelWriter(self.filename)

        data_df = self.grpd_df.copy(deep=True)
        data_df['URL'] = data_df.URL.apply(
            lambda x: '=HYPERLINK("{url}", "{url}")'.format(url=x)
        )
        data_df.to_excel(writer, sheet_name='Results', index=False)

        DFI_df = pd.DataFrame([name for name in self.scraper_names])
        DFI_df.columns = ['DFI']
        DFI_df.to_excel(writer, sheet_name='DFI', index=False)

        search_terms_df = pd.DataFrame([term for term in self.search_terms])
        search_terms_df.columns = ['Search Terms']
        search_terms_df.to_excel(writer, sheet_name='Search Terms', index=False)

        writer.save()

    def get_table_html(self):
        # Prep HTML
        table_html = self.grpd_df.to_html(classes=['table', 'tableformat'])
        table_html = table_html.replace('style="text-align: right;"', '')
        return table_html

    def _process_df(self):
        grpd_df = (self.master_df.fillna('')  # to avoid losing records in the groupby
                   .groupby(['Project Name', 'URL', 'Status', 'DFI'])
                   .agg(lambda z: tuple(z))
                   .reset_index()
                   )
        grpd_df['Search Term'] = [', '.join(set(i)) for i in grpd_df['Search Term']]

        # Add Reference Columns
        grpd_df['Reviewed'] = None

        return grpd_df

    def _make_absolute_filepath(self):
        now = datetime.now().replace(microsecond=0).isoformat().replace(':', '-')
        filename = '{}_results.xlsx'.format(now)
        path = Path('app') / Path('output_data')
        filepath = path / Path(filename)
        return filepath.absolute()
