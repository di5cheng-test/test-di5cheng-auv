from src.pages import dispatch_new
import time
from src.common.random_param import Random_param as ran

dispatch = dispatch_new.Dispatch()
dispatch_token = dispatch.dispatch_login(username="songkangkang002", password="123456")

for n in range(2):
    fleet_name = "auto" + str(int(time.time()))
    address = "团结路" + str(n) + "号"
    contact = ran().create_name()
    contact_phone = 13000030016 + n
    admin_name = "suwei002"
    admin_id = "5cd28e049f6608369dd7ea33"
    region_source = 5
    id_card = ran().create_IDcard()
    company_id_number = str(int(time.time()))
    id_card_pic_m = "J5DEA926D60CFB8B02A"
    id_card_pic_p = "J95848896B0315044FF"
    business = "J571CB18220CFB8A08F"
    business_2 = "JF57F9F0040CFB8A895"
    status = 1
    car_type = 4          # random.randint(1, 4)
    password = "123456"
    user_name = ran().create_name()
    admin_user_id = 408065
    dispatch.dispatch_md_40_cmd_13(cookie=dispatch_token, fleet_name=fleet_name, address=address, contact=contact,
                                   contact_phone=contact_phone, admin_name=admin_name, admin_id=admin_id,
                                   region_source=region_source, id_card=id_card, company_id_number=company_id_number,
                                   id_card_pic_m=id_card_pic_m, id_card_pic_p=id_card_pic_p, business=business,
                                   business_2=business_2, status=status, car_type=car_type, password=password,
                                   user_name=user_name, admin_user_id=admin_user_id)
