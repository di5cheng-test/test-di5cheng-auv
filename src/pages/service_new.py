# coding:utf-8
import requests
from src.common import config
from src.common.logger import MyLog
import random

global null
null = None

url_service = config.get_service_url()
log = MyLog()


class Service(object):
    def service_login(self, username, password):
        # 客服登录
        # 返回值是登录用的token
        url = url_service + 'xf/sy/busi.do?md=40&cmd=1'
        param = {"username": username, "password": password}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        log.logger().info(response)
        if "errors" in response:
            log.logger().info("登录失败")
            return response
        else:
            MyLog().logger().info("登录成功")
            return response["data"]["login"]

    def service_md_40_cmd_5(self, cookie, username=None):
        # 查询小五
        # username：小五名称
        url = url_service + 'xf/sy/busi.do?md=40&cmd=5'
        f_headers = {"token": cookie}
        param = {"status": 1, "region_source": 2, "username": username}
        if username is None:
            del param["username"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_6(self, cookie, goods_type, company_name, username, mobile, password, id_card_pic_m, id_card,
                            id_card_pic_p, business, business_2, business_3, admin_user_id, address, company_id_number,
                            admin_name, status, region_source):
        # 新增货主
        # 参数名	必选	类型	长度	描述	取值说明
        # company_name	是	string	64	公司全称
        # region_source	否	int	4	1pc货主2app3微信端4pc前线后台5pc调度后台
        # status	是	int	4	状态0待审核 1审核通过 2审核驳回 3资料不全待完善-1已禁用 后台修改需要传这个参数
        # long_contract_is_overdue	是	int	4	是否签署协议 0否 1是
        # user_id	是	int	4	用户登录id
        # username	否	string	32	联系人姓名
        # admin_user_id	是	int	4	调度客服uid
        # admin_name	是	string	24	后台客服姓名
        # password	否	string	64	密码
        # mobile	否	long	8	联系方式
        # id_card	否	string	32	身份证号码
        # address	否	string	64	公司地址
        # first_people	否	int	4	发展人
        # company_id_number	否	string	64	三证合一
        # id_card_pic_m	否	string	64	身份证图片正面
        # id_card_pic_p	否	string	64	身份证图片反面
        # business	否	string	64	营业执照
        # business_2	否	string	64	危化品运输许可证
        # business_3	否	string	64	银行开户许可证
        # birthday	否	long	8	生日
        # goods_type	否	int	4	公司性质 1厂家 2贸易商 3中介 4租户
        # gender	否	int	4	性别1女 2男
        url = url_service + 'xf/sy/busi.do?md=40&cmd=6'
        f_headers = {"token": cookie}
        param = {"goods_type": goods_type, "company_name": company_name, "username": username, "mobile": mobile,
                 "password": password, "id_card_pic_m": id_card_pic_m, "id_card_pic_p": id_card_pic_p,
                 "business": business, "business_2": business_2, "business_3": business_3, "address": address,
                 "admin_user_id": admin_user_id, "company_id_number": company_id_number, "id_card": id_card,
                 "admin_name": admin_name, "status": status, "region_source": region_source}
        print(param)
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_7(self, cookie, page, status, type=None, company_name=None):
        # 查询货主
        # 参数名	必选	类型	长度	描述	取值说明
        # company_name	否	string	64	公司名称
        # page	是	int	4	页码
        # status	是	int	4	状态0待审核 1审核通过 2审核驳回 3资料不全待完善-1已禁用 后台修改需要传这个参数
        # type	否	int	8	运单搜索时候用传1
        url = url_service + 'xf/sy/busi.do?md=40&cmd=7'
        f_headers = {"token": cookie}
        param = {"page": page, "company_name": company_name, "status": status, "type": type}
        if type is None:
            del param["type"]
        if company_name is None:
            del param["company_name"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_45(self, cookie, a):
        # 货源详情
        #  参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	货单ID
        url = url_service + 'xf/sy/busi.do?md=40&cmd=45'
        f_headers = {"token": cookie}
        param = {"a": a}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_52(self, cookie):
        # 客服信息
        url = url_service + 'xf/sy/busi.do?md=40&cmd=52'
        f_headers = {"token": cookie}
        param = {}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_60(self, cookie, a, b):
        # 货运报停结束
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货单ID
        # b	是	int	4	10报停20完结
        url = url_service + 'xf/sy/busi.do?md=40&cmd=60'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 货单货运列表
    def service_md_40_cmd_80(self, cookie, d, e, u, a=None, b=None, c=None, f=None, y=None, z=None, ab=None, ac=None,
                             ad=None, ae=None, af=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	12	装货地区
        # b	否	string	12	卸货地区
        # c	否	long	4	装货时间20190101
        # d	是	int	4	类型	1:在运 2:已完成
        # e	是	long	8	当前页
        # f	否	String	24	货主公司id
        # u	是	int	24	前线UID
        # y	否	String	24	货单编号
        # z	否	long	24	货主手机号
        # ab	否	String	24	货品名称
        # ac	否	long	24	装货时间起始时间
        # ad	否	long	24	装货时间结束时间
        # ae	否	long	24	装货地
        # af	否	long	24	卸货地
        url = url_service + 'xf/sy/busi.do?md=40&cmd=80'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "u": u,
                 "y": y,
                 "z": z,
                 "ab": ab,
                 "ac": ac,
                 "ad": ad,
                 "ae": ae,
                 "af": af
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if f is None:
            del param["f"]
        if y is None:
            del param["y"]
        if z is None:
            del param["z"]
        if ab is None:
            del param["ab"]
        if ac is None:
            del param["ac"]
        if ad is None:
            del param["ad"]
        if ae is None:
            del param["ae"]
        if af is None:
            del param["af"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_118(self, cookie, a, b, d, i, j, k, m, n, o, s, w, c=None, e=None, f=None, g=None, h=None,
                              l=None,
                              p=None, q=None, r=None, t=None, u=None, v=None, x=None, y=None, z=None, a1=None):
        # 参数名	必选	类型	长度	说明
        # a	是	string	4	公司id
        # b	是	int	4	1pc货主2车队app3微信端4pc前线后台5pc调度后台6 电子合同系统7财务系统
        # c	是	string	4	5城id （弃用）
        # e	是	int	4	5城签署人uid （弃用）
        # g	是	string	4	5城签署人开户ca id （弃用）
        # d	是	string	4	本方公司id
        # f	是	int	4	本方签署人uid
        # h	是	string	4	本方签署人开户id
        # i	否	string	4	货单号或者运单号
        # j	是	int	4	合同类别1框架合同2运单合同 3货单合同
        # k	是	string	64	本地合同html地址（线下多图片逗号隔开） （线下）
        # m	是	int	4	甲方0 待签署 1已签署
        # n	是	int	4	乙方0 待签署 1已签署
        # o	是	int	4	1线上 2线下
        # p	否	string	4	操作人uid 逗号隔开（非框架合同不用传）
        # s	是	string	24	本方公司名称
        # w	是	int	4	1长约2短约
        # l	否	long	4	生效日期 长约必传
        # q	否	long	4	失效日期 长约必传
        # u	是	int	4	提交人uid
        # v	是	string	4	提交人姓名
        # z	是	long	4	提交人手机号
        # t	是	string	4	本方签署人姓名（电子合同系统使用）
        # r	是	long	4	本方签署人手机号（电子合同系统使用）
        # x	是	int	4	1是（电子合同系统使用）
        # y	是	int	4	合同id（电子合同系统使用）
        # a1	是	string	4	合同编号（电子合同系统使用）
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i, "j": j, "k": k, "l": l, "m": m,
                 "n": n, "o": o, "p": p, "q": q, "r": r, "s": s, "t": t, "u": u, "v": v, "w": w, "x": x, "y": y, "z": z,
                 "a1": a1}
        if c is None:
            del param["c"]
        if e is None:
            del param["e"]
        if f is None:
            del param["f"]
        if g is None:
            del param["g"]
        if h is None:
            del param["h"]
        if l is None:
            del param["l"]
        if p is None:
            del param["p"]
        if q is None:
            del param["q"]
        if r is None:
            del param["r"]
        if t is None:
            del param["t"]
        if u is None:
            del param["u"]
        if v is None:
            del param["v"]
        if x is None:
            del param["x"]
        if y is None:
            del param["y"]
        if z is None:
            del param["z"]
        if a1 is None:
            del param["a1"]
        url = url_service + 'xf/sy/busi.do?md=40&cmd=118'
        f_headers = {"token": cookie}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_120(self, cookie, g, h, f=None):
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

    def service_md_40_cmd_123(self, cookie, a, b):
        # 获取客服审核对账单
        url = url_service + 'xf/sy/busi.do?md=123&cmd=123'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 发布询价货单
    def service_md_40_cmd_180(self, cookie, a, b, c, d, e, f, h, j, k, l, n, g=None, i=None, m=None, o=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	货单类型	1长途 2 短途
        # b	是	int	24	需求车数
        # c	是	String	5	询价装货地
        # d	是	String	5	询价卸货地
        # e	是	String	10	货品名称
        # f	是	int	24	是否开票	是否开发票0不开票 1开票 默认0
        # g	否	String	24	备注
        # h	是	[]	24	小五id集合
        # h	a	是	int	24	小五id
        # h	b	是	String	24	小五名称
        # i	否	int	24	是否全选	选择全选 传任意数字 无需传小五id集合 未选择不传
        # j	是	int	24	吨数
        # k	是	int	24	前线id
        # l	是	int	24	来源	来源1pc货主2app3微信端4pc前线后台5pc调度后台
        # m	否	String	24	账期
        # n	是	int	24	装货时间
        # o	否	String	24	备注2
        url = url_service + 'xf/sy/busi.do?md=40&cmd=180'
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
                 "j": j,
                 "k": k,
                 "l": l,
                 "m": m,
                 "n": n,
                 "o": o
                 }
        if g is None:
            del param["g"]
        if i is None:
            del param["i"]
        if m is None:
            del param["m"]
        if o is None:
            del param["o"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 代办事项-询价列表
    def service_md_40_cmd_183(self, cookie, h, i, a=None, b=None, c=None, d=None, e=None, f=None, g=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	String	24	货单编号
        # b	否	String	24	货主ID
        # c	否	long	24	联系人手机号
        # d	否	String	24	装货地
        # e	否	String	24	卸货地
        # f	否	long	24	装货时间起始时间
        # g	否	long	24	装货时间结束时间
        # h	否	int	24	起始页
        # i	是	int	24	前线uid
        url = url_service + 'xf/sy/busi.do?md=40&cmd=183'
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
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        if f is None:
            del param["f"]
        if g is None:
            del param["g"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 车队报价列表
    def service_md_40_cmd_184(self, cookie, a, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货单id
        # b	是	int	24	起始页
        url = url_service + 'xf/sy/busi.do?md=40&cmd=184'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 货单询价详情
    def service_md_40_cmd_185(self, cookie, a):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	String	24	货单id
        url = url_service + 'xf/sy/busi.do?md=40&cmd=185'
        f_headers = {"token": cookie}
        param = {"a": a}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 询价管理-询价列表
    def service_md_40_cmd_186(self, cookie, f, h, a=None, b=None, c=None, d=None, e=None, i=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	String	24	询价单编号
        # b	否	long	50	装货(询价)时间开始
        # c	否	long	50	装货(询价)时间结束
        # d	否	String	24	装货地
        # e	否	String	24	卸货地
        # f	是	int	50	页数
        # h	是	int	50	前线客服id
        # i	否	int	24	0：询价待处理；1：询价已处理 2:已取消 默认:0
        url = url_service + 'xf/sy/busi.do?md=40&cmd=186'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "h": h,
                 "i": i
                 }
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        if i is None:
            del param["i"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 代办事项-询价列表
    def service_md_40_cmd_187(self, cookie, a, b, c, d, e, f, g, i, j, k, l, m, n, o, p, q, r, v, x, z, ab, ac, ae, ah,
                              aj, w=None, af=None, ak=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        # b	是	int	24	发货类型	发货类型：1长途 2短途
        # c	是	int	24	结算方式	1 装货磅单 2卸货磅单
        # d	是	int	24	下家是否开票	0不开票 1开票 默认0
        # e	是	String	24	发货装货地
        # f	是	String	24	发货卸货地
        # g	是	int	24	商品单价
        # i	是	String	24	装货地
        # j	是	String	24	装货地详细地址
        # k	是	String	24	卸货地
        # l	是	String	24	卸货地详细地址
        # m	是	long	24	装货时间
        # n	是	int	24	承担损耗
        # o	是	int	24	发货吨数KG
        # p	是	int	24	上家运价 货主价格
        # q	是	int	24	上家是否开票	0不开票 1开票 默认0
        # r	是	int	24	下家运价 车队价格
        # v	是	String	24	备注
        # w	否	String	24	车队公司id
        # x	是	String	24	车队报价id
        # z	是	int	24	车队报价
        # ab	是	String	24	货主公司id
        # ac	是	int	24	需求车数
        # ae	是	String	24	账期
        # ah	是	String	24	货主公司名称
        # af	否	String	24	备注2
        # aj	是	[]	24	小五id集合
        # ak	否	int	24	是否全选	选择全选 传任意数字 无需传小五id集合 未选择不传
        url = url_service + 'xf/sy/busi.do?md=40&cmd=187'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "i": i,
                 "j": j,
                 "k": k,
                 "l": l,
                 "m": m,
                 "n": n,
                 "o": o,
                 "p": p,
                 "q": q,
                 "r": r,
                 "v": v,
                 "ac": ac,
                 "ae": ae,
                 "ah": ah,
                 "aj": aj,
                 "w": w,
                 "x": x,
                 "z": z,
                 "ab": ab,
                 "af": af,
                 "ak": ak}
        if w is None:
            del param["w"]
        if af is None:
            del param["af"]
        if ak is None:
            del param["ak"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_188(self, cookie, a):
        # 询价管理-结束询价
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        url = url_service + 'xf/sy/busi.do?md=40&cmd=188'
        f_headers = {"token": cookie}
        param = {"a": a}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    def service_md_40_cmd_189(self, cookie, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, r, y, z, ab=None, af=None,
                              q=None, t=None, u=None, x=None, w=None, s=None):
        # 发布报车货单
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	货单类型	1长途 2 短途
        # b	是	String	24	货主id
        # c	是	String	5	装货地
        # d	是	String	5	卸货地
        # e	是	long	15	装货时间
        # f	是	String	10	货品名称
        # g	是	String	5	发货装货地
        # h	是	int	10	发货吨数
        # i	是	int	10	需求车数
        # j	是	int	10	承担损耗比例	损耗 1、2、3 分别表示千1、千2、千3 大于10表示kg
        # k	是	String	5	发货卸货地
        # l	是	int	10	上家运价 货主价格
        # m	是	int	10	上家是否开票	发票类型 0不开票 1开票 默认0
        # n	是	int	10	下家运价 车队价格
        # o	是	int	10	下家是否开票	发票类型 0不开票 1开票 默认0
        # p	是	int	10	商品单价
        # q	否	String	10	备注
        # r	是	[]	24	小五id集合
        # s	否	int	24	是否全选	选择全选 传任意数字 无需传小五id集合 未选择不传
        # t	否	String	24	详细装货地
        # u	否	String	24	详细卸货地
        # x	否	int	24	前线uid
        # y	是	String	24	货主公司名称
        # z	是	int	24	来源	来源1pc货主2app3微信端4pc前线后台5pc调度后台
        # w	否	String	24	账期
        # ab	否	int	24	结算方式	1 装货磅单 2卸货磅单
        # af	否	String	24	备注2
        url = url_service + 'xf/sy/busi.do?md=40&cmd=189'
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
                 "j": j,
                 "k": k,
                 "l": l,
                 "m": m,
                 "n": n,
                 "o": o,
                 "p": p,
                 "q": q,
                 "r": r,
                 "s": s,
                 "t": t,
                 "u": u,
                 "w": w,
                 "x": x,
                 "y": y,
                 "z": z,
                 "ab": ab,
                 "af": af
                 }
        if q is None:
            del param["q"]
        if s is None:
            del param["s"]
        if t is None:
            del param["t"]
        if u is None:
            del param["u"]
        if x is None:
            del param["x"]
        if w is None:
            del param["w"]
        if ab is None:
            del param["ab"]
        if af is None:
            del param["af"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 常用地址列表
    def service_md_40_cmd_190(self, cookie, a, b, c, d=None, e=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线uid
        # b	是	int	24	类型	1 装货 2卸货
        # c	是	int	24	地址类型	1 三级联动地址 2发货地址
        # d	否	String	24	地址模糊搜索
        # e	是	int	24	起始页
        url = url_service + 'xf/sy/busi.do?md=40&cmd=190'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b, "c": c, "d": d, "e": e}
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 前线常用地址新增
    def service_md_40_cmd_207(self, cookie, a, b=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线跟单id
        # b	否	String	50	货品名
        url = url_service + 'xf/sy/busi.do?md=40&cmd=207'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        if b is None:
            del param["b"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

        # 货源详情车辆列表

    def service_md_40_cmd_210(self, cookie, a, b, c, e, d=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        # b	是	int	24	车辆状态	101取消 1待确认 3 (3已确认 7运输中 9运输完毕)
        # c	是	int	24	页数
        # d	否	String	24	车牌号
        # e	是	int	24	1:搜索 2:下载
        url = url_service + 'xf/sy/busi.do?md=40&cmd=210'
        f_headers = {"token": cookie}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e}
        if d is None:
            del param["d"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 批量确认车辆
    def service_md_40_cmd_212(self, cookie, a, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	[]	24	数据集合
        # a	a	是	string	24	车单ID
        # a	b	是	int	4	类型	1:确认 2:拒绝 101后台取消
        url = url_service + 'xf/sy/busi.do?md=40&cmd=212'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
        return response

    # 前线常用地址新增
    def service_md_40_cmd_220(self, cookie, a, b, c, d, e):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线uid
        # b	是	int	24	类型	1 装货 2卸货
        # c	是	String	24	三级联动地址
        # d	是	String	24	详细地址
        # e	是	int	24	1三级联动地址
        url = url_service + 'xf/sy/busi.do?md=40&cmd=220'
        f_headers = {"token": cookie}
        param = {"a": a, "b": b, "c": c, "d": d, "e": e}
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        log.logger().info(response)
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

    def service_md_120_cmd_120(self, cookie, g, h, f=None):
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
