# coding:utf-8
import random
from src.common import config
from src.pages import service_new as service
import time

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.service = service.Service()
        self.service_token = self.service.service_login(username=config.get_account("service")["username"],
                                                        password=config.get_account("service")["password"])

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")
    #
    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    # 用例1：发布询价单
    def test_case001(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 查询货主
        company_name = "第五城来了"
        shipper_info = self.service.service_cmd_7(cookie=self.service_token, page=1, status=1,
                                                  company_name=company_name)
        shipper_id = shipper_info["data"][0]["company_id"]
        # 查询小五
        dispatch_name = "taotao02"
        dispatch_info = self.service.service_cmd_5(cookie=self.service_token, username=dispatch_name)
        dispatch_id = dispatch_info["data"][0]["user_id"]
        # 选择小五
        dispatches = {"a": dispatch_id, "b": dispatch_name}
        # 货单类型
        invoice_type = random.randint(1, 2)
        # 开票类型
        billing_type = random.choice([0, 1])
        # 备注
        remark = "auto test"
        # 装货地
        loading = "江苏南京"
        # 卸货地
        unloading = "山东东营"
        # 货品名称
        product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
        # 发布一条询价信息
        send_result = self.service.service_cmd_180(cookie=self.service_token, a=invoice_type, b=shipper_id, c=loading,
                                                   d=unloading, e=product_name, f=billing_type, g=remark,
                                                   h=[dispatches], j=company_name, k=service_id, l=4)
        # 验证接口返回
        assert send_result == {"code": 0}

    # 用例2：发布报车货单
    def test_case002(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 查询货主
        company_name = "第五城来了"
        shipper_info = self.service.service_cmd_7(cookie=self.service_token, page=1, status=1,
                                                  company_name=company_name)
        shipper_id = shipper_info["data"][0]["company_id"]
        # 查询小五
        dispatch_name = "taotao02"
        dispatch_info = self.service.service_cmd_5(cookie=self.service_token, username=dispatch_name)
        dispatch_id = dispatch_info["data"][0]["user_id"]
        # 选择小五
        dispatches = {"a": dispatch_id, "b": dispatch_name}
        # 货单类型
        invoice_type = random.randint(1, 2)
        # 装货时间
        loading_time = int(time.time()) * 1000
        # 发货吨数
        tonnage = random.randint(500, 1000) * 1000
        # 备注
        remark = "auto test"
        # 需求车数
        need_car_num = random.randint(10, 20)
        # 装货地
        loading = self.service.service_randomlocation(cookie=self.service_token)
        # 装货地详细地址
        loading_info = "中山北路" + str(random.randint(100, 200)) + "号"
        # 卸货地
        unloading = self.service.service_randomlocation(cookie=self.service_token)
        # 卸货地详细地址
        unloading_info = "华山南路" + str(random.randint(100, 200)) + "号"
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
        # 货品名称
        product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
        # 信息费
        info_price = random.randint(70, 100) * 100
        # 货品单价
        per_price = random.randint(1000, 2000) * 100
        # 发布一条报车货单
        send_result = self.service.service_cmd_189(cookie=self.service_token, a=invoice_type, b=shipper_id, c=loading,
                                                   d=unloading, e=loading_time, f=product_name, g=per_price, h=tonnage,
                                                   i=need_car_num, j=loss, l=up_price, m=up_billing_type, n=down_pirce,
                                                   o=down_billing_type, p=info_price, q=remark, r=[dispatches],
                                                   t=loading_info, u=unloading_info, x=service_id, y=company_name, z=4)
        # 验证接口返回
        assert send_result == {"code": 0}

    # 客服查询询价列表
    def test_case003(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 获取查询待处理询价列表
        shipper_list = self.service.service_cmd_186(cookie=self.service_token, f=0, j=1, k=10, m=service_id)
        assert shipper_list["code"] == 0
        # 获取查询已处理询价列表
        shipper_list = self.service.service_cmd_186(cookie=self.service_token, f=1, j=1, k=10, m=service_id)
        assert shipper_list["code"] == 0

    # 客服查询货单列表
    def test_case004(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 获取查询进行中货单列表
        shipper_list = self.service.service_cmd_80(cookie=self.service_token, d=1, e=1, u=service_id)
        assert shipper_list["code"] == 0
        # 获取查询已完成货单列表
        shipper_list = self.service.service_cmd_80(cookie=self.service_token, d=2, e=1, u=service_id)
        assert shipper_list["code"] == 0

    # 客服查询代办事项-询价列表
    def test_case005(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 获取查询代办事项-询价列表
        shipper_list = self.service.service_cmd_183(cookie=self.service_token, h=1, i=service_id)
        assert shipper_list["code"] == 0

    # 客服查看报价
    def test_case006(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 获取查询代办事项-查看报价
        shipper_list = self.service.service_cmd_184(cookie=self.service_token, a="5d6351fc95fe297a7c8266fd")
        assert shipper_list["a"] != []

    # 客服常用装卸货地址
    def test_case007(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 查询货主
        company_name = "第五城来了"
        shipper_info = self.service.service_cmd_7(cookie=self.service_token, page=1, status=1,
                                                  company_name=company_name)
        shipper_id = shipper_info["data"][0]["company_id"]
        # 客服常用装货地址
        shipper_list = self.service.service_cmd_190(cookie=self.service_token, a=shipper_id, b=1)
        assert shipper_list["code"] == 0
        # 客服常用卸货地址
        shipper_list = self.service.service_cmd_190(cookie=self.service_token, a=shipper_id, b=2)
        assert shipper_list["code"] == 0

    # 客服立即找车
    def test_case008(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 查询货主
        company_name = "第五城来了"
        shipper_info = self.service.service_cmd_7(cookie=self.service_token, page=1, status=1,
                                                  company_name=company_name)
        shipper_id = shipper_info["data"][0]["company_id"]
        # 查询小五
        dispatch_name = "taotao02"
        dispatch_info = self.service.service_cmd_5(cookie=self.service_token, username=dispatch_name)
        dispatch_id = dispatch_info["data"][0]["user_id"]
        # 选择小五
        dispatches = {"a": dispatch_id, "b": dispatch_name}
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
        # 货主装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽滁州", "山东 东营"])
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
        # 货品名称
        product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
        # 信息费
        info_price = random.randint(70, 100) * 100
        # 货品单价
        per_price = random.randint(1000, 2000) * 100
        # 记录当前时间
        time_now = int(time.time()) * 1000
        source_id = ""
        # 客服查询待办事项-待处理报价
        unconfirm_source_list = self.service.service_cmd_183(cookie=self.service_token, h=1, i=service_id)
        if unconfirm_source_list["data"] == []:
            print("没有待处理的报价")
        else:
            unconfirm_source = random.choice(unconfirm_source_list["data"])
            print("随机选择待处理报价")
            print(unconfirm_source)
            source_id = unconfirm_source["a"]
        # 客服待处理报价货单报价列表
        unconfirm_price_list = self.service.service_cmd_184(cookie=self.service_token, a=source_id)
        unconfirm_price_id = ""
        enterprise = ""
        enterprise_price = ""
        enterprise_car_num = ""
        if unconfirm_price_list["a"] == []:
            print("没有待处理的报价")
        else:
            unconfirm_price = random.choice(unconfirm_price_list["a"])
            unconfirm_price_id = unconfirm_price["a"]
            enterprise = unconfirm_price["f"]
            enterprise_price = unconfirm_price["c"]
            enterprise_car_num = unconfirm_price["d"]
            # 客服常用装货地址
        shipper_list_loading = self.service.service_cmd_190(cookie=self.service_token, a=shipper_id, b=1)
        assert shipper_list_loading["code"] == 0
        # 随机选择一个地址作为装货地址
        loading_address = random.choice(shipper_list_loading["data"])
        print("随机选择一个地址作为装货地址")
        print(loading_address)
        # 装货地
        loading = loading_address["a"]
        # 装货地详细地址
        loading_info = loading_address["b"]
        # 客服常用卸货地址
        shipper_list_unloading = self.service.service_cmd_190(cookie=self.service_token, a=shipper_id, b=2)
        assert shipper_list_unloading["code"] == 0
        # 随机选择一个地址作为卸货地址
        unloading_address = random.choice(shipper_list_unloading["data"])
        print("随机选择一个地址作为卸货地址")
        print(unloading_address)
        # 卸货地
        unloading = unloading_address["a"]
        # 卸货地详细地址
        unloading_info = unloading_address["b"]
        # 客服确认报价（立即找车）
        send_result = self.service.service_cmd_187(cookie=self.service_token, a=source_id, i=loading, j=loading_info,
                                                   k=unloading, l=unloading_info, m=loading_time, n=loss, o=tonnage,
                                                   p=up_price, q=up_billing_type, r=down_pirce, s=down_billing_type,
                                                   t=per_price, u=info_price, v=remark, w=enterprise,
                                                   x=unconfirm_price_id, y=enterprise_car_num, z=enterprise_price,
                                                   ab=shipper_id, ac=need_car_num)
        # 验证接口返回
        assert send_result == {"code": 0}

    # 客服结束询价
    def test_case009(self):
        # 通过接口获取客服信息
        service_info = self.service.service_cmd_52(cookie=self.service_token)
        # 提取客服ID
        service_id = service_info["user_id"]
        # 查询待处理询价单
        enquiry_list = self.service.service_cmd_186(cookie=self.service_token, f=0, j=1, k=10, m=service_id)
        if enquiry_list["a"] == []:
            print("没有待处理的询价单")
        else:
            enquiry = random.choice(enquiry_list["a"])
            print(enquiry)
            source_id = enquiry["s"]
            # 客服关闭询价
            send_result = self.service.service_cmd_188(cookie=self.service_token, a=source_id)
            # 验证接口返回
            assert send_result == {"code": 0}

