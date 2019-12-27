# coding:utf-8
from src.common import config
from src.pages import app
from ctypes import *
from src.common.random_param import Random_param as ran

# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

# 登录信息参数
login_param = common.app_login_param(username="133327827656", password="123456")
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
    car_info_param = ran().create_app_car_info(fleet_id=enterprise)
    common.app_add_car(library=library, param=car_info_param)
    gua_car_info_param = ran().create_app_gua_car_info(fleet_id=enterprise)
    common.app_add_gua_car(library=library, param=gua_car_info_param)
