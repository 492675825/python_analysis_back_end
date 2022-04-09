import logging
import shutil
from pathlib import Path

import traceback
import pandas as pd
import numpy as np
import ssl
from lxml import etree
import requests
import time
import re
import os
import concurrent.futures


class gold_data:

    def __init__(self):

        self.root_path = str(Path(__file__).resolve().parent.parent.parent.parent.parent)
        self.save_path = self.root_path + "/download/gold/daily_batch/"
        print(self.save_path)

        if os.path.exists(self.save_path):
            shutil.rmtree(self.save_path)

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                          'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36'
        }
        self.root_link = 'https://www.sge.com.cn'

    def get_data_by_page_number(self, page_number):
        page_link = []
        version_date = []
        update_version_date = []
        url_list = [f'https://www.sge.com.cn/sjzx/mrhqsj?p={page_number}']

        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        for url in url_list:
            print(url)
            respond_t1 = requests.get(url=url, headers=self.header)
            respond_t1_page = respond_t1.text
            html_t1 = etree.HTML(respond_t1_page)
            # 获取一页中所有的link
            link_t1 = html_t1.xpath(r"//div[@class='articleList border_ea mt30 mb30']//a/@href")
            page_link = page_link + link_t1
            # 获取一页中所有的日期
            ver_date = html_t1.xpath(r"//div[@class='articleList border_ea mt30 mb30']//a//span[@class='fr']/text()")
            version_date = version_date + ver_date
            update_version_date = [d.replace("-", '') for d in version_date]
        target_url = [self.root_link + f'{u}' for u in page_link]

        # 获取每个表格页面唯一的编号
        page_unique_number = [num.split("/")[-1] for num in page_link]
        # print(page_unique_number)

        for tar_url, num in zip(target_url, update_version_date):
            try:
                dataframe_list = []
                response = requests.get(tar_url, headers=self.header)
                response_page = response.text
                html = etree.HTML(response_page)
            except Exception as e:
                print(f">>> [ERROR] url error..{tar_url}")

            try:
                # 获取表格行数
                row_count = html.xpath(r'//tbody//tr')
                # 获取表格列数
                column_count = html.xpath(r'//tbody//tr[1]/td')

                category_name = html.xpath(r'//tbody//tr[1]//td')

                # 获取字段名
                category_name_list = [name.xpath('string(.)').strip() for name in category_name]
                if category_name_list[0] == '':
                    category_name_list[0] = '合约'
                for row in range(2, len(row_count) + 1):
                    row_content = html.xpath(f'//tbody//tr[{row}]//td')
                    row_context_list = [item.xpath('string(.)').strip() for item in row_content]
                    dataframe_list.append(row_context_list)
                df = pd.DataFrame(dataframe_list, columns=category_name_list)
                # for num in page_unique_number:
                df.to_csv(self.save_path + f'page_{page_number}_{num}.csv', index=False)
            except Exception as e:
                print(f">>> [ERROR] fail to get data page={page_number},version_Date={num},url={tar_url}")
                # logging.error(f">>> [ERROR] fail to get data page={page_number},version_Date={num},url={tar_url}")

        print(f">>> [Complete] Page {page_number} complete..")
        logging.info(f">>> [Complete] Page {page_number} complete..")

    # 获取最大的页码
    def get_max_page_number(self):
        try:
            url = r'https://www.sge.com.cn/sjzx/mrhqsj?p=1'
            response = requests.get(url, headers=self.header)
            response.encoding = response.apparent_encoding
            get_html_code = response.text
            html = etree.HTML(get_html_code)
            max_page_num = html.xpath(
                r"//div[@class='pagination']//div[@class='paginationBar fl']//ul[@class='clear']//li[7]/text()")
            max_page_number = int(max_page_num[0])
            print('max_page_number:', max_page_number)
            return max_page_number
        except Exception as e:
            print(">>>> [ERROR] get max page number error..")

    def tread_pool_batch_run(self):
        max_page_number = self.get_max_page_number()
        page_number_list = list(range(1, max_page_number + 1))
        with concurrent.futures.ThreadPoolExecutor() as pl:
            pl.map(self.get_data_by_page_number, page_number_list)

    def noraml_batch_run(self):
        max_page_number = self.get_max_page_number()
        for p in range(1, max_page_number):
            self.get_data_by_page_number(page_number=p)

    def main(self):
        start_time = time.time()
        data = gold_data()
        data.get_data_by_page_number(page_number=1)
        end_time = time.time()
        print("cost:", round((end_time - start_time), 2))


if __name__ == '__main__':
    start_time = time.time()
    data = gold_data()
    data.get_data_by_page_number(page_number=1)
    end_time = time.time()
    print("cost:", round((end_time - start_time), 2))
