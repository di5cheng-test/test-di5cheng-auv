# coding:utf-8
import requests
from src.common import config
from src.common.logger import MyLog

global null
null = None

url_operation = config.get_operation_url()
log = MyLog()


class Operation(object):
    def operation_login(self, phoneNum, passWord):
        # 运营登录
        url = url_operation + "userLogin?md=46&cmd=1"
        json = {"phoneNum": phoneNum, "passWord": passWord}
        r = requests.post(url=url, json=json)
        response = eval(r.text)
        log.logger().info(response)
        return response['token']

    def operation_md_40_cmd_12(self, cookie, page, status, fleet_name=None):
        # 车队认证审核列表
        url = url_operation + 'queryFleetInfoList?md=40&cmd=12'
        f_headers = {"token": cookie}
        param = {"page": page, "fleet_name": fleet_name, "status": status}
        if fleet_name is None:
            param["fleet_name"] = ""
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def operation_md_40_cmd_15(self, cookie, fleet_id, fleet_name, contact, user_name, status, create_at, user_id,
                               admin_id, contact_phone, id_card, id_card_pic_m, id_card_pic_p, company_id_number,
                               business, business_2, address, region_source, first_people, car_type, contract, content,
                               car_type_detail, status_name, exist, admin_name, admin_user_id):
        # 车队认证审核
        url = url_operation + 'modifyFleet?md=40&cmd=15'
        f_headers = {"token": cookie}
        param = {"code": 0, "fleet_id": fleet_id, "fleet_name": fleet_name, "contact": contact, "user_name": user_name,
                 "status": status, "create_at": create_at, "user_id": user_id, "admin_id": admin_id,
                 "contact_phone": contact_phone, "id_card": id_card, "id_card_pic_m": id_card_pic_m,
                 "id_card_pic_p": id_card_pic_p, "company_id_number": company_id_number, "business": business,
                 "business_2": business_2, "address": address, "region_source": region_source,
                 "first_people": first_people, "car_type": car_type, "contract": contract, "content": content,
                 "car_type_detail": car_type_detail, "status_name": status_name, "exist": exist,
                 "admin_name": admin_name, "admin_user_id": admin_user_id}
        print(param)
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def operation_md_40_cmd_51(self, cookie, fleet_id):
        # 车队认证审核详情
        url = url_operation + 'fleetDetailInfo?md=40&cmd=51'
        f_headers = {"token": cookie}
        param = {"fleet_id": fleet_id}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

# {"code":0,"fleet_id":"5e0170c0743a49581b460727","fleet_name":"auto1577152574","contact":"凤托托","user_name":"凤托托","status":1,"create_at":1577153219205,"user_id":422003,"admin_id":"5cce48ba9f660834f3fa32f6","contact_phone":13000050007,"id_card":"220723198201214372","id_card_pic_m":"J5DEA926D60CFB8B02A","id_card_pic_p":"J95848896B0315044FF","company_id_number":"1577152574","business":"J571CB18220CFB8A08F","business_2":"JF57F9F0040CFB8A895","address":null,"region_source":2,"first_people":null,"car_type":3,"contract":0,"content":"","car_type_detail":"","status_name":"待审核","exist":1,"admin_name":"测试小五","admin_user_id":407954}
