# coding:utf-8
from src.common import config
from src.pages import auv_app_new as app
from src.pages import operation
from ctypes import *
from src.common.random_param import Random_param as ran
import hashlib
import time
import random

global null
null = None

# 车队账号
username = "13327827656"
password = "123456"
# 给密码进行MD5加密
p_md5 = hashlib.md5(password.encode())

# 运营管理平台登录
op = operation.Operation()
operation_token = op.operation_login(phoneNum="13327827656", passWord="123456")

# 初始化
library = cdll.LoadLibrary(config.get_library())
common = app.Common()
common.initSDK(library=library, init_info=config.get_app_url())

for n in range(1):
    phone = 13000050007 + n
    name = ran().create_name()
    name_2 = ran().create_name()
    code = "696969"
    company_name = "auto" + str(int(time.time()))
    id_card = ran().create_IDcard()
    id_card_pic_m = "J5DEA926D60CFB8B02A"
    id_card_pic_p = "J95848896B0315044FF"
    business = "J571CB18220CFB8A08F"
    business_2 = "JF57F9F0040CFB8A895"
    company_id_number = str(int(time.time()))

    # 获取短信验证码参数
    code_param = common.app_code_param(phone=phone)
    # 获取短信验证码
    common.app_code(library=library, param=code_param)
    # 注册信息参数
    regist_param = common.app_regist_param(phone=phone, password=p_md5.hexdigest(), name=name, code=code)
    print(regist_param)
    # 注册
    common.app_regist(library=library, param=regist_param)
    # 登录信息参数
    login_param = common.app_login_param(username=phone, password=password)
    # 登录
    common.app_login(library=library, param=login_param)
    # 认证参数
    approve_param = common.auv_param_md_40_cmd_24(b=company_name, k=name, d=phone, e=id_card_pic_m, f=id_card_pic_p,
                                                  j=id_card, c=name_2, g=company_id_number, h=business, i=business_2)
    print(approve_param)
    # 提交认证
    approve_result = common.auv_md_40_cmd_24(library=library, param=approve_param)
    # 提取车队编号
    fleet_id = approve_result["a"]
    # 运营平台获取车队详情
    fleet_info = op.operation_md_40_cmd_51(cookie=operation_token, fleet_id=fleet_id)
    # 审核通过
    op.operation_md_40_cmd_15(cookie=operation_token,
                              fleet_id=fleet_info["fleet_id"],
                              fleet_name=fleet_info["fleet_name"],
                              contact=fleet_info["contact"],
                              user_name=fleet_info["user_name"],
                              status=1,
                              create_at=fleet_info["create_at"],
                              user_id=fleet_info["user_id"],
                              contact_phone=fleet_info["contact_phone"],
                              id_card=fleet_info["id_card"],
                              id_card_pic_m=fleet_info["id_card_pic_m"],
                              id_card_pic_p=fleet_info["id_card_pic_p"],
                              company_id_number=fleet_info["company_id_number"],
                              business=fleet_info["business"],
                              business_2=fleet_info["business_2"],
                              address="",
                              region_source=fleet_info["region_source"],
                              first_people=252,
                              car_type=random.randint(1, 4),
                              contract=fleet_info["contract"],
                              content="",
                              admin_name="测试小五",
                              admin_id="5cce48ba9f660834f3fa32f6",
                              admin_user_id=407954,
                              exist=1,
                              car_type_detail="",
                              status_name="待审核")
    # 登出参数
    login_out_param = common.app_login_out_param()
    # 登出
    common.app_login_out(library=library, param=login_out_param)


# phone = 13000050004
# name = ran().create_name()
# name_2 = ran().create_name()
# code = "696969"
# company_name = "auto" + str(int(time.time()))
# id_card = ran().create_IDcard()
# id_card_pic_m = "J5DEA926D60CFB8B02A"
# id_card_pic_p = "J95848896B0315044FF"
# business = "J571CB18220CFB8A08F"
# business_2 = "JF57F9F0040CFB8A895"
# company_id_number = str(int(time.time()))
# # 登录信息参数
# login_param = common.app_login_param(username="13000050004", password="123456")
# # 登录
# common.app_login(library=library, param=login_param)
# # 认证参数
# approve_param = common.auv_param_md_40_cmd_24(b=name, k=company_name, d=phone, e=id_card_pic_m, f=id_card_pic_p,
#                                               j=id_card, c=name_2, g=company_id_number, h=business, i=business_2)
# print(approve_param)
# # 提交认证
# common.auv_md_40_cmd_24(library=library, param=approve_param)
# 登出参数
login_out_param = common.app_login_out_param()
# 登出
common.app_login_out(library=library, param=login_out_param)

# fleet_info = op.operation_md_40_cmd_51(cookie=operation_token, fleet_id="5dfae187743a4903b26f8e03")
#
# op.operation_md_40_cmd_15(cookie=operation_token,
#                           fleet_id=fleet_info["fleet_id"],
#                           fleet_name=fleet_info["fleet_name"],
#                           contact=fleet_info["contact"],
#                           user_name=fleet_info["user_name"],
#                           status=1,
#                           create_at=fleet_info["create_at"],
#                           user_id=fleet_info["user_id"],
#                           contact_phone=fleet_info["contact_phone"],
#                           id_card=fleet_info["id_card"],
#                           id_card_pic_m=fleet_info["id_card_pic_m"],
#                           id_card_pic_p=fleet_info["id_card_pic_p"],
#                           company_id_number=fleet_info["company_id_number"],
#                           business=fleet_info["business"],
#                           business_2=fleet_info["business_2"],
#                           address="",
#                           region_source=fleet_info["region_source"],
#                           first_people=252,
#                           car_type=random.randint(1, 4),
#                           contract=fleet_info["contract"],
#                           content="",
#                           admin_name="测试小五",
#                           admin_id="5cce48ba9f660834f3fa32f6",
#                           admin_user_id=407954,
#                           exist=1,
#                           car_type_detail="",
#                           status_name="待审核")
