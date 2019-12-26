# coding:utf-8
from src.pages import shipper
from src.pages import dispatch_new as dispatch
from src.pages import service_new as service
from src.pages import auv_app_new
from src.pages import finance
from src.pages import contract
from src.pages import auv_service
from ctypes import *
import random
from src.common import config
from src.common.random_param import Random_param as ran
import time

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.shipper = shipper.Shipper()
        self.service = service.Service()
        self.dispatch = dispatch.Dispatch()
        self.contract = contract.Contract()
        self.finance = finance.Finance()
        self.shipper_token = self.shipper.shipper_login(mobile=config.get_account("shipper")["username"],
                                                        password=config.get_account("shipper")["password"])
        self.service_token = self.service.service_login(username=config.get_account("service")["username"],
                                                        password=config.get_account("service")["password"])
        self.dispatch_token = self.dispatch.dispatch_login(username=config.get_account("dispatch")["username"],
                                                           password=config.get_account("dispatch")["password"])
        self.contract_token = self.contract.contract_md_40_cmd_1(username=config.get_account("contract")["username"],
                                                                 password=config.get_account("contract")["password"])
        self.finance_token = self.finance.finance_login(username=config.get_account("finance")["username"],
                                                        password=config.get_account("finance")["password"])
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

    # 询价报价报车流程
    def test_case001(self):
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
        for n in range(pagesize, 0, -1):
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
        count = 0
        last_time = 0
        # app货源大厅找到该货单
        for n in range(10):
            # 货单列表参数
            manifest_list_param = self.app.auv_param_md_40_cmd_16(b=last_time)
            # 获取货单列表
            manifest_list_info = self.app.auv_md_40_cmd_16(library=self.library, param=manifest_list_param)
            manifest_list = eval(manifest_list_info["pBody"])["b"]
            for manifest in manifest_list:
                if source_id != manifest["a"]:
                    last_time = manifest["i"]
                    continue
                else:
                    count += 1
                    break
            if count == 1:
                break
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
                                                                    d=un_billing_type, e=loading_s, f=unloading_s,
                                                                    g=per_price, i=loading, j=loading_info,
                                                                    k=unloading, l=unloading_info, m=loading_time,
                                                                    n=loss, o=tonnage, p=up_price, q=up_billing_type,
                                                                    r=down_pirce, v=remark, w=self.enterprise,
                                                                    x=report_id, z=reprot_price, ab=shipper_id,
                                                                    ac=need_car_num, ae=payment_days, ah=company_name,
                                                                    aj=[dispatch])
        # 立即报车
        enquiry_car_result = self.service_app.auv_md_41_cmd_86(library=self.service_library, param=enquiry_car_param)
        source_num = eval(enquiry_car_result["pBody"])["a"]
        assert eval(enquiry_car_result["pBody"])["code"] == 0

        # app 添加车辆
        car_info_param = ran().create_app_car_info(fleet_id=self.enterprise)
        car_number = eval(car_info_param)["a"]
        addcar_info = self.app.auv_md_40_cmd_161(library=self.library, param=car_info_param)
        addcar_result = eval(addcar_info["pBody"])
        assert addcar_result == {"a": 0}
        # app 车辆列表查看该车
        app_carinfo_list_param = self.app.auv_param_md_40_cmd_164(a=0, b=self.enterprise)
        app_carinfo_list_info = self.app.auv_md_40_cmd_164(library=self.library, param=app_carinfo_list_param)
        app_carinfo_list = eval(app_carinfo_list_info["pBody"])["s"]
        count = 0
        car_id = ""
        for carinfo in app_carinfo_list:
            if car_number == carinfo["a"]:
                count = count + 1
                car_id = carinfo["d"]
                break
            else:
                continue
        assert count == 1
        # app 添加挂车
        gua_car_info_param = ran().create_app_gua_car_info(fleet_id=self.enterprise)
        gua_car_number = eval(gua_car_info_param)["a"]
        add_gua_car_info = self.app.auv_md_40_cmd_165(library=self.library, param=gua_car_info_param)
        add_gua_car_result = eval(add_gua_car_info["pBody"])
        assert add_gua_car_result == {"a": 0}
        # app 挂车列表查看该挂车
        app_gua_carinfo_list_info_param = self.app.auv_param_md_40_cmd_169(a=self.enterprise, b=0)
        app_gua_carinfo_list_info = self.app.auv_md_40_cmd_169(library=self.library,
                                                               param=app_gua_carinfo_list_info_param)
        app_gua_carinfo_list = eval(app_gua_carinfo_list_info["pBody"])["s"]
        count = 0
        gua_car_id = ""
        for gua_carinfo in app_gua_carinfo_list:
            if gua_car_number == gua_carinfo["a"]:
                count = count + 1
                gua_car_id = gua_carinfo["d"]
                break
            else:
                continue
        assert count == 1
        # app 添加司机
        driver_param = ran().create_app_driver_info(fleet_id=self.enterprise)
        driver_name = eval(driver_param)["a"]
        driver_phone = eval(driver_param)["c"]
        app_add_driver_info = self.app.auv_md_40_cmd_170(library=self.library, param=driver_param)
        app_add_driver_result = eval(app_add_driver_info["pBody"])
        assert app_add_driver_result == {"a": 0}
        # app 司机列表查看该司机
        app_driverinfo_list_param = self.app.auv_param_md_40_cmd_174(a=self.enterprise, b=0)
        app_driverinfo_list_info = self.app.auv_md_40_cmd_174(library=self.library, param=app_driverinfo_list_param)
        app_driverinfo_list = eval(app_driverinfo_list_info["pBody"])["s"]
        count = 0
        driver_uid = ""
        driver_id = ""
        for driverinfo in app_driverinfo_list:
            if driver_name == driverinfo["a"] and driver_phone == driverinfo["b"]:
                count = count + 1
                driver_uid = driverinfo["c"]
                driver_id = driverinfo["g"]
                break
            else:
                continue
        assert count == 1
        # app 添加押运员
        driver_ya_param = ran().create_app_driver_ya_info(fleet_id=self.enterprise)
        driver_ya_name = eval(driver_ya_param)["a"]
        driver_ya_phone = eval(driver_ya_param)["b"]
        app_add_driver_ya_info = self.app.auv_md_40_cmd_176(library=self.library, param=driver_ya_param)
        app_add_driver_ya_result = eval(app_add_driver_ya_info["pBody"])
        assert app_add_driver_ya_result == {"a": 0}
        # app 押运员列表查看该押运员
        app_driverinfo_list_ya_param = self.app.auv_param_md_40_cmd_184(a=self.enterprise, b=0)
        app_driverinfo_list_ya_info = self.app.auv_md_40_cmd_184(library=self.library,
                                                                 param=app_driverinfo_list_ya_param)
        app_driverinfo_ya_list = eval(app_driverinfo_list_ya_info["pBody"])["s"]
        count = 0
        driver_ya_uid = ""
        driver_ya_id = ""
        for driverinfo_ya in app_driverinfo_ya_list:
            if driver_ya_name == driverinfo_ya["b"] and driver_ya_phone == driverinfo_ya["c"]:
                count = count + 1
                driver_ya_uid = driverinfo_ya["a"]
                driver_ya_id = driverinfo_ya["g"]
                break
            else:
                continue
        assert count == 1
        # app 添加运力
        app_add_capacity_param = self.app.auv_param_md_40_cmd_180(a=car_id, b=gua_car_id, c=driver_id,
                                                                  d=driver_ya_id, e=self.enterprise, f=driver_uid,
                                                                  g=driver_ya_uid)
        app_add_capacity_info = self.app.auv_md_40_cmd_180(library=self.library, param=app_add_capacity_param)
        app_add_capacity_result = eval(app_add_capacity_info["pBody"])
        assert app_add_capacity_result == {"a": 0}
        # app 运力列表查看该运力
        app_capacitylist_param = self.app.auv_param_md_40_cmd_181(a=self.enterprise, b=0)
        app_capacitylist_info = self.app.auv_md_40_cmd_181(library=self.library, param=app_capacitylist_param)
        app_capacitylist = eval(app_capacitylist_info["pBody"])["s"]
        count = 0
        for capacity in app_capacitylist:
            if driver_id == capacity["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        driver = {"d": car_id, "e": driver_id}
        use_driver = (driver,)
        # 获取我的货源列表
        my_source_param = self.app.auv_param_md_40_cmd_34(a=self.enterprise, b=0)
        my_source_list_info = self.app.auv_md_40_cmd_34(library=self.library, param=my_source_param)
        my_source_list = eval(my_source_list_info["pBody"])["b"]
        count = 0
        for my_source in my_source_list:
            if source_id == my_source["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # 报车参数
        car_report_param = self.app.auv_param_md_40_cmd_69(a=source_id, b=self.enterprise, c=use_driver)
        # 发起报车
        car_report_info = self.app.auv_md_40_cmd_69(library=self.library, param=car_report_param)
        car_report_result = eval(car_report_info["pBody"])
        assert car_report_result == {"a": 0}

        # 客服查询待确认车辆列表
        uncheck_carlist_param = self.service_app.auv_param_md_41_cmd_117(a=source_id, b=1, c=1, e=1)
        uncheck_carlist_info = self.service_app.auv_md_41_cmd_117(library=self.service_library,
                                                                  param=uncheck_carlist_param)
        uncheck_carlist = eval(uncheck_carlist_info["pBody"])["a"]
        count = 0
        waybillcar_id = ""
        for uncheck_car in uncheck_carlist:
            if uncheck_car["m"] == car_number:
                count += 1
                waybillcar_id = uncheck_car["n"]
            else:
                continue
        assert count == 1
        # 客服确认车辆
        confirm_car_param = self.service_app.auv_param_md_40_cmd_10(a=waybillcar_id, b=1)
        uncheck_carlist_info = self.service_app.auv_md_40_cmd_10(library=self.service_library, param=confirm_car_param)
        # assert eval(uncheck_carlist_info["pBody"]) == {'code': 0}

        # 车队查看进行中的运单
        transport_list_param = self.app.auv_param_md_40_cmd_25(a=self.enterprise, b=0, c=1)
        transport_list_info = self.app.auv_md_40_cmd_25(library=self.library, param=transport_list_param)
        transport_list = eval(transport_list_info["pBody"])["b"]
        count = 0
        transport_id = ""
        for transport in transport_list:
            if transport["m"] == source_id:
                count = count + 1
                transport_id = transport["a"]
                break
            else:
                continue
        assert count == 1
        # 运单详情中查看报车列表
        transport_car_list_param = self.app.auv_param_md_40_cmd_17(e=transport_id, b=0)
        transport_car_list_info = self.app.auv_md_40_cmd_17(library=self.library, param=transport_car_list_param)
        transport_car_list = eval(transport_car_list_info["pBody"])["b"]
        count = 0
        for transport_car in transport_car_list:
            if transport_car["a"] == waybillcar_id:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # 上传装卸货磅单
        loading_param = self.app.auv_param_md_40_cmd_26(a=waybillcar_id, b=random.choice(config.get_picture()),
                                                        c=random.randint(1, 100) * 1000,
                                                        d=random.choice(config.get_picture()),
                                                        e=random.randint(1, 100) * 1000)
        self.app.auv_md_40_cmd_26(library=self.library, param=loading_param)
        # 查看装卸货磅单
        loading_info_param = self.app.auv_param_md_40_cmd_27(a=waybillcar_id)
        loading_unload_info = self.app.auv_md_40_cmd_27(library=self.library, param=loading_info_param)
        loading_info = eval(loading_unload_info["pBody"])
        assert loading_info["b"] == eval(loading_param)["b"]
        # 生成线下合同
        contract_param = ran().create_apply_uncontract_param(a=self.enterprise, d=self.enterprise, i=transport_id,
                                                             s=self.enterprise_name,
                                                             u=self.user_uid, v=self.user_name,
                                                             z=int(config.get_account("app")["username"]))
        self.app.auv_md_40_cmd_118(library=self.library, param=contract_param)
        # app查询合同列表
        contract_list_param = self.app.auv_param_md_40_cmd_117(a=self.enterprise, b=0, c=2)
        contract_list_info = self.app.auv_md_40_cmd_117(library=self.library, param=contract_list_param)
        contract_list = eval(contract_list_info["pBody"])["a"]
        count = 0
        contract_id = ""
        for contracts in contract_list:
            if contracts["i"] == transport_id:
                contract_id = contracts["b"]
            else:
                continue
        # 电子合同平台查看线下待审核列表
        key_id = ""
        contract_uncheck_list = self.contract.contract_md_48_cmd_13(cookie=self.contract_token, a=1, c=0, d=2,
                                                                    b=self.enterprise_name)
        print(contract_uncheck_list)
        for uncheck_contract in contract_uncheck_list["a"]:
            if uncheck_contract["i"] == contract_id:
                key_id = uncheck_contract["e"]
                break
            else:
                continue
        # 电子合同平台查询线下合同详情
        contract_uncheck_info = self.contract.contract_md_48_cmd_18(cookie=self.contract_token, a=key_id)

        # 电子合同平台审核通过线下合同
        self.contract.contract_md_48_cmd_12(cookie=self.contract_token, a=self.enterprise_name,
                                            b=contract_uncheck_info["f"], e=self.enterprise, f=key_id, g=1, h=remark)

        # 客服上传货主合同
        result = self.service.service_md_40_cmd_118(cookie=self.service_token, a=shipper_id, b=4, d=shipper_id,
                                                    i=source_num, j=3, m=1, n=1, o=2, w=2, s=company_name,
                                                    k=random.choice(config.get_picture()))
        assert result["code"] == 0
        # 客服确认货主合同
        service_source_info = self.service.service_md_40_cmd_45(cookie=self.service_token, a=source_id)
        assert service_source_info["u"] == -1
        # 货主查看线下合同列表
        shipper_contract_list = self.shipper.shipper_getContractList(cookie=self.shipper_token, a=shipper_id, b=0, c=2,
                                                                     e=2, f=1)
        count = 0
        shipper_contract_id = ""
        for shipper_contract in shipper_contract_list["a"]:
            if shipper_contract["i"] == source_num:
                shipper_contract_id = shipper_contract["b"]
                count += 1
                break
            else:
                continue
        assert count == 1
        # 电子合同平台查看线下待审核列表
        key_id = ""
        contract_uncheck_list = self.contract.contract_md_48_cmd_13(cookie=self.contract_token, a=1, c=0, d=2,
                                                                    b=company_name)
        print(contract_uncheck_list)
        for uncheck_contract in contract_uncheck_list["a"]:
            if uncheck_contract["i"] == shipper_contract_id:
                key_id = uncheck_contract["e"]
                break
            else:
                continue
        # 电子合同平台查询线下合同详情
        contract_uncheck_info = self.contract.contract_md_48_cmd_18(cookie=self.contract_token, a=key_id)

        # 电子合同平台审核通过线下合同
        self.contract.contract_md_48_cmd_12(cookie=self.contract_token, a="",
                                            b=contract_uncheck_info["f"], e="", f=key_id, g=1,
                                            h=remark)
        # 小五确认运单完成
        result = self.dispatch.dispatch_md_40_cmd_61(cookie=self.dispatch_token, a=transport_id, b=2)
        assert result == {'code': 0}
        # 客服进行货单完成操作
        result = self.service.service_md_40_cmd_60(cookie=self.service_token, a=source_id, b=20)
        assert result == {'code': 0}
        # 添加一个收款账户
        addBank_param = ran().create_addBank_param(enterprise=self.enterprise)
        addBank_result = self.app.auv_md_40_cmd_56(library=self.library, param=addBank_param)
        account_id = eval(addBank_result["pBody"])['a']
        # 获取银行账户列表
        getBankList_params = self.app.auv_param_md_40_cmd_57(a=self.enterprise)
        bankList_info = self.app.auv_md_40_cmd_57(library=self.library, param=getBankList_params)
        bankList = eval(bankList_info["pBody"])['a']
        count = 0
        for account in bankList:
            if account["a"] == account_id:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # APP发起对账
        applyRecon_params = self.app.auv_param_md_40_cmd_42(a=transport_id, b=account_id)
        self.app.auv_md_40_cmd_42(library=self.library, param=applyRecon_params)
        # 客服获取待审核列表，拿到其对账单id
        waitServiceCheckList = self.service.service_md_40_cmd_120(cookie=self.service_token, h=1, g=1)
        count = 0
        service_accountOderId = ""
        for waitServiceCheck in waitServiceCheckList["data"]:
            if waitServiceCheck['c'] == transport_id:
                count += 1
                service_accountOderId = waitServiceCheck['a']
            else:
                continue
        assert count == 1
        print('客服待审核列表中存在对账单A，状态为待客服审核')

        # 客服审核数据A,审核通过
        result = self.service.service_md_40_cmd_123(cookie=self.service_token, a=service_accountOderId, b=0)
        assert result == {'code': 0}

        # 审核成功后，客服查看已审核列表，确认是否存在对账单A
        serviceCheckDoneList = self.service.service_md_40_cmd_120(cookie=self.service_token, g=1, h=1, f=1)
        count = 0
        for serviceCheckDone_A in serviceCheckDoneList["data"]:
            if serviceCheckDone_A['a'] == service_accountOderId and serviceCheckDone_A['m'] == 3:
                count += 1
            else:
                continue
        assert count == 1
        print('客服已审核列表中存在对账单A，状态为待复核员审核')

        # 获取财务登录信息
        finance_userinfo = self.finance.finance_UserInfo(cookie=self.finance_token)
        finance_usename = finance_userinfo["username"]

        # 财务系统复核员查看待审核列表，确认是否存在对账单A
        waitCaiwuCheckList = self.finance.finance_CheckList(cookie=self.finance_token, g=3, h=1)
        count = 0
        for waitCaiwuCheck_A in waitCaiwuCheckList["data"]:
            if waitCaiwuCheck_A['a'] == service_accountOderId and waitCaiwuCheck_A['m'] == 3:
                count += 1
            else:
                continue
        assert count == 1
        print("复核员待审核列表中存在对账单A，状态为“待复核员审核”")
        # 财务系统复核员审核
        result = self.finance.finance_Check(cookie=self.finance_token, a=service_accountOderId)
        assert result == {'code': 0}

        # 财务系统复核员查看已审核列表
        caiwuCheckDoneList = self.finance.finance_CheckList(cookie=self.finance_token, g=3, h=1, f=1)
        count = 0
        for caiwuCheckDone_A in caiwuCheckDoneList["data"]:
            if caiwuCheckDone_A['a'] == service_accountOderId and caiwuCheckDone_A['m'] == 5:
                count += 1
            else:
                continue
        assert count == 1
        print("复核员已审核列表中存在对账单A，状态为“待财务审核”")

        # 财务系统财务查看待付款列表
        waitCaiwuPaymentList = self.finance.finance_CheckList(cookie=self.finance_token, g=5, h=1)
        count = 0
        for waitCaiwuPayment in waitCaiwuPaymentList["data"]:
            if waitCaiwuPayment['a'] == service_accountOderId and waitCaiwuPayment['m'] == 5:
                count += 1
            else:
                continue
        assert count == 1
        print("财务待付款列表中存在对账单A，状态为“待财务付款”")

        # 财务确认付款
        finance_Payment_params = self.finance.finance_PayMoney_param(a=service_accountOderId,
                                                                     b=random.choice(config.get_picture()),
                                                                     e=finance_usename)
        result = self.finance.finance_Paymoney(token=self.finance_token, param=finance_Payment_params)
        assert result == {'code': 0}

        # 财务系统财务查看已付款列表
        caiwuPaymentDoneList = self.finance.finance_CheckList(cookie=self.finance_token, g=5, h=1, f=1)
        count = 0
        for caiwuPaymentDone in caiwuPaymentDoneList["data"]:
            if caiwuPaymentDone['a'] == service_accountOderId and caiwuPaymentDone['m'] == 7:
                count += 1
            else:
                continue
        assert count == 1
        print("财务已付款列表中存在对账单A，状态为“已付款”")
        print("- - - 用例执行完毕！ - - -")

    # 报车单报车流程
    def test_case002(self):
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
        enquiry_car_param = self.service_app.auv_param_md_41_cmd_81(a=invoice_type, b=shipper_id, c=loading,
                                                                    d=unloading, e=loading_time, f=product_name,
                                                                    g=loading_s, h=tonnage, i=need_car_num, j=loss,
                                                                    k=unloading_s, l=up_price, m=up_billing_type,
                                                                    n=down_pirce, o=un_billing_type, p=per_price,
                                                                    q=remark, r=[dispatch], t=loading_info,
                                                                    u=unloading_info, x=front_id, y=company_name, z=2,
                                                                    w=payment_days, ab=method_settlement)
        # 发布报车货单
        enquiry_car_result = self.service_app.auv_md_41_cmd_81(library=self.service_library, param=enquiry_car_param)
        source_num = eval(enquiry_car_result["pBody"])["a"]
        assert eval(enquiry_car_result["pBody"])["code"] == 0
        # 查看货源列表参数
        goods_list_param = self.service_app.auv_param_md_40_cmd_1(d=1, ae=1)
        # 查看货源列表
        goods_list_info = self.service_app.auv_md_40_cmd_1(library=self.service_library, param=goods_list_param)
        pagesize = eval(goods_list_info["pBody"])["pageSize"]
        count = 0
        source_id = ""
        for n in range(pagesize, 0, -1):
            # 查看货源列表参数
            goods_list_param = self.service_app.auv_param_md_40_cmd_1(d=1, ae=n)
            goods_list_info = self.service_app.auv_md_40_cmd_1(library=self.service_library, param=goods_list_param)
            goods_list = eval(goods_list_info["pBody"])["a"]
            for goods in goods_list:
                if goods["a"] == loading and goods["b"] == unloading and goods["d"] == need_car_num and \
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
        assert loading_s == goods_info["a"] and unloading_s == goods_info["b"] and product_name == goods_info["o"]

        # app 添加车辆
        car_info_param = ran().create_app_car_info(fleet_id=self.enterprise)
        car_number = eval(car_info_param)["a"]
        addcar_info = self.app.auv_md_40_cmd_161(library=self.library, param=car_info_param)
        addcar_result = eval(addcar_info["pBody"])
        assert addcar_result == {"a": 0}
        # app 车辆列表查看该车
        app_carinfo_list_param = self.app.auv_param_md_40_cmd_164(a=0, b=self.enterprise)
        app_carinfo_list_info = self.app.auv_md_40_cmd_164(library=self.library, param=app_carinfo_list_param)
        app_carinfo_list = eval(app_carinfo_list_info["pBody"])["s"]
        count = 0
        car_id = ""
        for carinfo in app_carinfo_list:
            if car_number == carinfo["a"]:
                count = count + 1
                car_id = carinfo["d"]
                break
            else:
                continue
        assert count == 1
        # app 添加挂车
        gua_car_info_param = ran().create_app_gua_car_info(fleet_id=self.enterprise)
        gua_car_number = eval(gua_car_info_param)["a"]
        add_gua_car_info = self.app.auv_md_40_cmd_165(library=self.library, param=gua_car_info_param)
        add_gua_car_result = eval(add_gua_car_info["pBody"])
        assert add_gua_car_result == {"a": 0}
        # app 挂车列表查看该挂车
        app_gua_carinfo_list_info_param = self.app.auv_param_md_40_cmd_169(a=self.enterprise, b=0)
        app_gua_carinfo_list_info = self.app.auv_md_40_cmd_169(library=self.library,
                                                               param=app_gua_carinfo_list_info_param)
        app_gua_carinfo_list = eval(app_gua_carinfo_list_info["pBody"])["s"]
        count = 0
        gua_car_id = ""
        for gua_carinfo in app_gua_carinfo_list:
            if gua_car_number == gua_carinfo["a"]:
                count = count + 1
                gua_car_id = gua_carinfo["d"]
                break
            else:
                continue
        assert count == 1
        # app 添加司机
        driver_param = ran().create_app_driver_info(fleet_id=self.enterprise)
        driver_name = eval(driver_param)["a"]
        driver_phone = eval(driver_param)["c"]
        app_add_driver_info = self.app.auv_md_40_cmd_170(library=self.library, param=driver_param)
        app_add_driver_result = eval(app_add_driver_info["pBody"])
        assert app_add_driver_result == {"a": 0}
        # app 司机列表查看该司机
        app_driverinfo_list_param = self.app.auv_param_md_40_cmd_174(a=self.enterprise, b=0)
        app_driverinfo_list_info = self.app.auv_md_40_cmd_174(library=self.library, param=app_driverinfo_list_param)
        app_driverinfo_list = eval(app_driverinfo_list_info["pBody"])["s"]
        count = 0
        driver_uid = ""
        driver_id = ""
        for driverinfo in app_driverinfo_list:
            if driver_name == driverinfo["a"] and driver_phone == driverinfo["b"]:
                count = count + 1
                driver_uid = driverinfo["c"]
                driver_id = driverinfo["g"]
                break
            else:
                continue
        assert count == 1
        # app 添加押运员
        driver_ya_param = ran().create_app_driver_ya_info(fleet_id=self.enterprise)
        driver_ya_name = eval(driver_ya_param)["a"]
        driver_ya_phone = eval(driver_ya_param)["b"]
        app_add_driver_ya_info = self.app.auv_md_40_cmd_176(library=self.library, param=driver_ya_param)
        app_add_driver_ya_result = eval(app_add_driver_ya_info["pBody"])
        assert app_add_driver_ya_result == {"a": 0}
        # app 押运员列表查看该押运员
        app_driverinfo_list_ya_param = self.app.auv_param_md_40_cmd_184(a=self.enterprise, b=0)
        app_driverinfo_list_ya_info = self.app.auv_md_40_cmd_184(library=self.library,
                                                                 param=app_driverinfo_list_ya_param)
        app_driverinfo_ya_list = eval(app_driverinfo_list_ya_info["pBody"])["s"]
        count = 0
        driver_ya_uid = ""
        driver_ya_id = ""
        for driverinfo_ya in app_driverinfo_ya_list:
            if driver_ya_name == driverinfo_ya["b"] and driver_ya_phone == driverinfo_ya["c"]:
                count = count + 1
                driver_ya_uid = driverinfo_ya["a"]
                driver_ya_id = driverinfo_ya["g"]
                break
            else:
                continue
        assert count == 1
        # app 添加运力
        app_add_capacity_param = self.app.auv_param_md_40_cmd_180(a=car_id, b=gua_car_id, c=driver_id,
                                                                  d=driver_ya_id, e=self.enterprise, f=driver_uid,
                                                                  g=driver_ya_uid)
        app_add_capacity_info = self.app.auv_md_40_cmd_180(library=self.library, param=app_add_capacity_param)
        app_add_capacity_result = eval(app_add_capacity_info["pBody"])
        assert app_add_capacity_result == {"a": 0}
        # app 运力列表查看该运力
        app_capacitylist_param = self.app.auv_param_md_40_cmd_181(a=self.enterprise, b=0)
        app_capacitylist_info = self.app.auv_md_40_cmd_181(library=self.library, param=app_capacitylist_param)
        app_capacitylist = eval(app_capacitylist_info["pBody"])["s"]
        count = 0
        for capacity in app_capacitylist:
            if driver_id == capacity["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        driver = {"d": car_id, "e": driver_id}
        use_driver = (driver,)
        # app货源大厅找到该货单
        count = 0
        last_time = 0
        for n in range(10):
            # 货单列表参数
            manifest_list_param = self.app.auv_param_md_40_cmd_16(b=last_time)
            # 获取货单列表
            manifest_list_info = self.app.auv_md_40_cmd_16(library=self.library, param=manifest_list_param)
            manifest_list = eval(manifest_list_info["pBody"])["b"]
            for manifest in manifest_list:
                if source_id != manifest["a"]:
                    last_time = manifest["i"]
                    continue
                else:
                    count = count + 1
                    break
            if count == 1:
                break
        assert count == 1
        # 报车参数
        car_report_param = self.app.auv_param_md_40_cmd_69(a=source_id, b=self.enterprise, c=use_driver)
        # 发起报车
        car_report_info = self.app.auv_md_40_cmd_69(library=self.library, param=car_report_param)
        car_report_result = eval(car_report_info["pBody"])
        assert car_report_result == {"a": 0}
        # 获取我的货源列表
        my_source_param = self.app.auv_param_md_40_cmd_34(a=self.enterprise, b=0)
        my_source_list_info = self.app.auv_md_40_cmd_34(library=self.library, param=my_source_param)
        my_source_list = eval(my_source_list_info["pBody"])["b"]
        count = 0
        for my_source in my_source_list:
            if source_id == my_source["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1

        # 客服查询待确认车辆列表
        uncheck_carlist_param = self.service_app.auv_param_md_41_cmd_117(a=source_id, b=1, c=1, e=1)
        uncheck_carlist_info = self.service_app.auv_md_41_cmd_117(library=self.service_library,
                                                                  param=uncheck_carlist_param)
        uncheck_carlist = eval(uncheck_carlist_info["pBody"])["a"]
        count = 0
        waybillcar_id = ""
        for uncheck_car in uncheck_carlist:
            if uncheck_car["m"] == car_number:
                count += 1
                waybillcar_id = uncheck_car["n"]
            else:
                continue
        assert count == 1
        # 客服确认车辆
        confirm_car_param = self.service_app.auv_param_md_40_cmd_10(a=waybillcar_id, b=1)
        uncheck_carlist_info = self.service_app.auv_md_40_cmd_10(library=self.service_library, param=confirm_car_param)
        # assert eval(uncheck_carlist_info["pBody"]) == {'code': 0}

        # 车队查看进行中的运单
        transport_list_param = self.app.auv_param_md_40_cmd_25(a=self.enterprise, b=0, c=1)
        transport_list_info = self.app.auv_md_40_cmd_25(library=self.library, param=transport_list_param)
        transport_list = eval(transport_list_info["pBody"])["b"]
        count = 0
        transport_id = ""
        for transport in transport_list:
            if transport["m"] == source_id:
                count = count + 1
                transport_id = transport["a"]
                break
            else:
                continue
        assert count == 1
        # 运单详情中查看报车列表
        transport_car_list_param = self.app.auv_param_md_40_cmd_17(e=transport_id, b=0)
        transport_car_list_info = self.app.auv_md_40_cmd_17(library=self.library, param=transport_car_list_param)
        transport_car_list = eval(transport_car_list_info["pBody"])["b"]
        count = 0
        for transport_car in transport_car_list:
            if transport_car["a"] == waybillcar_id:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # 上传装卸货磅单
        loading_param = self.app.auv_param_md_40_cmd_26(a=waybillcar_id, b=random.choice(config.get_picture()),
                                                        c=random.randint(1, 100) * 1000,
                                                        d=random.choice(config.get_picture()),
                                                        e=random.randint(1, 100) * 1000)
        self.app.auv_md_40_cmd_26(library=self.library, param=loading_param)
        # 查看装卸货磅单
        loading_info_param = self.app.auv_param_md_40_cmd_27(a=waybillcar_id)
        loading_unload_info = self.app.auv_md_40_cmd_27(library=self.library, param=loading_info_param)
        loading_info = eval(loading_unload_info["pBody"])
        assert loading_info["b"] == eval(loading_param)["b"]
        # 生成线下合同
        contract_param = ran().create_apply_uncontract_param(a=self.enterprise, d=self.enterprise, i=transport_id,
                                                             s=self.enterprise_name,
                                                             u=self.user_uid, v=self.user_name,
                                                             z=int(config.get_account("app")["username"]))
        self.app.auv_md_40_cmd_118(library=self.library, param=contract_param)
        # app查询合同列表
        contract_list_param = self.app.auv_param_md_40_cmd_117(a=self.enterprise, b=0, c=2)
        contract_list_info = self.app.auv_md_40_cmd_117(library=self.library, param=contract_list_param)
        contract_list = eval(contract_list_info["pBody"])["a"]
        count = 0
        contract_id = ""
        for contracts in contract_list:
            if contracts["i"] == transport_id:
                contract_id = contracts["b"]
            else:
                continue
        # 电子合同平台查看线下待审核列表
        key_id = ""
        contract_uncheck_list = self.contract.contract_md_48_cmd_13(cookie=self.contract_token, a=1, c=0, d=2,
                                                                    b=self.enterprise_name)
        print(contract_uncheck_list)
        for uncheck_contract in contract_uncheck_list["a"]:
            if uncheck_contract["i"] == contract_id:
                key_id = uncheck_contract["e"]
                break
            else:
                continue
        # 电子合同平台查询线下合同详情
        contract_uncheck_info = self.contract.contract_md_48_cmd_18(cookie=self.contract_token, a=key_id)

        # 电子合同平台审核通过线下合同
        self.contract.contract_md_48_cmd_12(cookie=self.contract_token, a=self.enterprise_name,
                                            b=contract_uncheck_info["f"], e=self.enterprise, f=key_id, g=1, h=remark)

        # 客服上传货主合同
        result = self.service.service_md_40_cmd_118(cookie=self.service_token, a=shipper_id, b=4, d=shipper_id,
                                                    i=source_num, j=3, m=1, n=1, o=2, w=2, s=company_name,
                                                    k=random.choice(config.get_picture()))
        assert result["code"] == 0
        # 客服确认货主合同
        service_source_info = self.service.service_md_40_cmd_45(cookie=self.service_token, a=source_id)
        assert service_source_info["u"] == -1
        # 货主查看线下合同列表
        shipper_contract_list = self.shipper.shipper_getContractList(cookie=self.shipper_token, a=shipper_id, b=0, c=2,
                                                                     e=2, f=1)
        count = 0
        shipper_contract_id = ""
        for shipper_contract in shipper_contract_list["a"]:
            if shipper_contract["i"] == source_num:
                shipper_contract_id = shipper_contract["b"]
                break
            else:
                continue
        # 电子合同平台查看线下待审核列表
        key_id = ""
        contract_uncheck_list = self.contract.contract_md_48_cmd_13(cookie=self.contract_token, a=1, c=0, d=2,
                                                                    b=company_name)
        print(contract_uncheck_list)
        for uncheck_contract in contract_uncheck_list["a"]:
            if uncheck_contract["i"] == shipper_contract_id:
                key_id = uncheck_contract["e"]
                break
            else:
                continue
        # 电子合同平台查询线下合同详情
        contract_uncheck_info = self.contract.contract_md_48_cmd_18(cookie=self.contract_token, a=key_id)

        # 电子合同平台审核通过线下合同
        self.contract.contract_md_48_cmd_12(cookie=self.contract_token, a="",
                                            b=contract_uncheck_info["f"], e="", f=key_id, g=1,
                                            h=remark)
        # 小五确认运单完成
        result = self.dispatch.dispatch_md_40_cmd_61(cookie=self.dispatch_token, a=transport_id, b=2)
        assert result == {'code': 0}
        # 客服进行货单完成操作
        result = self.service.service_md_40_cmd_60(cookie=self.service_token, a=source_id, b=20)
        assert result == {'code': 0}
        # 添加一个收款账户
        addBank_param = ran().create_addBank_param(enterprise=self.enterprise)
        addBank_result = self.app.auv_md_40_cmd_56(library=self.library, param=addBank_param)
        account_id = eval(addBank_result["pBody"])['a']
        # 获取银行账户列表
        getBankList_params = self.app.auv_param_md_40_cmd_57(a=self.enterprise)
        bankList_info = self.app.auv_md_40_cmd_57(library=self.library, param=getBankList_params)
        bankList = eval(bankList_info["pBody"])['a']
        count = 0
        for account in bankList:
            if account["a"] == account_id:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # APP发起对账
        applyRecon_params = self.app.auv_param_md_40_cmd_42(a=transport_id, b=account_id)
        self.app.auv_md_40_cmd_42(library=self.library, param=applyRecon_params)
        # 客服获取待审核列表，拿到其对账单id
        waitServiceCheckList = self.service.service_md_40_cmd_120(cookie=self.service_token, h=1, g=1)
        count = 0
        service_accountOderId = ""
        for waitServiceCheck in waitServiceCheckList["data"]:
            if waitServiceCheck['c'] == transport_id:
                count += 1
                service_accountOderId = waitServiceCheck['a']
            else:
                continue
        assert count == 1
        print('客服待审核列表中存在对账单A，状态为待客服审核')

        # 客服审核数据A,审核通过
        result = self.service.service_md_40_cmd_123(cookie=self.service_token, a=service_accountOderId, b=0)
        assert result == {'code': 0}

        # 审核成功后，客服查看已审核列表，确认是否存在对账单A
        serviceCheckDoneList = self.service.service_md_40_cmd_120(cookie=self.service_token, g=1, h=1, f=1)
        count = 0
        for serviceCheckDone_A in serviceCheckDoneList["data"]:
            if serviceCheckDone_A['a'] == service_accountOderId and serviceCheckDone_A['m'] == 3:
                count += 1
            else:
                continue
        assert count == 1
        print('客服已审核列表中存在对账单A，状态为待复核员审核')

        # 获取财务登录信息
        finance_userinfo = self.finance.finance_UserInfo(cookie=self.finance_token)
        finance_usename = finance_userinfo["username"]

        # 财务系统复核员查看待审核列表，确认是否存在对账单A
        waitCaiwuCheckList = self.finance.finance_CheckList(cookie=self.finance_token, g=3, h=1)
        count = 0
        for waitCaiwuCheck_A in waitCaiwuCheckList["data"]:
            if waitCaiwuCheck_A['a'] == service_accountOderId and waitCaiwuCheck_A['m'] == 3:
                count += 1
            else:
                continue
        assert count == 1
        print("复核员待审核列表中存在对账单A，状态为“待复核员审核”")
        # 财务系统复核员审核
        result = self.finance.finance_Check(cookie=self.finance_token, a=service_accountOderId)
        assert result == {'code': 0}

        # 财务系统复核员查看已审核列表
        caiwuCheckDoneList = self.finance.finance_CheckList(cookie=self.finance_token, g=3, h=1, f=1)
        count = 0
        for caiwuCheckDone_A in caiwuCheckDoneList["data"]:
            if caiwuCheckDone_A['a'] == service_accountOderId and caiwuCheckDone_A['m'] == 5:
                count += 1
            else:
                continue
        assert count == 1
        print("复核员已审核列表中存在对账单A，状态为“待财务审核”")

        # 财务系统财务查看待付款列表
        waitCaiwuPaymentList = self.finance.finance_CheckList(cookie=self.finance_token, g=5, h=1)
        count = 0
        for waitCaiwuPayment in waitCaiwuPaymentList["data"]:
            if waitCaiwuPayment['a'] == service_accountOderId and waitCaiwuPayment['m'] == 5:
                count += 1
            else:
                continue
        assert count == 1
        print("财务待付款列表中存在对账单A，状态为“待财务付款”")

        # 财务确认付款
        finance_Payment_params = self.finance.finance_PayMoney_param(a=service_accountOderId,
                                                                     b=random.choice(config.get_picture()),
                                                                     e=finance_usename)
        result = self.finance.finance_Paymoney(token=self.finance_token, param=finance_Payment_params)
        assert result == {'code': 0}

        # 财务系统财务查看已付款列表
        caiwuPaymentDoneList = self.finance.finance_CheckList(cookie=self.finance_token, g=5, h=1, f=1)
        count = 0
        for caiwuPaymentDone in caiwuPaymentDoneList["data"]:
            if caiwuPaymentDone['a'] == service_accountOderId and caiwuPaymentDone['m'] == 7:
                count += 1
            else:
                continue
        assert count == 1
        print("财务已付款列表中存在对账单A，状态为“已付款”")
        print("- - - 用例执行完毕！ - - -")
