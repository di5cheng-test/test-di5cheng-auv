# coding:utf-8

from src.pages import dispatch_new
import random

global null
null = None

dispatch = dispatch_new.Dispatch()
dispatch_token = dispatch.dispatch_login(username="songkangkang002", password="123456")

x_list = dispatch.dispatch_md_40_cmd_200(cookie=dispatch_token, d=0, e=1, f=10)
x_inquiry = random.choice(x_list["a"])
source_id = x_inquiry["a"]
inquiry_id = x_inquiry["p"]
dispatch_id = x_inquiry["r"]

fleet_list = dispatch.dispatch_md_40_cmd_127(cookie=dispatch_token, a=source_id, i=1, z=0, h=dispatch_id)
if fleet_list["data"] != []:
    fleet_info = random.choice(fleet_list["data"])
    fleet_id = fleet_info["a"]
    fleet_uid = fleet_info["b"]
    fleet_dispatch_id = random.choice(fleet_info["lst"])["b"]
    fleet_dispatch = [{"e": fleet_id, "f": fleet_uid, "g": fleet_dispatch_id}]
    print(fleet_dispatch)
    dispatch.dispatch_md_40_cmd_64(cookie=dispatch_token, a=source_id, d=fleet_dispatch)
