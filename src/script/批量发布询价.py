# coding:utf-8INIT_DEV

from config import global_parameter
from src.pages import shipper

global null
null = None

shipper = shipper.Shipper()
shipper_token = shipper.shipper_login(mobile=global_parameter.shipper_account["username"],
                                      password=global_parameter.shipper_account["password"])

# 通过接口获取货主的认证信息
shipper_info = shipper.shipper_getcompanyInfo(cookie=shipper_token)
# 提取公司名称
shipper_company = shipper_info["data"]["getShipper"]["company_name"]
# 设置循环次数
count = 10
for n in range(count):
    # 生成一组询价参数
    inquire_param = shipper.inquire_param(cookie=shipper_token, company_name=shipper_company)
    # 发布一条询价信息
    shipper.shipper_sendInquire(cookie=shipper_token, param=inquire_param)
