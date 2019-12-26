# coding:utf-8
import requests
import random
import time
from src.common import config
from src.common.logger import MyLog

global null
null = None

url_service = config.get_service_url()


class Service(object):
    def service_login(self, username, password):
        # 客服登录
        # 返回值是登录用的token
        url = url_service + 'xf/sy/busi.do?md=40&cmd=1'
        param = {"username": username, "password": password}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        if "errors" in response:
            return response
        else:
            return response["data"]["login"]

    def service_info(self, cookie):
        # 客服信息
        url = url_service + 'xf/sy/busi.do?md=40&cmd=52'
        f_headers = {"token": cookie}
        param = {}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_getInquires(self, cookie, type_num, time_num):
        # 客服待处理询价列表
        # 根据type：0 未处理  1已处理
        # time：决定分页页数
        url = url_service + 'xf/sy/busi.do?md=40&cmd=41'
        f_headers = {"token": cookie}
        param = {"d": type_num, "e": time_num}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def offerInquire_randomparam(self, inquire_id, company_id, username, service_price=None):
        param = {}
        param["inquire_id"] = inquire_id
        param["company_id"] = company_id
        param["username"] = username
        param["up_price"] = random.randint(100, 4000) * 100
        param["down_price"] = random.randint(100, 4000) * 100
        param["need_car_num"] = random.randint(10, 400)
        param["service_price"] = ""
        if service_price is None:
            del param["service_price"]
        else:
            param["service_price"] = service_price
        MyLog().logger().info(param)
        return param

    def service_offerInquire(self, cookie, param):
        # 客服报价
        url = url_service + 'offerInquire'
        f_headers = {"token": cookie}
        json = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_getShippers(self, cookie, page, status, company_name=None):
        # 客服查货主列表
        # 客服代替货主发货时需要先查询货主列表
        url = url_service + 'xf/sy/busi.do?md=40&cmd=7'
        f_headers = {"token": cookie}
        param = {"page": page, "company_name": company_name, "status": status}
        if company_name is None:
            del param["company_name"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_location(self, cookie, parent_id):
        # 客服获取区代码
        # parent_id 为1，返回全国省份，为2以后返回省下面的城市
        url = url_service + 'getRegion'
        f_headers = {"token": cookie}
        param = {"parent_id": parent_id}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_randomlocation(self, cookie):
        # 客服端自动随机获取省市区
        province_list = self.service_location(cookie=cookie, parent_id=1)
        province = random.choice(province_list)
        province_name = province["region_name"]
        province_id = province["region_id"]
        city_list = self.service_location(cookie=cookie, parent_id=province_id)
        city = random.choice(city_list)
        city_name = city["region_name"]
        city_id = city["region_id"]
        area_list = self.service_location(cookie=cookie, parent_id=city_id)
        area = random.choice(area_list)
        area_name = area["region_name"]
        area_id = area["region_id"]
        location = province_name + "-" + city_name + "-" + area_name
        MyLog().logger().info(location)
        return location

    def service_fahuoparam(self, cookie, company_id, company_name):
        start_address = self.service_randomlocation(cookie=cookie)
        end_address = self.service_randomlocation(cookie=cookie)
        # 客服代替货主发货的参数列表
        param = {}
        param["shipper_id"] = company_id
        param["shipper_name"] = company_name
        param["source_name"] = random.choice(["甲苯", "二甲苯", "丙酮"])
        param["start_address"] = start_address
        param["end_address"] = end_address
        param["start_address_detail"] = "团结路" + str(random.randint(1, 10000)) + "号"
        param["end_address_detail"] = "友谊路" + str(random.randint(1, 10000)) + "号"
        param["load_time"] = int(time.time() * 1000)
        param["need_car_num"] = random.randint(2, 50)
        param["invoice_type"] = random.randint(0, 1)
        param["losePercent"] = random.randint(0, 3)
        param["up_price"] = random.randrange(100, 500) * 100
        param["down_price"] = random.randrange(100, 500) * 100
        param["service_price"] = random.randrange(100, 500) * 100
        param["send_source_num"] = random.randrange(50, 300) * 1000
        param["source_price"] = random.randrange(100, 500) * 100
        param["remark"] = "for test"
        MyLog().logger().info(param)
        return param

    def service_createSource(self, cookie, param):
        # 客服发布货源
        # 结合 service_fahuoparam 方法
        url = url_service + 'createSource'
        f_headers = {"token": cookie}
        param = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_createservice(self, cookie, param):
        # 客服添加一个货主
        url = url_service + 'createservice'
        f_headers = {"token": cookie}
        param = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_getSourcesByService(self, cookie, type_num, page, company_id=None):
        # 客服查询货单列表 time是页数
        param = {"d": type_num, "e": page, "f": ""}
        if company_id is None:
            del param["f"]
        else:
            param = {"d": type_num, "e": page, "f": company_id}
        url = url_service + 'xf/sy/busi.do?md=40&cmd=80'
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_getServices(self, cookie, status, region_source):
        # 获取客服列表
        url = url_service + 'xf/sy/busi.do?md=40&cmd=5'
        f_headers = {"token": cookie}
        param = {"status": status, "region_source": region_source}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_checkShipper(self, cookie, status, goods_type, content, admin_user_id, company_id, admin_name):
        # 客服添加一个货主
        url = url_service + 'createservice'
        f_headers = {"token": cookie}
        param = {"variables": {
            "input": {"status": status, "goods_type": goods_type, "content": content, "admin_user_id": admin_user_id,
                      "company_id": company_id, "admin_name": admin_name}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_getstatements(self, cookie, g, h, f=None):
        # 获取车队对账单
        url = url_service + 'xf/sy/busi.do?md=120&cmd=120'
        f_headers = {"token": cookie}
        #    f  是否为已审核列表  1是
        #    g 	状态              1待前线审核 3待财务审核 5待付款
        #    h 起始页
        param = {"f": f, "g": g, "h": h}
        if f is None:
            del param["f"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def service_statementscheck(self, cookie, a, b):
        # 获取客服审核对账单
        url = url_service + 'xf/sy/busi.do?md=123&cmd=123'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response
