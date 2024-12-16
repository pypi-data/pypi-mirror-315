#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
def start():
    print("import successful")
# constants
 

__author__ = 'shancx'
 
__author_email__ = 'shancx@126.com'



# @Time : 2023/09/27 下午8:52
# @Author : shanchangxi
# @File : util_log.py
import time
import logging  
from logging import handlers

def mkDir(path):
    if "." in path:
        os.makedirs(os.path.dirname(path),exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

loggers = logging.getLogger()
loggers.setLevel(logging.INFO) 
log_name =  './project_S.log'
mkDir(log_name)
logfile = log_name
time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', encoding='utf-8')
time_rotating_file_handler.setLevel(logging.INFO)   
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
time_rotating_file_handler.setFormatter(formatter)
loggers.addHandler(time_rotating_file_handler)


"""      
import tracback
try:

except Exception as e:
   
     logger.info(traceback.format_exc())
"""


'''
 ##定義一個streamHandler
# print_handler = logging.StreamHandler()  
# print_handler.setFormatter(formatter) 
# loggers.addHandler(print_handler)
'''

"""
from main import makeAll,options
from multiprocessing import Pool
import datetime
from config import logger,output
import time
import pandas as pd
import os
from itertools import product
import threading

def excuteCommand(cmd):
    print(cmd)
    os.system(cmd)

def gpuPro(makeListUTC, isPhase, isDebug, gpu, isOverwrite):
    productList = product(makeListUTC, [isPhase], [isDebug], [gpu], [isOverwrite])

    with Pool(4) as p:
        p.map(makeAll, productList)

if __name__ == '__main__':
    cfg = options()
    isPhase = cfg.isPhase
    isDebug = cfg.isDebug
    sepSec = cfg.sepSec
    gpu = cfg.gpu
    pool = cfg.pool
    isOverwrite = cfg.isOverwrite
    timeList = pd.date_range(cfg.times[0], cfg.times[-1], freq=f"{sepSec}s")
    logger.info(f"时间段check {timeList}")
    gpuNum = 2
    eachGPU = 4

    makeListUTC = []
    for UTC in timeList:
        UTCStr = UTC.strftime("%Y%m%d%H%M")
        outpath = f"{output}/{UTCStr[:4]}/{UTCStr[:8]}/MSP2_WTX_AIW_QPF_L88_CHN_{UTCStr}_00000-00300-00006.nc"
        if not os.path.exists(outpath) or isOverwrite:
            makeListUTC.append(UTC)
    [print(element) for element in makeListUTC]

    phaseCMD = "--isPhase" if isPhase else ""
    debugCMD = "--isDebug" if isDebug else ""
    OverwriteCMD = "--isOverwrite"  
    gpuCMD = f"--gpu={gpu}"
    # cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {OverwriteCMD} {gpuCMD}",makeListUTC))
    cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {gpuCMD}",makeListUTC))

    with Pool(pool) as p:
        p.map(excuteCommand, cmdList)
"""


'''
# @Time : 2023/09/27 下午8:52
# @Author : shanchangxi
# @File : util_log.py
import time
import logging  
from logging import handlers
 
logger = logging.getLogger()
logger.setLevel(logging.INFO) 
log_name =  'project_tim_tor.log'
logfile = log_name
time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', encoding='utf-8')
time_rotating_file_handler.setLevel(logging.INFO)   
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
time_rotating_file_handler.setFormatter(formatter)
logger.addHandler(time_rotating_file_handler)
print_handler = logging.StreamHandler()   
print_handler.setFormatter(formatter)   
logger.addHandler(print_handler)

'''

'''
###解决方法  pip install torch==2.4.0  torchvision    torchaudio三个同时安装  python 3.12  解决cuda启动不了的问题

Res网络
'''