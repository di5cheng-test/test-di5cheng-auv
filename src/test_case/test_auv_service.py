from ctypes import *
from src.pages import auv_service
from src.pages import auv_app_new
from src.common import config
from src.common.random_param import Random_param as ran
import random
import time

global null
null = None


class Test_case(object):
    def setup_class(self):
        # 客服app登录
        self.service_library = cdll.LoadLibrary(config.get_library("service_library_path"))
        self.service_app = auv_service.Common()
        self.service_app.initSDK(library=self.service_library, init_info=config.get_app_url())
        # 登录信息参数
        service_login_param = self.service_app.app_login_param(username=config.get_account("app_serivce")["username"],
                                                               password=config.get_account("app_serivce")["password"])
        # 登录
        service_login_info = self.service_app.app_login(library=self.service_library, param=service_login_param)
        self.service_user_uid = eval(service_login_info["pBody"])["i"]
        # 车队app登录
        self.library = cdll.LoadLibrary(config.get_library())
        self.app = auv_app_new.Common()
        self.app.initSDK(library=self.library, init_info=config.get_app_url())
        # 登录信息参数
        login_param = self.app.app_login_param(username=config.get_account("app")["username"],
                                               password=config.get_account("app")["password"])
        # 登录
        login_info = self.app.app_login(library=self.library, param=login_param)
        self.user_uid = eval(login_info["pBody"])["i"]
        # 获取货品名称列表
        goods_name_list_param = self.service_app.auv_param_md_41_cmd_115()
        goods_name_list_info = self.service_app.auv_md_41_cmd_115(library=self.service_library,
                                                                  param=goods_name_list_param)
        self.goods_name_list = eval(goods_name_list_info["pBody"])["a"]
        # 车队认证信息参数
        enterprise_info_param = self.app.auv_param_md_40_cmd_23()
        # 获取车队认证信息
        enterprise_info = self.app.auv_md_40_cmd_23(library=self.library, param=enterprise_info_param)
        # 车队ID
        self.enterprise = eval(enterprise_info["pBody"])["a"]
        # 车队名称
        self.enterprise_name = eval(enterprise_info["pBody"])["b"]
        # 姓名
        self.user_name = eval(enterprise_info["pBody"])["c"]

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")

    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    # 添加前线常用装货地址
    def test_case001(self):
        # 添加前线常用装货地址参数
        front_id = int(self.service_user_uid)
        loading_address = ran().create_area_name()
        loading_detailed_address = "团结路" + ran().random_num(num=3) + "号"
        add_address_param = self.service_app.auv_param_md_41_cmd_135(a=front_id, b=1, c=loading_address,
                                                                     d=loading_detailed_address, e=1)
        # 添加前线常用地址
        result = self.service_app.auv_md_41_cmd_135(library=self.service_library, param=add_address_param)
        assert eval(result["pBody"]) == {'code': 0}
        # 前线常用地址列表参数
        address_list_param = self.service_app.auv_param_md_41_cmd_82(a=front_id, b=1, c=1, e=1)
        # 前线常用地址列表查询刚添加的地址
        address_list_info = self.service_app.auv_md_41_cmd_82(library=self.service_library, param=address_list_param)
        address_list = eval(address_list_info["pBody"])["a"]
        count = 0
        address_id = ""
        for address_info in address_list:
            if address_info["a"] == loading_address and address_info["b"] == loading_detailed_address:
                count += 1
                address_id = address_info["e"]
                break
            else:
                continue
        assert count == 1
        # 删除刚添加的地址参数
        del_address_param = self.service_app.auv_param_md_41_cmd_134(a=address_id)
        del_result = self.service_app.auv_md_41_cmd_134(library=self.service_library, param=del_address_param)
        assert eval(del_result["pBody"]) == {'code': 0}
        # 前线常用地址列表查询刚添加的地址
        address_list_info = self.service_app.auv_md_41_cmd_82(library=self.service_library, param=address_list_param)
        address_list = eval(address_list_info["pBody"])["a"]
        count = 0
        for address_info in address_list:
            if address_info["a"] == loading_address and address_info["b"] == loading_detailed_address:
                count += 1
                break
            else:
                continue
        assert count == 0

    # 添加前线常用卸货地址
    def test_case002(self):
        # 添加前线常用卸货地址参数
        front_id = int(self.service_user_uid)
        unloading_address = ran().create_area_name()
        unloading_detailed_address = "团结路" + ran().random_num(num=3) + "号"
        add_address_param = self.service_app.auv_param_md_41_cmd_135(a=front_id, b=2, c=unloading_address,
                                                                     d=unloading_detailed_address, e=1)
        # 添加前线常用地址
        result = self.service_app.auv_md_41_cmd_135(library=self.service_library, param=add_address_param)
        assert eval(result["pBody"]) == {'code': 0}
        # 前线常用地址列表参数
        address_list_param = self.service_app.auv_param_md_41_cmd_82(a=front_id, b=2, c=1, e=1)
        # 前线常用地址列表
        address_list_info = self.service_app.auv_md_41_cmd_82(library=self.service_library, param=address_list_param)
        address_list = eval(address_list_info["pBody"])["a"]
        count = 0
        address_id = ""
        for address_info in address_list:
            if address_info["a"] == unloading_address and address_info["b"] == unloading_detailed_address:
                count += 1
                address_id = address_info["e"]
                break
            else:
                continue
        assert count == 1
        # 删除刚添加的地址参数
        del_address_param = self.service_app.auv_param_md_41_cmd_134(a=address_id)
        del_result = self.service_app.auv_md_41_cmd_134(library=self.service_library, param=del_address_param)
        assert eval(del_result["pBody"]) == {'code': 0}
        # 前线常用地址列表查询刚添加的地址
        address_list_info = self.service_app.auv_md_41_cmd_82(library=self.service_library, param=address_list_param)
        address_list = eval(address_list_info["pBody"])["a"]
        count = 0
        for address_info in address_list:
            if address_info["a"] == unloading_address and address_info["b"] == unloading_detailed_address:
                count += 1
                break
            else:
                continue
        assert count == 0

    # 发布询价单
    def test_case003(self):
        # 当前客服id
        front_id = int(self.service_user_uid)
        # 需求车数
        need_car_num = random.randint(10, 100)
        # 货主装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货品名称
        product_name = random.choice(self.goods_name_list)["a"]
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
        # 查询小五列表参数
        query_dispatch_param = self.service_app.auv_param_md_41_cmd_83(a=2)
        dispatch_list_info = self.service_app.auv_md_41_cmd_83(library=self.service_library, param=query_dispatch_param)
        # 选择小五
        dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
        # 询价参数
        enquiry_param = self.service_app.auv_param_md_41_cmd_80(a=invoice_type, b=need_car_num, c=loading_s,
                                                                d=unloading_s,
                                                                e=product_name, f=billing_type, g=remark, h=[dispatch],
                                                                j=tonnage, k=front_id, l=2, m=payment_days,
                                                                n=loading_time)
        # 发布询价货单
        enquiry_result = self.service_app.auv_md_41_cmd_80(library=self.service_library, param=enquiry_param)
        assert eval(enquiry_result["pBody"]) == {'code': 0}
        # 查看询价列表参数
        enquiry_list_param = self.service_app.auv_param_md_41_cmd_96(f=1, h=front_id)
        # 查看询价列表
        enquiry_list_info = self.service_app.auv_md_41_cmd_96(library=self.service_library, param=enquiry_list_param)
        enquiry_list = eval(enquiry_list_info["pBody"])["a"]
        count = 0
        source_id = ""
        enquiry_id = ""
        for enquiry in enquiry_list:
            if enquiry["d"] == product_name and enquiry["f"] == billing_type and enquiry["g"] == loading_s and \
                    enquiry["h"] == unloading_s and enquiry["i"] == need_car_num and enquiry["l"] == invoice_type:
                source_id = enquiry["n"]
                enquiry_id = enquiry["c"]
                count += 1
                break
            else:
                continue
        assert count == 1
        # 查看询价单详情
        enquiry_info_param = self.service_app.auv_param_md_41_cmd_85(a=source_id, b=front_id)
        enquiry_info_result = self.service_app.auv_md_41_cmd_85(library=self.service_library, param=enquiry_info_param)
        enquiry_info = eval(enquiry_info_result["pBody"])
        assert enquiry_id == enquiry_info["d"]

    # 发布报车单
    def test_case004(self):
        # 当前客服id
        front_id = int(self.service_user_uid)
        # 需求车数
        need_car_num = random.randint(10, 100)
        # 货主装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货主卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 装货地三级联动
        loading = ran().create_area_name()
        # 装货地详细地址
        loading_info = "中山北路" + str(random.randint(100, 200)) + "号"
        # 卸货地三级联动
        unloading = ran().create_area_name()
        # 卸货地详细地址
        unloading_info = "华山南路" + str(random.randint(100, 200)) + "号"
        # 货品名称
        product_name = random.choice(self.goods_name_list)["a"]
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
        # 查询货主公司参数
        shipper_list_param = self.service_app.auv_param_md_41_cmd_97(b=front_id, c=1, d=10)
        shipper_list_info = self.service_app.auv_md_41_cmd_97(library=self.service_library, param=shipper_list_param)
        # 选择公司
        shipper_id = random.choice(eval(shipper_list_info["pBody"])["a"])["a"]
        company_name = random.choice(eval(shipper_list_info["pBody"])["a"])["c"]
        # 查询小五列表参数
        query_dispatch_param = self.service_app.auv_param_md_41_cmd_83(a=2)
        dispatch_list_info = self.service_app.auv_md_41_cmd_83(library=self.service_library, param=query_dispatch_param)
        # 选择小五
        dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
        # 报车参数
        enquiry_car_param = self.service_app.auv_param_md_41_cmd_81(a=invoice_type, b=shipper_id, c=loading_s,
                                                                    d=unloading_s,
                                                                    e=loading_time, f=product_name, g=loading,
                                                                    h=tonnage,
                                                                    i=need_car_num, j=loss, k=unloading, l=up_price,
                                                                    m=up_billing_type, n=down_pirce, o=un_billing_type,
                                                                    p=per_price,
                                                                    q=remark, r=[dispatch], t=loading_info,
                                                                    u=unloading_info,
                                                                    x=front_id, y=company_name, z=2, w=payment_days,
                                                                    ab=method_settlement)
        # 发布报车货单
        enquiry_car_result = self.service_app.auv_md_41_cmd_81(library=self.service_library, param=enquiry_car_param)
        assert eval(enquiry_car_result["pBody"])["code"] == 0
        # 查看货源列表参数
        goods_list_param = self.service_app.auv_param_md_40_cmd_1(d=1, ae=1)
        # 查看货源列表
        goods_list_info = self.service_app.auv_md_40_cmd_1(library=self.service_library, param=goods_list_param)
        goods_list = eval(goods_list_info["pBody"])["a"]
        count = 0
        source_id = ""
        for goods in goods_list:
            if goods["a"] == loading_s and goods["b"] == unloading_s and goods["d"] == need_car_num and \
                    goods["h"] == company_name and goods["o"] == product_name:
                count += 1
                source_id = goods["f"]
                break
            else:
                continue
        assert count == 1
        # 查看货单详情
        goods_info_param = self.app.auv_param_md_40_cmd_4(a=source_id)
        goods_info_result = self.app.auv_md_40_cmd_4(library=self.library, param=goods_info_param)
        goods_info = eval(goods_info_result["pBody"])
        assert loading == goods_info["a"] and unloading == goods_info["b"] and product_name == goods_info["o"]

    # 常用货品名称
    def test_case005(self):
        # 当前客服id
        front_id = int(self.service_user_uid)
        # 需求车数
        need_car_num = random.randint(10, 100)
        # 货主装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货品名称
        product_name = random.choice(self.goods_name_list)["a"]
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
        # 查询小五列表参数
        query_dispatch_param = self.service_app.auv_param_md_41_cmd_83(a=2)
        dispatch_list_info = self.service_app.auv_md_41_cmd_83(library=self.service_library, param=query_dispatch_param)
        # 选择小五
        dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
        # 询价参数
        enquiry_param = self.service_app.auv_param_md_41_cmd_80(a=invoice_type, b=need_car_num, c=loading_s,
                                                                d=unloading_s,
                                                                e=product_name, f=billing_type, g=remark, h=[dispatch],
                                                                j=tonnage, k=front_id, l=2, m=payment_days,
                                                                n=loading_time)
        # 发布询价货单
        enquiry_result = self.service_app.auv_md_41_cmd_80(library=self.service_library, param=enquiry_param)
        assert eval(enquiry_result["pBody"]) == {'code': 0}
        # 查找常用货品名称列表
        goods_name_list_param = self.service_app.auv_param_md_41_cmd_114(a=front_id)
        goods_name_list_info = self.service_app.auv_md_41_cmd_114(library=self.service_library,
                                                                  param=goods_name_list_param)
        goods_name_list = eval(goods_name_list_info["pBody"])["a"]
        count = 0
        for goods_name in goods_name_list:
            if product_name == goods_name["a"]:
                count += 1
                break
            else:
                continue
        assert count == 1

    # 给询价单报价并确认询价立即报车
    def test_case006(self):
        # 当前客服id
        front_id = int(self.service_user_uid)
        # 需求车数
        need_car_num = random.randint(10, 100)
        # 货主装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货品名称
        product_name = random.choice(self.goods_name_list)["a"]
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
        # 查询小五列表参数
        query_dispatch_param = self.service_app.auv_param_md_41_cmd_83(a=2)
        dispatch_list_info = self.service_app.auv_md_41_cmd_83(library=self.service_library, param=query_dispatch_param)
        # 选择小五
        dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
        # 询价参数
        enquiry_param = self.service_app.auv_param_md_41_cmd_80(a=invoice_type, b=need_car_num, c=loading_s,
                                                                d=unloading_s,
                                                                e=product_name, f=billing_type, g=remark, h=[dispatch],
                                                                j=tonnage, k=front_id, l=2, m=payment_days,
                                                                n=loading_time)
        # 发布询价货单
        enquiry_result = self.service_app.auv_md_41_cmd_80(library=self.service_library, param=enquiry_param)
        assert eval(enquiry_result["pBody"]) == {'code': 0}
        # 查看询价列表参数
        enquiry_list_param = self.service_app.auv_param_md_41_cmd_96(f=1, h=front_id)
        # 查看询价列表
        enquiry_list_info = self.service_app.auv_md_41_cmd_96(library=self.service_library, param=enquiry_list_param)
        pagesize = eval(enquiry_list_info["pBody"])["pageSize"]
        count = 0
        source_id = ""
        enquiry_id = ""
        for n in range(1, pagesize + 1):
            # 查看询价列表参数
            enquiry_list_param = self.service_app.auv_param_md_41_cmd_96(f=n, h=front_id)
            # 查看询价列表
            enquiry_list_info = self.service_app.auv_md_41_cmd_96(library=self.service_library,
                                                                  param=enquiry_list_param)
            enquiry_list = eval(enquiry_list_info["pBody"])["a"]
            for enquiry in enquiry_list:
                if enquiry["d"] == product_name and enquiry["f"] == billing_type and enquiry["g"] == loading_s and \
                        enquiry["h"] == unloading_s and enquiry["i"] == need_car_num and enquiry["l"] == invoice_type:
                    source_id = enquiry["n"]
                    enquiry_id = enquiry["c"]
                    count += 1
                    break
                else:
                    continue
            if count == 1:
                break
            else:
                continue
        assert count == 1

        # 查看询价单详情
        enquiry_info_param = self.service_app.auv_param_md_41_cmd_85(a=source_id, b=front_id)
        enquiry_info_result = self.service_app.auv_md_41_cmd_85(library=self.service_library, param=enquiry_info_param)
        enquiry_info = eval(enquiry_info_result["pBody"])
        assert enquiry_id == enquiry_info["d"]

        # 车队app 获取询价列表
        source_list_param = self.app.auv_param_md_40_cmd_16(b=0)
        source_list_info = self.app.auv_md_40_cmd_16(library=self.library, param=source_list_param)
        source_list = eval(source_list_info["pBody"])["b"]
        count = 0
        for source in source_list:
            if source["a"] == source_id:
                count += 1
                break
            else:
                continue
        assert count == 1
        # 车队报价
        reprot_price = random.randint(80, 200) * 100
        up_car_num = random.randint(1, need_car_num)
        goods_report_param = self.app.auv_param_md_40_cmd_33(a=source_id, b=reprot_price, c=up_car_num,
                                                             d=self.enterprise)
        # 发起报价
        self.app.auv_md_40_cmd_33(library=self.library, param=goods_report_param)
        report_id = ""
        # 客服端查询报价列表
        report_price_list_param = self.service_app.auv_param_md_41_cmd_84(a=source_id)
        report_price_list_info = self.service_app.auv_md_41_cmd_84(library=self.service_library,
                                                                   param=report_price_list_param)
        report_price_list = eval(report_price_list_info["pBody"])["a"]
        count = 0
        for report in report_price_list:
            if report["c"] == reprot_price and report["d"] == up_car_num and report["f"] == self.enterprise:
                report_id = report["a"]
                count += 1
            else:
                continue
        assert count == 1
        # 货品单价
        per_price = random.randint(1000, 2000) * 100
        # 装货地三级联动
        loading = ran().create_area_name()
        # 装货地详细地址
        loading_info = "中山北路" + str(random.randint(100, 200)) + "号"
        # 卸货地三级联动
        unloading = ran().create_area_name()
        # 卸货地详细地址
        unloading_info = "华山南路" + str(random.randint(100, 200)) + "号"
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
        # 账期
        payment_days = random.choice(["周结", "月结", "双月结", "见票结算", "见单结算"])
        # 结算方式
        method_settlement = random.choice([0, 1])
        # 备注
        remark = "auto test"
        # 查询货主公司参数
        shipper_list_param = self.service_app.auv_param_md_41_cmd_97(b=front_id, c=1, d=10)
        shipper_list_info = self.service_app.auv_md_41_cmd_97(library=self.service_library, param=shipper_list_param)
        # 选择公司
        shipper_id = random.choice(eval(shipper_list_info["pBody"])["a"])["a"]
        company_name = random.choice(eval(shipper_list_info["pBody"])["a"])["c"]
        # 查询小五列表参数
        query_dispatch_param = self.service_app.auv_param_md_41_cmd_83(a=2)
        dispatch_list_info = self.service_app.auv_md_41_cmd_83(library=self.service_library, param=query_dispatch_param)
        # 选择小五
        dispatch = random.choice(eval(dispatch_list_info["pBody"])["a"])
        # 立即报车参数
        enquiry_car_param = self.service_app.auv_param_md_41_cmd_86(a=source_id, b=invoice_type, c=method_settlement,
                                                                    d=un_billing_type, e=loading, f=unloading,
                                                                    g=per_price, i=loading_s, j=loading_info,
                                                                    k=unloading_s, l=unloading_info, m=loading_time,
                                                                    n=loss, o=tonnage, p=up_price, q=up_billing_type,
                                                                    r=down_pirce, v=remark, w=self.enterprise,
                                                                    x=report_id, z=reprot_price, ab=shipper_id,
                                                                    ac=need_car_num, ae=payment_days, ah=company_name,
                                                                    aj=[dispatch])
        # 发布报车货单
        enquiry_car_result = self.service_app.auv_md_41_cmd_86(library=self.service_library, param=enquiry_car_param)
        assert eval(enquiry_car_result["pBody"])["code"] == 0
