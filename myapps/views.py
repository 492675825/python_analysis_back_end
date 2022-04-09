from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from myapps.core.gold.script.data_transform import data_transform
from myapps.core.gold.script.gold_spider import gold_data

import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_job

# 设置定时作业01 -- 获取每日gold数据,并增量插入数据库
try:
    scheduler = BackgroundScheduler()


    @register_job(scheduler, "interval", seconds=3600, id="daily_gold_cycle")
    def daily_gold_data_cycle():
        print("Cycle Job start..")
        print(f"Start Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        start_time = time.time()
        gold = gold_data()
        gold.get_data_by_page_number(page_number=1)
        end_time = time.time()
        print(">>> get gold data cost:", round((end_time - start_time), 2))
        gold_etl = data_transform()
        gold_etl.main()
        print("[Cycle job complete..]")


    scheduler.start()
except Exception as e:
    scheduler.shutdown()


class gold_daily_data(View):
    def get(self, request):
        data = data_transform()
        data.main()
        return JsonResponse({"code": 0, "msg": "success"})
