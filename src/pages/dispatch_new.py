# coding:utf-8
import requests
from src.common import config
from src.common.logger import MyLog

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
        MyLog().logger().info(response)
        if "errors" in response:
            return response
        else:
            return response["data"]["login"]

    def dispatch_md_40_cmd_13(self, cookie, fleet_name, address, contact, contact_phone, admin_id, region_source,
                              id_card, company_id_number, id_card_pic_m, id_card_pic_p, business, business_2, status,
                              car_type, password, user_name, admin_name, admin_user_id):
        # 运单详情页
        # 参数名	必选	类型	长度	描述	取值说明
        # fleet_name	是	string	64	车队全称
        # password	是	string	64	密码
        # address	是	string	64	车队地址
        # contact	是	string	64	联系人
        # user_name	是	string	64	法人姓名
        # contact_phone	是	int	4	联系方式
        # id_card	是	string	32	身份证号
        # admin_id	是	string	24	后台客服id
        # admin_user_id	是	int	4	调度客服uid
        # admin_name	是	string	24	后台客服姓名
        # first_people	否	string	4	开拓者
        # car_type	是	int	4	车队类型1：A,2：B,3：C,4：D
        # region_source	是	int	4	1pc货主2app3微信端4pc前线后台5pc调度后台
        # company_id_number	是	string	32	三证合一号码
        # id_card_pic_m	是	string	64	身份证图片正面
        # id_card_pic_p	是	string	64	身份证图片反面
        # business	是	string	64	营业执照图片
        # business_2	是	string	64	危化品运输许可证图片
        # status	是	int	4	0待审核 1审核通过 2审核驳回-1已删除
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=13'
        f_headers = {"token": cookie}
        param = {"fleet_name": fleet_name, "address": address, "contact": contact, "contact_phone": contact_phone,
                 "admin_id": admin_id, "region_source": region_source, "id_card": id_card, "business_2": business_2,
                 "company_id_number": company_id_number, "id_card_pic_m": id_card_pic_m, "status": status,
                 "id_card_pic_p": id_card_pic_p, "business": business, "admin_user_id": admin_user_id,
                 "car_type": car_type, "password": password, "user_name": user_name, "admin_name": admin_name}
        MyLog().logger().info(param)
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_23(self, cookie, a):
        # 运单详情页
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=23'
        f_headers = {"token": cookie}
        param = {"a": a}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_47(self, cookie, a, b, c=None, e=None):
        # 获取货单中的运单列表
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	货单ID
        # c	否	string	24	当前调度uid
        # b	是	long	8	本地最小报价时间，默认0
        # e	否	string	24	车队名称
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=47'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b, "c": c, "e": e}
        if c is None:
            del param["c"]
        if e is None:
            del param["e"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_49(self, cookie, a, b):
        # 确认车辆
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	车单ID
        # b	是	int	4	类型	1:确认 2:拒绝 101后台取消
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=49'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_dispatchInfo(self, cookie):
        # 查询小五基本信息
        url = url_dispatch + 'dispatchInfo'
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_61(self, cookie, a, b, c=None, d=None):
        # 运单完成
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	运单ID
        # b	是	int	4	2结束
        # c	否	int	4	变动金额
        # d	否	String	512	备注	不超过100个字
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=61'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b, "c": c, "d": d}
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_64(self, cookie, a, d):
        # 批量定向询价
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源ID
        # d	是	array	--	车队id列表	[1,2,3....]
        # d	e	是	String	32	车队id
        # d	f	是	int	32	车队uid
        # d	g	是	int	32	车队调度uid
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=64'
        f_headers = {"token": cookie}
        param = {"a": a, "d": d}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_65(self, cookie, a, b, c, d):
        # 批量定向派单
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源ID
        # b	是	int	4	上报车数
        # c	是	int	4	报价金额
        # d	是	array	--	车队id列表	[1,2,3....]
        # d	e	是	String	32	车队id
        # d	f	是	int	32	车队uid
        # d	g	是	int	32	车队调度uid
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=65'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b, "c": c, "d": d}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 查询小五车队列表
    def dispatch_md_40_cmd_127(self, cookie, a, i, z, g=None, h=None, b=None, c=None, d=None, e=None, f=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源ID
        # b	是	String	24	车队名称
        # c	是	String	24	联系人姓名
        # d	是	String	24	联系人手机号
        # e	是	int	24	询价状态 0否1是
        # f	是	int	24	派单状态 0否1是
        # g	是	int	24	车队是否已自主报价 0否 1是
        # z	是	long	24	时间
        # h	是	String	24	货单小5关联id
        # i	是	int	24	查询类型 1询价 2报车
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=127'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h,
                 "i": i,
                 "z": z
                 }
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        if f is None:
            del param["f"]
        if g is None:
            del param["g"]
        if h is None:
            del param["h"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_md_40_cmd_142(self, cookie, a, b):
        # 车队司机列表
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=142'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待处理询价
    def dispatch_md_40_cmd_183(self, cookie, a, b, c, d, e, f):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	4	page
        # f	是	int	4	pageSize
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=183'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f
                 }
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待处理货单
    def dispatch_md_40_cmd_184(self, cookie, a, b, c, d, e, f, g, h):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	12	page
        # f	是	int	8	pageSize
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=184'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h
                 }
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待确认车辆
    def dispatch_md_40_cmd_185(self, cookie, a, b, c, d, e, f):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	4	page
        # f	是	int	4	pageSize
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=185'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f
                 }
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待处理询价
    def dispatch_md_40_cmd_200(self, cookie, d, e, f, a=None, b=None, c=None, g=None, t1=None, t2=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	4	page
        # f	是	int	4	pageSize
        # g	否	string	12	询价编码
        # t1	否	long	8	起始时间
        # t2	否	long	8	终止时间
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=200'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "t1": t1,
                 "t2": t2
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if g is None:
            del param["g"]
        if t1 is None:
            del param["t1"]
        if t2 is None:
            del param["t2"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待处理货单
    def dispatch_md_40_cmd_201(self, cookie, d, e, f, a=None, b=None, c=None, g=None, h=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	12	page
        # f	是	int	8	pageSize
        # g	是	int	8	来源 1询价 2报车
        # h	是	int	8	开票 0否 1是
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=201'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if g is None:
            del param["g"]
        if h is None:
            del param["h"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 待确认车辆
    def dispatch_md_40_cmd_202(self, cookie, e, f, d=0, a=None, b=None, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	4	page
        # f	是	int	4	pageSize
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=202'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 货单管理-进行中
    def dispatch_md_40_cmd_203(self, cookie, e, f, g, d=0, a=None, b=None, c=None, h=None, i=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	货单编号
        # b	否	string	12	装货地区
        # c	否	string	12	卸货地区
        # d	是	long	8	本地最小报价时间，默认0
        # e	是	int	4	page
        # f	是	int	4	pageSize
        # g	否	int	4	1进行中 2已完成
        # h	否	string	4	货主公司名称
        # i	否	int	4	联系人手机号
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=203'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h,
                 "i": i
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if h is None:
            del param["h"]
        if i is None:
            del param["i"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 小五报车列表
    def dispatch_md_40_cmd_204(self, cookie, e, f, g=None, a=None, b=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	车队名称
        # b	否	string	12	车牌号
        # e	是	int	4	page
        # f	是	int	4	pageSize
        # g	否	string	12	货单id
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=204'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "e": e,
                 "f": f,
                 "g": g
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if g is None:
            del param["g"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 小五报价
    def dispatch_md_40_cmd_205(self, cookie, a, b, c, e):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	货源id
        # b	是	int	12	报价金额
        # c	是	int	4	车数
        # e	是	String	32	询价编码
        url = url_dispatch + 'xf/sy/busi.do?md=40&cmd=205'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "e": e
                 }
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dispatch_getCarsByOrderId(self, cookie, order_id, type, time):
        # 运单详情页车辆列表
        url = url_dispatch + 'getCarsByOrderId'
        f_headers = {"token": cookie}
        param = {"variables": {"input": {"id": order_id, "type": type, "time": time}}}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response
