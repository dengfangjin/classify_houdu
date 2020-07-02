#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project: process_classify_houdu
Author : Advance
Time   : 2020-06-16 12:59
Desc   :
"""
import shutil
import datetime
import os, sys
import os.path as op

max_num = 200
fn_img = 'template.jpg'


def main(root_dir):
    if not op.exists(root_dir):
        os.mkdir(root_dir)
    else:
        shutil.rmtree(root_dir)
        os.mkdir(root_dir)

    if not op.exists(op.join(root_dir, 'mark')):
        os.mkdir(op.join(root_dir, 'mark'))
    if not op.exists(op.join(root_dir, 'marked')):
        os.mkdir(op.join(root_dir, 'marked'))

    for i in range(max_num):
        print(f'\r process:{i + 1} / {max_num}', end='')
        dirname = datetime.datetime.now().strftime('%Y%m%d') + str(i).zfill(4)
        if not op.exists(op.join(root_dir, 'mark', dirname)):
            os.mkdir(op.join(root_dir, 'mark', dirname))
        img_name = dirname + '.jpg'
        txt_name = dirname + '.txt'
        txt = f'tag@#$this_is_a_tag@#$num@#${str(i).zfill(4)}'
        shutil.copy(fn_img, op.join(root_dir, 'mark', dirname, img_name))
        with open(op.join(root_dir, 'mark', dirname, txt_name), 'w') as f:
            f.write(txt)
    print('done')


if __name__ == '__main__':
    # main('xjzp_zheng1')
    main(sys.argv[1])
