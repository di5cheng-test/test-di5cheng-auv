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
    value = ""
    if env == "TEST":
        value = config.get("url", "URL_TEST_SHIPPER")
    if env == "DEV":
        value = config.get("url", "URL_DEV_SHIPPER")
    if env == "REAL":
        value = config.get("url", "URL_REAL_SHIPPER")
    return value


def get_service_url():  # 获取url
    env = get_environment()
    value = ""
    if env == "TEST":
        value = config.get("url", "URL_TEST_SERVICE")
    if env == "DEV":
        value = config.get("url", "URL_DEV_SERVICE")
    if env == "REAL":
        value = config.get("url", "URL_REAL_SERVICE")
    return value


def get_dispatch_url():  # 获取url
    env = get_environment()
    value = ""
    if env == "TEST":
        value = config.get("url", "URL_TEST_DISPATCH")
    if env == "DEV":
        value = config.get("url", "URL_DEV_DISPATCH")
    if env == "REAL":
        value = config.get("url", "URL_REAL_DISPATCH")
    return value


def get_finance_url():  # 获取url
    env = get_environment()
    value = ""
    if env == "TEST":
        value = config.get("url", "URL_TEST_FINANCE")
    if env == "DEV":
        value = config.get("url", "URL_DEV_FINANCE")
    if env == "REAL":
        value = config.get("url", "URL_REAL_FINANCE")
    return value


def get_app_url():  # 获取url
    env = get_environment()
    value = ""
    if env == "TEST":
        value = bytes(config.get("url", "INIT_TEST"), encoding="utf-8")
    if env == "DEV":
        value = bytes(config.get("url", "INIT_DEV"), encoding="utf-8")
    if env == "REAL":
        value = bytes(config.get("url", "INIT_REAL"), encoding="utf-8")
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
    value = ""
    if env == "TEST":
        value = eval(config.get("account", (account_type+"_test")))
    if env == "DEV":
        value = eval(config.get("account", (account_type+"_dev")))
    if env == "REAL":
        value = eval(config.get("account", (account_type+"_real")))
    return value



def get_picture():
    env = get_environment()
    value = ""
    if env == "TEST":
        value = config.get("picture", "JPG_TEST").split(",")
    if env == "DEV":
        value = config.get("picture", "JPG_DEV").split(",")
    if env == "REAL":
        value = config.get("picture", "JPG_REAL").split(",")
    return value


def get_excel():
    excel_path = path + config.get("excel", "excel_path")
    return excel_path


def get_library():
    library_path = path + config.get("library", "library_path")
    return library_path


def get_report_path():
    report_path = path + config.get("report", "report_path")
    return report_path
