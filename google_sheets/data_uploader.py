import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '../credentials.json')

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1HBdzHadjWKeoCWGWeY0UKEoqBZnwHFMzWjvlMml1NVU'
SAMPLE_RANGE_NAME = 'Sheet1'


def upload_sheets_data() -> pd.DataFrame:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

    # Call the Sheets API
    result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=SAMPLE_RANGE_NAME).execute()

    data_from_sheet = result.get('values', [])

    return pd.DataFrame(data=data_from_sheet[1:], columns=[0])


# array = {'values': [[5, 6, None, 100], ['=SUM(A1:A4)', '=SUM(B1:B4)']]}
# range_ = A1Range.create_a1range_from_list(SAMPLE_RANGE_NAME, 4, 1, arrauply['values']).format()
# response = service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                          range=range_,
#                          valueInputOption='USER_ENTERED',
#                          body=array).execute()


if __name__ == "__main__":
    upload_sheets_data()
