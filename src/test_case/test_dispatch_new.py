# coding:utf-8
import random
from src.common import config
from src.pages import shipper
from src.pages import dispatch_new as dispatch
from src.pages import service_new as service
import allure

global null
null = None


@allure.feature("web端小五测试用例套件")
class Test_case(object):
    def setup_class(self):
        self.shipper = shipper.Shipper()
        self.service = service.Service()
        self.dispatch = dispatch.Dispatch()
        self.shipper_token = self.shipper.shipper_login(mobile=config.get_account("shipper")["username"],
                                                        password=config.get_account("shipper")["password"])
        self.service_token = self.service.service_login(username=config.get_account("service")["username"],
                                                        password=config.get_account("service")["password"])
        self.dispatch_token = self.dispatch.dispatch_login(username=config.get_account("dispatch")["username"],
                                                           password=config.get_account("dispatch")["password"])

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")
    #
    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    @allure.story("用例分组-1")
    @allure.title("用例1：小五新增车队")
    @allure.description("登录小五web端，使用小五的新增车队功能生成一组车队")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("这里是步骤说明一")
    def test_case001(self):
        # 获取小五的基本信息
        dispatch_info = self.dispatch.dispatch_info(cookie=self.dispatch_token)
        # 提取 username
        username = dispatch_info["data"]["data"]["username"]
        # 提取 user_id
        user_id = dispatch_info["data"]["data"]["user_id"]
        # 提取 admin_id
        admin_id = dispatch_info["data"]["data"]["admin_id"]
        # 生成一组车队参数
        fleet_param = self.dispatch.dispatch_ranfleetparam(admin_id=admin_id, admin_name=username,
                                                           admin_user_id=user_id)
        # 新增一个车队
        send_result = self.dispatch.dispatch_createFleet(cookie=self.dispatch_token, param=fleet_param)
        # 验证接口返回
        assert send_result == {"data": {"code": 0}}
        # 查询车队列表，确认新增的车队已经增加
        get_fleets = self.dispatch.dispatch_getFleets(cookie=self.dispatch_token, page=1)
        page_size = get_fleets["data"]["data"]["pagesize"]
        count = 0
        # 获取每一页的车队信息
        for page_num in range(page_size):
            result = self.dispatch.dispatch_getFleets(cookie=self.dispatch_token, page=(page_num + 1))
            # 在fleets中查找是否存在新增的车队
            for fleet in result["data"]["data"]["rows"]:
                if str(fleet["contact_phone"]) == fleet_param["contact_phone"] and \
                        fleet["contact"] == fleet_param["contact"]:
                    count = count + 1
                else:
                    continue
        assert count == 1

    # 用例2: 小五给车队增加车辆
    def test_case002(self):
        # 查询车队列表
        get_fleets = self.dispatch.dispatch_getFleets(cookie=self.dispatch_token, page=1)
        # 任意选择一个车队id
        fleet_id = random.choice(get_fleets["data"]["data"]["rows"])["fleet_id"]
        # 生成一组车辆信息
        car_param = self.dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=global_parameter.jpg_id)
        # 新增一个车辆
        send_result = self.dispatch.dispatch_createCarByFleet(cookie=self.dispatch_token, param=car_param)
        # 验证接口返回
        assert send_result["code"] == 0
        # 查询该货主车辆列表
        car_list = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id, page=1)
        page_size = car_list["pagesize"]
        count = 0
        for page_num in range(page_size):
            result = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id,
                                                             page=(page_num + 1))
            # 查找是否存在新增的车辆
            for car in result["data"]:
                if car["car_number"] == car_param["car_number"]:
                    count = count + 1
                else:
                    continue
        assert count == 1

    # 用例2: 小五给车队删除车辆
    def test_case003(self):
        # 查询车队列表
        get_fleets = self.dispatch.dispatch_getFleets(cookie=self.dispatch_token, page=1)
        # 任意选择一个车队id
        fleet_id = random.choice(get_fleets["data"]["data"]["rows"])["fleet_id"]
        # 生成一组车辆信息
        car_param = self.dispatch.carinfo_param(fleet_id=fleet_id, yingyun_pic=global_parameter.jpg_id)
        # 新增一个车辆
        send_result = self.dispatch.dispatch_createCarByFleet(cookie=self.dispatch_token, param=car_param)
        # 验证接口返回
        assert send_result["code"] == 0
        # 查询该货主车辆列表
        car_list = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id, page=1)
        page_size = car_list["pagesize"]
        car_id = ""
        for page_num in range(page_size):
            result = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id,
                                                             page=(page_num + 1))
            # 查找是否存在新增的车辆
            for car in result["data"]:
                if car["car_number"] == car_param["car_number"]:
                    car_id = car["car_id"]
                else:
                    continue
        # 删除该车辆
        result = self.dispatch.dispatch_delCarByFleet(cookie=self.dispatch_token, fleet_id=fleet_id, car_id=car_id)
        # 验证接口返回
        assert result == {"data": {"code": 0}}
        # 查询该货主车辆列表
        car_list = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id, page=1)
        page_size = car_list["pagesize"]
        count = 0
        for page_num in range(page_size):
            result = self.dispatch.dispatch_getCarsByFleetId(cookie=self.dispatch_token, fleet_id=fleet_id,
                                                             page=(page_num + 1))
            # 查找是否存在删除的车辆
            for car in result["data"]:
                if car["car_number"] == car_param["car_number"]:
                    count = count + 1
                else:
                    continue
        assert count == 0

    def test_case004(self):
        list_cars = []
        time = 0
        while True:
            cars = self.dispatch.dispatch_getCarsByOrderId(cookie=self.dispatch_token,
                                                           order_id="5d18e6b495fe2936f397e008", type=2, time=time)
            if cars == {"data": {"data": []}}:
                break
            else:
                list_cars = list_cars + cars["data"]["data"]
                time = cars["data"]["data"][-1]["create_at"]
        print(len(list_cars))
        for car in list_cars:
            print(car)

    def test_case005(self):
        self.dispatch.dispatch_fleetlist(cookie=self.dispatch_token, page=1, status=0)
        self.dispatch.dispatch_carlist(cookie=self.dispatch_token, c=1, e=1)
        self.dispatch.dispacth_driverlist(cookie=self.dispatch_token, c=1, d=1)
