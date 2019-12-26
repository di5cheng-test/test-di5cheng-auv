# coding:utf-8

import random
from src.pages import dispatch
from src.common.random_param import Random_param as ran

# 批量加车类型
# 0 选择一个随机车队
# 1 指定一个车队
source_type = 1
fleet_id = "5ceb4fa8743a49698ec5f0db"
jpg = "J507BA2F950D931E7D1"
car_num = 3

dispatch = dispatch.Dispatch()
dispatch_token = dispatch.dispatch_login(username="songkangkang002", password="123456")

car_number = ran().create_carNumber(length=5)
gua_number = ran().create_carNumber(length=4)
m_user = ran().create_name()
m_mobile = 13000040001
car_ton = random.randint(20000, 100000)
m_id_card = "J2066F098D0CE8054D1"
yingyun_pic = "J2066F098D0CE8054D1"
status = 1
region_source = 5
first_people = 252

if source_type == 0:
    get_pagesize = dispatch.dispatch_getFleets(cookie=dispatch_token, page=1)
    pagesize = get_pagesize["data"]["data"]["pagesize"]
    # 查询车队列表
    get_fleets = dispatch.dispatch_getFleets(cookie=dispatch_token, page=random.randint(1, pagesize))
    # 任意选择一个车队id
    fleet_id = random.choice(get_fleets["data"]["data"]["rows"])["fleet_id"]
    for n in range(car_num):
        # 生成一组车辆信息
        m_mobile = m_mobile + n
        car_param = dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=jpg)
        # 新增一个车辆
        send_result = dispatch.dispatch_createCarByFleet(cookie=dispatch_token, param=car_param)

else:
    for n in range(car_num):
        # 生成一组车辆信息
        m_mobile = m_mobile + n
        car_param = dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=jpg)
        # 新增一个车辆
        send_result = dispatch.dispatch_createCarByFleet(cookie=dispatch_token, param=car_param)
