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
from bs4 import BeautifulSoup
from apscheduler.scheduler import Scheduler
PATH = os.path.dirname(os.path.abspath(__file__))

class AppChina:

    def __init__(self):
        self.schema_dic = {}

    def write_schema(self, json_str):
        timestamp = time.strftime('cr_download_stat-%Y%m%d.json')
        filename = os.path.join(PATH, 'download-stat', timestamp)
        with codecs.open(filename, mode='a', encoding='utf-8') as af:
            af.write(json_str+'\n')
    def appchina(self):
        self.schema_dic['source'] = 'dev.appchina.com'
        login_url = 'http://dev.appchina.com/market/auth/login_post.action?mode=dev'
        post_data = {
            'login':'13718710748',
            'password':'**',
            }
        cookie = cookielib.CookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        post_data = urllib.urlencode(post_data)
        req = urllib2.Request(login_url, post_data)
        self.opener.open(req)
        try:
            html = self.opener.open(req, timeout=15).read()
        except BaseException:
            time.sleep(120)
            try:
                html = self.opener.open(req, timeout=15).read()
            except BaseException:
                time.sleep(120)
                try:
                    html = self.opener.open(req, timeout=15).read()
                except BaseException:
                    self.schema_dic['err'] = 'request timed out'
                    json_str = simplejson.dumps(self.schema_dic)
                    self.write_schema(json_str)
                    return
        soup = BeautifulSoup(html)
        try:
            div_level_str = soup.find('div', class_='apps widget-content')
            span_level_str = div_level_str.find('span', id=None)
            download_str = span_level_str.text
            download_count = ''.join(re.findall(r'[\d]+', download_str))
        except BaseException, e:
            self.schema_dic['err'] = 'login failed... or html changed the div pattern!'
            json_str = simplejson.dumps(self.schema_dic)
            self.write_schema(json_str)
            return
        self.schema_dic['err'] = 'null'
        self.schema_dic['num'] = download_count
        self.get_version_param()
        json_str = simplejson.dumps(self.schema_dic)
        # print json_str
        self.write_schema(json_str)
    def get_version_param(self):
        url = "http://dev.appchina.com/market/dev/dev_app.action?applicationId=1107556"
        try:
            html = self.opener.open(url, timeout=15).read()
        except BaseException:
            time.sleep(120)
            try:
                html = self.opener.open(url, timeout=15).read()
            except BaseException:
                time.sleep(120)
                try:
                    html = self.opener.open(url, timeout=15).read()
                except BaseException:
                    self.schema_dic['ver'] = 'version page request timed out!'
                    return
        soup = BeautifulSoup(html)
        try:
            td_level_str = soup.find('td', id='versioninfo')
            div_level_str = td_level_str.find('div')
            span_level_str = div_level_str.find_all('span')[-1]
            version_str = span_level_str.text.strip()
            version = re.search(r'[\d\.]+', version_str).group()
        except BaseException:
            self.schema_dic['ver'] = 'version div do not match pattern!'
            return
        self.schema_dic['ver'] = version
if __name__ == "__main__":
    app = AppChina()
    app.appchina()
