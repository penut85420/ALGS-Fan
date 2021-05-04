import os
import pickle
import random
import datetime as dt
from loguru import logger
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class NiceSheet:
    def __init__(self):
        self.last_idx = -1
        self.get_sheet()
        self.update_interval = dt.timedelta(hours=1)

    def get_msg(self):
        if dt.datetime.now() - self.last_update > self.update_interval:
            self.get_sheet()

        v = len(self.values)
        self.last_idx += v + 1
        self.last_idx %= v

        return self.values[self.last_idx][0]

    def get_sheet(self):
        spreadsheet_id = os.getenv('SHEET_ID')
        worksheet_id = 0

        creds = pickle.loads(bytearray.fromhex(os.getenv('SHEET_TOKEN')))

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.get(spreadsheetId=spreadsheet_id).execute()
        for worksheet in result['sheets']:
            if worksheet['properties']['sheetId'] == worksheet_id:
                worksheet_name = worksheet['properties']['title']
        range_name = f'{worksheet_name}!B2:B'
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        self.values = values
        self.last_update = dt.datetime.now()
        ts = self.last_update.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'Nice Sheet last update: {ts}')
