import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

import pandas as pd

class GoogleSheet:

    def __init__(self, json_credentials, spreadsheet_id):
        self.json_credentials = json_credentials
        self.spreadsheet_id = spreadsheet_id
        self.gc = None
        self.worksheet = None

    def connect(self):
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        # Add your service account file
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.json_credentials, scope)
        # Authenticate
        self.gc = gspread.authorize(creds)

    def get_worksheet(self, worksheet_name=None):
        # Ensure we're connected before trying to use self.gc
        self.connect()
        # Open the spreadsheet
        spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
        # Open the specific worksheet if name is given, else open the first sheet of the spreadsheet
        self.worksheet = spreadsheet.worksheet(worksheet_name) if worksheet_name else spreadsheet.sheet1

    def get_all_values(self):
        return self.worksheet.get_all_values()

    def to_dataframe(self, worksheet_name=None):
        self.get_worksheet(worksheet_name)
        values = self.get_all_values()
        return pd.DataFrame(values[1:], columns=values[0])  # Using the first row as column names

# Usage:
# gs = GoogleSheet('sheets-service-account.json', '1pFwRozK2yW7_3XR0UPb2THK4rxcgbulukoA2Xq70QeQ')
# df = gs.to_dataframe('reddit')
# print(df)




class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def upload_dataframe(self, df, table_name, if_exists='fail'):
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)

    def close(self):
        self.conn.close()


def dataframe_to_text_file(df, output_file):
    with open(output_file, 'w') as file:
        for _, row in df.iterrows():
            file.write('Softtitle: ' + str(row['softTitle']) + '\n')
            file.write('Publisher: ' + str(row['publisher']) + '\n')
            file.write('Author: ' + str(row['author/0']) + '\n')
            file.write('Date: ' + str(row['date']) + '\n')
            file.write('Text: ' + str(row['text']) + '\n')
            file.write('---END OF ARTICLE---\n\n')


# Usage:

#db = Database('example.db')
#df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
#db.upload_dataframe(df, 'my_table')
#print(db.fetchall("SELECT * FROM my_table"))
#db.close()
