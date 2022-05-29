import os.path

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from myapps.core.gold.script.data_transform import data_transform
from myapps.core.gold.script.gold_spider import gold_data
from myapps.core.nonfarm.script.nonfarm_data_delta import get_page
from myapps.core.news.script.news_script import get_news_from_website
from myapps.core.lottery.script import seven_star
from myapps import models
import pandas as pd
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
        print(">>> get gold data start..")
        start_time = time.time()
        gold = gold_data()
        gold.get_data_by_page_number(page_number=1)
        end_time = time.time()
        print(">>> get gold data cost:", round((end_time - start_time), 2))
        print(">>> gold data ETL start..")
        gold_etl = data_transform()         
        gold_etl.main()
        print(">>> get non farm data start..")
        non_farm_delta = get_page()
        non_farm_delta.get_data(showScreen=False)
        print(">>> get news start..")
        news_data = get_news_from_website()
        news_data.main()
        print(">>> start running sql..")
        os.system("C:/Users/xiongyuan/Desktop/Sql/run_sql.bat")
        for i in range(1, 11):
            data = seven_star.lottery_seven_star(page_number=i)
            data.get_result()
            print(f"update page:{i}")
        print(f"[Cycle job complete..][{time.strftime('%Y-%m-%d %H:%M:%S')}]")



    scheduler.start()
except Exception as e:
    scheduler.shutdown()


class gold_daily_data(View):
    def get(self, request):
        data = data_transform()
        data.main()
        return JsonResponse({"code": 0, "msg": "success"})


class non_farm_data(View):
    def get(self, request):
        df = pd.read_csv(r"C:\Users\xiongyuan\PycharmProjects\python_analysis_back_end\download\nonfarm\nonfarm.csv")
        # version_date,current_value,predict_value,previous_value,refresh_date
        bd_list = []
        for ver, cur_val, prd_val, pre_val, ref_dte in zip(
                df['version_date'].values,
                df['current_value'].values,
                df['predict_value'].values,
                df['previous_value'].values,
                df['refresh_date'].values):
            bd_list.append(models.non_farm(
                version_date=ver,
                current_value=cur_val,
                predict_value=prd_val,
                previous_value=pre_val,
                refresh_date=ref_dte
            ))
        models.non_farm.objects.bulk_create(bd_list)
        return JsonResponse({"code": 0, "msg": "success"})


class nonfarm_data_delta(View):
    def get(self, request):
        csv_path = os.path.dirname(os.path.dirname(__file__)) + "/download/nonfarm/nonfarm_delta.csv"
        df = pd.read_csv(csv_path)
        db = models.non_farm.objects.all().values()
        df_db = pd.DataFrame(db)
        db_version_date_list = [ver.strftime("%Y-%m-%d") for ver in df_db['version_date'].values]

        df_version_date_list = list(df['version_date'].values)

        for ver in df_version_date_list:
            if ver in db_version_date_list:
                pass
            else:
                print("find new date")
                data = df[df['version_date'] == ver]
                insert_list = []
                for ver_date, cur_val, prd_val, pre_val, ref_date in zip(
                        data['version_date'].values, data['current_value'].values, data['predict_value'].values,
                        data['previous_value'].values, data['refresh_date'].values
                ):
                    insert_list.append(models.non_farm(
                        version_date=ver_date,
                        current_value=cur_val,
                        predict_value=prd_val,
                        previous_value=pre_val,
                        refresh_date=ref_date
                    ))
                models.non_farm.objects.bulk_create(insert_list)

        return JsonResponse({"code": 0, "msg": "success"})


class cctv_world_news(View):
    def get(self, request):
        data = get_news_from_website()
        data.main()
        return JsonResponse({"code": 0, "msg": "success"})


# http://127.0.0.1:8000/lottery_seven_star/seven/
class lottery_seven_star(View):
    def get(self, request):
        '''
        七星彩
        :param request:
        :return:
        '''
        csv_path = r"C:\Users\xiongyuan\Desktop\PycharmProjects\python_analysis_back_end\download\lottery\seven_star\seven_star.csv"
        for i in range(1, 11):
            data = seven_star.lottery_seven_star(page_number=i)
            data.get_result()
            print(f"update page:{i}")
        db = models.lottery_seven_star.objects.all().values()
        df = pd.DataFrame(db)
        df.to_csv(csv_path, index=False)
        return JsonResponse({"code": 0, "msg": "success"})
