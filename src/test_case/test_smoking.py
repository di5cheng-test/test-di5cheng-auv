# coding:utf-8
from src.pages import shipper
from src.pages import dispatch
from src.pages import service
from src.pages import app
from src.pages import finance
from ctypes import *
import random
from src.common import config
from src.common.random_param import Random_param as ran

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.shipper = shipper.Shipper()
        self.service = service.Service()
        self.dispatch = dispatch.Dispatch()
        self.finance = finance.Finance()
        self.shipper_token = self.shipper.shipper_login(mobile=config.get_account("shipper")["username"],
                                                        password=config.get_account("shipper")["password"])
        self.service_token = self.service.service_login(username=config.get_account("service")["username"],
                                                        password=config.get_account("service")["password"])
        self.dispatch_token = self.dispatch.dispatch_login(username=config.get_account("dispatch")["username"],
                                                           password=config.get_account("dispatch")["password"])
        self.finance_token = self.finance.finance_login(username=config.get_account("finance")["username"],
                                                        password=config.get_account("finance")["password"])
        self.library = cdll.LoadLibrary(config.get_library())
        self.common = app.Common()
        self.common.initSDK(library=self.library, init_info=config.get_app_url())

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")

    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    # 用例1：货主端发布询价，
    #        货主端查询并确认发布成功
    #        客服端查询并确认货主的询价
    #        客服端发起报价
    #        客服端查询并确认报价成功
    #        货主端查询并确认客服已报价
    #        货主端确认客服的报价
    #        货主端查看并确认生成了货单
    #        客服端查看并确认生成了货单
    #        调度端查看并确认生成了货单

    def test_case001(self):
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

        # 客服查询待处理的列表
        service_inquire_list = self.service.service_getInquires(cookie=self.service_token, type_num=0, time_num=0)
        count = 0
        # 遍历询价列表查询是否存在该条询价信息
        for inquire in service_inquire_list["a"]:
            if inquire_id == inquire["f"]:
                count = count + 1
            else:
                continue
        assert count == 1
        # 客服报价的参数
        offerInquire_param = self.service.offerInquire_randomparam(inquire_id=inquire_id,
                                                                   company_id=shipper_company_id,
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
                count = count + 1
            else:
                continue
        assert count == 1
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

        # 货主确认报价
        confirm = self.shipper.shipper_confirmInquire(cookie=self.shipper_token, inquire_id=inquire_id,
                                                      isConfirm=1)
        # 验证接口返回
        assert confirm == {"data": {"confirmInquire": 0}}
        # 货主查看进行中的货单列表
        shipper_source_list = self.shipper.shipper_getSources(cookie=self.shipper_token, type_num=1, time_num=0)
        count = 0
        source_id = ""
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
                source_id = source["f"]
            else:
                continue
        assert count == 1

        # 客服查询货单列表
        service_source_list = self.service.service_getSourcesByService(cookie=self.service_token, type_num=0, page=1)
        pagesize = service_source_list["pagesize"]
        count = 0
        for n in range(pagesize):
            # 遍历列表查询是否生成该条询价对应的货单信息
            service_source_list = self.service.service_getSourcesByService(cookie=self.service_token, type_num=0,
                                                                           page=n + 1)
            for source in service_source_list["a"]:
                if source_id == source["f"]:
                    count = count + 1
                else:
                    continue
        assert count == 1

        # 调度查询货单列表
        dispatch_source_list = self.dispatch.dispatch_getMonitorOrder(cookie=self.dispatch_token, type_num=1,
                                                                      time_num=0)
        # 遍历列表查询是否生成该条询价对应的货单信息
        count = 0
        for source in dispatch_source_list["a"]:
            if source_id == source["f"]:
                count = count + 1
            else:
                continue
        assert count == 1

        # 登录信息参数
        login_param = self.common.app_login_param(username=config.get_account("app")["username"],
                                                  password=config.get_account("app")["password"])
        # 登录
        login_info = self.common.app_login(library=self.library, param=login_param)
        user_uid = eval(login_info["pBody"])["i"]
        # 车队认证信息参数
        enterprise_info_param = self.common.enterprise_info_param()
        # 获取车队认证信息
        enterprise_info = self.common.enterprise_info(library=self.library, param=enterprise_info_param)
        # 车队ID
        enterprise = eval(enterprise_info["pBody"])["a"]
        # 车队名称
        enterprise_name = eval(enterprise_info["pBody"])["b"]
        # 姓名
        user_name = eval(enterprise_info["pBody"])["c"]
        last_time = 0
        count = 0
        for n in range(10):
            # 货单列表参数
            manifest_list_param = self.common.manifest_list_param(b=last_time)
            # 获取货单列表
            manifest_list_info = self.common.manifest_list(library=self.library, param=manifest_list_param)
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
        # 报价参数
        self.goods_report_param = self.common.goods_report_param(a=source_id, b=random.randint(100, 590) * 100,
                                                                 c=random.randint(1,
                                                                                  offerInquire_param["need_car_num"]),
                                                                 d=enterprise)
        # 发起报价
        self.common.goods_report(library=self.library, param=self.goods_report_param)
        # 获取我的报价列表
        my_report_param = self.common.my_report_list_param(a=enterprise, b=0)
        my_report_list_info = self.common.my_report_list(library=self.library, param=my_report_param)
        my_report_list = eval(my_report_list_info["pBody"])["b"]
        count = 0
        for my_report in my_report_list:
            if source_id == my_report["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # 调度查询待确认报价
        offer_id = ""
        dispatch_offer_list = self.dispatch.dispatch_getOfferBySourceId(cookie=self.dispatch_token, id=source_id,
                                                                        time=0)
        for offer in dispatch_offer_list["data"]["data"]:
            if enterprise_name == offer["fleet_name"]:
                offer_id = offer["id"]
                assert str(offer["mobile"]) == config.get_account("app")["username"]
                break
            else:
                continue
        # 调度确认报价
        result = self.dispatch.dispatch_confirmOffer(cookie=self.dispatch_token, source_id=source_id, id=offer_id,
                                                     type=1)
        assert result == {"data": {"code": 0}}
        # app 查询运单列表
        transport_id = ""
        transport_num = 0
        transport_list_param = self.common.transport_list_param(a=enterprise, b=0, c=1)
        self.common.transport_list(library=self.library, param=transport_list_param)
        for n in range(10):
            transport_list_info = app.response
            if transport_list_info["iErr"] == -1:
                continue
            else:
                transport_list = eval(transport_list_info["pBody"])["b"]
                for transport in transport_list:
                    if source_id == transport["m"]:
                        transport_id = transport["a"]
                        transport_num = transport["q"]
                    else:
                        continue
                break

        # 调度查看运单列表
        dispatch_order_list = self.dispatch.dispatch_getOrderBySourceId(cookie=self.dispatch_token, source_id=source_id,
                                                                        time=0)
        for order in dispatch_order_list["a"]:
            if transport_num == order["s"]:
                assert str(order["k"]) == config.get_account("app")["username"]
                break
            else:
                continue

        # app 添加车辆
        car_info_param = ran().create_app_car_info(fleet_id=enterprise)
        car_number = eval(car_info_param)["a"]
        addcar_info = self.common.app_add_car(library=self.library, param=car_info_param)
        addcar_result = eval(addcar_info["pBody"])
        assert addcar_result == {"a": 0}
        # app 车辆列表查看该车
        app_carinfo_list_param = self.common.app_carinfo_list_param(a=0, b=enterprise)
        app_carinfo_list_info = self.common.app_carinfo_list(library=self.library, param=app_carinfo_list_param)
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
        gua_car_info_param = ran().create_app_gua_car_info(fleet_id=enterprise)
        gua_car_number = eval(gua_car_info_param)["a"]
        add_gua_car_info = self.common.app_add_gua_car(library=self.library, param=gua_car_info_param)
        add_gua_car_result = eval(add_gua_car_info["pBody"])
        assert add_gua_car_result == {"a": 0}
        # app 挂车列表查看该挂车
        app_gua_carinfo_list_info_param = self.common.app_carinfo_list_param(a=enterprise, b=0)
        app_gua_carinfo_list_info = self.common.app_gua_carinfo_list(library=self.library,
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
        driver_param = ran().create_app_driver_info(fleet_id=enterprise)
        driver_name = eval(driver_param)["a"]
        driver_phone = eval(driver_param)["c"]
        app_add_driver_info = self.common.app_add_driver(library=self.library, param=driver_param)
        # app_add_driver_result = eval(app_add_driver_info["pBody"])
        # assert app_add_driver_result == {"a": 0}
        # app 司机列表查看该司机
        app_driverinfo_list_param = self.common.app_driverinfo_list_param(a=enterprise, b=0)
        app_driverinfo_list_info = self.common.app_driverinfo_list(library=self.library,
                                                                   param=app_driverinfo_list_param)
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
        driver_ya_param = ran().create_app_driver_ya_info(fleet_id=enterprise)
        driver_ya_name = eval(driver_ya_param)["a"]
        driver_ya_phone = eval(driver_ya_param)["b"]
        app_add_driver_ya_info = self.common.app_add_driver_ya(library=self.library, param=driver_ya_param)
        app_add_driver_ya_result = eval(app_add_driver_ya_info["pBody"])
        assert app_add_driver_ya_result == {"a": 0}
        # app 押运员列表查看该押运员
        app_driverinfo_list_ya_param = self.common.app_ya_driverinfo_list_param(a=enterprise, b=0)
        app_driverinfo_list_ya_info = self.common.app_ya_driverinfo_list(library=self.library,
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
        app_add_capacity_param = self.common.app_add_capacity_param(a=car_id, b=gua_car_id, c=driver_id,
                                                                    d=driver_ya_id, e=enterprise, f=driver_uid,
                                                                    g=driver_ya_uid)
        app_add_capacity_info = self.common.app_add_capacity(library=self.library, param=app_add_capacity_param)
        app_add_capacity_result = eval(app_add_capacity_info["pBody"])
        assert app_add_capacity_result == {"a": 0}
        # app 运力列表查看该运力
        app_capacitylist_param = self.common.app_capacitylist_param(a=enterprise, b=0)
        app_capacitylist_info = self.common.app_capacitylist(library=self.library, param=app_capacitylist_param)
        app_capacitylist = eval(app_capacitylist_info["pBody"])["s"]
        count = 0
        for capacity in app_capacitylist:
            if driver_id == capacity["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        driver = {"b": car_id, "c": driver_id}
        use_driver = (driver,)
        # 车队端上报车辆
        waillbill_report_car_param = self.common.waillbill_report_car_param(a=transport_id, d=enterprise, e=use_driver)
        report_result_info = self.common.waillbill_report_car(library=self.library, param=waillbill_report_car_param)
        report_result = eval(report_result_info["pBody"])["a"][0]
        assert report_result["c"] == 1
        # 小五查询运单详情的车辆列表
        car_list = self.dispatch.dispatch_getCarsByOrderId(cookie=self.dispatch_token, order_id=transport_id, type=2,
                                                           time=0)
        count = 0
        for car in car_list["data"]["data"]:
            if report_result["a"] == car["car_id"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
        # 小五确认车辆
        result = self.dispatch.dispatch_confirmCar(cookie=self.dispatch_token, car_id=report_result["a"], type=1)
        assert result == {"data": {"code": 0}}
        # 车队确认承运
        agree_param = self.common.waillbill_agree_param(a=transport_id)
        self.common.waillbill_agree(library=self.library, param=agree_param)
        # 上传装卸货磅单
        loading_param = self.common.loading_unload_upload_param(a=report_result["a"],
                                                                b=random.choice(config.get_picture()),
                                                                c=random.randint(1, 100) * 1000,
                                                                d=random.choice(config.get_picture()),
                                                                e=random.randint(1, 100) * 1000)
        self.common.loading_unload_upload(library=self.library, param=loading_param)
        # 查看装卸货磅单
        loading_info_param = self.common.loading_unload_info_param(a=report_result["a"])
        loading_unload_info = self.common.loading_unload_info(library=self.library, param=loading_info_param)
        loading_info = eval(loading_unload_info["pBody"])
        assert loading_info["b"] == eval(loading_param)["b"]
        # 生成线下合同
        contract_param = ran().create_apply_uncontract_param(a=enterprise, d=enterprise, i=transport_id,
                                                             s=enterprise_name,
                                                             u=user_uid, v=user_name,
                                                             z=int(config.get_account("app")["username"]))
        self.common.app_apply_contract(library=self.library, param=contract_param)
        # 小五确认合同已生成
        orderinfo = self.dispatch.dispatch_getOrderinfo(cookie=self.dispatch_token, a=transport_id)
        assert orderinfo["m"] == 0
        assert orderinfo["n"] == 2
        # 运单完成
        result = self.dispatch.dispatch_comfirm_transport(cookie=self.dispatch_token, transport_id=transport_id, type=2)
        assert result == {'code': 0}
        # 添加一个收款账户
        addBank_param = ran().create_addBank_param(enterprise=enterprise)
        addBank_result = self.common.addBankaccount(library=self.library, param=addBank_param)
        account_id = eval(addBank_result["pBody"])['a']
        # 获取银行账户列表
        getBankList_params = self.common.getBankList_params(a=enterprise)
        bankList_info = self.common.getBankList(library=self.library, param=getBankList_params)
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
        applyRecon_params = self.common.apply_recon_fleet_params(a=transport_id, b=account_id)
        self.common.apply_recon_fleet(library=self.library, param=applyRecon_params)
        # 客服获取待审核列表，拿到其对账单id
        waitServiceCheckList = self.service.service_getstatements(cookie=self.service_token, h=1, g=1)
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
        result = self.service.service_statementscheck(cookie=self.service_token, a=service_accountOderId, b=0)
        assert result == {'code': 0}

        # 审核成功后，客服查看已审核列表，确认是否存在对账单A
        serviceCheckDoneList = self.service.service_getstatements(cookie=self.service_token, g=1, h=1, f=1)
        count = 0
        for serviceCheckDone_A in serviceCheckDoneList["data"]:
            if serviceCheckDone_A['a'] == service_accountOderId and serviceCheckDone_A['m'] == 3:
                count += 1
            else:
                continue
        assert count == 1
        print('客服已审核列表中存在对账单A，状态为待复核员审核')

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
                                                                     b=random.choice(config.get_picture()))
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
