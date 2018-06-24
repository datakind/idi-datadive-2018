from datetime import datetime
from pathlib import Path

class TableBuilder(object):
    def __init__(self, master_df):
        self.master_df = master_df
        self.grpd_df = self._process_df()

    def save_df(self):
        # Save
        now = datetime.now().replace(microsecond=0).isoformat().replace(':', '-')
        name = '{}_results.csv'.format(now)
        path = Path('app') / Path('output_data')
        filepath = path / Path(filename)
        self.grpd_df.to_csv(filepath, index=False)

        # TODO: optional: to_excel, with urls converted to live links

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
        grpd_df['Search Term'] = [', '.join(i) for i in grpd_df['Search Term']]

        # Add Reference Columns
        grpd_df['Reviewed'] = None

        # TODO: Add informative headers
        return grpd_df
