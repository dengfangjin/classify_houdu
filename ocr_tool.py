# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:36:18 2020

@author: advance
"""
import re
import json
import os, sys
import os.path as op
import shutil
import requests
import datetime
from requests_toolbelt import MultipartEncoder
from util.log_util import logger

env = 0  # SIT:0  PROD:1
classify_url_houdu = r'http://10.7.139.170:30069?apikey=de7b1e90-6312-443a-8f88d0f472b1f228'
classify_url_houdu_sit = r'http://127.0.0.1:8000/classify'
img_format = r'.jpg|.JPG|.bmp|.BMP|.png|.PNG'
classes = {
    'jkjj': '借款借据',
    'nhxexydkjj': '农户和小额信用贷款借据',
    'xjzp_fan': '现金支票反面',
    'xjzp_zheng': '现金支票正面',
    'xjjkd': '现金缴款单',
    'pjhjspzlyd': '票据和结算凭证领用单',
    'others': '其他凭证',
}


def req_classify(img_path):
    url = classify_url_houdu if env == 1 else classify_url_houdu_sit
    img_name = op.basename(img_path)
    f = open(img_path, 'rb')
    payload = {'image': (img_name, f, 'image/jpeg')}
    m = MultipartEncoder(fields=payload)
    headers = {'content-type': m.content_type}
    results = None
    try:
        response = requests.request('post', url, data=m,
                                    headers=headers, timeout=10.0)
        if response.status_code != 200:
            logger.warning('分类响应结果：{}\n\
                   分类响应状态码：{}'.format(response.text, response.status_code))
        else:
            results = json.loads(response.text, encoding='utf-8')
    except Exception as e:
        logger.error('分类请求错误:{}'.format(e))
    finally:
        f.close()
    # 【挡板，上线前取消。】
    # results = {"data": {"result": {"probability": [0.99999556],"classes": ["ywwts"]}},"status": 0}
    return results


def main(path, cls_true):
    if cls_true not in classes.keys():
        print(f'ERROR: Please input {json.dumps(classes, indent=4, ensure_ascii=False)}')
        return 0
    path = path[:-1] if path[-1] in [r'/', '\\'] else path
    mark_dir = op.join(path, 'mark')
    others_dir = op.join(path, 'others_images' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    img_paths = []
    for d in os.listdir(mark_dir):
        if op.isdir(op.join(mark_dir, d)):
            for f in os.listdir(op.join(mark_dir, d)):
                if len(re.findall(img_format, f)) > 0:
                    img_paths.append(op.join(mark_dir, d, f))

    other_count = 0
    for idx, img_path in enumerate(img_paths):
        print(f'\rProcess: {idx+1}/{len(img_paths)}', end='')
        img_dir = op.dirname(img_path)
        res = req_classify(img_path)
        if res:
            if float(res['data']['result']['probability'][0]) > 0.9:
                cls_img = res['data']['result']['classes'][0]
                logger.info(f'{img_path} --> {cls_img} is not {cls_true}')
                if cls_img != cls_true:
                    logger.warning(f'{img_path} --> {cls_img} is not {cls_true}' )
                    shutil.move(img_dir, op.join(others_dir, op.basename(img_dir)))
                    other_count += 1
    print(f'\nothers_count:{other_count}')


if __name__ == '__main__':
    main('billinfo/xjzp_zheng1/', 'xjzp_zheng')  # 目录，平台返回类型值
    # main(sys.argv[1],sys.argv[2])
