# ALGS Fan 藍兔小粉絲

## 簡介
+ 這是藍兔工作室的 Twitch Bot 指令機器人，具備簡單的指令功能。

## 指令
+ `!hello !哈囉` 可以跟本機器人打招呼。
+ `!星海比賽 !比賽 !日程` 可以查看下一場比賽與剩餘時間。
+ `!Nice` 可以召喚 Nice 的封號。

## 部署
### 事前準備
+ 安裝 [Git](https://git-scm.com/)
    + 若作業系統為 Windows 則點擊 [Download x.xx.x for Windows](https://git-scm.com/download/win)
+ 安裝 [Python 3](https://www.python.org/downloads/)
    + 版本只要在 3.6 以上即可。
    + 根據作業系統選擇適當的版本下載。
    + 例如 [Python 3.7.7 Windows x86-64 executable installer](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)。

### 環境部署
+ 開啟命令列安裝 `pipenv` 套件
    + `py -m pip install pipenv`
    + 安裝的過程可能會跳出警告
        > `WARNING: The scripts pipenv-resolver.exe and pipenv.exe are installed in 'C:\Users\[Username]\AppData\Local\Programs\Python\Python37\Scripts' which is not on PATH.`
    + 將 `C:\Users\[Username]\AppData\Local\Programs\Python\Python37\Scripts` 加入 PATH 環境變數：
        + 打開資料夾，對本機按右鍵 > 內容，點擊左邊的「進階系統設定」，選擇「進階」分頁 > 環境變數。
        + 編輯「使用者變數」那一個區塊裡面名稱為 Path 的變數。
        + 新增此路徑並按確定。
        + 環境變數更動完之後需要重新開啟命令列。
+ 複製本專案
    + `git clone git@github.com:penut85420/ALGS-Fan.git`
+ 安裝需求套件
    + `pipenv run pip install -r requirements.txt`
+ 放入憑證
+ 啟動機器人
    + `pipenv run python algs_fan.py`

## Issue
+ `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)`
    + 開啟瀏覽器前往 [Twitch](https://www.twitch.tv/) 一次即可。