__author__ = 'huafeng'

import os
import sys
import time
import subprocess
PATH = os.path.dirname(os.path.abspath(__file__))
def call_shell():
    command = 'ls *.py'
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    all_spiders_list = popen.stdout.readlines()
    for spider in [item for item in all_spiders_list if item.strip() != 'execute_all_spiders.py']:
        print 'python %s'%spider.strip()
        os.system('python %s'%spider.strip())
    mv_and_update_db_filename = os.path.join(os.path.dirname(PATH), 'mv_json_file.py')
    os.system('python %s'%mv_and_update_db_filename)
if __name__ ==  '__main__':
    call_shell()
