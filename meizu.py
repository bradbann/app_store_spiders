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
    schema_dic['source'] = 'meizu.com'
    url = 'http://app.meizu.com/phone/apps/0a05e270be3a4443817b437e64938657'
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
        li_level_list = soup.find_all('li', class_='extContent')
        version_str = li_level_list[2].text.strip()
        version = re.search(r'[\d\.]+', version_str).group()
        download_count_str = li_level_list[3].text.strip()
        download_count = re.search(r'\d+', download_count_str).group()
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