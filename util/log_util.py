#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project: cal_acc_linux
Author : Advance
Time   : 2020-06-10 11:11
Desc   : 按照info error 分级别入不同的日志文件
"""

import os
import re
import datetime
import logging
import inspect
import logging.handlers

dirname = 'log'
log_name = 'process_classify_houdu'

if not os.path.exists(dirname):
    os.mkdir(dirname)

handlers = {
    # logging.NOTSET: os.path.join(dir, bname + '_notset.log'),
    # logging.DEBUG: os.path.join(dir, bname + '_debug.log'),
    logging.INFO: os.path.join(dirname, log_name + '_info.log'),
    logging.WARNING: os.path.join(dirname, log_name + '_warning.log'),
    logging.ERROR: os.path.join(dirname, log_name + '_error.log'),
    # logging.CRITICAL: os.path.join(dir, bname + '_critical.log'),
}

for level in handlers.keys():
    path = os.path.abspath(handlers[level])
    handlers[level] = logging.handlers.TimedRotatingFileHandler(path, when='W0', interval=1, backupCount=12,
                                                                encoding='utf-8', delay=False)
    # 设置追加格式：
    handlers[level].suffix = "%Y-%m-%d-%H-%M-%S.log"
    handlers[level].extMatch = r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.log$"
    handlers[level].extMatch = re.compile(handlers[level].extMatch)


class Log(object):
    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        for log_level in handlers.keys():
            logger = logging.getLogger(str(log_level))
            # 是否需要打印到屏幕？注释下面3行可以取消
            console = logging.StreamHandler()
            console.setLevel(logging.ERROR)  # log_level
            logger.addHandler(console)
            logger.addHandler(handlers[log_level])
            logger.setLevel(log_level)
            self.__loggers.update({log_level: logger})

    def show(self, log_level, message):
        frame, fn, line, fucname, code, un = inspect.stack()[2]
        return '{} - {} - [{} {} {}]: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                 log_level.upper(), os.path.basename(fn), line, fucname, message)

    def info(self, message):
        self.__loggers[logging.INFO].info(self.show('INFO', message))

    def error(self, message):  # INFO 记录了info 和 error
        self.__loggers[logging.INFO].error(self.show('ERROR', message))
        self.__loggers[logging.ERROR].error(self.show('ERROR', message))

    def warning(self, message):
        self.__loggers[logging.INFO].warning(self.show('WARNING', message))
        self.__loggers[logging.WARNING].warning(self.show('WARNING', message))

    def debug(self, message):
        self.__loggers[logging.INFO].debug(self.show('DEBUG', message))

    def critical(self, message):
        self.__loggers[logging.INFO].critical(self.show('critical', message))


logger = Log()

if __name__ == "__main__":
    for _ in range(10):
        logger.debug("test----------debug")
        logger.info("test----------info")
        logger.warning("test----------warning")
        logger.error("test----------error")
        logger.critical("test----------critical")
