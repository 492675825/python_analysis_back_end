from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 等待页面加载
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
import pandas as pd
from myapps import models


class get_page:
    def __init__(self):
        self.root_path = str(Path(__file__).resolve().parent.parent.parent.parent.parent)
        self.save_path = self.root_path + "/download/nonfarm/nonfarm_delta.csv"

    def get_data(self, showScreen=False):

        print(">>> [Start] get non-farm data start..")
        # 不弹出浏览器
        if not showScreen:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(options=options)
        # 弹出浏览器
        elif showScreen:
            driver = webdriver.Chrome()
        driver.get("https://datacenter.jin10.com/reportType/dc_nonfarm_payrolls")
        time.sleep(3)
        driver.maximize_window()  # 全屏

        time.sleep(5)
        driver.find_element(By.ID, 'dcVideoClose').click()  # 中途可能会有窗口弹出

        version_date = driver.find_elements(By.XPATH, '//tbody//tr//td[2]')
        date_list = [x.text for x in version_date]
        current_value = driver.find_elements(By.XPATH, '//tbody//tr//td[3]//a')
        current_value_list = [x.text for x in current_value]
        predict_value = driver.find_elements(By.XPATH, '//tbody//tr//td[4]//a')
        predict_value_list = [x.text for x in predict_value]
        previous_value = driver.find_elements(By.XPATH, '//tbody//tr//td[5]//a')
        previous_value_list = [x.text for x in previous_value]

        date_value_list = []
        for dte in date_list:
            if len(dte) != 0:
                date_value_list.append(dte)
            else:
                pass

        num = len(date_value_list)

        predict_value_list = predict_value_list[:num]
        previous_value_list = previous_value_list[:num]
        current_value_list = current_value_list[:num]

        df = pd.DataFrame(date_value_list)
        df['current_value'] = current_value_list
        df['predict_value'] = predict_value_list
        df['previous_value'] = previous_value_list
        df.columns = ['version_date', 'current_value', 'predict_value', 'previous_value']

        df['version_date'] = df['version_date'].str.replace("年", "-")
        df['version_date'] = df['version_date'].str.replace("月", "-")
        df['version_date'] = df['version_date'].str.replace("日", "")
        df['refresh_date'] = list([time.strftime("%Y-%m-%d %H:%M:%S")]) * len(df)
        # print(df.head())
        print(">>> [Complete] get non-farm data complete..")
        df.to_csv(self.save_path, index=False)

        dataset = models.non_farm.objects.all().values()
        df_model = pd.DataFrame(dataset)
        version_date_list = list(df_model['version_date'].values)
        for ver_date, curr_val, pred_val, prev_val, ref_date in zip(
            df['version_date'].values,
                df['current_value'].values,
                df['predict_value'].values,
                df['previous_value'].values,
                df['refresh_date'].values
        ):
            if ver_date in version_date_list:
                pass
            else:
                models.non_farm.objects.all().create(
                    version_date=ver_date,
                    current_value=curr_val,
                    predict_value=pred_val,
                    previous_value=prev_val,
                    refresh_date=ref_date
                )
        return df


if __name__ == '__main__':
    data = get_page()
    data.get_data(showScreen=False)
