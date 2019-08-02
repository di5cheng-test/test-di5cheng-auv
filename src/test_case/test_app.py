from ctypes import *
from src.pages import app
from src.common import config
from src.common.random_param import Random_param as ran
import random

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.library = cdll.LoadLibrary(config.get_library())
        self.common = app.Common()
        self.common.initSDK(library=self.library, init_info=config.get_app_url())
        # 登录信息参数
        login_param = self.common.app_login_param(username=config.get_account("app")["username"],
                                                  password=config.get_account("app")["password"])
        # 登录
        login_info = self.common.app_login(library=self.library, param=login_param)
        self.user_uid = eval(login_info["pBody"])["i"]

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")

    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    def test_case001(self):

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

        transport_list_param = self.common.transport_list_param(a=enterprise, b=0, c=1)
        transport_list_info = self.common.transport_list(library=self.library, param=transport_list_param)
        transport_list = eval(transport_list_info["pBody"])["b"]
        transport_id = random.choice(transport_list)["a"]
        # 生成线下合同
        contract_param = ran().create_apply_uncontract_param(a=enterprise, d=enterprise, i=transport_id,
                                                             s=enterprise_name, u=int(self.user_uid), v=user_name,
                                                             z=int(config.get_account("app")["username"]))
        result = self.common.app_apply_contract(library=self.library, param=contract_param)

    def test_case002(self):
        # 车队认证信息参数
        enterprise_info_param = self.common.enterprise_info_param()
        # 获取车队认证信息
        enterprise_info = self.common.enterprise_info(library=self.library, param=enterprise_info_param)
        # 车队ID
        enterprise = eval(enterprise_info["pBody"])["a"]
        # 车队名称
        enterprise_name = eval(enterprise_info["pBody"])["b"]
        # app 添加车辆
        car_info_param = ran().create_app_car_info(fleet_id=enterprise)
        car_number = eval(car_info_param)["a"]
        addcar_info = self.common.app_add_car(library=self.library, param=car_info_param)
        addcar_result = addcar_info["pBody"]
        assert addcar_result == ""
        # app 车辆列表查看该车
        app_carinfo_list_param = self.common.app_carinfo_list_param(a=0, b=enterprise)
        app_carinfo_list_info = self.common.app_carinfo_list(library=self.library, param=app_carinfo_list_param)
        app_carinfo_list = eval(app_carinfo_list_info["pBody"])["s"]
        count = 0
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
        add_gua_car_result = add_gua_car_info["pBody"]
        assert add_gua_car_result == '{"a":0}'
        # app 挂车列表查看该挂车
        app_gua_carinfo_list_info_param = self.common.app_carinfo_list_param(a=enterprise, b=0)
        app_gua_carinfo_list_info = self.common.app_gua_carinfo_list(library=self.library,
                                                                     param=app_gua_carinfo_list_info_param)
        app_gua_carinfo_list = eval(app_gua_carinfo_list_info["pBody"])["s"]
        count = 0
        for gua_carinfo in app_gua_carinfo_list:
            if gua_car_number == gua_carinfo["a"]:
                count = count + 1
                gua_car_id = gua_carinfo["d"]
                break
            else:
                continue
        assert count == 1

    def test_case003(self):
        # 车队认证信息参数
        enterprise_info_param = self.common.enterprise_info_param()
        # 获取车队认证信息
        enterprise_info = self.common.enterprise_info(library=self.library, param=enterprise_info_param)
        # 车队ID
        enterprise = eval(enterprise_info["pBody"])["a"]
        # 车队名称
        enterprise_name = eval(enterprise_info["pBody"])["b"]
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
            if driver_uid == capacity["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1
