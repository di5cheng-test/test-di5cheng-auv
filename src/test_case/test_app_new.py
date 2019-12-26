from ctypes import *
from src.pages import auv_app_new as app
from src.common import config
from src.common.random_param import Random_param as ran
import random

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.library = cdll.LoadLibrary(config.get_library())
        self.app = app.Common()
        self.app.initSDK(library=self.library, init_info=config.get_app_url())
        # 登录信息参数
        login_param = self.app.app_login_param(username=config.get_account("app")["username"],
                                               password=config.get_account("app")["password"])
        # 登录
        login_info = self.app.app_login(library=self.library, param=login_param)
        self.user_uid = eval(login_info["pBody"])["i"]
        # 车队认证信息参数
        enterprise_info_param = self.app.auv_param_md_40_cmd_23()
        # 获取车队认证信息
        self.enterprise_info = self.app.auv_md_40_cmd_23(library=self.library, param=enterprise_info_param)
        # 车队ID
        self.enterprise = eval(self.enterprise_info["pBody"])["a"]
        # 车队名称
        self.enterprise_name = eval(self.enterprise_info["pBody"])["b"]
        # 姓名
        self.user_name = eval(self.enterprise_info["pBody"])["c"]

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")

    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    def test_case001(self):
        my_source_param = self.app.auv_param_md_40_cmd_34(a=self.enterprise, b=0)
        my_source_list_info = self.app.auv_md_40_cmd_34(library=self.library, param=my_source_param)

        # 车队查看进行中的运单
        transport_list_param = self.app.auv_param_md_40_cmd_25(a=self.enterprise, b=0, c=1)
        transport_list_info = self.app.auv_md_40_cmd_25(library=self.library, param=transport_list_param)
        transport_list = eval(transport_list_info["pBody"])["b"]
        for transport in transport_list:
            transport_id = transport["m"]
            print(transport_id)
            transport_car_list_param = self.app.auv_param_md_40_cmd_17(e=transport_id, b=0)
            self.app.auv_md_40_cmd_17(library=self.library, param=transport_car_list_param)

    def test_case002(self):
        # 查看运力列表
        capacity_list_param = self.app.auv_param_md_40_cmd_181(a=self.enterprise, b=0)
        capacity_list_info = self.app.auv_md_40_cmd_181(library=self.library, param=capacity_list_param)
        capacity_list = eval(capacity_list_info["pBody"])["s"]

    def test_case003(self):
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

    def test_case004(self):
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
        for gua_carinfo in app_gua_carinfo_list:
            if gua_car_number == gua_carinfo["a"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1

    def test_case005(self):
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
        for driverinfo in app_driverinfo_list:
            if driver_name == driverinfo["a"] and driver_phone == driverinfo["b"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1

    def test_case006(self):
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
        for driverinfo_ya in app_driverinfo_ya_list:
            if driver_ya_name == driverinfo_ya["b"] and driver_ya_phone == driverinfo_ya["c"]:
                count = count + 1
                break
            else:
                continue
        assert count == 1

    def test_case007(self):
        # app 车辆列表查看车辆
        app_carinfo_list_param = self.app.auv_param_md_40_cmd_164(a=0, b=self.enterprise)
        app_carinfo_list_info = self.app.auv_md_40_cmd_164(library=self.library, param=app_carinfo_list_param)
        app_carinfo_list = eval(app_carinfo_list_info["pBody"])["s"]
        # 随机取车辆
        car_id = random.choice(app_carinfo_list)["d"]
        # app 挂车列表查看挂车
        app_gua_carinfo_list_info_param = self.app.auv_param_md_40_cmd_169(a=self.enterprise, b=0)
        app_gua_carinfo_list_info = self.app.auv_md_40_cmd_169(library=self.library,
                                                               param=app_gua_carinfo_list_info_param)
        app_gua_carinfo_list = eval(app_gua_carinfo_list_info["pBody"])["s"]
        # 随机取挂车
        gua_car_id = random.choice(app_gua_carinfo_list)["d"]
        # app 司机列表查看司机
        app_driverinfo_list_param = self.app.auv_param_md_40_cmd_174(a=self.enterprise, b=0)
        app_driverinfo_list_info = self.app.auv_md_40_cmd_174(library=self.library, param=app_driverinfo_list_param)
        app_driverinfo_list = eval(app_driverinfo_list_info["pBody"])["s"]
        # 随机取司机
        driverinfo = random.choice(app_driverinfo_list)
        driver_uid = driverinfo["c"]
        driver_id = driverinfo["g"]
        # app 押运员列表查看押运员
        app_driverinfo_list_ya_param = self.app.auv_param_md_40_cmd_184(a=self.enterprise, b=0)
        app_driverinfo_list_ya_info = self.app.auv_md_40_cmd_184(library=self.library,
                                                                 param=app_driverinfo_list_ya_param)
        app_driverinfo_ya_list = eval(app_driverinfo_list_ya_info["pBody"])["s"]
        # 随机取押运员
        driver_ya_info = random.choice(app_driverinfo_ya_list)
        driver_ya_uid = driver_ya_info["a"]
        driver_ya_id = driver_ya_info["g"]
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
