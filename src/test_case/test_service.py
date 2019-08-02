# coding:utf-8
import pytest
import random
from src.common import random_param
from config import global_parameter
from src.pages import shipper
from src.pages import dispatch
from src.pages import service

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.shipper = shipper.Shipper()
        self.service = service.Service()
        self.dispatch = dispatch.Dispatch()
        self.shipper_token = self.shipper.shipper_login(mobile=global_parameter.shipper_account["username"],
                                                        password=global_parameter.shipper_account["password"])
        self.service_token = self.service.service_login(username=global_parameter.service_account["username"],
                                                        password=global_parameter.service_account["password"])
        self.dispatch_token = self.service.service_login(username=global_parameter.service_account["username"],
                                                         password=global_parameter.service_account["password"])

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")
    #
    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    # 用例1：客服端查询待处理的询价列表
    def test_case001(self):
        # 通过接口获取货主的认证信息
        shipper_info = self.shipper.shipper_getcompanyInfo(cookie=self.shipper_token)
        # 提取公司名称
        shipper_company = shipper_info["data"]["getShipper"]["company_name"]
        # 生成一组询价参数
        inquire_param = self.shipper.inquire_param(cookie=self.shipper_token, company_name=shipper_company)
        # 发布一条询价信息
        send_result = self.shipper.shipper_sendInquire(cookie=self.shipper_token, param=inquire_param)
        # 验证接口返回
        assert send_result == {'data': {'sendInquire': 0}}
        # 货主查询询价列表
        inquire_list = self.shipper.shipper_getInquires(cookie=self.shipper_token, type_num=0, time_num=0)
        # 遍历询价列表查询是否存在该条询价信息
        count = 0
        inquire_id = ""
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_param["source_name"] == inquire["source_name"] and \
                    inquire_param["start_address"] == inquire["start_address"] and \
                    inquire_param["end_address"] == inquire["end_address"] and \
                    inquire_param["load_time"] == inquire["load_time"] and \
                    inquire_param["send_source_num"] == inquire["send_source_num"] and \
                    inquire_param["losePercent"] == inquire["losePercent"]:
                count = 1
                inquire_id = inquire["id"]
            else:
                continue
        assert count == 1

        # 客服查询待报价的列表
        service_inquire_list = self.service.service_getInquires(cookie=self.service_token, type_num=0, time_num=0)
        count = 0
        # 遍历询价列表查询是否存在该条询价信息
        for inquire in service_inquire_list["a"]:
            if inquire_id == inquire["f"]:
                count = 1
            else:
                continue
        assert count == 1

    # 用例2：客服端查询已处理的询价列表
    def test_case002(self):
        # 通过接口获取货主的认证信息
        shipper_info = self.shipper.shipper_getcompanyInfo(cookie=self.shipper_token)
        # 提取公司名称
        shipper_company = shipper_info["data"]["getShipper"]["company_name"]
        # 提取用户名称
        shipper_username = shipper_info["data"]["getShipper"]["username"]
        # 提取company_id
        shipper_company_id = shipper_info["data"]["getShipper"]["company_id"]
        # 生成一组询价参数
        inquire_param = self.shipper.inquire_param(cookie=self.shipper_token, company_name=shipper_company)
        # 发布一条询价信息
        send_result = self.shipper.shipper_sendInquire(cookie=self.shipper_token, param=inquire_param)
        # 验证接口返回
        assert send_result == {'data': {'sendInquire': 0}}
        # 货主查询询价列表
        inquire_list = self.shipper.shipper_getInquires(cookie=self.shipper_token, type_num=0, time_num=0)
        # 遍历询价列表查询是否存在该条询价信息
        count = 0
        inquire_id = ""
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_param["source_name"] == inquire["source_name"] and \
                    inquire_param["start_address"] == inquire["start_address"] and \
                    inquire_param["end_address"] == inquire["end_address"] and \
                    inquire_param["load_time"] == inquire["load_time"] and \
                    inquire_param["send_source_num"] == inquire["send_source_num"] and \
                    inquire_param["losePercent"] == inquire["losePercent"]:
                count = 1
                inquire_id = inquire["id"]
            else:
                continue
        assert count == 1
        # 客服报价的参数
        offerInquire_param = self.service.offerInquire_randomparam(inquire_id=inquire_id, company_id=shipper_company_id,
                                                                   username=shipper_username)
        # 客服发起报价
        offerInquire = self.service.service_offerInquire(cookie=self.service_token, param=offerInquire_param)
        # 验证接口返回
        assert offerInquire == {"data": {"offerInquire": 0}}
        # 客服查询已处理的列表
        service_inquire_list = self.service.service_getInquires(cookie=self.service_token, type_num=1, time_num=0)
        count = 0
        # 遍历询价列表查询是否存在该条询价信息
        for inquire in service_inquire_list["a"]:
            if inquire_id == inquire["f"]:
                count = 1
            else:
                continue
        assert count == 1

    # 客服代替货主发布货单
    def test_case003(self):
        # 获取已验证的货主列表
        shipper_list = self.service.service_getShippers(cookie=self.service_token, page=1, status=1)
        # 随机选择一个货主company_name,company_id
        shipper_info = random.choice(shipper_list["data"])
        company_name = shipper_info["company_name"]
        company_id = shipper_info["company_id"]
        # 生成一组随机货源信息
        source_param = self.service.service_fahuoparam(cookie=self.service_token, company_id=company_id,
                                                       company_name=company_name)
        # 发布货源
        source_result = self.service.service_createSource(cookie=self.service_token, param=source_param)
        assert source_result == {"data": {"createSource": 0}}
        # 查询货源列表
        service_source_list = self.service.service_getSourcesByService(cookie=self.service_token, type_num=1,
                                                                       page=1, company_id=company_id)
        pagesize = service_source_list["pagesize"]
        count = 0
        for n in range(pagesize):
            service_source_list = self.service.service_getSourcesByService(cookie=self.service_token, type_num=1,
                                                                           page=1, company_id=company_id)
            for source in service_source_list["a"]:
                if source_param["start_address"] == source["a"] and \
                        source_param["end_address"] == source["b"] and \
                        source_param["need_car_num"] == source["d"] and \
                        source_param["source_name"] == source["o"] and \
                        source_param["up_price"] == source["t"]:
                    count = count + 1
                else:
                    continue
        assert count >= 1
