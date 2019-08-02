# coding:utf-8

import random
from config import global_parameter
from src.pages import service

global null
null = None

# 批量发货类型
# 0 选择一个随机货主，所有货都由该货主发货
# 1 每次随机一个货主发一次货
# 2 指定货主发布货
source_type = 2

# 指定货主的信息
source_shipper_id = "5d09e4fdd54a6b5990c10d87"
source_shipper_name = "陈氏贸易集团"
# 发货数量
source_num = 2

service = service.Service()
service_token = service.service_login(username=global_parameter.service_account["username"],
                                      password=global_parameter.service_account["password"])
# 客服查询货主列表
get_pagesize = service.service_getShippers(cookie=service_token, page=1, status=1)
pagesize = get_pagesize["pagesize"]

if source_type == 0:
    # 随机获取某一页货主
    shippers_list = service.service_getShippers(cookie=service_token, page=random.randint(1, pagesize), status=1)
    # 随机选择当前页的货主
    shipper_info = random.choice(shippers_list["data"])
    shipper_id = shipper_info["company_id"]
    shipper_name = shipper_info["company_name"]
    for n in range(source_num):
        # 发货
        param = service.service_fahuoparam(cookie=service_token, company_id=shipper_id, company_name=shipper_name)
        service.service_createSource(cookie=service_token, param=param)

elif source_type == 1:
    for n in range(source_num):
        # 随机获取某一页货主
        shippers_list = service.service_getShippers(cookie=service_token, page=random.randint(1, pagesize), status=1)
        # 随机选择当前页的货主
        shipper_info = random.choice(shippers_list["data"])
        shipper_id = shipper_info["company_id"]
        shipper_name = shipper_info["company_name"]
        # 发货
        param = service.service_fahuoparam(cookie=service_token, company_id=shipper_id, company_name=shipper_name)
        service.service_createSource(cookie=service_token, param=param)

else:
    for n in range(source_num):
        # 发货
        param = service.service_fahuoparam(cookie=service_token, company_id=source_shipper_id,
                                           company_name=source_shipper_name)
        service.service_createSource(cookie=service_token, param=param)
