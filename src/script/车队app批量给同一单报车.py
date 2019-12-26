# coding:utf-8
from src.common import config
from src.pages import auv_app_new as app
from ctypes import *

global null
null = None

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

time = 0
# 查询运力列表


for n in range(0, 100):
    capacity_list_param = common.auv_param_md_40_cmd_181(a=enterprise, b=time)
    capacity_list_info = common.auv_md_40_cmd_181(library=library, param=capacity_list_param)
    if eval(capacity_list_info["pBody"]) == {"a": 1}:
        break
    else:
        capacity_list = eval(capacity_list_info["pBody"])["s"]
        last_time = capacity_list[-1]["l"]
        print(capacity_list)
        driver_list = []
        for n in range(0, len(capacity_list)):
            driver = {"d": capacity_list[n]["g"], "e": capacity_list[n]["a"]}
            driver_list.append(driver)
    print()
    # 货单列表参数
    manifest_list_param = common.auv_param_md_40_cmd_16(b=0)
    # 获取货单列表
    manifest_list_info = common.auv_md_40_cmd_16(library=library, param=manifest_list_param)
    manifest_list = eval(manifest_list_info["pBody"])["b"]
    for manifest in manifest_list:
        # 判断是否为报车单
        if manifest["k"] == 2:
            # 报车参数
            car_report_param = common.auv_param_md_40_cmd_69(a=manifest["a"], b=enterprise, c=tuple(driver_list))
            # 发起报车
            common.auv_md_40_cmd_69(library=library, param=car_report_param)
    if time != last_time:
        time = last_time
    else:
        break
