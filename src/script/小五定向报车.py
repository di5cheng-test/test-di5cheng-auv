# coding:utf-8

import random
from src.pages import dispatch_new

dispatch = dispatch_new.Dispatch()
dispatch_token = dispatch.dispatch_login(username="songkangkang002", password="123456")
dispatch_info = dispatch.dispatch_dispatchInfo(cookie=dispatch_token)
dispatch_id = dispatch_info["data"]["data"]["admin_id"]
# {"a":"5df9819d743a4927484c65ba","b":1,"c":20000,"d":[{"e":"5dca198b9f66081342b0a918","f":419945,"g":419945}]}
# 获取货单
source_list_info = dispatch.dispatch_md_40_cmd_201(cookie=dispatch_token, d=0, e=1, f=10)

source_info = random.choice(source_list_info["a"])
source_price = source_info["k"]
source_id = source_info["a"]
print(source_info, source_price, source_id)

fleet_list_1 = dispatch.dispatch_md_40_cmd_127(cookie=dispatch_token, a=source_id, g=0, z=0, h=dispatch_id, i=2)
if fleet_list_1["data"] != []:
    fleet_info = random.choice(fleet_list_1["data"])
    fleet_id = fleet_info["a"]
    fleet_uid = fleet_info["b"]
    fleet_dispatch_id = random.choice(fleet_info["lst"])["a"]
    fleet_dispatch = [{"e": fleet_id, "f": fleet_uid, "g": fleet_dispatch_id}]
    car_num = random.randint(2, 10)
    dispatch.dispatch_md_40_cmd_65(cookie=dispatch_token, a=source_id, b=1, c=source_price, d=fleet_dispatch)

fleet_list_2 = dispatch.dispatch_md_40_cmd_127(cookie=dispatch_token, a=source_id, g=1, z=0, i=2)
if fleet_list_2["data"] != []:
    fleet_info = random.choice(fleet_list_2["data"])
    fleet_id = fleet_info["a"]
    fleet_uid = fleet_info["b"]
    fleet_dispatch_id = random.choice(fleet_info["lst"])["a"]
    fleet_dispatch = [{"e": fleet_id, "f": fleet_uid, "g": fleet_dispatch_id}]
    car_num = random.randint(2, 10)
    dispatch.dispatch_md_40_cmd_65(cookie=dispatch_token, a=source_id, b=1, c=source_price, d=fleet_dispatch)

# for source in source_list_info["a"]:
#     source_id = source["a"]
#     fleet_list_1 = dispatch.dispatch_md_40_cmd_127(cookie=dispatch_token, a=source_id, g=0, z=0, h=dispatch_id, i=2)
#     fleet_list_2 = dispatch.dispatch_md_40_cmd_127(cookie=dispatch_token, a=source_id, g=1, z=0, i=2)
