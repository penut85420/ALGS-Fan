import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TWSC_CALENDAR = '59o7f5ng87g2ilq635r5r78o04@group.calendar.google.com'
WEEK_DELTA = datetime.timedelta(days=7)
CRED_PATH = './credentials.json'
TOKEN_PATH = './token.pickle'

class TWSCCalendar:
    def __init__(self):
        self.creds = self.get_creds()

    def get_creds(self):
        creds = None

        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CRED_PATH, SCOPES)
                creds = flow.run_local_server()
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def _get_utcstr(self, t):
        return t.strftime('%Y-%m-%dT00:00:00Z')

    def _get_time(self):
        now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)
        end = now + WEEK_DELTA

        now = self._get_utcstr(now)
        end = self._get_utcstr(end)

        return now, end

    def get_events(self, max_result=50):
        service = build('calendar', 'v3', credentials=self.creds)

        now, end = self._get_time()

        events_result = service.events().list(  # pylint: disable=no-member
            calendarId=TWSC_CALENDAR, maxResults=max_result, singleEvents=True,
            timeMin=now, timeMax=end, orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    def parse_event(self, e):
        title = e['summary'].replace('[SC2] ', '')
        start = self.get_date(e, 'start')
        end = self.get_date(e, 'end')

        return start, end, title

    def get_date(self, e, key):
        date = e[key].get('dateTime', e[key].get('date'))
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+08:00')
        date = date - datetime.timedelta(hours=8)

        return date

    def get_next_event(self, next_only=False):
        now = datetime.datetime.utcnow()
        for e in self.get_events():
            start, end, title = self.parse_event(e)

            if '📺' not in title:
                continue

            if now > end:
                continue
            
            if (now < start and next_only) or not next_only:
                break

        if now > start and now < end:
            return f'目前播放的比賽為「{title}」。欲知詳情請在聊天室輸入 !b'

        diff = start - now
        seconds = diff.total_seconds()

        days = int(seconds / 60 / 60 / 24)
        hours = int(seconds / 60 / 60 % 24)
        minutes = int(seconds / 60 % 60)

        return (
            f'離下一場比賽「{title}」'
            f'還有 「{days} 天 {hours} 小時 {minutes} 分鐘」，'
            '點連結加入社群 Google日曆，'
            '掌握整個月的賽事轉播 📅 '
            'http://bit.ly/TWSCSC2CAL'
        )

if __name__ == '__main__':
    tc = TWSCCalendar()
    for e in tc.get_events(max_result=5):
        start, end, title = tc.parse_event(e)
        print(start, end, title)
    print(tc.get_next_event(next_only=False))
