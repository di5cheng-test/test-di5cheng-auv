# coding=utf-8

import random
from src.pages import service_new
import time
from src.common.random_param import Random_param as ran

service = service_new.Service()
service_token = service.service_login(username="songkangkang001", password="123456")

for n in range(10):
    goods_type = random.choice([1, 2, 3, 4])
    company_name = "auto" + str(int(time.time()))
    username = "自动" + str(n)
    mobile = 13000020041 + n
    password = '123456'
    id_card_pic_m = "J2066F098D0CE8054D1"
    id_card_pic_p = "J3F4B83A5F0CE805CD6"
    business = "J5E49C05910CE806581"
    business_2 = "J74A7E49530CE8070C4"
    business_3 = "JAA48461450CE807CCC"
    admin_user_id = 407953
    address = "autoaddress" + str(n)
    company_id_number = str(int(time.time()))
    id_card = ran().create_IDcard()
    admin_name = "test-service"
    status = 1
    region_source = 1
    service.service_md_40_cmd_6(cookie=service_token, goods_type=goods_type, company_name=company_name,
                                username=username, mobile=mobile, password=password, id_card=id_card,
                                id_card_pic_m=id_card_pic_m, id_card_pic_p=id_card_pic_p, business=business,
                                business_2=business_2, business_3=business_3, admin_user_id=admin_user_id,
                                address=address, company_id_number=company_id_number, admin_name=admin_name,
                                status=status, region_source=region_source)


# {"goods_type": 2, "company_name": "auto1575427818", "username": "自动0", "mobile": 13000020000, "password": "123456",
#  "id_card_pic_m": "J9BF9637E00CED47269", "id_card_pic_p": "J6E86BF9820CED47B13", "business": "J2E86735440CED48301",
#  "business_2": "J35424EF660CED48AFC", "business_3": "J2657B1BC80CED492F1", "admin_user_id": 407953,
#  "address": "autoaddress0", "company_id_number": "autonumber0", "id_card": "511112197203017878",
#  "admin_name": "test-service", "status": 0, "region_source": 1}
# {'goods_type': 2, 'company_name': 'auto1575427818', 'username': '自动0', 'mobile': 13000020000, 'password': 123456,
#  'id_card_pic_m': 'J2066F098D0CE8054D1', 'id_card_pic_p': 'J3F4B83A5F0CE805CD6', 'business': 'J5E49C05910CE806581',
#  'business_2': 'J74A7E49530CE8070C4', 'business_3': 'JAA48461450CE807CCC', 'address': 'autoaddress0',
#  'admin_user_id': 407953, 'company_id_number': 'autonumber0', 'id_card': '511112197203017878',
#  'admin_name': 'test-service', 'status': 0, 'region_source': 1}
