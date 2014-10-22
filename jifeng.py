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

def write_schema(json_str):
    timestamp = time.strftime('cr_download_stat-%Y%m%d.json')
    filename = os.path.join(PATH, 'download-stat', timestamp)
    with codecs.open(filename, mode='a', encoding='utf-8') as af:
        af.write(json_str+'\n')

def jifeng():
    schema_dic = {}
    schema_dic['source'] = 'dev.gfan.com'
    login_url = "http://dev.gfan.com/Aspx/DevApp/LoginUser.aspx"
    post_data = {
        'loginUser$txtEmail':'komoxo2702',
        'loginUser$txtPsw':'**',
        'q':'全站搜索...',
        'loginUser$btnSubmit':'登+录',
        '__VIEWSTATE':'/wEPDwULLTE1MjEwNTcyNjEPZBYCAgMPZBYCAgcPZBYCZg8WAh4EaHJlZgUefi9Bc3B4L0RldkFwcC9SZWdEZXZfTWFpbi5hc3B4ZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUTbG9naW5Vc2VyJGNoa0Nvb2tpZb0MrkjrGkdkui4c+TqJWafGbtRW',
        '__EVENTVALIDATION':'/wEWBgKRgfTuBAK83MqjAwLm15PfCgLa8ZalDAKG7tHCDALvp7LDBvUq4wb3fS7yBmEy6xcsPzIX2ojf'
    }
    cookiejar = cookielib.CookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(login_url, post_data)
    response = opener.open(req)
    if response.getcode() != 200:
        schema_dic['err'] = 'login failed...'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    try:
        html = opener.open('http://dev.gfan.com/Aspx/DevApp/DevInfo_Main.aspx').read()
    except BaseException:
        time.sleep(120)
        try:
            html = opener.open('http://dev.gfan.com/Aspx/DevApp/DevInfo_Main.aspx').read()
        except BaseException:
            time.sleep(120)
            try:
                html = opener.open('http://dev.gfan.com/Aspx/DevApp/DevInfo_Main.aspx').read()
            except BaseException:
                schema_dic['err'] = 'login failed... or request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    soup = BeautifulSoup(html)
    try:
        table_level_str = soup.find_all('table', class_='t_1202')[-1]
        tr_level_str = table_level_str.find_all('tr')[-1]
        version_str = tr_level_str.find('td', text=re.compile(r'\w')).text
        version = re.search(r'[\d\.]+', version_str).group()
        download_count = tr_level_str.find('a', text=re.compile(r'\d')).text
    except BaseException:
        schema_dic['err'] = 'html changed div pattern'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    schema_dic['num'] = download_count
    schema_dic['err'] = 'null'
    schema_dic['ver'] = version
    json_str = simplejson.dumps(schema_dic)
    write_schema(json_str)
if __name__ == "__main__":
    jifeng()

