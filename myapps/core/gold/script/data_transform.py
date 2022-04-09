import shutil
import time
from pathlib import Path

import pandas as pd
import numpy as np
import re
import os

from myapps import models


class data_transform:

    def __init__(self):
        self.root_path = str(Path(__file__).resolve().parent.parent.parent.parent.parent)
        self.csv_path = self.root_path + "/download/gold/daily_batch/"

    def insert_data(self):
        '''
            将每天爬虫爬取的当日数据插入数据库 temp_gold_data
        :return:
        '''
        dataset = models.gold_data.objects.all().values()
        df = pd.DataFrame(dataset)
        version_date_from_database = list(df['version_date'].values)
        new_batch_file_list = os.listdir(self.csv_path)
        new_batch_temp01 = [batch.replace(".csv", "") for batch in new_batch_file_list]
        new_batch_temp02 = [batch.split("_") for batch in new_batch_temp01]
        new_batch_date_list = [batch[2] for batch in new_batch_temp02]

        for ver, file in zip(new_batch_date_list, new_batch_file_list):
            if int(ver) in version_date_from_database:
                print(f">>> [old] batch {ver}")
            else:
                print(f">>> [new] batch {ver}")
                data = pd.read_csv(self.csv_path + f"{file}")
                data = data[["合约", "开盘价", "最高价", "最低价", "收盘价", "涨跌（元）"]]
                data.columns = ["item", "open", "high", "low", "close", "up_or_down"]
                data['version_date'] = list([ver] * len(data))
                dataset_list = []
                for item, open, high, low, close, up_down, ver_date in zip(
                        data['item'].values, data['open'].values, data['high'].values,
                        data['low'].values, data['close'].values, data['up_or_down'].values,
                        data['version_date'].values):
                    dataset_list.append(models.gold_data(
                        item=item,
                        open=open,
                        high=high,
                        low=low,
                        close=close,
                        up_or_down=up_down,
                        version_date=ver_date
                    ))
                models.gold_data.objects.bulk_create(dataset_list)

    def main(self):
        self.insert_data()


if __name__ == '__main__':
    data = data_transform()
    data.main()
