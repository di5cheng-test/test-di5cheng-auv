# coding:utf-8

from src.pages import dispatch_new
import random

global null
null = None

offer_type = 0
# offer_type 1表示随机给某个询价单报价 ，否则批量给全部询价单报价
dispatch = dispatch_new.Dispatch()
dispatch_token = dispatch.dispatch_login(username="songkangkang002", password="123456")

if offer_type == 1:
    x_list = dispatch.dispatch_md_40_cmd_200(cookie=dispatch_token, d=0, e=1, f=10)
    x_inquiry = random.choice(x_list["a"])
    source_id = x_inquiry["a"]
    inquiry_id = x_inquiry["p"]
    price = random.randint(100, 10000)
    car_num = random.randint(10, 100)
    print(x_inquiry, source_id, inquiry_id, price, car_num)
    dispatch.dispatch_md_40_cmd_205(cookie=dispatch_token, a=source_id, b=price, c=car_num, e=inquiry_id)
else:
    x_list = dispatch.dispatch_md_40_cmd_200(cookie=dispatch_token, d=0, e=1, f=10)
    page = x_list["x"]
    for n in range(1, page + 1):
        x_list = dispatch.dispatch_md_40_cmd_200(cookie=dispatch_token, d=0, e=n, f=10)
        for x_inquiry in x_list["a"]:
            source_id = x_inquiry["a"]
            inquiry_id = x_inquiry["p"]
            price = random.randint(100, 10000)
            car_num = random.randint(10, 100)
            print(x_inquiry, source_id, inquiry_id, price, car_num)
            dispatch.dispatch_md_40_cmd_205(cookie=dispatch_token, a=source_id, b=price, c=car_num, e=inquiry_id)
