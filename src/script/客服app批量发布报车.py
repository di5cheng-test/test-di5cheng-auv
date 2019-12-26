from ctypes import *
from src.pages import auv_service
from src.common import config
import random
import time
from src.common.random_param import Random_param as ran

# 客服账号
username = "13300010001"
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
# 当前客服id
front_id = int(service_user_uid)

# 获取货品名称列表
goods_name_list_param = service_app.auv_param_md_41_cmd_115()
goods_name_list_info = service_app.auv_md_41_cmd_115(library=service_library, param=goods_name_list_param)
goods_name_list = eval(goods_name_list_info["pBody"])["a"]

# 查询小五列表参数
query_dispatch_param = service_app.auv_param_md_41_cmd_83(a=2)
dispatch_list_info = service_app.auv_md_41_cmd_83(library=service_library, param=query_dispatch_param)

# 查询货主公司参数
shipper_list_param = service_app.auv_param_md_41_cmd_97(b=front_id, c=1, d=100)
shipper_list_info = service_app.auv_md_41_cmd_97(library=service_library, param=shipper_list_param)

for n in range(0, 10):
    # 需求车数
    need_car_num = random.randint(10, 100)
    # 货主装货地
    loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 合肥", "山东 东营"])
    # 货主卸货地
    unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 合肥", "山东 东营"])
    # 装货地三级联动
    loading = ran().create_area_name()
    # 装货地详细地址
    loading_info = "中山北路" + str(random.randint(100, 200)) + "号"
    # 卸货地三级联动
    unloading = ran().create_area_name()
    # 卸货地详细地址
    unloading_info = "华山南路" + str(random.randint(100, 200)) + "号"
    # 货品名称
    product_name = random.choice(goods_name_list)["a"]
    # 货品单价
    per_price = random.randint(1000, 2000) * 100
    # 货单类型
    invoice_type = random.randint(1, 2)
    # 货主价格
    up_price = random.randint(700, 1000) * 100
    # 上家是否开票
    up_billing_type = random.choice([0, 1])
    # 车队价格
    down_pirce = random.randint(500, 700) * 100
    # 下家是否开票
    un_billing_type = random.choice([0, 1])
    # 承担损耗
    loss = random.choice([0, 1])
    # 装货时间
    loading_time = (int(time.time()) + 2000000) * 1000
    # 发货吨数
    tonnage = random.randint(500, 1000) * 1000
    # 账期
    payment_days = random.choice(["周结", "月结", "双月结", "见票结算", "见单结算"])
    # 结算方式
    method_settlement = random.choice([0, 1])
    # 备注
    remark = "auto test"
    # 选择小五
    dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
    # 选择公司
    shipper_id = random.choice(eval(shipper_list_info["pBody"])["a"])["a"]
    company_name = random.choice(eval(shipper_list_info["pBody"])["a"])["c"]
    # 询价参数
    if dispatch_type == 1:
        # 报车参数
        enquiry_car_param = service_app.auv_param_md_41_cmd_81(a=invoice_type, b=shipper_id, c=loading, d=unloading,
                                                               e=loading_time, f=product_name, g=loading_s,
                                                               h=tonnage, i=need_car_num, j=loss, k=unloading_s,
                                                               l=up_price, m=up_billing_type, n=down_pirce,
                                                               o=un_billing_type, p=per_price, q=remark, r=[dispatch],
                                                               t=loading_info, u=unloading_info, s=1,
                                                               x=front_id, y=company_name, z=2, w=payment_days,
                                                               ab=method_settlement)

    else:
        enquiry_car_param = service_app.auv_param_md_41_cmd_81(a=invoice_type, b=shipper_id, c=loading, d=unloading,
                                                               e=loading_time, f=product_name, g=loading_s, h=tonnage,
                                                               i=need_car_num, j=loss, k=unloading_s, l=up_price,
                                                               m=up_billing_type, n=down_pirce, o=un_billing_type,
                                                               p=per_price, q=remark, r=[dispatch], t=loading_info,
                                                               u=unloading_info, x=front_id, y=company_name, z=2,
                                                               w=payment_days, ab=method_settlement)
    # 发布报车货单
    enquiry_car_result = service_app.auv_md_41_cmd_81(library=service_library, param=enquiry_car_param)
