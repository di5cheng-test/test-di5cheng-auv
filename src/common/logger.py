import logging
import os
import time
from logging.handlers import RotatingFileHandler
from src.common import config


class MyLog(object):
    def __init__(self):
        global format_, maxBytes, backupCount, logLevel, reportPath, logPath

        format_ = config.get_config_log('format').replace('@', '%')  # 日志内容的格式
        backupCount = int(config.get_config_log('backupCount'))  # 日志大小和数目
        maxBytes = int(config.get_config_log('maxBytes'))
        logLevel = int(config.get_config_log('level'))  # 日志级别
        now = time.strftime('%Y-%m-%d_%H_%M_%S')  # 文件的日期格式
        # log文件的存放路径
        logPath = os.path.abspath(os.path.join(os.getcwd(), "../..")) + '/result/logs/' + now + '.log'
        # report文件的存放路径
        reportPath = os.path.abspath(os.path.join(os.getcwd(), "../..")) + '/result/report/' + now + '.html'

    # 保存日志到文件的函数
    # 日志存放路径
    @staticmethod
    def get_log_path():
        return logPath

    # 测试报告存放路径
    @staticmethod
    def get_report_path():
        return reportPath

    @classmethod
    def logger(cls):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logLevel)
        if not logger.handlers:
            rfhandler = RotatingFileHandler(cls.get_log_path(), maxBytes=maxBytes, backupCount=backupCount,
                                            encoding='utf-8')  # 创建一个handler,用于写入文件
            log_format = logging.Formatter(format_)  # 定义handler的输出格式
            rfhandler.setFormatter(log_format)  # 给handler添加formatter
            logger.addHandler(rfhandler)  # 给logger添加handler
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(log_format)  # 设置屏幕上显示的格式
            logger.addHandler(sh)  # 把对象加到logger里
            # logger.removeHandler(rfhandler)
        return logger


MyLog().logger()
