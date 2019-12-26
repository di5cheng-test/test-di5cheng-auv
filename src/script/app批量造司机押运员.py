# coding:utf-8
from src.common import config
from src.pages import app
from src.common.random_param import Random_param as ran
from ctypes import *

# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

# 登录信息参数
login_param = common.app_login_param(username="13000030016", password="123456")
# 登录
common.app_login(library=library, param=login_param)
# 车队认证信息参数
enterprise_info_param = common.enterprise_info_param()
# 获取车队认证信息
enterprise_info = common.enterprise_info(library=library, param=enterprise_info_param)
# 车队ID
enterprise = eval(enterprise_info["pBody"])["a"]
# 车队名称
enterprise_name = eval(enterprise_info["pBody"])["b"]

for n in range(10):
    driver_param = ran().create_app_driver_info(fleet_id=enterprise)
    common.app_add_driver(library=library, param=driver_param)
    driver_ya_param = ran().create_app_driver_ya_info(fleet_id=enterprise)
    common.app_add_driver_ya(library=library, param=driver_ya_param)
