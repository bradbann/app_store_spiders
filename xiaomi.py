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

PATH = os.path.dirname(os.path.abspath(__file__))

class XiaoMi:
    def __init__(self):
        self.schema_dic = {}
        self.schema_dic['source'] = 'dev.xiaomi.com'

    def write_schema(self, json_str):
        timestamp = time.strftime('cr_download_stat-%Y%m%d.json')
        filename = os.path.join(PATH, 'download-stat', timestamp)
        with codecs.open(filename, mode='a', encoding='utf-8') as af:
            af.write(json_str+'\n')
    def xiaomi(self):
        login_url = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
        cookiejar = cookielib.CookieJar()
        cookie_hanlder = urllib2.HTTPCookieProcessor(cookiejar)
        self.opener = urllib2.build_opener(cookie_hanlder)
        post_data = {
                    'user' : 'hexinwei@baiwenbao.com',
                    'pwd' : '**',
                    'callback' : 'https://account.xiaomi.com' ,
                    'sid' : 'passport',
                    'hidden' : '',
                    'qs' : '%3Fsid%3Dpassport',
                    '_sign' : 'KKkRvCpZoDC+gLdeyOsdMhwV0Xg='
                }
        post_data = urllib.urlencode(post_data)
        try:
            req = urllib2.Request(login_url,post_data)
            self.opener.open(req)
        except BaseException,e:
	    print e
            self.schema_dic['err'] = 'login failed...'
            json_str = simplejson.dumps(self.schema_dic)
#            self.write_schema(json_str)
            return
        url = "http://dev.xiaomi.com/datacenter/appview/2882303761517161250?userId=284229258"
        try:
            html = self.opener.open(url).read()
        except BaseException:
            time.sleep(120)
            try:
                html = self.opener.open(url).read()
            except BaseException:
                time.sleep(120)
                try:
                    html = self.opener.open(url).read()
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
            self.schema_dic['err'] = 'login failed... or html changed the div pattern!'
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
            html = self.opener.open(url).read()
        except BaseException:
            time.sleep(120)
            try:
                html = self.opener.open(url).read()
            except BaseException:
                time.sleep(120)
                try:
                    html = self.opener.open(url).read()
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
