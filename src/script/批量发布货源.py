# coding:utf-8

import random
from src.pages import service_new as service
from src.common import config
import time

global null
null = None

# 批量发货类型
# 0 选择一个随机货主，所有货都由该货主发货
# 1 每次随机一个货主发一次货
# 2 指定货主发布货
source_type = 2

# 货主名称
company_name = "第五城来了"

# 发货数量
source_num = 10

service = service.Service()
service_token = service.service_login(username=config.get_account("service")["username"],
                                      password=config.get_account("service")["password"])
# 通过接口获取客服信息
service_info = service.service_cmd_52(cookie=service_token)
# 提取客服ID
service_id = service_info["user_id"]
for n in range(source_num):
    # 查询货主
    shipper_info = service.service_cmd_7(cookie=service_token, page=1, status=1,
                                         company_name=company_name)
    shipper_id = shipper_info["data"][0]["company_id"]
    # 查询小五
    dispatch_name = "taotao02"
    dispatch_info = service.service_cmd_5(cookie=service_token, username=dispatch_name)
    dispatch_id = dispatch_info["data"][0]["user_id"]
    # 选择小五
    dispatches = {"a": dispatch_id, "b": dispatch_name}
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 装货时间
    loading_time = int(time.time()) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 备注
    remark = "auto test"
    # 需求车数
    need_car_num = random.randint(10, 20)
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
    # 发布一条报车货单
    send_result = service.service_cmd_189(cookie=service_token, a=invoice_type, b=shipper_id, c=loading,
                                          d=unloading, e=loading_time, f=product_name, g=per_price, h=tonnage,
                                          i=need_car_num, j=loss, l=up_price, m=up_billing_type, n=down_pirce,
                                          o=down_billing_type, p=info_price, q=remark, r=[dispatches],
                                          t=loading_info, u=unloading_info, x=service_id, y=company_name, z=4)
