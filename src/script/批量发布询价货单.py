# coding:utf-8
from src.pages import service_new as service
import random
import time

global null
null = None

service = service.Service()
service_token = service.service_login(username="songkangkang001", password="123456")

# 通过接口获取客服信息
service_info = service.service_md_40_cmd_52(cookie=service_token)
# 提取客服ID
service_id = service_info["user_id"]
# 查询小五
dispatch_info = service.service_md_40_cmd_5(cookie=service_token)
dispatch = random.choice(dispatch_info["data"])
# 选择小五
dispatches = {"a": dispatch["user_id"], "b": dispatch["username"]}

# 设置循环次数
count = 1
for n in range(count):
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 装货时间
    loading_time = (int(time.time()) + 2000000) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 备注
    remark = "auto test"
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
    # 是否开票
    billing_type = random.choice([0, 1])
    # 货品名称
    product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
    # 信息费
    info_price = random.randint(70, 100) * 100
    # 货品单价
    per_price = random.randint(1000, 2000) * 100
    # 账期
    payment_days = random.choice(["周结", "月结", "双月结", "见票结算", "见单结算"])
    # 记录当前时间
    time_now = int(time.time()) * 1000
    # 备注 2
    remark2 = random.choice(["卸结", "好装好卸", "干净货", "蒸罐", "要报备车", "下装口", "车数可循环"])
    # 发布一条询价货单
    send_result = service.service_md_40_cmd_180(cookie=service_token, a=invoice_type, b=need_car_num, c=loading_s,
                                                d=unloading_s, i=1, j=tonnage, k=service_id, l=2, o=remark2,
                                                e=product_name, f=billing_type, g=remark, h=[dispatches],
                                                m=payment_days, n=loading_time)
    # {"a":2,"b":1,"c":"张家港","d":"东营","e":"甲苯","f":1,"g":"ff","h":[{"a":407944,"b":"田中峰"}],"j":2000,"k":408059,
    # "l":4,"m":"周结","n":1576648112473,"o":"卸结 好装好卸"}
    print("已发布" + str(n + 1) + "条")
    # 验证接口返回
    assert send_result == {"code": 0}
