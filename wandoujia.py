__author__ = 'huafeng'
#encoding:utf-8
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
def wandoujia():
    schema_dic = {}
    schema_dic['source'] = 'wandoujia.com'
    url = "http://www.wandoujia.com/apps/com.komoxo.octopusime"
    try:
        html = urllib2.urlopen(url, timeout=15).read()
        pass
    except BaseException, e:
        time.sleep(120)
        try:
            html = urllib2.urlopen(url, timeout=15).read()
        except BaseException, e:
            time.sleep(120)
            try:
                html = urllib2.urlopen(url, timeout=15).read()
            except BaseException:
                schema_dic['err'] = 'request timed out'
                json_str = simplejson.dumps(schema_dic)
                write_schema(json_str)
                return
    soup = BeautifulSoup(html)
    try:
        div_level_str = soup.find('div', class_='num-list')
        download_count_str = div_level_str.find('i').text
        download_count = re.search(r'[\d\.]+', download_count_str).group()
        if u'万' in download_count_str:
            download_count = str(int(float(download_count)*10000))
    except BaseException, e:
        schema_dic['err'] = 'login failed...or html chenged div pattern'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    schema_dic['num'] = download_count.strip()
    schema_dic['err'] = 'null'
    try:
        version_dl_level_str = soup.find('dl', class_='infos-list')
        # print version_dl_level_str
        dd_level_str = version_dl_level_str.find_all('dd', class_=False, text=re.compile(r'[\w\.\_\-]+'))[1]
        version_str = dd_level_str.text.strip()
        version = re.search(r'[\d\.]+', version_str).group()
    except:
        schema_dic['ver'] = 'version div do not match pattern!'
        json_str = simplejson.dumps(schema_dic)
        write_schema(json_str)
        return
    schema_dic['ver'] = version
    json_str = simplejson.dumps(schema_dic)
    write_schema(json_str)

if __name__ == "__main__":
    wandoujia()