from ctypes import *
from src.pages import auv_service
from src.common import config
import random
import time

# 客服账号
username = "17777777771"
password = "123456"
# 添加小五类型：1全部调度，非1为随机某个小五
dispatch_type = 0

# 客服app登录
service_library = cdll.LoadLibrary(config.get_library("service_library_path"))
service_app = auv_service.Common()
service_app.initSDK(library=service_library, init_info=config.get_app_url())
# 登录信息参数
service_login_param = service_app.app_login_param(username=username, password=password)
# 登录
service_login_info = service_app.app_login(library=service_library, param=service_login_param)
service_user_uid = eval(service_login_info["pBody"])["i"]

# 获取货品名称列表
goods_name_list_param = service_app.auv_param_md_41_cmd_115()
goods_name_list_info = service_app.auv_md_41_cmd_115(library=service_library, param=goods_name_list_param)
goods_name_list = eval(goods_name_list_info["pBody"])["a"]

# 查询小五列表参数
query_dispatch_param = service_app.auv_param_md_41_cmd_83(a=2)
dispatch_list_info = service_app.auv_md_41_cmd_83(library=service_library, param=query_dispatch_param)

for n in range(0, 10):
    # 当前客服id
    front_id = int(service_user_uid)
    # 需求车数
    need_car_num = random.randint(10, 100)
    # 货主装货地
    loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 合肥", "山东 东营"])
    # 卸货地
    unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 合肥", "山东 东营"])
    # 货品名称
    product_name = random.choice(goods_name_list)["a"]
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 是否开票
    billing_type = random.choice([0, 1])
    # 装货时间
    loading_time = (int(time.time()) + 2000000) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 账期
    payment_days = random.choice(["周结", "月结", "双月结", "见票结算", "见单结算"])
    # 备注
    remark = "auto test"
    # 选择小五
    dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
    # 询价参数
    if dispatch_type == 1:
        enquiry_param = service_app.auv_param_md_41_cmd_80(a=invoice_type, b=need_car_num, c=loading_s,
                                                           d=unloading_s, i=1, j=tonnage, k=front_id, l=2,
                                                           e=product_name, f=billing_type, g=remark, h=[dispatch],
                                                           m=payment_days, n=loading_time)
    else:
        enquiry_param = service_app.auv_param_md_41_cmd_80(a=invoice_type, b=need_car_num, c=loading_s,
                                                           d=unloading_s, j=tonnage, k=front_id, l=2,
                                                           e=product_name, f=billing_type, g=remark, h=[dispatch],
                                                           m=payment_days, n=loading_time)
    # 发布询价货单
    service_app.auv_md_41_cmd_80(library=service_library, param=enquiry_param)
