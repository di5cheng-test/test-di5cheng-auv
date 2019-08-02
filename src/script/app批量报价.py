# coding:utf-8
from config import global_parameter
from src.pages import app
from ctypes import *
import random

# 初始化
library = cdll.LoadLibrary(global_parameter.library)
common = app.Common()
common.initSDK(library=library, init_info=global_parameter.init)

# 登录信息参数
login_param = common.app_login_param(username=global_parameter.app_account["username"],
                                     password=global_parameter.app_account["password"])
# 登录
common.app_login(library=library, param=login_param)
# 车队认证信息参数
enterprise_info_param = common.enterprise_info_param()
# 获取车队认证信息
enterprise_info = common.enterprise_info(library=library, param=enterprise_info_param,)
# 车队ID
enterprise = eval(enterprise_info["pBody"])["a"]
# 车队名称
enterprise_name = eval(enterprise_info["pBody"])["b"]
last_time = 0
count = 0
for n in range(10):
    # 货单列表参数
    manifest_list_param = common.manifest_list_param(b=last_time)
    # 获取货单列表
    manifest_list_info = common.manifest_list(library=library, param=manifest_list_param,)
    if eval(manifest_list_info["pBody"]) == {"a": 0}:
        print("最后一页")
    else:
        manifest_list = eval(manifest_list_info["pBody"])["b"]
        last_time = manifest_list[-1]["i"]
        for manifest in manifest_list:
            # 报价参数
            goods_report_param = common.goods_report_param(a=manifest["a"],
                                                           b=random.randint(100, 590) * 100,
                                                           c=random.randint(1, manifest["h"]),
                                                           d=enterprise)
            # 发起报价
            common.goods_report(library=library, param=goods_report_param)

