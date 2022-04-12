from pathlib import Path

import pandas as pd
import requests
import os
from lxml import etree
import json
from myapps import models
import time


# world_1 ~ world_7
# https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_1.jsonp?cb=world

class get_news_from_website:
    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                          'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36'
        }
        self.root_path = str(Path(__file__).resolve().parent.parent.parent.parent.parent)
        self.save_path = self.root_path + '/download/news/'

    def cctv_world_news(self):
        # 央视国际新闻只保存最近的500条，即i=0 to i=7
        for i in range(1, 8):
            print(f">>> [start] cctv_world_new page = {i}")
            world_url = f'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_{i}.jsonp?cb=world'
            res = requests.get(url=world_url, headers=self.header)
            res.encoding = 'gzip'
            content = res.text
            content = content.replace("world(", "")
            content = content[:-1]
            df = json.loads(content)
            df_list = df['data']['list']
            version_date_list = [item['focus_date'] for item in df_list]
            title_list = [item['title'] for item in df_list]
            brief_list = [item['brief'] for item in df_list]
            key_word_list = [item['keywords'] for item in df_list]
            detail_url_list = [item['url'] for item in df_list]
            version_date_list = pd.DataFrame(version_date_list)
            title_list = pd.DataFrame(title_list)
            brief_list = pd.DataFrame(brief_list)
            key_word_list = pd.DataFrame(key_word_list)
            detail_url_list = pd.DataFrame(detail_url_list)
            df = pd.concat([version_date_list, title_list, brief_list, key_word_list, detail_url_list], axis=1)
            df.columns = ["version_date", "title", "brief", "keyword", "url"]
            df.to_csv(self.save_path + f"cctv/world/world_news_{i}.csv", index=False)
        file_list = os.listdir(self.save_path + "cctv/world")
        for file in file_list:

            data = pd.read_csv(self.save_path + f'cctv/world/{file}')
            csv_version_date_list = list(data['version_date'].values)
            db_data = models.cctv_world_news.objects.all().values()
            db_data = pd.DataFrame(db_data)
            db_version_date_list = list(db_data['version_date'].values)
            for ver_date in csv_version_date_list:
                if ver_date in db_version_date_list:
                    pass
                else:
                    insert_df = data[data['version_date'] == ver_date]
                    models.cctv_world_news.objects.create(
                        version_date=insert_df['version_date'].values[0],
                        title=insert_df['title'].values[0],
                        brief=insert_df['brief'].values[0],
                        keyword=insert_df['keyword'].values[0],
                        url=insert_df['url'].values[0],
                        refresh_date=time.strftime("%Y-%m-%d"),
                        news_type="world"
                    )

    def cctv_china_news(self):
        # https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
        # 央视国际新闻只保存最近的500条，即i=0 to i=7
        for i in range(1, 8):
            print(f">>> [start] cctv_china_new page = {i}")
            world_url = f'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_{i}.jsonp?cb=china'
            res = requests.get(url=world_url, headers=self.header)
            res.encoding = 'gzip'
            content = res.text
            content = content.replace("china(", "")
            content = content[:-1]
            df = json.loads(content)
            df_list = df['data']['list']
            version_date_list = [item['focus_date'] for item in df_list]
            title_list = [item['title'] for item in df_list]
            brief_list = [item['brief'] for item in df_list]
            key_word_list = [item['keywords'] for item in df_list]
            detail_url_list = [item['url'] for item in df_list]
            version_date_list = pd.DataFrame(version_date_list)
            title_list = pd.DataFrame(title_list)
            brief_list = pd.DataFrame(brief_list)
            key_word_list = pd.DataFrame(key_word_list)
            detail_url_list = pd.DataFrame(detail_url_list)
            df = pd.concat([version_date_list, title_list, brief_list, key_word_list, detail_url_list], axis=1)
            df.columns = ["version_date", "title", "brief", "keyword", "url"]
            df.to_csv(self.save_path + f"cctv/china/china_news_{i}.csv", index=False)
        file_list = os.listdir(self.save_path + "cctv/china")
        for file in file_list:

            data = pd.read_csv(self.save_path + f'cctv/china/{file}')
            csv_version_date_list = list(data['version_date'].values)
            db_data = models.cctv_china_news.objects.all().values()
            db_data = pd.DataFrame(db_data)
            db_version_date_list = list(db_data['version_date'].values)
            for ver_date in csv_version_date_list:
                if ver_date in db_version_date_list:
                    pass
                else:
                    insert_df = data[data['version_date'] == ver_date]
                    models.cctv_china_news.objects.create(
                        version_date=insert_df['version_date'].values[0],
                        title=insert_df['title'].values[0],
                        brief=insert_df['brief'].values[0],
                        keyword=insert_df['keyword'].values[0],
                        url=insert_df['url'].values[0],
                        refresh_date=time.strftime("%Y-%m-%d"),
                        news_type="china"
                    )
    def cctv_economy_news(self):
        # https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/economy_zixun_1.jsonp?cb=economy_zixun
        # i = 1 to 3
        # https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
        # 央视国际新闻只保存最近的104条，即i=0 to i=3
        for i in range(1, 4):
            print(f">>> [start] cctv_economy_new page = {i}")
            world_url = f'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/economy_zixun_{i}.jsonp?cb=economy_zixun'
            res = requests.get(url=world_url, headers=self.header)
            res.encoding = 'gzip'
            content = res.text
            content = content.replace("economy_zixun(", "")
            content = content[:-1]
            df = json.loads(content)
            df_list = df['data']['list']
            version_date_list = [item['focus_date'] for item in df_list]
            title_list = [item['title'] for item in df_list]
            brief_list = [item['brief'] for item in df_list]
            key_word_list = [item['keywords'] for item in df_list]
            detail_url_list = [item['url'] for item in df_list]
            version_date_list = pd.DataFrame(version_date_list)
            title_list = pd.DataFrame(title_list)
            brief_list = pd.DataFrame(brief_list)
            key_word_list = pd.DataFrame(key_word_list)
            detail_url_list = pd.DataFrame(detail_url_list)
            df = pd.concat([version_date_list, title_list, brief_list, key_word_list, detail_url_list], axis=1)
            df.columns = ["version_date", "title", "brief", "keyword", "url"]
            df.to_csv(self.save_path + f"cctv/economy/economy_news_{i}.csv", index=False)
        file_list = os.listdir(self.save_path + "cctv/economy")
        for file in file_list:

            data = pd.read_csv(self.save_path + f'cctv/economy/{file}')
            csv_version_date_list = list(data['version_date'].values)
            db_data = models.cctv_economy_news.objects.all().values()
            db_data = pd.DataFrame(db_data)
            db_version_date_list = list(db_data['version_date'].values)
            for ver_date in csv_version_date_list:
                if ver_date in db_version_date_list:
                    pass
                else:
                    insert_df = data[data['version_date'] == ver_date]
                    models.cctv_economy_news.objects.create(
                        version_date=insert_df['version_date'].values[0],
                        title=insert_df['title'].values[0],
                        brief=insert_df['brief'].values[0],
                        keyword=insert_df['keyword'].values[0],
                        url=insert_df['url'].values[0],
                        refresh_date=time.strftime("%Y-%m-%d"),
                        news_type="economy"
                    )


    def main(self):
        self.cctv_world_news()
        self.cctv_china_news()
        self.cctv_economy_news()


if __name__ == '__main__':
    data = get_news_from_website()
    data.main()
