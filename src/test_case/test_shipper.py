# coding:utf-8
import pytest
import random
from src.common import random_param
from config import global_parameter
from src.pages import shipper
from src.pages import dispatch
from src.pages import service
import os

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
        self.dispatch_token = self.dispatch.dispatch_login(username=global_parameter.dispatch_account["username"],
                                                           password=global_parameter.dispatch_account["password"])

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")
    #
    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    # 用例1：测试货主端发布询价接口
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

    # 用例2: 测试货主端查询询价单列表接口（分为待报价和已报价两种）
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
                count = count + 1
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
        # 货主查询已报价的列表
        inquire_list = self.shipper.shipper_getInquires(cookie=self.shipper_token, type_num=1, time_num=0)
        count = 0
        # 遍历询价列表查询是否存在该条询价信息
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_id == inquire["id"]:
                count = count + 1
            else:
                continue
        assert count == 1

    # 用例3：测试货主确认报价接口（确认报价）
    def test_case003(self):
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
        # 遍历询价列表找到该条询价信息获取id
        inquire_id = ""
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_param["source_name"] == inquire["source_name"] and \
                    inquire_param["start_address"] == inquire["start_address"] and \
                    inquire_param["end_address"] == inquire["end_address"] and \
                    inquire_param["load_time"] == inquire["load_time"] and \
                    inquire_param["send_source_num"] == inquire["send_source_num"] and \
                    inquire_param["losePercent"] == inquire["losePercent"]:
                inquire_id = inquire["id"]
            else:
                continue
        # 客服报价的参数
        offerInquire_param = self.service.offerInquire_randomparam(inquire_id=inquire_id, company_id=shipper_company_id,
                                                                   username=shipper_username)
        # 客服发起报价
        offerInquire = self.service.service_offerInquire(cookie=self.service_token, param=offerInquire_param)
        # 验证接口返回
        assert offerInquire == {"data": {"offerInquire": 0}}
        # 货主确认报价
        confirm = self.shipper.shipper_confirmInquire(cookie=self.shipper_token, inquire_id=inquire_id, isConfirm=1)
        # 验证接口返回
        assert confirm == {"data": {"confirmInquire": 0}}

    # 用例4：测试货主确认报价接口（取消报价）
    def test_case004(self):
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
        # 遍历询价列表找到该条询价信息获取id
        count = 0
        inquire_id = ""
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_param["source_name"] == inquire["source_name"] and \
                    inquire_param["start_address"] == inquire["start_address"] and \
                    inquire_param["end_address"] == inquire["end_address"] and \
                    inquire_param["load_time"] == inquire["load_time"] and \
                    inquire_param["send_source_num"] == inquire["send_source_num"] and \
                    inquire_param["losePercent"] == inquire["losePercent"]:
                inquire_id = inquire["id"]
            else:
                continue
        # 客服报价的参数
        offerInquire_param = self.service.offerInquire_randomparam(inquire_id=inquire_id,
                                                                   company_id=shipper_company_id,
                                                                   username=shipper_username)
        # 客服发起报价
        offerInquire = self.service.service_offerInquire(cookie=self.service_token, param=offerInquire_param)
        # 验证接口返回
        assert offerInquire == {"data": {"offerInquire": 0}}
        # 货主确认报价
        confirm = self.shipper.shipper_confirmInquire(cookie=self.shipper_token, inquire_id=inquire_id, isConfirm=0)
        # 验证接口返回
        assert confirm == {"data": {"confirmInquire": 0}}
        # 取消报价后不会生成货单
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=1, time_num=0)
        count = 0
        # 遍历列表查询是否生成该条询价对应的货单信息
        for source in shipper_source_list["a"]:
            if inquire_param["source_name"] == source["o"] and \
                    inquire_param["start_address"] == source["a"] and \
                    inquire_param["end_address"] == source["b"] and \
                    inquire_param["load_time"] == source["c"] and \
                    inquire_param["send_source_num"] == source["n"] and \
                    source["t"] == offerInquire_param["up_price"] and \
                    source["d"] == offerInquire_param["need_car_num"]:
                count = 1
            else:
                continue
        assert count == 0

    # 用例5：查询货单（进行中的货单）
    def test_case005(self):
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
        # 遍历询价列表找到该条询价信息获取id
        count = 0
        inquire_id = ""
        for inquire in inquire_list["data"]["getInquires"]:
            if inquire_param["source_name"] == inquire["source_name"] and \
                    inquire_param["start_address"] == inquire["start_address"] and \
                    inquire_param["end_address"] == inquire["end_address"] and \
                    inquire_param["load_time"] == inquire["load_time"] and \
                    inquire_param["send_source_num"] == inquire["send_source_num"] and \
                    inquire_param["losePercent"] == inquire["losePercent"]:
                inquire_id = inquire["id"]
            else:
                continue
        # 客服报价的参数
        offerInquire_param = self.service.offerInquire_randomparam(inquire_id=inquire_id,
                                                                   company_id=shipper_company_id,
                                                                   username=shipper_username)
        # 客服发起报价
        offerInquire = self.service.service_offerInquire(cookie=self.service_token, param=offerInquire_param)
        # 验证接口返回
        assert offerInquire == {"data": {"offerInquire": 0}}
        # 货主确认报价
        confirm = self.shipper.shipper_confirmInquire(cookie=self.shipper_token, inquire_id=inquire_id, isConfirm=1)
        # 验证接口返回
        assert confirm == {"data": {"confirmInquire": 0}}
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=1, time_num=0)
        count = 0
        # 遍历列表查询是否生成该条询价对应的货单信息
        for source in shipper_source_list["a"]:
            if inquire_param["source_name"] == source["o"] and \
                    inquire_param["start_address"] == source["a"] and \
                    inquire_param["end_address"] == source["b"] and \
                    inquire_param["load_time"] == source["c"] and \
                    inquire_param["send_source_num"] == source["n"] and \
                    source["t"] == offerInquire_param["up_price"] and \
                    source["d"] == offerInquire_param["need_car_num"]:
                count = count + 1
            else:
                continue
        assert count == 1

    # 用例6 : 查询已完成的货单（暂时无法串联业务，只能查询）
    def test_case006(self):
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=2, time_num=0)
        assert "a" in shipper_source_list

    # 用例7 ： 货主端查询某货单的车辆监控地图（暂时无法串联业务，只能查询）
    def test_case007(self):
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=1, time_num=0)
        # 列表中随机获取一个货单
        source_id = random.choice(shipper_source_list["a"])["f"]
        # 查看该货单的车辆监控地图
        cars_map = self.shipper.shipper_getCarsMapBySourceId(cookie=self.shipper_token, sourceId=source_id)
        assert "data" in cars_map

    # 用例8： 货主端查询某货单的车辆列表（暂时无法串联业务，只能查询）
    def test_case008(self):
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=1, time_num=0)
        # 列表中随机获取一个货单
        source_id = random.choice(shipper_source_list["a"])["f"]
        # 查看该货单的车辆列表
        car_list = self.shipper.shipper_getCarsBySourceId(cookie=self.shipper_token, sourceId=source_id, time=0)
        assert "data" in car_list

    # 用例9 ：货主编辑基本信息
    def test_case009(self):
        # 生成一组随机的货主基础信息
        shipper_baseinfo = self.shipper.ran_baseinfo_param()
        # 修改货主的基础信息
        edit_shipper = self.shipper.shipper_editBaseCompanyInfo(cookie=self.shipper_token, param=shipper_baseinfo)
        assert edit_shipper == {"data": {"code": 0}}
        # 查询货主基础信息确认修改成功
        company_info = self.shipper.shipper_getcompanyInfo(cookie=self.shipper_token)["data"]["getShipper"]
        assert shipper_baseinfo["nikename"] == company_info["nikename"]
        assert shipper_baseinfo["gender"] == company_info["gender"]
        assert shipper_baseinfo["birthday"] == company_info["birthday"]
