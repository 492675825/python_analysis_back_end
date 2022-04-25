from urllib import parse
import http.cookiejar as cookielib

import requests
import os
from lxml.html import etree
import time


class download_file:
    def __init__(self):
        self.url = 'https://www.dnc.gov.hk/tm/login'
        self.download_url = 'https://www.dnc.gov.hk/tm/download'
        self.download_url_md5 = 'https://www.dnc.gov.hk/download/full-sms-20220421.md5'
        self.download_url_zip = 'https://www.dnc.gov.hk/download/full-sms-20220421.zip'
        self.logout_url = 'https://www.dnc.gov.hk/tm/logout'
        self.account = 'haseebp'
        self.pwd = 'Edoo2204#'
        self.form_data = {
            "Login": self.account,
            "Password": self.pwd,
            "SecurityCode": "",
            "UserSeq": "0",
            "UserHashSeq": "null"
        }
        self.form_data_download = {
            "RegisterType": "S",
            "ButtonAction": "download",
            "SourceType": "ContainDate",
            "UserSeq": "3",
            "UserHashSeq": "1a53b8f12e541acb3d7fb370ff67a73e"
        }
        self.form_data_logout = {
            "mItem": "menu_9",
            "page": "",
            "subPage": "",
            "UserSeq": "5",
            "UserHashSeq": "03dc691bbba1e038eab0c48d9045e6be"
        }
        self.form_data_zip = {
            "RegisterType": 'S'
            , 'CheckSum': '9708c88943fccc17850ca2e7af4a8655'
            , 'CheckSumSHA256': '9f6c4d142d69bc5e622a5cac4cf7295c6e8d01d921715387f536928b98897898'
            , 'Download': 'Download List'
            , 'DownloadType': 'Download'
            , 'ListFileName': 'full-sms-20220421.zip'
            , 'ChecksumFileNameMD5': 'full-sms-20220421.md5'
            , 'ChecksumFileNameSHA256': 'full-sms-20220421.sha2'
            , 'SubFolder': '0085'
            , 'ListFileDownloadName': 'full-sms-20220421.zip'
            , 'ChecksumDownloadNameMD5': 'full-sms-20220421.md5'
            , 'ChecksumDownloadNameSHA256': 'full-sms-20220421.sha2'
            , 'SourceFileName': 'DNC-SMS-REGDATE-20220420.csv'
            , 'SourceSize': '12401064bytes'
            , 'SourceChecksumMD5': 'df30d2aeefae771b9a92ab8cba76f605'
            , 'SourceChecksumSHA256': '9bedf31d3daa59ca57dfc0bea9dc8d33ce31c3317f7a8e2c888c3101ae52c4f0'
            , 'SourceFileDate': 'Sun Mar 20 23:00:46 HKT 2022'
            , 'SortedChecksumMD5': 'null'
            , 'SortedChecksumSHA256': 'null'
            , 'UserSeq': '5'
            , 'UserHashSeq': "59857a5f3d260be14db26f69092edeff"
        }
        self.form_data_md5 = {
            "RegisterType": "S"
            , "CheckSum": "9708c88943fccc17850ca2e7af4a8655"
            , "CheckSumSHA256": "9f6c4d142d69bc5e622a5cac4cf7295c6e8d01d921715387f536928b98897898"
            , "DownloadChecksumMD5": "Download MD5"
            , "DownloadType": "DownloadChecksumMD5"
            , "ListFileName": "full-sms-20220421.zip"
            , "ChecksumFileNameMD5": "full-sms-20220421.md5"
            , "ChecksumFileNameSHA256": "full-sms-20220421.sha2"
            , "SubFolder": "0085"
            , "ListFileDownloadName": "full-sms-20220421.zip"
            , "ChecksumDownloadNameMD5": "full-sms-20220421.md5"
            , "ChecksumDownloadNameSHA256": "full-sms-20220421.sha2"
            , "SourceFileName": "DNC-SMS-REGDATE-20220420.csv"
            , "SourceSize": "12401064bytes"
            , "SourceChecksumMD5": "df30d2aeefae771b9a92ab8cba76f605"
            , "SourceChecksumSHA256": "9bedf31d3daa59ca57dfc0bea9dc8d33ce31c3317f7a8e2c888c3101ae52c4f0"
            , "SourceFileDate": "Sun Mar 20 23:00:46 HKT 2022"
            , "SortedChecksumMD5": "null"
            , "SortedChecksumSHA256": "null"
            , "UserSeq": "21"
            , "UserHashSeq": "7f25a0ead642416b63a67e36a419d7dd"
        }
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }
        self.download_header_tier01 = {
            "referer": "https://www.dnc.gov.hk/tm/login",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        }
        self.download_header_tier02 = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
            "referer": "https://www.dnc.gov.hk/tm/download"
        }

    def download_start(self):
        session = requests.session()
        login = session.post(url=self.url, data=self.form_data, headers=self.header)
        cookie = login.cookies
        res = login.text
        print(res)
        logout = session.post(url=self.logout_url,
                              data=self.form_data_logout,
                              headers=self.header,
                              cookies=cookie
                              )
        session.close()

    def main(self):
        self.download_start()


if __name__ == '__main__':
    data = download_file()
    data.main()
