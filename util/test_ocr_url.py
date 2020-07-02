# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 13:24:32 2019

@author: Advance
"""

from flask import Flask, escape, url_for
from flask import request
import os
import logging  # 写日志
import logging.handlers  # 必须导入
import time
import json
import random

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello,world'


cout_req = 1


@app.route('/classify', methods=['GET', 'POST'])
def upload_file_1():
    time.sleep(0.01)
    global cout_req
    print(f'count:{cout_req}')
    cout_req += 1
    dirname = 'save_files_dir_multipart'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if request.method == 'POST':
        img = request.files['image']
        params = request.query_string
        fn = img.filename
        img.save(os.path.join(dirname, fn))

        p = ['jkjj', 'xjzp_zheng']
        classes = {
            'jkjj': '借款借据',
            'nhxexydkjj': '农户和小额信用贷款借据',
            'xjzp_fan': '现金支票反面',
            'xjzp_zheng': '现金支票正面',
            'xjjkd': '现金缴款单',
            'pjhjspzlyd': '票据和结算凭证领用单',
            'others': '其他凭证',
        }

        p = list(classes.keys())
        # p = ['xjzp_zheng']
        res = {'data': {'result': {'probability': [0.9999], 'classes': [random.choice(p)]}}, 'status': 0}
        res = json.dumps(res, ensure_ascii=False)
        print()
        print('票据分类：')
        print('params:', params)
        print('fn:', fn)
        print('res:', res)
        print()
        return res


@app.route('/recognize', methods=['GET', 'POST'])
def upload_file_2():
    time.sleep(0.01)
    dirname = 'save_files_dir_multipart'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if request.method == 'POST':
        img = request.files['k1']
        fn = img.filename
        img.save(os.path.join(dirname, fn))
        params = request.query_string
        # ywwts
        res_ywwts = {"data": {
            "result": [
                # {"name":"委托日期(yyyymmdd)","text":"20200605"},
                {"name": "委托日期(yyyymmdd)_yyyy", "text": "2020"},
                {"name": "委托日期(yyyymmdd)_mm", "text": "6"},
                {"name": "委托日期(yyyymmdd)_dd", "text": "5"},
                {"name": "委托人全称", "text": "重庆有限公司1"},
                {"name": "委托人账号或地址", "text": "123456789"},
                {"name": "收款人/持票人名称", "text": "重庆有限公司2"},
                {"name": "收款人账号或住址", "text": "1234567890"},
                {"name": "票据/凭证号码", "text": "012345678"},
                {"name": "小写金额", "text": "520000"},
                {"name": "大写金额", "text": "伍仟贰佰元整"},
                {"name": "用途/摘要", "text": "买车"},
                {"name": "附加信息/备注", "text": "给自己买"}]},
            "status": 0}

        res_zzzp = {"data": {
            "result": [
                # {"name":"委托日期(yyyymmdd)","text":"20200605"},
                {"name": "出票/凭证日期(大写)_yyyy", "text": "贰零贰零"},
                {"name": "出票/凭证日期(大写)_mm", "text": "陆"},
                {"name": "出票/凭证日期(大写)_dd", "text": "壹"},
                {"name": "收款人/持票人名称", "text": "重庆有限公司1"},
                {"name": "付款人/出票人帐号", "text": "123456789"},
                {"name": "票据/凭证号码", "text": "012345678"},
                {"name": "小写金额", "text": "520000"},
                {"name": "大写金额", "text": "伍仟贰佰元整"},
                {"name": "用途/摘要", "text": "买车"},
                {"name": "支付密码", "text": "1234567890123456"},
                {"name": "出票行行号", "text": "123456789012"}]},
            "status": 0}

        # 修改接口
        res = json.dumps(res_zzzp, ensure_ascii=False)

        print('文字识别：')
        print('params:', params)
        print('fn:', fn)
        print('res', res)
        print()

        return res


if __name__ == '__main__':
    import re
    import logging.config

    dirname = 'log'
    bname = 'ocrapi.log'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    logging.getLogger().setLevel(logging.INFO)  # 设置全局
    handler = logging.handlers.TimedRotatingFileHandler(os.path.join(dirname, bname), when='M', interval=1,
                                                        backupCount=3,
                                                        delay=False)  # 文件名不能有下横杠！！！不能命名为ocr_api,而需要ocrapi，不然不能第二次写入
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)

    handler.suffix = "%Y-%m-%d.log"
    handler.extMatch = r"^\d{4}-\d{2}-\d{2}.log$"
    handler.extMatch = re.compile(handler.extMatch)

    app.logger.addHandler(handler)

    app.run(host='0.0.0.0', port=8000, debug=0)
