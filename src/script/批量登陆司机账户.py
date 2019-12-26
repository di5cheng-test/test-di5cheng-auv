import random
from src.pages import dispatch_new
import time
from src.common.random_param import Random_param as ran
from src.common import config
from src.pages import auv_app_new as app
from ctypes import *

# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

dispatch = dispatch_new.Dispatch()
dispatch_token = dispatch.dispatch_login(username="test-dispatch", password="123456")

drivers_info = dispatch.dispatch_md_40_cmd_142(cookie=dispatch_token, a="5e005cc5743a493816c64338", b=1)

for driver in drivers_info["data"]:
    driver_phone = driver["b"]
    # 登录信息参数
    login_param = common.app_login_param(username=driver_phone, password="123456")
    # 登录
    common.app_login(library=library, param=login_param)
    time.sleep(5)
    # 登出参数
    login_out_param = common.app_login_out_param()
    # 登出
    common.app_login_out(library=library, param=login_out_param)
    time.sleep(0.5)
