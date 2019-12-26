# coding:utf-8
from src.common import config
from src.pages import auv_app_new as app
from ctypes import *
import random

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

dispatch_list_param = common.auv_param_md_40_cmd_73(a=0, b=enterprise)
dispatch_list_info = common.auv_md_40_cmd_73(library=library, param=dispatch_list_param)
dispatch_list = eval(dispatch_list_info["pBody"])["a"]
time = 0
# 查询车队调度列表
for n in range(4):
    dispatch_list_param = common.auv_param_md_40_cmd_73(a=time, b=enterprise)
    dispatch_list_info = common.auv_md_40_cmd_73(library=library, param=dispatch_list_param)
    dispatch_list = eval(dispatch_list_info["pBody"])["a"]
    last_time = dispatch_list[-1]["e"]
    print(dispatch_list)
    for dispatch in dispatch_list:
        print(dispatch)
        phone = dispatch["c"]
        # 登录退出参数
        login_out_param = common.app_login_out_param()
        # 登录退出
        common.app_login_out(library=library, param=login_out_param)
        # 登录信息参数
        login_param = common.app_login_param(username=phone, password=password)
        # 登录
        common.app_login(library=library, param=login_param)
        # 货单列表参数
        manifest_list_param = common.auv_param_md_40_cmd_16(b=0)
        # 获取货单列表
        manifest_list_info = common.auv_md_40_cmd_16(library=library, param=manifest_list_param)
        manifest_list = eval(manifest_list_info["pBody"])["b"]
        for manifest in manifest_list:
            # 判断是否为询价货
            if manifest["k"] == 1:
                # 报价参数
                enterprise_price = random.randint(100, 590) * 100
                enterprise_car_num = random.randint(10, 100)
                goods_report_param = common.auv_param_md_40_cmd_33(a=manifest["a"], b=enterprise_price,
                                                                   c=enterprise_car_num, d=enterprise)
                # 发起报价
                common.auv_md_40_cmd_33(library=library, param=goods_report_param)
            else:
                continue
    if time != last_time:
        time = last_time
    else:
        break
