# coding:utf-8

from config import global_parameter
from src.pages import service

global null
null = None

# 报价类型
# 0 所有询价单均报价
# 1 指定 货主询价单进行报价
inquire_type = 0
# 公司id
inquire_company_id = "5cee4b22743a496726250af8"
# 公司联系人姓名
inquire_username = "yoho股份有限公司"

service = service.Service()
service_token = service.service_login(username=global_parameter.service_account["username"],
                                      password=global_parameter.service_account["password"])

if inquire_type == 0:
    # 客服查询待报价的列表
    for n in range(100):
        service_inquire_list = service.service_getInquires(cookie=service_token, type_num=0, time_num=0)
        if service_inquire_list == {"a": []}:
            print("无可报价的询价")
            break
        else:
            for inquire in service_inquire_list["a"]:
                # 获取货单id
                inquire_id = inquire["f"]
                # 货单对应的公司id
                inquire_company_id = inquire["g"]
                # 货单对应的公司联系人姓名
                inquire_username = inquire["i"]
                # 客服报价的参数
                offerInquire_param = service.offerInquire_randomparam(inquire_id=inquire_id,
                                                                      company_id=inquire_company_id,
                                                                      username=inquire_username)
                service.service_offerInquire(cookie=service_token, param=offerInquire_param)

else:
    for n in range(100):
        service_inquire_list = service.service_getInquires(cookie=service_token, type_num=0, time_num=0)
        if service_inquire_list == {"a": []}:
            print("无可报价的询价")
            break
        else:
            for inquire in service_inquire_list["a"]:
                if inquire_company_id == inquire["g"]:
                    # 获取货单id
                    inquire_id = inquire["f"]
                    # 客服报价的参数
                    offerInquire_param = service.offerInquire_randomparam(inquire_id=inquire_id,
                                                                          company_id=inquire_company_id,
                                                                          username=inquire_username)
                    service.service_offerInquire(cookie=service_token, param=offerInquire_param)
                else:
                    continue
