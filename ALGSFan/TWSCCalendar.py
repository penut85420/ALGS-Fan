import datetime
import re

from googleapiclient.discovery import build

from ALGSFan.Utils import load_json, load_token

WEEK_DELTA = datetime.timedelta(days=7)


class TWSCCalendar:
    def __init__(self):
        self.config = load_json("Config.json")["calendar_info"]
        self.calendar_id = self.config["id"]
        self.creds = load_token(self.config["token"])

    def get_utcstr(self, t):
        return t.strftime("%Y-%m-%dT00:00:00Z")

    def get_week_range(self):
        now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)
        end = now + WEEK_DELTA

        now = self.get_utcstr(now)
        end = self.get_utcstr(end)

        return now, end

    def get_events(self, max_result=50):
        service = build("calendar", "v3", credentials=self.creds)

        now, end = self.get_week_range()

        events_result = (
            service.events()
            .list(
                calendarId=self.calendar_id,
                maxResults=max_result,
                singleEvents=True,
                timeMin=now,
                timeMax=end,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        return events

    def parse_event(self, e):
        title = e["summary"].replace("[SC2] ", "")
        start = self.get_date(e, "start")
        end = self.get_date(e, "end")

        return start, end, title

    def retrieve_para(self, e, begin_token, end_token):
        desc = e["description"]

        begin_idx = desc.find(begin_token) + len(begin_token)
        end_idx = desc.find(end_token)
        if end_idx == -1:
            end_idx = len(desc)
        desc = desc[begin_idx:end_idx].strip().replace("\n", " ")

        return desc

    def parse_desc(self, e):
        return self.retrieve_para(e, "📄賽事資訊", "📇")

    def parse_sign(self, e):
        return self.retrieve_para(e, "🔗報名連結", "📄")

    def parse_url(self, e):
        return re.findall("(https?://[^\s]+)", e["description"])

    def get_date(self, e, key):
        date = e[key].get("dateTime", e[key].get("date"))
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+08:00")
        except ValueError:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
        date = date - datetime.timedelta(hours=8)

        return date

    def get_next_event(self, next_only=False):
        now = datetime.datetime.utcnow()
        start = end = title = None
        for e in self.get_events():
            start, end, title = self.parse_event(e)
            desc = self.parse_url(e)[0]

            if "📺" not in title:
                continue

            if now > end:
                continue

            if (now < start and next_only) or not next_only:
                break

        if start is None:
            return "目前沒有比賽"

        if now > start and now < end:
            return f"目前有星海比賽「{title}」正在直播 (〃∀〃)，" f"欲知詳情請看「 {desc} 」"

        diff = start - now
        seconds = diff.total_seconds()

        days = int(seconds / 60 / 60 / 24)
        hours = int(seconds / 60 / 60 % 24)
        minutes = int(seconds / 60 % 60)

        return (
            f"離下一場比賽「{title}」"
            f"還有 「{days} 天 {hours} 小時 {minutes} 分鐘」。"
            f"賽事資訊：「 {desc} 」"
        )

    def get_next_sign(self):
        now = datetime.datetime.utcnow()
        is_found = False
        for e in self.get_events():
            start, end, title = self.parse_event(e)
            desc = self.parse_sign(e)

            if "📜" not in title:
                continue

            if now < start:
                is_found = True
                break

        if not is_found:
            return "目前一週內沒有可供報名的賽事唷 (☍﹏⁰) 若想知道更多比賽行程請看社群賽事行事曆 http://bit.ly/TWSCSC2CAL"

        return f"下一場公開可報名的賽事為「{title}」。" f"賽事資訊：{desc}"
