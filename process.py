import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import date, timedelta

scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
d = date.today()

source = client.open("Zdroj (kopie).xlsm").sheet1
fnd = client.open('fnddaily{}.xls'.format(d.strftime('%d%m%Y'))).sheet1

source_df = pd.DataFrame(source.get_all_records())
fnddaily = pd.DataFrame(fnd.get_all_records())

existing_columns = list(source_df.columns.values)
still_not_existing = True


# add not existing dates columns
while still_not_existing:
    if d.strftime('%-d.%-m.%Y') not in existing_columns:
        source.update_cell(1, existing_columns.__len__()+1, d.strftime('%-d.%-m.%Y'))
        source = client.open("Zdroj (kopie).xlsm").sheet1
        source_df = pd.DataFrame(source.get_all_records())
        existing_columns = list(source_df.columns.values)
    else:
        still_not_existing = False

# source_df.set_index("ISIN", inplace=True)

for index, row in fnddaily.iterrows():
    try:
        # column index
        column_index_0 = source_df.columns.get_loc(row['Datum'])
        column_index = existing_columns.__len__() - 1 - column_index_0

        # row index
        row_index = source_df.index[source_df['ISIN'] == row['ISIN']].tolist()[0]
        source.update_cell(row_index+2, column_index+1, row['Cena/ks'])
    except:
        pass
