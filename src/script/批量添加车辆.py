# coding:utf-8

import random
from src.common import random_param
from config import global_parameter
from src.pages import dispatch

# 批量加车类型
# 0 选择一个随机车队
# 1 指定一个车队
source_type = 1
fleet_id = "5ceb4fa8743a49698ec5f0db"
jpg = "J507BA2F950D931E7D1"
car_num = 3

dispatch = dispatch.Dispatch()
dispatch_token = dispatch.dispatch_login(username=global_parameter.dispatch_account["username"],
                                         password=global_parameter.dispatch_account["password"])
if source_type == 0:
    get_pagesize = dispatch.dispatch_getFleets(cookie=dispatch_token, page=1)
    pagesize = get_pagesize["data"]["data"]["pagesize"]
    # 查询车队列表
    get_fleets = dispatch.dispatch_getFleets(cookie=dispatch_token, page=random.randint(1, pagesize))
    # 任意选择一个车队id
    fleet_id = random.choice(get_fleets["data"]["data"]["rows"])["fleet_id"]
    for n in range(car_num):
        # 生成一组车辆信息
        car_param = dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=jpg)
        # 新增一个车辆
        send_result = dispatch.dispatch_createCarByFleet(cookie=dispatch_token, param=car_param)

else:
    for n in range(car_num):
        # 生成一组车辆信息
        car_param = dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=jpg)
        # 新增一个车辆
        send_result = dispatch.dispatch_createCarByFleet(cookie=dispatch_token, param=car_param)

