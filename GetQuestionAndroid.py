# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : 答题闯关辅助，截屏 ，OCR 识别，百度搜索
import io
from PIL import Image
from common import screenshot, ocr, methods
from threading import Thread
import traceback
import time
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('./config/configure.conf', encoding='utf-8')

while True:

    
    t = time.clock()    
    # 截图
    bScreenshot = screenshot.check_screenshot()
    # bScreenshot.save(io.BytesIO(),'PNG')
    # bScreenshot.seek(0)
    # bScreenImg = bScreenshot.read()
    try:
        image_file = io.BytesIO(bScreenshot)
        img = Image.open(image_file)
        # 文字识别
        question, choices = ocr.ocr_img_baidu(img, config)
    except Exception:
        print('识别失败', traceback.format_exc())
        continue

    # t = time.clock()
    # 用不同方法输出结果，取消某个方法在前面加上#

    # # 打开浏览器方法搜索问题
    # methods.run_algorithm(0, question, choices)
    # # 将问题与选项一起搜索方法，并获取搜索到的结果数目
    # methods.run_algorithm(1, question, choices)
    # # 用选项在问题页面中计数出现词频方法
    # methods.run_algorithm(2, question, choices)

    # 多线程
    # if question and choices:
    #     m1 = Thread(target=methods.run_algorithm, args=(0, question, choices))
    #     m2 = Thread(target=methods.run_algorithm, args=(1, question, choices))
    #     m3 = Thread(target=methods.run_algorithm, args=(2, question, choices))
    #     m1.start()
    #     m2.start()
    #     m3.start()
    if question and choices:
        m1 = Thread(methods.run_algorithm(0, question, choices))
        m2 = Thread(methods.run_algorithm(1, question, choices))
        m3 = Thread(methods.run_algorithm(2, question, choices))
        m1.start()
        m2.start()
        m3.start()

    end_time = time.clock()
    print('用时: {0}'.format(end_time - t))

    go = input('输入回车继续运行,输入 n 回车结束运行: ')
    if go == 'n':
        break

    print('------------------------')