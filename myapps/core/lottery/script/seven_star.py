import pandas as pd
import requests
from lxml.html import etree
import os
import json
from myapps import models


class lottery_seven_star:
    def __init__(self, page_number=1):
        self.source_url = f'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=04&provinceId=0&pageSize=30&isVerify=1&pageNo={page_number}'
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }

    def get_result(self):
        res = requests.get(url=self.source_url, headers=self.header)
        json_content = json.loads(res.text)
        dict_context = json_content['value']['list']
        result_number = []
        result_date = []
        for i in range(len(dict_context)):
            result_number.append(dict_context[i]['lotteryDrawResult'])
            result_date.append(dict_context[i]['lotteryDrawTime'])
        result_number = [num.replace(" ", ",") for num in result_number]
        result_number = [num.split(',') for num in result_number]
        result_01 = [num[0] for num in result_number]
        result_02 = [num[1] for num in result_number]
        result_03 = [num[2] for num in result_number]
        result_04 = [num[3] for num in result_number]
        result_05 = [num[4] for num in result_number]
        result_06 = [num[5] for num in result_number]
        result_07 = [num[6] for num in result_number]

        df = pd.DataFrame(result_date, columns=['version_date'])
        df['number_01'] = result_01
        df['number_02'] = result_02
        df['number_03'] = result_03
        df['number_04'] = result_04
        df['number_05'] = result_05
        df['number_06'] = result_06
        df['final_number'] = result_07
        # insert_list = []
        dataset = models.lottery_seven_star.objects.all().values()
        data = pd.DataFrame(dataset)
        version_date_db = data['version_date'].values
        for ver_date in result_date:
            if ver_date in version_date_db:
                pass
            else:

                models.lottery_seven_star.objects.create(
                    version_date=ver_date,
                    number_01=df[df['version_date'] == ver_date]['number_01'].values[0],
                    number_02=df[df['version_date'] == ver_date]['number_02'].values[0],
                    number_03=df[df['version_date'] == ver_date]['number_03'].values[0],
                    number_04=df[df['version_date'] == ver_date]['number_04'].values[0],
                    number_05=df[df['version_date'] == ver_date]['number_05'].values[0],
                    number_06=df[df['version_date'] == ver_date]['number_06'].values[0],
                    final_number=df[df['version_date'] == ver_date]['final_number'].values[0]
                )
        print("seven_star complete..")

        # for ver_date, n_01, n_02, n_03, n_04, n_05, n_06, n_07 in zip(
        #         df['version_date'].values,
        #         df['number_01'].values,
        #         df['number_02'].values,
        #         df['number_03'].values,
        #         df['number_04'].values,
        #         df['number_05'].values,
        #         df['number_06'].values,
        #         df['final_number'].values
        # ):
        #     insert_list.append(models.lottery_seven_star(
        #         version_date=ver_date,
        #         number_01=n_01,
        #         number_02=n_02,
        #         number_03=n_03,
        #         number_04=n_04,
        #         number_05=n_05,
        #         number_06=n_06,
        #         final_number=n_07
        #     ))
        # models.lottery_seven_star.objects.bulk_create(insert_list)



if __name__ == '__main__':
    data = lottery_seven_star()
    data.get_result()
