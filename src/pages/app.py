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

    def app_login_param(self, username, password):
        param = "{w:%s,i:192.168.4.114,d:94-DE-80-77-81-F1,p:100,h:3,o:1,c:4,e:%s,l:1}" % (password, username)
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

    def manifest_list_param(self, b):
        # b：时间戳
        param = {"b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def manifest_list(self, library, param):
        # app 获取货源信息列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x10, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x10)
        return response

    def enterprise_info_param(self):
        c_param = bytes('', encoding="utf-8")
        return c_param

    def enterprise_info(self, library, param):
        # 获取认证信息
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x17, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x17)
        return response

    def goods_report_param(self, a, b, c, d):
        param = {"a": a,  # a:货品ID
                 "b": b,  # b:上报价格
                 "c": c,  # c:上报车数
                 "d": d  # d:车队id
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def goods_report(self, library, param):
        # app 货源报价
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 33, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=33)
        return response

    def my_report_list_param(self, a, b):
        param = {"a": a,  # a:车队id
                 "b": b  # b:时间戳
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def my_report_list(self, library, param):
        # app 我的报价列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x22, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x22)
        return response

    def transport_list_param(self, a, b, c):
        param = {"a": a,  # a:车队id
                 "b": b,  # b:时间戳
                 "c": c  # c:运单状态 1：运输中; 10：已完成
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def transport_list(self, library, param):
        # app 我的运单列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x19, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x19)
        return response

    def waillbill_report_car_param(self, a, d, e):
        param = {"a": a,  # a:运单id
                 "d": d,  # b:车队id
                 "e": e  # e:司机列表
                 }
        # car_param参考格式
        # e =     (
        #                 {
        #             b = 5ceb5b88743a4920b1c25fce;// 车辆id
        #             c = 407606;// 司机id
        #         },
        #                 {
        #             b = 5ceb4168743a49698ec5f03f;
        #             c = 407578;
        #         }
        #     )
        c_param = bytes(json.dumps(param), encoding="utf-8")
        print(c_param)
        return c_param

    def waillbill_report_car(self, library, param):
        # app 上报车辆
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x25, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x25)
        return response

    def my_truck_list_param(self, b, a):
        param = {"a": a,  # a:时间戳
                 "b": b  # b:车队id
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def my_truck_list(self, library, param):
        # app 我的车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x15, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x15)
        return response

    def delete_truck_param(self, a, b):
        param = {"a": a,  # a:车队id
                 "b": b  # b:车辆id
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def delete_truck(self, library, param):
        # app 删除车辆
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x16, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x16)
        return response

    def transport_detail_param(self, a):
        param = {"a": a}  # 运单id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def transport_detail(self, library, param):
        # app 运单详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x1C, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x1C)
        return response

    def event_report_param(self, a, b, c, d, f, g, j, h, k, ea, eb):
        param = {
            "a": a,  # 运单id
            "b": b,  # 事件类型 1：一般 2：严重 3：紧急
            "c": c,  # 语音文件ID
            "d": d,  # 文字描述
            "f": f,  # 经纬度，维度在前
            "g": g,  # 当前地址
            "j": j,  # 车牌号
            "h": h,  # 当前用户手机号码
            "k": k,  # 当前用户昵称
            "e": [{"a": ea,  # 上传文件ID
                   "b": eb  # 上传文件类型 1：图片 2：视频
                   }]}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def event_report(self, library, param):
        # app 故障事件上传
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x23, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x23)
        return response

    def loading_unload_upload_param(self, a, b, c, d, e):
        param = {
            "a": a,  # 运单id
            "b": b,  # 装货磅单id
            "c": c,  # 装货磅单数值
            "d": d,  # 卸货磅单
            "e": e,  # 卸货磅单数值
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def loading_unload_upload(self, library, param):
        # app 上传装卸货磅单
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 26, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=26)
        return response

    def waillbill_agree_param(self, a):
        param = {"a": a}  # 承运车辆运输id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def waillbill_agree(self, library, param):
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 39, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=39)
        return response

    def loading_unload_info_param(self, a):
        param = {"a": a}  # 承运车辆运输id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def loading_unload_info(self, library, param):
        # app 装卸货磅单查询
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 27, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=27)
        return response

    def enter_driver_info_param(self, a, b, c, d, e, f, g):
        param = {"a": a,  # 车队id
                 "b": b,  # 司机姓名
                 "c": c,  # 手机号码
                 "d": d,  # 身份证
                 "e": e,  # 车牌号码
                 "f": f,  # 挂车牌号码
                 "g": g  # 荷载吨数
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def enter_driver_info(self, library, param):
        # app 添加车辆
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x28, 0x13, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=0x13)
        return response

    def addBank_param(self, a, b, c, d, e):
        param = {"a": a,  # 车队id
                 "b": b,  # 图片id
                 "c": c,  # 开户名称
                 "d": d,  # 开户账号
                 "e": e,  # 开户行
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def addBankaccount(self, library, param):
        # app 增加收款银行账户列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 56, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=56)
        return response

    def getBankList_params(self, a):
        param = {"a": a}  # 车队id
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def getBankList(self, library, param):
        # app 获取银行账户列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 57, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=57)
        return response

    def apply_recon_fleet_params(self, a, b):
        param = {"a": a,  # 运单id
                 "b": b  # 账户编号
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def apply_recon_fleet(self, library, param):
        # app 发起对账
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 42, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=42)
        return response

    def app_apply_contract_param(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z,
                                 a1):
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

    def app_apply_contract(self, library, param):
        # app 确认生成合同
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 118, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=118)
        return response

    def app_carlist_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	8	本地时间戳
        # c	否	string	12	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_carlist(self, library, param):
        # app 车队车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 164, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=164)
        return response

    def app_carinfo_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	string	12	车辆id
        # c	否	string	12	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_carinfo(self, library, param):
        # app 车队车辆详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 160, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=160)
        return response

    def app_add_car_param(self, a, b, c, d, e, f, o, g, h, i, j, k, l, p, m, n, r, q):
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

    def app_add_car(self, library, param):
        # app 添加车辆
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 161, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=161)
        return response

    def app_carinfo_list_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	long	8	本地时间戳
        # b	是	string	12	车队id
        # c	否	string	12	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_carinfo_list(self, library, param):
        # app 车队车辆详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 164, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=164)
        return response

    def app_add_gua_car_param(self, a, b, c, d, e, f, o, g, h, i, j, k, l, p, m, n, r, q, t):
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

    def app_add_gua_car(self, library, param):
        # app 添加挂车
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 165, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=165)
        return response

    def app_gua_carinfo_list_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	4	车队id
        # b	是	long	8	本地时间戳
        # c	否	string	12	挂车号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_gua_carinfo_list(self, library, param):
        # app 挂车车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 169, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=169)
        return response

    def app_add_driver_param(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, r):
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

    def app_add_driver(self, library, param):
        # app 添加司机
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 170, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=170)
        return response

    def app_driverinfo_list_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	8	本地时间戳
        # c	否	long	8	手机号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_driverinfo_list(self, library, param):
        # app 车队车辆详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 174, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=174)
        return response

    def app_add_driver_ya_param(self, a, b, c, d, e, f, r):
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

    def app_add_driver_ya(self, library, param):
        # app 添加押运员
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 176, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=176)
        return response

    def app_ya_driverinfo_list_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	8	本地时间戳
        # c	否	long	8	手机号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_ya_driverinfo_list(self, library, param):
        # app 押运员列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 184, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=184)
        return response

    def app_add_capacity_param(self, a, b, c, d, e, f, g):
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

    def app_add_capacity(self, library, param):
        # app 添加运力
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 180, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=180)
        return response

    def app_capacitylist_param(self, a, b, c=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	string	12	车队id
        # b	是	long	24	本地时间戳
        # c	否	string	24	车牌号
        param = {"a": a, "b": b, "c": c}
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def app_capacitylist(self, library, param):
        # app 运力列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 181, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=181)
        return response
