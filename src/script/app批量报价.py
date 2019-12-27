# coding:utf-8
from src.common import config
from src.pages import auv_app_new
from ctypes import *
import random

global null
null = None

library = cdll.LoadLibrary(config.get_library())
app = auv_app_new.Common()
app.initSDK(library=library, init_info=config.get_app_url())
# 登录信息参数
login_param = app.app_login_param(username="13327827656", password="123456")
# 登录
login_info = app.app_login(library=library, param=login_param)
user_uid = eval(login_info["pBody"])["i"]

# 车队认证信息参数
enterprise_info_param = app.auv_param_md_40_cmd_23()
# 获取车队认证信息
enterprise_info = app.auv_md_40_cmd_23(library=library, param=enterprise_info_param)
# 车队ID
enterprise = eval(enterprise_info["pBody"])["a"]
# 车队名称
enterprise_name = eval(enterprise_info["pBody"])["b"]
# 姓名
user_name = eval(enterprise_info["pBody"])["c"]
time = 0
for n in range(100):
    # 货源大厅
    source_param = app.auv_param_md_40_cmd_16(b=time)
    source_list_info = app.auv_md_40_cmd_16(library=library, param=source_param)
    source_list = eval(source_list_info["pBody"])["b"]
    last_time = source_list[-1]["i"]
    if last_time == time:
        break
    else:
        time = last_time
        for source in source_list:
            # 获取货单id
            source_id = source["a"]
            # 判断是否为询价单
            if source["k"] == 1:
                # 报价参数
                enterprise_price = random.randint(100, 590) * 100
                enterprise_car_num = random.randint(10, 100)
                goods_report_param = app.auv_param_md_40_cmd_33(a=source_id, b=enterprise_price,
                                                                c=enterprise_car_num, d=enterprise)
                # 发起报价
                app.auv_md_40_cmd_33(library=library, param=goods_report_param)
            # 判断是否为报车单
            elif source["k"] == 2:
                # app 运力列表查看运力
                capacity_list_param = app.auv_param_md_40_cmd_181(a=enterprise, b=0)
                capacity_list_info = app.auv_md_40_cmd_181(library=library, param=capacity_list_param)
                capacity_list = eval(capacity_list_info["pBody"])["s"]
                # 随机抽取一个运力
                capacity = random.choice(capacity_list)
                car_id = capacity["g"]
                driver_id = capacity["n"]
                driver = {"d": car_id, "e": driver_id}
                use_driver = (driver,)
                # 报车参数
                car_report_param = app.auv_param_md_40_cmd_69(a=source_id, b=enterprise, c=use_driver)
                # 发起报车
                car_report_info = app.auv_md_40_cmd_69(library=library, param=car_report_param)
                car_report_result = eval(car_report_info["pBody"])
                assert car_report_result == {"a": 0}
            else:
                print("脏数据")
                continue
