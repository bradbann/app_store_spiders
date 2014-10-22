__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import urllib2
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
    schema_dic['source'] = 'app.lenovo.com'
    url = 'http://app.lenovo.com/appdetail/com.komoxo.octopusime/0'
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
        ul_level_str = soup.find('ul', class_='detailAppInfo fl')
        app_info_list = ul_level_str.find_all('li')
        li_version_info_str = app_info_list[1]#version in the second position of the list
        version_info_str = li_version_info_str.text
        version = re.search(r'[\d\.]+', version_info_str).group()
    except BaseException:
        schema_dic['err'] = 'version_info changed div pattern'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    try:
        div_level_str = soup.find('div', class_='f12 detailDownNum cb clearfix')
        download_count_str = div_level_str.text
        # print download_count_str
        download_count = re.search(r'[\d\.]', download_count_str).group()
        if u'千' in download_count_str:
            download_count = str(int(float(download_count)*1000))
        elif u'万' in download_count_str:
            download_count = str(int(float(download_count)*10000))
        # print download_count
    except BaseException:
        schema_dic['err'] = 'download_count changed div pattern'
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
