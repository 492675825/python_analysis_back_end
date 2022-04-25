import time
from datetime import datetime, timedelta

today = datetime.today()
today_str = str(today)
dt = datetime.strftime(today, "%Y%m%d")
yesterday = today + timedelta(days=-1)
yt = datetime.strftime(yesterday, "%Y%m%d")
print(today)
print(today_str)
print(dt)
print(yt)