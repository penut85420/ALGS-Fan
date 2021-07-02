import os
import pickle
import random
import datetime as dt
from loguru import logger
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class ALGS_Sheet:
    def __init__(self, sents_worksheet_id, clips_worksheet_id, name='Unnamed'):
        self.sents = None
        self.clips = None
        self.sents_worksheet_id = sents_worksheet_id
        self.clips_worksheet_id = clips_worksheet_id
        self.name = name
        self.sequence = []
        self.last_idx = -1
        self.get_sheet()
        self.update_interval = dt.timedelta(hours=1)

    def get_msg(self):
        if dt.datetime.now() - self.last_update > self.update_interval:
            self.get_sheet()

        v = len(self.sents)
        self.last_idx += v + 1
        self.last_idx %= v

        if not self.sequence:
            self.sequence = list(range(len(self.clips)))
            random.shuffle(self.sequence)

        return (
            f'{self.sents[self.last_idx][0]} '
            f'{self.clips[self.sequence.pop()][0]}'
        )

    def get_sheet(self):
        spreadsheet_id = os.getenv('SHEET_ID')
        creds = pickle.loads(bytearray.fromhex(os.getenv('SHEET_TOKEN')))

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.get(spreadsheetId=spreadsheet_id).execute()

        def get_value(worksheet_id, range):
            for worksheet in result['sheets']:
                if worksheet['properties']['sheetId'] == worksheet_id:
                    worksheet_name = worksheet['properties']['title']

            range_name = f'{worksheet_name}!{range}'
            _result = sheet.values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = _result.get('values', [])

            return values

        self.sents = get_value(self.sents_worksheet_id, 'B2:B')
        self.clips = get_value(self.clips_worksheet_id, 'B2:B')

        self.last_update = dt.datetime.now()
        ts = self.last_update.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'{self.name} Sheet last update: {ts}')
