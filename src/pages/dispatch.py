# coding:utf-8
import requests
from src.common.logger import MyLog
from src.common import config

global null
null = None

url_dispatch = config.get_dispatch_url()


class Dispatch(object):
    def dispatch_login(self, username, password):
        # 小五登录
        # 返回值是登录用的token
        url = url_dispatch + 'login'
        param = {"variables": {"input": {"username": username, "password": password}}}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        if "errors" in response:
            MyLog().sendlog("登录失败")
            return response
        else:
            MyLog().sendlog("登录成功")
            return response["data"]["login"]

    def dispatch_dispatchInfo(self, cookie):
        # 查询小五基本信息
        url = url_dispatch + 'dispatchInfo'
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_confirmSource(self, cookie, id):
        # 将货单完成
        url = url_dispatch + 'confirmSource'
        f_headers = {"token": cookie}
        param = {"variables": {"id": id, "type": 20}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getMonitorOrder(self, cookie, type_num, time_num):
        # 小五查询货单列表
        # time ：滚动分页，取当前页左后一条的时间戳，第一页默认为0
        # type ：1进行中 2已完成
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=57'
        f_headers = {"token": cookie}
        param = {"d": type_num, "e": time_num}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getUnconfirmOffer(self, cookie, time):
        # 小五查看待办事宜中的待确认报价列表中的货单列表
        # 返回的是所有的，含有未确认报价的，货单
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=43'
        f_headers = {"token": cookie}
        param = {"e": time}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getOfferBySourceId(self, cookie, id, time):
        # 小五查看货单详情中的的待确认的报价列表
        # 返回的是当前货单ID下的已报价待确认的报价列表
        url = url_dispatch + 'getOfferBySourceId'
        f_headers = {"token": cookie}
        param = {"variables": {"id": id, "time": time}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_confirmOffer(self, cookie, source_id, id, type):
        # 小五确认报价
        # source_id , 货单的ID
        # id，报价单的ID
        url = url_dispatch + 'confirmOffer'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"id": id, "source_id": source_id, "type": type}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getOrderBySourceId(self, cookie, source_id, time):
        # 获取货单中的运单列表
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=47'
        f_headers = {"token": cookie}
        param = {"a": source_id, "b": time}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getOrderinfo(self, cookie, a):
        # 运单详情页
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=23'
        f_headers = {"token": cookie}
        param = {"a": a}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getCarsByOrderId(self, cookie, order_id, type, time):
        # 运单详情页车辆列表
        url = url_dispatch + 'getCarsByOrderId'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"id": order_id, "type": type, "time": time}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_confirmCar(self, cookie, car_id, type):
        # 确认车辆
        url = url_dispatch + 'confirmCar'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"id": car_id, "type": type}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def carinfo_param(self, fleet_id, car_number, gua_number, m_user, m_mobile, car_ton, m_id_card, status,
                      region_source, yingyun_pic, first_people):
        # 添加车辆的信息
        param = {"fleet_id": fleet_id,
                 "car_number": car_number,
                 "gua_number": gua_number,
                 "m_user": m_user,
                 "m_mobile": m_mobile,
                 "car_ton": car_ton,
                 "m_id_card": m_id_card,
                 "yingyun_pic": yingyun_pic,
                 "status": status,
                 "region_source": region_source,
                 "first_people": first_people
                 }
        return param

    def dispatch_createCarByFleet(self, cookie, param):
        # 小五给车队增加车辆
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=18'
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_delCarByFleet(self, cookie, fleet_id, car_id):
        # 小五给车队删除车辆
        url = url_dispatch + 'delCarByFleet'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"fleet_id": fleet_id, "car_id": car_id}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getCarsByFleetId(self, cookie, fleet_id, page):
        # 查询车队的车辆信息
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=19'
        f_headers = {"token": cookie}
        param = {"fleet_id": fleet_id, "page": page}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getFleets(self, cookie, page):
        # 小五查询车队信息列表
        url = url_dispatch + 'getFleets'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"page": page}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getEvents(self, cookie, event_status, page):
        # 小五获取应急信息列表
        # event_status:0未处理 1已处理
        url = url_dispatch + 'getEvents'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"event_status": event_status, "page": page}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_getEvent(self, cookie, id):
        # 小五获取应急信息
        url = url_dispatch + 'getEvent'
        f_headers = {"token": cookie}
        param = {"variables": {"id": id}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_confirmEvent(self, cookie, goodsevent_id, event_status, event_content, admin_name):
        # 小五处理应急信息
        # goodsevent_id ，事件ID
        # event_status ，0待处理，1已处理
        # event_content ，处理内容
        # admin_name ，处理的小五名
        url = url_dispatch + 'getEvent'
        f_headers = {"token": cookie}
        param = {"variables": {
            "input": {"goodsevent_id": goodsevent_id, "event_status": event_status, "event_content": event_content,
                      "admin_name": admin_name}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)["data"]["data"]
        MyLog().sendlog(response)
        return response

    def dispatch_fleet_info_param(self, fleet_name, address, contact, contact_phone, region_source, id_card,
                                  company_id_number, id_card_pic_m, id_card_pic_p, business, business_2, status,
                                  car_type, password, first_people, admin_id, admin_name, admin_user_id):
        # 小五注册直接认证通过的车队参数
        param = {
            "fleet_name": fleet_name,  # 车队名称
            "address": address,  # 公司地址
            "contact": contact,  # 联系人姓名
            "contact_phone": contact_phone,  # 联系人手机号码
            "admin_id": admin_id,  # 关联的小五admin_id
            "region_source": region_source,  # 注册渠道
            "id_card": id_card,  # 身份证号码
            "company_id_number": company_id_number,  # 三证合一码
            "id_card_pic_m": id_card_pic_m,  # 身份证正面照
            "id_card_pic_p": id_card_pic_p,  # 身份证背面照
            "business": business,  # 营业执照
            "business_2": business_2,  # 道路运输许可证
            "status": status,  # 注册后状态
            "car_type": car_type,  # 车队类型
            "password": password,  # 登录密码
            "first_people": first_people,  # 关联BD的工号
            "admin_name": admin_name,  # 关联的小五username
            "admin_user_id": admin_user_id  # 关联的小五user_id
        }
        MyLog().sendlog(param)
        return param

    def dispatch_createFleet(self, cookie, param):
        # 小五新增车队
        url = url_dispatch + 'createFleet'
        f_headers = {"token": cookie}
        json = {"variables": {"input": param}}
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        # {"data": {"code": 0}}
        return response

    def dispatch_comfirm_transport(self, cookie, transport_id, type, message_fee=None, content=None):
        # 运单完成
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=61'
        f_headers = {"token": cookie}
        json = {"a": transport_id, "b": type, "c": message_fee, "d": content}
        if message_fee is None:
            del json["c"]
        if content is None:
            del json["d"]
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_fleetlist(self, cookie, page, fleet_name=None, contact_phone=None, status=None):
        # 车队列表
        # 参数名	必选	类型	长度	描述	取值说明
        # page	是	int	4	页码
        # fleet_name	否	string	64	车队名称
        # contact_phone	否	long	8	手机号
        # status	是	int	4	0待审核 1审核通过 2审核驳回-1已删除 不传此参数代表全部
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=12'
        f_headers = {"token": cookie}
        json = {"page": page, "status": status, "fleet_name": fleet_name, "contact_phone": contact_phone}
        if fleet_name is None:
            del json["fleet_name"]
        if contact_phone is None:
            del json["contact_phone"]
        if status is None:
            del json["status"]
        MyLog().sendlog(json)
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispatch_carlist(self, cookie, c, a=None, b=None, d=None, e=None):
        # 车队司机列表
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	车队id
        # b	否	string	12	联系人名称
        # c	是	int	12	角色	1 车辆 2挂车
        # d	否	string	12	车队名称
        # e	否	int	12	起始页
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=158'
        f_headers = {"token": cookie}
        json = {"a": a, "b": b, "c": c, "d": d, "e": e}
        if a is None:
            del json["a"]
        if b is None:
            del json["b"]
        if d is None:
            del json["d"]
        if e is None:
            del json["e"]
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def dispacth_driverlist(self, cookie, a=None, b=None, c=None, d=None):
        # 车队司机列表
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	车队id
        # b	否	string	12	联系人名称
        # c	否	int	12	角色	1 押运员 2司机
        # d	否	int	12	起始页
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=156'
        f_headers = {"token": cookie}
        json = {"a": a, "b": b, "c": c, "d": d}
        if a is None:
            del json["a"]
        if b is None:
            del json["b"]
        if d is None:
            del json["d"]
        if d is None:
            del json["e"]
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response
