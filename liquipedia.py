import requests
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as BS

def search_match_list(player):
    player = player.lower()
    url = 'https://liquipedia.net/starcraft2/Liquipedia:Upcoming_and_ongoing_matches'
    bs = BS(requests.get(url).content, 'html5lib')

    for table in bs.find_all('table', attrs={'class': 'infobox_matches_content'}):
        left_name = table.find('td', attrs={'class': 'team-left'}).text.strip()
        _left_name = left_name.lower()
        right_name = table.find('td', attrs={'class': 'team-right'}).text.strip()
        _right_name = right_name.lower()

        if _left_name == player or _right_name == player:
            if _right_name == player:
                left_name, right_name = right_name, left_name
            timestamp = table.find('span', attrs={'class': 'match-countdown'}).text.strip()
            timestamp = pd.to_datetime(timestamp).to_pydatetime().replace(tzinfo=None)
            tournament = table.find_all('div')[-1].text.strip()
            is_live = True if timestamp < dt.datetime.utcnow() else False

            return left_name, right_name, timestamp, tournament, is_live

    return None

def search_next(player):
    result = search_match_list(player)
    if result is not None:
        left, right, ts, tour, is_live = result
        if not is_live:
            delta = ts - dt.datetime.utcnow()
            seconds = delta.total_seconds()
            minutes = int(seconds // 60 % 60)
            hours = int(seconds // 60 // 60 % 24)
            s = f'{hours} 小時 {minutes} 分鐘'
            if delta.days:
                s = f'{delta.days} 天 {s}'

            return f'距離 {left} 的下一場比賽「{tour}」對上 {right} 就在「{s}」之後'

        return f'{left} 正在「{tour}」與 {right} 進行對戰！'

    return f'沒有找到 {player} 最近的比賽 QQ'
