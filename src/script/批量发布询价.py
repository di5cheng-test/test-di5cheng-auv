# coding:utf-8

from src.pages import shipper
from src.pages import dispatch_new as dispatch
from src.pages import service_new as service
from src.pages import auv_app_new
from src.pages import finance
from ctypes import *
import random
from src.common import config
from src.common.random_param import Random_param as ran
import time

global null
null = None

service = service.Service()
service_token = service.service_login(username="dinghanwen01",
                                      password="123456")

# 通过接口获取客服信息
service_info = service.service_cmd_52(cookie=service_token)
# 提取客服ID
service_id = service_info["user_id"]
# 查询货主
company_name = "奶茶工坊"
shipper_info = service.service_cmd_7(cookie=service_token, page=1, status=1,
                                     company_name=company_name)
shipper_id = shipper_info["data"][0]["company_id"]
# 查询小五
dispatch_name = "dinghanwen02"
dispatch_info = service.service_cmd_5(cookie=service_token, username=dispatch_name)
dispatch_id = dispatch_info["data"][0]["user_id"]
# 选择小五
dispatches = {"a": dispatch_id, "b": dispatch_name}

# 设置循环次数
count = 100
for n in range(count):
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 装货时间
    loading_time = int(time.time()) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 备注
    remark = "DHW test"
    # 需求车数
    need_car_num = random.randint(10, 20)
    # 货主装货地
    loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
    # 卸货地
    unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
    # 装货地
    loading = service.service_randomlocation(cookie=service_token)
    # 装货地详细地址
    loading_info = "中山北路" + str(random.randint(100, 200)) + "号"
    # 卸货地
    unloading = service.service_randomlocation(cookie=service_token)
    # 卸货地详细地址
    unloading_info = "华山南路" + str(random.randint(100, 200)) + "号"
    # 承担损耗
    loss = random.choice([0, 1])
    # 上家价格
    up_price = random.randint(700, 1000) * 100
    # 上家开票
    up_billing_type = random.choice([0, 1])
    # 下家价格
    down_pirce = random.randint(500, 700) * 100
    # 下家开票
    down_billing_type = random.choice([0, 1])
    # 货品名称
    product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
    # 信息费
    info_price = random.randint(70, 100) * 100
    # 货品单价
    per_price = random.randint(1000, 2000) * 100
    # 记录当前时间
    time_now = int(time.time()) * 1000
    # 发布一条询价货单
    send_result = service.service_cmd_180(cookie=service_token, a=invoice_type, b=shipper_id, c=loading_s,
                                          d=unloading_s, e=product_name, f=up_billing_type, g=remark,
                                          h=[dispatches], j=company_name, k=service_id, l=4)
    print("已发布"+str(n)+"条")
    # 验证接口返回
    assert send_result == {"code": 0}
