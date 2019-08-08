# coding:utf-8
from src.common import config
from src.pages import app
from ctypes import *
from src.common.random_param import Random_param as ran

global null
null = None


# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

# 登录信息参数
login_param = common.app_login_param(username="13327827656", password="123456")
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
for n in range(2):
    # app 添加车辆
    car_info_param = ran().create_app_car_info(fleet_id=enterprise)
    car_number = eval(car_info_param)["a"]
    addcar_info = common.app_add_car(library=library, param=car_info_param)
    addcar_result = eval(addcar_info["pBody"])
    assert addcar_result == {"a": 0}
    # app 车辆列表查看该车
    app_carinfo_list_param = common.app_carinfo_list_param(a=0, b=enterprise)
    app_carinfo_list_info = common.app_carinfo_list(library=library, param=app_carinfo_list_param)
    app_carinfo_list = eval(app_carinfo_list_info["pBody"])["s"]
    count = 0
    car_id = ""
    for carinfo in app_carinfo_list:
        if car_number == carinfo["a"]:
            count = count + 1
            car_id = carinfo["d"]
            break
        else:
            continue
    assert count == 1
    # app 添加挂车
    gua_car_info_param = ran().create_app_gua_car_info(fleet_id=enterprise)
    gua_car_number = eval(gua_car_info_param)["a"]
    add_gua_car_info = common.app_add_gua_car(library=library, param=gua_car_info_param)
    add_gua_car_result = eval(add_gua_car_info["pBody"])
    assert add_gua_car_result == {"a": 0}
    # app 挂车列表查看该挂车
    app_gua_carinfo_list_info_param = common.app_carinfo_list_param(a=enterprise, b=0)
    app_gua_carinfo_list_info = common.app_gua_carinfo_list(library=library, param=app_gua_carinfo_list_info_param)
    app_gua_carinfo_list = eval(app_gua_carinfo_list_info["pBody"])["s"]
    count = 0
    gua_car_id = ""
    for gua_carinfo in app_gua_carinfo_list:
        if gua_car_number == gua_carinfo["a"]:
            count = count + 1
            gua_car_id = gua_carinfo["d"]
            break
        else:
            continue
    assert count == 1
    # app 添加司机
    driver_param = ran().create_app_driver_info(fleet_id=enterprise)
    driver_name = eval(driver_param)["a"]
    driver_phone = eval(driver_param)["c"]
    app_add_driver_info = common.app_add_driver(library=library, param=driver_param)
    # app_add_driver_result = eval(app_add_driver_info["pBody"])
    # assert app_add_driver_result == {"a": 0}
    # app 司机列表查看该司机
    app_driverinfo_list_param = common.app_driverinfo_list_param(a=enterprise, b=0)
    app_driverinfo_list_info = common.app_driverinfo_list(library=library, param=app_driverinfo_list_param)
    app_driverinfo_list = eval(app_driverinfo_list_info["pBody"])["s"]
    count = 0
    driver_uid = ""
    driver_id = ""
    for driverinfo in app_driverinfo_list:
        if driver_name == driverinfo["a"] and driver_phone == driverinfo["b"]:
            count = count + 1
            driver_uid = driverinfo["c"]
            driver_id = driverinfo["g"]
            break
        else:
            continue
    assert count == 1
    # app 添加押运员
    driver_ya_param = ran().create_app_driver_ya_info(fleet_id=enterprise)
    driver_ya_name = eval(driver_ya_param)["a"]
    driver_ya_phone = eval(driver_ya_param)["b"]
    app_add_driver_ya_info = common.app_add_driver_ya(library=library, param=driver_ya_param)
    app_add_driver_ya_result = eval(app_add_driver_ya_info["pBody"])
    assert app_add_driver_ya_result == {"a": 0}
    # app 押运员列表查看该押运员
    app_driverinfo_list_ya_param = common.app_ya_driverinfo_list_param(a=enterprise, b=0)
    app_driverinfo_list_ya_info = common.app_ya_driverinfo_list(library=library,
                                                                param=app_driverinfo_list_ya_param)
    app_driverinfo_ya_list = eval(app_driverinfo_list_ya_info["pBody"])["s"]
    count = 0
    driver_ya_uid = ""
    driver_ya_id = ""
    for driverinfo_ya in app_driverinfo_ya_list:
        if driver_ya_name == driverinfo_ya["b"] and driver_ya_phone == driverinfo_ya["c"]:
            count = count + 1
            driver_ya_uid = driverinfo_ya["a"]
            driver_ya_id = driverinfo_ya["g"]
            break
        else:
            continue
    assert count == 1
    # app 添加运力
    app_add_capacity_param = common.app_add_capacity_param(a=car_id, b=gua_car_id, c=driver_id,
                                                           d=driver_ya_id, e=enterprise, f=driver_uid,
                                                           g=driver_ya_uid)
    app_add_capacity_info = common.app_add_capacity(library=library, param=app_add_capacity_param)
    app_add_capacity_result = eval(app_add_capacity_info["pBody"])
    assert app_add_capacity_result == {"a": 0}
    # app 运力列表查看该运力
    app_capacitylist_param = common.app_capacitylist_param(a=enterprise, b=0)
    app_capacitylist_info = common.app_capacitylist(library=library, param=app_capacitylist_param)
    app_capacitylist = eval(app_capacitylist_info["pBody"])["s"]
    count = 0
    for capacity in app_capacitylist:
        if driver_id == capacity["a"]:
            count = count + 1
            break
        else:
            continue
    assert count == 1
