__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
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
    schema_dic['source'] = '91.com'
    url = "http://apk.91.com/Soft/Android/com.komoxo.octopusime-22869.html"
    try:
        html = urllib2.urlopen(url).read()
    except BaseException:
        time.sleep(120)
        try:
            html = urllib2.urlopen(url).read()
        except BaseException:
            time.sleep(120)
            try:
                html = urllib2.urlopen(url).read()
            except BaseException:
                schema_dic['err'] = 'request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    soup = BeautifulSoup(html)
    try:
        ul_level_str = soup.find('ul', class_='s_info')
        ver_count_str_list = ul_level_str.find_all('li', limit=2)
        version_str = ver_count_str_list[0].text
        version = re.search(r'[\d\.]+', version_str).group()
        download_count_str = ver_count_str_list[1].text.split(u'：')
        download_count = download_count_str[1]
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
