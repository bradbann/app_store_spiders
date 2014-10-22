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

# http://dev.store.nearme.com.cn/user/user_login?backurl=http://dev.store.nearme.com.cn/develop/dev_myapps_app
def main():
    schema_dic = {}
    schema_dic['source'] = 'dev.store.nearme.com.cn'
    login_url = "http://dev.store.nearme.com.cn/user/user_login"
    post_data = {
        'userName':'hexinwei@baiwenbao.com',
        'password':'**',
    }
    headers = {
        'Host':'dev.store.nearme.com.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
    }
    cj = cookielib.CookieJar()
    cookie_hanlder = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_hanlder)
    post_data = urllib.urlencode(post_data)
    try:
        req = urllib2.Request(login_url, post_data, headers=headers)
        opener.open(req)

    except BaseException:
        schema_dic['err'] = 'login failed...'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    url = "http://dev.store.nearme.com.cn/develop/dev_myapps_app"
    try:
        html = opener.open(url).read()
    except BaseException:
        time.sleep(120)
        try:
            html = opener.open(url).read()
        except BaseException:
            time.sleep(120)
            try:
                html = opener.open(url).read()
            except BaseException:
                schema_dic['err'] = 'request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    soup = BeautifulSoup(html)

    try:
        table_level_str = soup.find('table', class_='list_info')
        tr_level_str = table_level_str.find_all('tr')[-1]
        td_level_list = tr_level_str.find_all('td', text=re.compile('\d'))
        version_str =  td_level_list[0]
        version = re.search(r'[\d\.]+', version_str.text).group()
        download_count_str = td_level_list[-1]
        download_count = download_count_str.text.strip()
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
    main()
