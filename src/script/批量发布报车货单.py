# coding:utf-8

import random
from src.pages import service_new
import time
from src.common.random_param import Random_param as ran

global null
null = None

# 发货数量
source_num = 10

service = service_new.Service()
service_token = service.service_login(username="songkangkang001", password="123456")
# 通过接口获取客服信息
service_info = service.service_md_40_cmd_52(cookie=service_token)
# 提取客服ID
service_id = service_info["user_id"]
# 查询货主
shipper_list = service.service_md_40_cmd_7(cookie=service_token, page=1, status=1, type=1)
# 选择一个货主
shipper_info = random.choice(shipper_list["data"])
shipper_id = shipper_info["company_id"]
company_name = shipper_info["company_name"]
# 查询小五
dispatch_list = service.service_md_40_cmd_5(cookie=service_token)
dispatch_info = random.choice(dispatch_list["data"])
dispatch_id = dispatch_info["user_id"]
dispatch_name = dispatch_info["username"]
# 选择小五
dispatches = {"a": 407954, "b": "test-dispatch"}  # {"a": dispatch_id, "b": dispatch_name}

for n in range(source_num):
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 装货时间
    loading_time = int(time.time()) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 备注
    remark = "auto test"
    # 备注 2
    remark2 = random.choice(["卸结", "好装好卸", "干净货", "蒸罐", "要报备车", "下装口", "车数可循环"])
    # 需求车数
    need_car_num = random.randint(10, 20)
    # 装货地
    up_address_list_s = service.service_md_40_cmd_190(cookie=service_token, a=service_id, b=1, c=2)
    if up_address_list_s["a"] == []:
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
    else:
        loading_s = random.choice(up_address_list_s["a"])["a"]
    # 卸货地
    un_address_list_s = service.service_md_40_cmd_190(cookie=service_token, a=service_id, b=2, c=2)
    if un_address_list_s["a"] == []:
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
    else:
        unloading_s = random.choice(up_address_list_s["a"])["a"]
    # 装货地三级联动
    up_address_linkage = ran().create_area_name()
    # 装货地详细地址
    up_address_detail = "中山北路" + str(random.randint(100, 200)) + "号"
    # 新增装货地址
    result = service.service_md_40_cmd_220(cookie=service_token, a=service_id, b=1,
                                           c=up_address_linkage, d=up_address_detail, e=1)
    assert result == {"code": 0}
    # 查询装货地址列表
    address_list = service.service_md_40_cmd_190(cookie=service_token, a=service_id, b=1, c=1)
    count = 0
    for address in address_list["a"]:
        if address["a"] == up_address_linkage and address["b"] == up_address_detail:
            count += 1
            break
        else:
            continue
    assert count == 1
    # 卸货地三级联动
    un_address_linkage = ran().create_area_name()
    # 卸货地详细地址
    un_address_detail = "华山南路" + str(random.randint(100, 200)) + "号"
    # 新增卸货地址
    result = service.service_md_40_cmd_220(cookie=service_token, a=service_id, b=2,
                                           c=un_address_linkage, d=un_address_detail, e=1)
    assert result == {"code": 0}
    # 查询装货地址列表
    address_list = service.service_md_40_cmd_190(cookie=service_token, a=service_id, b=2, c=1)
    count = 0
    for address in address_list["a"]:
        if address["a"] == un_address_linkage and address["b"] == un_address_detail:
            count += 1
            break
        else:
            continue
    assert count == 1
    # 承担损耗
    loss = random.choice([0, 1, 2, 3])
    # 上家价格
    up_price = random.randint(700, 1000) * 100
    # 上家开票
    up_billing_type = random.choice([0, 1])
    # 下家价格
    down_pirce = random.randint(500, 700) * 100
    # 下家开票
    un_billing_type = random.choice([0, 1])
    # 账期
    payment_days = random.choice(["周结", "月结", "双月结", "见票结算", "见单结算"])
    # 货品名称
    used_product_name_list = service.service_md_40_cmd_207(cookie=service_token, a=service_id)
    if used_product_name_list["a"] == []:
        product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
    else:
        product_name = random.choice(used_product_name_list["a"])["a"]
    # 货品单价
    per_price = random.randint(1000, 2000) * 100
    # 结算方式
    method_settlement = random.choice([0, 1])
    # 发布一条报车货单
    send_result = service.service_md_40_cmd_189(cookie=service_token, a=invoice_type, b=shipper_id,
                                                c=up_address_linkage, d=un_address_linkage, e=loading_time,
                                                f=product_name, g=loading_s, h=tonnage, i=need_car_num, j=loss,
                                                k=unloading_s, l=up_price, m=up_billing_type,
                                                n=down_pirce, o=un_billing_type, p=per_price, q=remark,
                                                r=[dispatches], t=up_address_detail, u=un_address_detail,
                                                x=service_id, y=company_name, z=2, w=payment_days,
                                                ab=method_settlement, af=remark2)
    source_num = send_result["a"]
    # 验证接口返回
    assert send_result["code"] == 0
