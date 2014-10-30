__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import urllib
import urllib2
import cookielib
import simplejson
import requests
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))

class XiaoMi:
    def __init__(self):
        self.schema_dic = {}
        self.schema_dic['source'] = 'dev.xiaomi.com'
        self.s = requests.session()
    def write_schema(self, json_str):
        timestamp = time.strftime('cr_download_stat-%Y%m%d.json')
        filename = os.path.join(PATH, 'download-stat', timestamp)
        with codecs.open(filename, mode='a', encoding='utf-8') as af:
            af.write(json_str+'\n')
    def xiaomi(self):
        login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
        post_data = {
                    'user':'hexinwei@baiwenbao.com',
                    '_json' : 'true',
                    'pwd' : 'www.komoxo.com',
                    '_sign' : 'Io9EiE4pBAHhOg1VBHB0dzZtCI4=',
                  'callback':"http://dev.xiaomi.com/sts?sign=AvBYgOcCk%2BoGUoNZkjHLAVM2CuY%3D&followup=http%3A%2F%2Fdev.xiaomi.com%2Fhome",
                  'sid':"developer",
                  'qs':"%3Fcallback%3Dhttp%253A%252F%252Fdev.xiaomi.com%252Fsts%253Fsign%253DAvBYgOcCk%25252BoGUoNZkjHLAVM2CuY%25253D%2526followup%253Dhttp%25253A%25252F%25252Fdev.xiaomi.com%25252Fhome%26sid%3Ddeveloper",
                  'hidden':"",
                  "_sign":"Io9EiE4pBAHhOg1VBHB0dzZtCI4=",
                  'serviceParam' :'{"checkSafePhone":false}'
                }
        try:
            self.s.post(login_url, post_data)
        except BaseException:
            self.schema_dic['err'] = 'login failed...'
            json_str = simplejson.dumps(self.schema_dic)
            self.write_schema(json_str)
            return
        url = "http://dev.xiaomi.com/datacenter/appview/2882303761517161250?userId=284229258"
        try:
            html = self.s.get(url).text
        except BaseException:
            time.sleep(120)
            try:
                html = self.s.get(url).text
            except BaseException:
                time.sleep(120)
                try:
                    html = self.s.get(url).text
                except BaseException:
                    self.schema_dic['err'] = 'request timed out'
                    json_str = simplejson.dumps(self.schema_dic)
                    self.write_schema(json_str)
                    return
        soup = BeautifulSoup(html)
        try:
            table_level_str = soup.find('table', class_='table table-bordered')
            td_str = table_level_str.find('td').text
            download_count = td_str.replace(',','')
        except BaseException:
            self.schema_dic['err'] = 'html changed the div pattern!'
            json_str = simplejson.dumps(self.schema_dic)
            self.write_schema(json_str)
            return
        self.schema_dic['num'] = download_count
        self.schema_dic['err'] = 'null'
        self.get_version_param()
        json_str = simplejson.dumps(self.schema_dic)
        self.write_schema(json_str)
    def get_version_param(self):
        url = "http://dev.xiaomi.com/detail/1/36555b4f3d6ea1e291eb162335ea9e5f?userId=284229258"
        try:
            html = self.s.get(url).text
        except BaseException:
            time.sleep(120)
            try:
                html = self.s.get(url).text
            except BaseException:
                time.sleep(120)
                try:
                    html = self.s.get(url).text
                except BaseException:
                    self.schema_dic['ver'] = 'version page request timed out!'
                    return
        soup = BeautifulSoup(html)
        try:
            ul_level_str = soup.find('ul', class_='crumbs cf')
            version_str = ul_level_str.find('li', class_='active').text
            version = re.search(r'[\d\.]+', version_str).group()
        except BaseException:
            self.schema_dic['ver'] = 'version div do not match pattern!'
            return
        self.schema_dic['ver'] = version
if __name__ == "__main__":
    app = XiaoMi()
    app.xiaomi()
