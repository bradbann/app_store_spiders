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

def hiapk():
    schema_dic = {}
    schema_dic['source'] = 'dev.apk.hiapk.com'
    url = 'http://apk.hiapk.com/appinfo/com.komoxo.octopusime'
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
                schema_dic['err'] = 'login failed... or request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    soup = BeautifulSoup(html)
    div_level_str = soup.find('div', class_='code_box_border')
    download_count_div_level_str = div_level_str.find_all('div', class_='line_content')[1]
    download_count_str = download_count_div_level_str.find('span', text=re.compile('\d')).text
    download_count = float(re.search(r'([\d\.]+)', download_count_str).group(1))*10000
    # print int(download_count)
    version_str = soup.find('div', id='appSoftName').text.strip()
    version = re.search(r'[\d\.]+', version_str).group()
    # print version
    try:
        div_level_str = soup.find('div', class_='code_box_border')
        download_count_div_level_str = div_level_str.find_all('div', class_='line_content')[1]
        download_count_str = download_count_div_level_str.find('span', text=re.compile('\d')).text
        download_count = str(int(float(re.search(r'([\d\.]+)', download_count_str).group(1))*10000))
        version_str = soup.find('div', id='appSoftName').text.strip()
        version = re.search(r'[\d\.]+', version_str).group()
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
    hiapk()
