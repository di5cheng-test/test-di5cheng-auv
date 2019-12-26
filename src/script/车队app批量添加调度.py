# coding:utf-8
from src.common import config
from src.pages import auv_app_new as app
from ctypes import *
import random

# 车队账号
username = "13327827656"
password = "123456"

# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

# 登录信息参数
login_param = common.app_login_param(username=username, password=password)
# 登录
common.app_login(library=library, param=login_param)
# 车队认证信息参数
enterprise_info_param = common.auv_param_md_40_cmd_23()
# 获取车队认证信息
enterprise_info = common.auv_md_40_cmd_23(library=library, param=enterprise_info_param)
# 车队ID
enterprise = eval(enterprise_info["pBody"])["a"]
# 车队名称
enterprise_name = eval(enterprise_info["pBody"])["b"]

# 手机号
phone = random.randint(15000000000, 15999999999)

for n in range(100):
    name = "autotest" + str(n)
    iphone = phone + n
    dispatch_param = common.auv_param_md_40_cmd_71(a=name, b=iphone, c=enterprise)
    common.auv_md_40_cmd_71(library=library, param=dispatch_param)
