import os
import configparser

# 获取config配置文件
path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
config_path = path + '\\config\\config.ini'

# 实例化configParser对象
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')


def get_config(section, key):  # 根据标识和key获取相应的键值
    value = config.get(section, key)
    return value


def get_config_db(key):  # 获取数据库配置的相应键值
    value = config.get("db", key)
    return value


def get_config_log(key):  # 获取日志配置的相应键值
    value = config.get("log", key)
    return value


def get_config_driver():  # 获取浏览器配置的相应键值
    value = config.get("browser", "browserType")
    return value


def get_environment():
    value = config.get("environment", "Environmental")
    return value


def get_shipper_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_SHIPPER")
    return value


def get_service_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_SERVICE")
    return value


def get_dispatch_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_DISPATCH")
    return value


def get_finance_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_FINANCE")
    return value


def get_operation_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_OPERATION")
    return value


def get_contract_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env + "_CONTRACT")
    return value


def get_app_url():  # 获取url
    env = get_environment()
    value = bytes(config.get("url", "INIT_" + env), encoding="utf-8")
    return value


def get_result():  # 运行结果是否保留的参数
    value = int(config.get("result", "isClear"))
    return value


def get_server():
    Smtp_Server = config.get("email", "Smtp_Server")
    return Smtp_Server


def get_sender():
    Smtp_Sender = config.get("email", "Smtp_Server")
    return Smtp_Sender


def get_sender_pwd():
    Smtp_Sender_Password = config.get("email", "Smtp_Sender_Password")
    return Smtp_Sender_Password


def get_receiver():
    Smtp_Receiver = config.get("email", "Smtp_Receiver")
    return Smtp_Receiver


def get_account(account_type):
    env = get_environment()
    value = eval(config.get("account", (account_type + "_" + env.lower())))
    return value


def get_picture():
    env = get_environment()
    value = config.get("picture", "JPG_" + env).split(",")
    return value


def get_excel():
    excel_path = path + config.get("excel", "excel_path")
    return excel_path


def get_library(library=None):
    if library is None:
        library_path = path + config.get("library", "library_path")
    else:
        library_path = path + config.get("library", library)
    return library_path


def get_report_path():
    report_path = path + config.get("report", "report_path")
    return report_path
