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

def main():
    schema_dic = {}
    schema_dic['source'] = 'm.163.com'
    login_url = "https://reg.163.com/logins.jsp"
    post_data = {
        'url':'http://m.163.com/devsoft/index.html',
        'username':'hexinwei@baiwenbao.com',
        'password':'**'
    }
    cj = cookielib.CookieJar()
    cookie_hanlder = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_hanlder)
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(login_url, post_data)
    response = opener.open(req)
    if response.getcode() != 200:
        schema_dic['err'] = 'login failed...'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    url = 'http://m.163.com/dev/?username=hexinwei@baiwenbao.com'
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
        download_count_str = soup.find('span', class_='ico-download').text
        download_count = re.search(r'\d+', download_count_str).group()
    except BaseException:
        schema_dic['err'] = 'html changed div pattern'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    version_url = "http://ime.baiwenbao.com/ime/check_update?cat=octopus_formal"
    try:
        response = urllib2.urlopen(version_url).read()
    except BaseException:
        time.sleep(120)
        try:
            response = urllib2.urlopen(version_url).read()
        except BaseException:
            time.sleep(120)
            try:
                response = urllib2.urlopen(version_url).read()
            except BaseException:
                schema_dic['ver'] = 'version page request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    json_dic =  simplejson.loads(response)
    version_str = json_dic['version']
    version = re.search(r'[\d\.]+', version_str).group()
    schema_dic['num'] = download_count
    schema_dic['err'] = 'null'
    schema_dic['ver'] = version
    json_str = simplejson.dumps(schema_dic)
    write_schema(json_str)
if __name__ == "__main__":
    main()
