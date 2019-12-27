# coding:utf-8
from threading import Event
from ctypes import *
from src.common.logger import MyLog
import json
import time

response = {}
event = Event()
c_back = bytes('               ', encoding="utf-8")


class Common(object):
    def sdk_callback(self, iMid, iCmd, iErr, pBody, pMsgID, iLen):
        param = {"iMid": iMid,
                 "iCmd": iCmd,
                 "iErr": iErr,
                 "pBody": pBody.decode('utf-8'),
                 "pMsgID": pMsgID,
                 "iLen": iLen
                 }
        global response
        response = param
        if param["iMid"] != 0:
            event.set()

    def get_response(self, iCmd):
        global response
        for n in range(20):
            result = response
            MyLog().logger().info(result)
            if result["iCmd"] != iCmd:
                time.sleep(1)
                continue
            else:
                return result

    CMPRESULTFUNC = CFUNCTYPE(None, c_int, c_int, c_int, c_char_p, c_char_p, c_int)
    CMPRESULTFUNC.restype = c_char_p
    pResutFunc = CMPRESULTFUNC(sdk_callback)

    def initSDK(self, library, init_info):
        library.InitSDK.argtype = c_char_p
        library.InitSDK(init_info)
        library.SetNetState(1)
        library.RegistNotifyCallBack.restype = c_char_p
        global pResutFunc
        pResutFunc = self.CMPRESULTFUNC(self.sdk_callback)
        library.RegistNotifyCallBack(pResutFunc)

    def app_regist_param(self, phone, password, name, code, deviceuuid=None):
        if deviceuuid is None:
            param = {"m": phone, "w": password, "n": name, "c": code, "a": "9417B966-5CC6-4E54-A32A-CB9D06FC2CA1"}
        else:
            param = {"m": phone, "w": password, "n": name, "c": code, "a": deviceuuid}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_regist(self, library, param):
        # app调注册接口
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x06, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x06)
        return response

    def app_code_param(self, phone):
        param = {"m": phone, "p": 100, "n": 3, "o": 1, "c": 3}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_code(self, library, param):
        # app获取短信验证码
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x04, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x04)
        return response

    def app_login_param(self, username, password):
        param = "{w:%s,i:192.168.4.114,d:94-DE-80-77-81-F1,p:100,h:3,o:1,c:2,e:%s,l:1}" % (password, username)
        c_param = bytes(param, encoding="utf-8")
        return c_param

    def app_login(self, library, param):
        # app调登录接口
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x01, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x01)
        return response

    def app_login_out_param(self):
        param = ""
        c_param = bytes(param, encoding="utf-8")
        return c_param

    def app_login_out(self, library, param):
        # app退出登录接口
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x12, 0x02, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x02)
        return response

    def auv_param_md_40_cmd_4(self, a):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	货单ID
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_4(self, library, param):
        # 货源详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 4, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=4)
        return response

    def auv_param_md_40_cmd_16(self, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # b	是	long	8	本地最小时间戳，默认0
        param = {"b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_16(self, library, param):
        # 货源列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 16, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=16)
        return response

    def auv_param_md_40_cmd_17(self, e, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # z	是	long	8	运单ID
        # b	是	long	8	时间戳，默认0
        param = {"e": e, "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_17(self, library, param):
        # 详情车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 17, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=17)
        return response

    def auv_param_md_40_cmd_23(self):
        c_param = bytes('', encoding="utf-8")
        return c_param

    def auv_md_40_cmd_23(self, library, param):
        # 获取认证信息
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 23, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=23)
        return response

    def auv_param_md_40_cmd_24(self, b, k, d, e, f, g, h, i, j, c):
        param = {"k": k, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i, "j": j, "c": c, "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_24(self, library, param):
        # 上传认证资料
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 24, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=24)
        return response

    def auv_param_md_40_cmd_25(self, a, b, c):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	32	车队id
        # b	是	long	8	本地最小时间戳，默认0
        # c	是	int	8	运单状态 1:进行中;2:结束;3:未签订协议;4:结算中;5:待付款;6:付款结算;7:异常;10:运单对账结束
        param = {"a": a, "b": b, "c": c}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_25(self, library, param):
        # 运单列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 25, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=25)
        return response

    def auv_param_md_40_cmd_26(self, a, b, c, d, e):
        param = {
            "a": a,  # 运单id
            "b": b,  # 装货磅单
            "c": c,  # 装货磅单数值
            "d": d,  # 卸货磅单
            "e": e,  # 卸货磅单数值
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_26(self, library, param):
        # app 上传装卸货磅单
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 26, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=26)
        return response

    def auv_param_md_40_cmd_27(self, a):
        param = {"a": a}  # 承运车辆运输id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_27(self, library, param):
        # app 装卸货磅单查询
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 27, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=27)
        return response

    def auv_param_md_40_cmd_28(self, a):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	运单ID
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_28(self, library, param):
        # 运单详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 28, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=28)
        return response

    def auv_param_md_40_cmd_33(self, a, b, c, d):
        param = {"a": a,  # a:货品ID
                 "b": b,  # b:上报价格
                 "c": c,  # c:上报车数
                 "d": d  # d:车队id
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_33(self, library, param):
        # app 货源报价
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 33, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=33)
        return response

    def auv_param_md_40_cmd_34(self, a, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	8	车队id
        # b	是	long	8	本地最小时间戳，默认0
        param = {"a": a, "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_34(self, library, param):
        # 车队货源列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 34, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=34)
        return response

    def auv_param_md_40_cmd_39(self, a):
        param = {"a": a}  # 承运车辆运输id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_39(self, library, param):
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 39, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=39)
        return response

    def auv_param_md_40_cmd_42(self, a, b):
        param = {"a": a,  # 运单id
                 "b": b  # 账户编号
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_42(self, library, param):
        # app 发起对账
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 42, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=42)
        return response

    def auv_param_md_40_cmd_53(self, a):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	货单ID
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_53(self, library, param):
        # 车队货源详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 53, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=53)
        return response

    def auv_param_md_40_cmd_56(self, a, b, c, d, e):
        param = {"a": a,  # 车队id
                 "b": b,  # 图片id
                 "c": c,  # 开户名称
                 "d": d,  # 开户账号
                 "e": e,  # 开户行
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_56(self, library, param):
        # app 增加收款银行账户列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 56, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=56)
        return response

    def auv_param_md_40_cmd_57(self, a):
        param = {"a": a}  # 车队id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_57(self, library, param):
        # app 获取银行账户列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 57, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=57)
        return response

    def auv_param_md_40_cmd_69(self, a, b, c):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	货源ID
        # b	是	string	24	车队ID
        # c	否	--	0..10]	数据列表
        # c	d	是	string	24	车辆ID
        # c	e	是	int	6	司机ID
        param = {"a": a, "b": b, "c": c}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_69(self, library, param):
        # 货源报车
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 69, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=69)
        return response

    def auv_param_md_40_cmd_71(self, a, b, c):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	32	姓名
        # b	是	long	8	手机号
        # c	是	string	32	车队id
        param = {"a": a, "b": b, "c": c}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_71(self, library, param):
        # App车队调度新增
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 71, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=71)
        return response

    def auv_param_md_40_cmd_73(self, a, b):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	long	8	本地最小时间戳，默认0
        # b	是	string	24	车队id
        param = {"a": a, "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_73(self, library, param):
        # App车队成员列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 73, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=73)
        return response

    def auv_param_md_40_cmd_117(self, a, b, c, d=None):
        # 上级元素	参数名	必选	类型	长度	说明
        # a	是	string	64	公司id
        # b	是	long	8	本地最小时间戳，默认0
        # c	是	int	4	1线上 2线下
        # d	是	int	4	0待签署1已签署 线下不需要
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d}
        if d is None:
            del param["d"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_117(self, library, param):
        # App合同列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 117, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=117)
        return response

    def auv_param_md_40_cmd_118(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, a1):
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
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_118(self, library, param):
        # app 确认生成合同
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 118, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=118)
        return response

    def auv_param_md_40_cmd_161(self, a, b, c, d, e, f, o, g, h, i, j, k, l, p, m, n, r, q):
        # 参数名	必选	类型	长度	描述
        # a	是	string	12	车牌号
        # b	是	int	4	车辆类型 1 重型半挂牵引车2中型半挂牵引车3轻型半挂牵引车
        # c	否	string	8	车辆道路运输证正面
        # d	否	string	4	代理证正面
        # e	否	string	4	代理证反面
        # f	否	long	32	运输证证件有效起始日期
        # o	否	long	32	运输证证件有效截止日期
        # g	否	string	8	车辆行驶证正本正面
        # h	否	string	4	车辆行驶证正本反面
        # i	否	string	4	车辆行驶证副本正面
        # j	否	string	4	车辆行驶证副本反面
        # k	否	string	4	车辆识别代码
        # l	否	long	4	行驶证证件起始有效期
        # p	否	long	4	行驶证证件截止有效期
        # m	否	string	4	挂车id
        # n	是	string	4	车队id
        # r	是	int	4	保存2 提交0
        # q	是	int	4	来源1安卓2ios3小五pc
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "o": o, "g": g, "h": h, "i": i, "j": j, "k": k, "l": l,
                 "p": p, "m": m, "n": n, "r": r, "q": q}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_161(self, library, param):
        # app 添加车辆
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 161, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=161)
        return response

    def auv_param_md_40_cmd_164(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	long	8	本地时间戳
        # b	是	string	12	车队id
        # c	否	string	12	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_164(self, library, param):
        # app 车队车辆详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 164, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=164)
        return response

    def auv_param_md_40_cmd_165(self, a, b, c, d, e, f, o, g, h, i, j, k, l, p, m, n, r, q, t):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	挂车号
        # b	是	int	4	罐体类型 1铁罐2不锈钢罐3铝合金罐4内衬塑罐
        # c	否	string	8	车辆道路运输证正面
        # d	否	string	4	代理证正面
        # e	否	string	4	代理证反面
        # f	否	long	32	运输证证件有效起始日期
        # o	否	long	32	运输证证件有效截止日期
        # g	否	string	8	车辆行驶证正本正面
        # h	否	string	4	车辆行驶证正本反面
        # i	否	string	4	车辆行驶证副本正面
        # j	否	string	4	车辆行驶证副本反面
        # k	否	string	4	车辆识别代码
        # l	否	long	4	行驶证证件起始有效期
        # p	否	long	4	行驶证证件截止有效期
        # n	是	string	4	车队id
        # r	是	int	4	保存2 提交0
        # m	是	int	4	荷载吨数
        # q	是	int	4	来源 来源1安卓2ios3小五pc
        # t	是	string	4	1上装口 2下装口可多选 字符串形式给我比如"1"或者"1,2"
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "o": o, "g": g, "h": h, "i": i, "j": j, "k": k, "l": l,
                 "p": p, "m": m, "n": n, "r": r, "q": q, "t": t}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_165(self, library, param):
        # app 添加挂车
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 165, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=165)
        return response

    def auv_param_md_40_cmd_169(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	4	车队id
        # b	是	long	8	本地时间戳
        # c	否	string	12	挂车号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_169(self, library, param):
        # app 挂车车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 169, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=169)
        return response

    def auv_param_md_40_cmd_170(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, r):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	司机姓名
        # b	是	string	4	身份证号
        # c	否	long	8	手机号
        # d	否	string	4	驾驶证正本正面
        # e	否	string	4	驾驶证副本正面
        # f	否	long	32	驾驶证件效起始有日期
        # g	否	long	32	驾驶证件效截止有日期
        # h	否	string	8	从业资格证正面
        # i	否	string	4	从业资格证号
        # j	否	long	4	行驶证证件起始有效期
        # k	否	long	4	行驶证证件截止有效期
        # l	是	string	4	车队id
        # m	否	string	4	押运证图片(兼押运员时上传）
        # n	否	long	32	押运证起始有效日期(兼押运员时上传）
        # o	否	long	32	押运证截止有效日期(兼押运员时上传）
        # r	是	int	4	保存2 提交0
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i, "j": j, "k": k, "l": l, "m": m,
                 "n": n, "o": o, "r": r}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_170(self, library, param):
        # app 添加司机
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 170, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=170)
        return response

    def auv_param_md_40_cmd_174(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	8	本地时间戳
        # c	否	long	8	手机号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_174(self, library, param):
        # app 车队车辆详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 174, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=174)
        return response

    def auv_param_md_40_cmd_176(self, a, b, c, d, e, f, r):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	押运员姓名
        # b	否	long	8	手机号
        # c	否	string	4	押运证图片
        # d	否	long	32	押运证起始有效日期
        # e	否	long	32	押运证截止有效日期
        # f	否	string	4	车队id
        # r	否	int	4	保存2 提交0
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "r": r}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_176(self, library, param):
        # app 添加押运员
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 176, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=176)
        return response

    def auv_param_md_40_cmd_180(self, a, b, c, d, e, f, g):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车辆id
        # b	是	string	4	挂车号id
        # c	是	int	8	司机id
        # d	是	int	8	押运员id
        # e	是	string	4	车队id
        # f	是	string	4	司机uid
        # g	是	string	4	押运员uid
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_180(self, library, param):
        # app 添加运力
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 180, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=180)
        return response

    def auv_param_md_40_cmd_181(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	24	本地时间戳
        # c	否	string	24	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_181(self, library, param):
        # app 运力列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 181, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=181)
        return response

    def auv_param_md_40_cmd_184(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	8	本地时间戳
        # c	否	long	8	手机号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_184(self, library, param):
        # app 押运员列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 184, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=184)
        return response
