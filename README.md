# ALGS Fan 藍兔小粉絲

## 簡介
+ 這是藍兔工作室的 Twitch Bot 指令機器人，具備簡單的指令功能。

## 指令
+ `!hello !哈囉` 可以跟本機器人打招呼。
+ `!星海比賽 !比賽 !日程` 可以查看當前比賽資訊或下一場比賽與剩餘時間。
+ `!下一場比賽 !nt` 可以查看下一場比賽與剩餘時間。
+ `!Nice` 可以召喚 Nice 的封號。
+ `!阿吉` 可以恭迎吉孤觀音。
+ `!堅持` 你還在堅持啥啊。

## 部署
### 事前準備
+ 安裝 [Git](https://git-scm.com/)
    + 若作業系統為 Windows 則點擊 [Download x.xx.x for Windows](https://git-scm.com/download/win)
+ 安裝 [Python 3](https://www.python.org/downloads/)
    + 版本只要在 3.6 以上即可。
    + 根據作業系統選擇適當的版本下載。
    + 例如 [Python 3.7.7 Windows x86-64 executable installer](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)。

### 取得憑證
+ 使用自己的 Google 帳號，根據[這個頁面](https://developers.google.com/calendar/quickstart/python)的 Step 1 獲得 **`credentials.json`** 的檔案。
+ 前往[這個頁面](https://twitchapps.com/tmi/)取得 **TMI Token**。
+ 前往[這個頁面](https://dev.twitch.tv/console/apps/create)創建一個 Twitch App。
    + 「OAuth 重新導向網址」輸入 `http://localhost` 即可。
    + 對此應用程式點擊「管理」，在頁面下方可以獲得「**用戶端 ID**」。

### 環境部署
+ 開啟命令列安裝 `pipenv` 套件：
    + `py -m pip install pipenv`
    + 安裝的過程可能會跳出警告：
        > `WARNING: The scripts pipenv-resolver.exe and pipenv.exe are installed in 'C:\Users\[Username]\AppData\Local\Programs\Python\Python37\Scripts' which is not on PATH.`
    + 將 `C:\Users\[Username]\AppData\Local\Programs\Python\Python37\Scripts` 加入 PATH 環境變數：
        + 打開資料夾，對本機按右鍵 > 內容，點擊左邊的「進階系統設定」，選擇「進階」分頁 > 環境變數。
        + 編輯「使用者變數」那一個區塊裡面名稱為 Path 的變數。
        + 新增此路徑並按確定。
        + 環境變數更動完之後需要重新開啟命令列。
+ 複製本專案並進入資料夾：
    + `git clone https://github.com/penut85420/ALGS-Fan.git & cd ALGS-Fan`
+ 安裝需求套件：
    + `pipenv run pip install -r requirements.txt`
+ 驗證設定：
    + 將 `credentials.json` 放入資料夾內。
    + 將 `.env.template` 檔案重新命名為 `.env`。
    + 編輯 `.env` 檔案的內容：
        + `TMI_TOKEN` 輸入之前取得的 TMI Token。
        + `CLIENT_ID` 輸入之前取得的用戶端 ID。
        + `BOT_NICK` 為 Twitch 帳號的 ID。
        + `CHANNEL` 輸入機器人要進入的頻道名稱，若有多個以半形逗號隔開，不須加空白。
            + Ex: `CHANNEL=algs_sc2,algs_fan`
+ 啟動機器人
    + `pipenv run python algs_fan.py`
    + 第一次啟動可能會需要操作驗證確認頁面

## 更新系統
+ 在專案資料夾內打開命令列並輸入更新指令：
    + `git pull origin master`

## Issue
+ `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)`
    + 開啟瀏覽器前往 [Twitch](https://www.twitch.tv/) 一次即可。
