# coding:utf-8
import requests
import random
import time
from config import global_parameter
from src.common import random_param
from src.common.logger import MyLog

global null
null = None
url_shipper = global_parameter.shipper


class Shipper(object):
    def shipper_login(self, mobile, password):
        # 货主登录
        # 返回值是登录用的token
        url = url_shipper + "login"
        param = {"variables": {"input": {"mobile": mobile, "password": password}}}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        if "errors" in response:
            MyLog().sendlog("登录失败")
            return response
        else:
            MyLog().sendlog("登录成功")
            return response["data"]["login"]

    def shipper_editShipperPassword(self, cookie, mobile, code, password):
        # 修改密码
        url = url_shipper + "getcompanyInfo"
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"mobile": mobile, "code": code, "password": password, "sms_type": 2}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getcompanyInfo(self, cookie):
        # 货主查询自己的资料
        url = url_shipper + "getcompanyInfo"
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def inquire_param(self, cookie, company_name):
        # 询价单参数
        start_address = self.shipper_randomlocation(cookie=cookie)
        end_address = self.shipper_randomlocation(cookie=cookie)
        param = {}
        param["company_name"] = company_name
        param["source_name"] = random.choice(["甲苯", "二甲苯", "丙酮"])
        param["start_address"] = start_address
        param["end_address"] = end_address
        param["start_address_detail"] = "团结路" + str(random.randint(1, 10000)) + "号"
        param["end_address_detail"] = "友谊路" + str(random.randint(1, 10000)) + "号"
        param["load_time"] = int(time.time() * 1000)
        param["invoice_type"] = random.randint(0, 1)
        param["losePercent"] = random.randint(0, 3)
        param["remark"] = "for test"
        param["send_source_num"] = random.randrange(100, 5000) * 1000
        param["source_price"] = random.randrange(100, 5000) * 100
        param["target_price"] = random.randrange(100, 5000) * 100
        MyLog().sendlog(param)
        return param

    def shipper_sendInquire(self, cookie, param):
        # 货主发布询价
        # 结合param参数列表
        url = url_shipper + "sendInquire"
        f_headers = {"token": cookie}
        json = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getInquires(self, cookie, type_num, time_num):
        # 货主获取询价列表
        # 根据type：0 未报价  1已报价
        # time 取当前页最后一条的time决定分页
        url = url_shipper + "getInquires"
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"type": type_num, "time": time_num}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_confirmInquire(self, cookie, inquire_id, isConfirm):
        # 货主确认报价
        # inquire_id 询价单的ID
        # 根据isConfirm：0 取消报价  1确认报价
        url = url_shipper + "confirmInquire"
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"inquire_id": inquire_id, "isConfirm": isConfirm}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_location(self, cookie, parent_id):
        # 货主获取区代码
        # parent_id 为1，返回全国省份，为2以后返回省下面的城市
        url = url_shipper + 'getRegion'
        f_headers = {"token": cookie}
        param = {"variables": {"parent_id": parent_id}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        return response

    def shipper_randomlocation(self, cookie):
        # 货主端自动随机获取省市区
        province_list = self.shipper_location(cookie=cookie, parent_id=1)
        province = random.choice(province_list["data"]["getRegion"])
        province_name = province["region_name"]
        province_id = province["region_id"]
        city_list = self.shipper_location(cookie=cookie, parent_id=province_id)
        city = random.choice(city_list["data"]["getRegion"])
        city_name = city["region_name"]
        city_id = city["region_id"]
        area_list = self.shipper_location(cookie=cookie, parent_id=city_id)
        area = random.choice(area_list["data"]["getRegion"])
        area_name = area["region_name"]
        area_id = area["region_id"]
        location = province_name + "-" + city_name + "-" + area_name
        MyLog().sendlog(location)
        return location

    def shipper_getSources(self, cookie, type_num, time_num):
        # 货主端查询货单列表
        url = url_shipper + 'xf/sy/busi.do?md=40&cmd=53'
        f_headers = {"token": cookie}
        param = {"d": type_num, "e": time_num}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getCarsMapBySourceId(self, cookie, sourceId):
        # 货主端查询车辆监控地图
        url = url_shipper + 'getCarsMapBySourceId'
        f_headers = {"token": cookie}
        param = {"variables": {"id": sourceId}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getCarsBySourceId(self, cookie, sourceId, time):
        # 货主端查询货单车辆列表
        url = url_shipper + 'getCarsBySourceId'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"id": sourceId, "time": time}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def baseinfo_param(self, nikename=None, gender=None, birthday=None):
        # 一个货多个基础信息参数
        param = {"nikename": "", "gender": "", "birthday": ""}
        if nikename is None:
            del param["nikename"]
        else:
            param["nikename"] = nikename
        if gender is None:
            del param["gender"]
        else:
            param["gender"] = gender
        if birthday is None:
            del param["birthday"]
        else:
            param["birthday"] = birthday
        return param

    def ran_baseinfo_param(self):
        # 生成一组随机基础信息
        param = {}
        param["nikename"] = random_param.Random_param().create_name()
        param["gender"] = random.randint(1, 2)
        param["birthday"] = int(time.time() * 1000)
        MyLog().sendlog(param)
        return param

    def shipper_editBaseCompanyInfo(self, cookie, param):
        # 修改基本资料
        url = url_shipper + 'editBaseCompanyInfo'
        f_headers = {"token": cookie}
        json = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def companyinfo_param(self, cookie):
        # 货主认证资料参数
        name_1 = random_param.Random_param().create_name()
        company_name = "南京" + name_1 + "股份有限公司"
        param = {}
        param["company_name"] = company_name
        param["username"] = random_param.Random_param().create_name()
        param["address"] = "南京市浦口区团结路" + str(random.randint(1, 10000)) + "号"
        param["company_id_number"] = random_param.Random_param().random_num(22)
        param["id_card"] = random_param.Random_param().create_IDcard()
        param["id_card_pic_m"] = "J5A2C73C9E0D93755A7"
        param["id_card_pic_p"] = "JF4B1F62400D9375F19"
        param["business"] = "J4697D6A730D93767B2"
        param["business_2"] = "JAABE2E2A70D9377CBC"
        param["business_3"] = "J4697D6A730D93767B2"
        MyLog().sendlog(param)
        return param

    def shipper_editCompanyInfo(self, cookie, param):
        # 编辑货主资料
        url = url_shipper + 'editCompanyInfo'
        f_headers = {"token": cookie}
        json = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getsourcelist(self, cookie, type, time):
        # 货主获取货单列表
        # 1进行中 2已完成
        url = url_shipper + 'xf/sy/busi.do?md=40&cmd=53'
        f_headers = {"token": cookie}
        json = {"d": type, "e": time}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getSourceInfo(self, cookie, SourceId):
        # 货主获取货单详情
        url = url_shipper + 'xf/sy/busi.do?md=40&cmd=45'
        f_headers = {"token": cookie}
        json = {"a": SourceId}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def shipper_getContractList(self, cookie, company_id, time, online, sign, type):
        # 货主获取电子合同列表
        # 参数名	必选	类型	长度	说明
        # a	是	string	64	公司id
        # b	是	long	8	本地最小时间戳，默认0
        # c	是	int	4	1线上 2线下
        # d	是	int	4	0待签署1已签署 线下不需要
        # e	否	int	4	1长约2短约 app不需要
        url = url_shipper + 'xf/sy/busi.do?md=40&cmd=117'
        f_headers = {"token": cookie}
        json = {"a": company_id, "b": time, "c": online, "d": sign, "e": type}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response
