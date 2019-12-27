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

    def auv_param_md_40_cmd_10(self, a, b):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	string	24	车单ID
        # b	是	int	4	类型	1:确认 2:取消
        param = {"a": a, "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_10(self, library, param):
        # app退出登录接口
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 10, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=10)
        return response

    def auv_param_md_41_cmd_80(self, a, b, c, d, e, f, h, j, k, l, n, o=None, g=None, i=None, m=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
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
        # o	是	int	24	备注2
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
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_80(self, library, param):
        # 发布询价货单
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 80, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=80)
        return response

    def auv_param_md_41_cmd_81(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, r, y, z, q=None, s=None, t=None,
                               u=None, x=None, w=None, ab=None, af=None):
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
                 "af": af}
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
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_81(self, library, param):
        # 发布报车货单
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 81, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=81)
        return response

    def auv_param_md_41_cmd_82(self, a, b, c, e, d=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线uid
        # b	是	int	24	类型	1 装货 2卸货
        # c	是	int	24	地址类型	1 三级联动地址 2发货地址
        # d	否	String	24	地址模糊搜索
        # e	是	int	24	起始页
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e}
        if d is None:
            del param["d"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_82(self, library, param):
        # 前线常用地址列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 82, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=82)
        return response

    def auv_param_md_41_cmd_83(self, a, b=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	类型	1pc前线后台2pc小五
        # b	否	string	24	小五名称
        param = {"a": a,
                 "b": b}
        if b is None:
            del param["b"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_83(self, library, param):
        # 后台客服列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 83, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=83)
        return response

    def auv_param_md_41_cmd_84(self, a):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	否	String	24	货单id
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_84(self, library, param):
        # 报价列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 84, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=84)
        return response

    def auv_param_md_41_cmd_85(self, a, b):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源ID
        # b	是	int	24	前线用户Uid
        param = {"a": a,
                 "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_85(self, library, param):
        # 询价详情
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 85, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=85)
        return response

    def auv_param_md_41_cmd_86(self, a, b, c, d, e, f, g, i, j, k, l, m, n, o, p, q, r, v, x, z, ab, ac, ae, ah, aj,
                               w=None, af=None, ak=None):
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
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_86(self, library, param):
        # 立即报车
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 86, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=86)
        return response

    def auv_param_md_41_cmd_88(self, a):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	int	50	前线uid
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_88(self, library, param):
        # 查看前线带处理报价条数
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 88, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=88)
        return response

    def auv_param_md_41_cmd_96(self, f, h, a=None, b=None, c=None, e=None, d=None, i=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	否	String	24	询价单编号
        # b	否	long	50	装货(询价)时间开始
        # c	否	long	50	装货(询价)时间结束
        # d	否	String	24	装货地
        # e	否	String	24	卸货地
        # f	是	int	50	页数
        # h	是	int	50	前线客服id
        # i	否	int	24	0：询价待处理；1：询价已处理 2:已取消 默认:0
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "h": h,
                 "i": i}
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
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_96(self, library, param):
        # 询价管理-询价列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 96, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=96)
        return response

    def auv_param_md_41_cmd_97(self, b, c, d, a=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	否	String	50	公司名称
        # b	是	int	50	用户登录id
        # c	是	int	8	页数
        # d	是	int	8	每页条数
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d}
        if a is None:
            del param["a"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_97(self, library, param):
        # 货主公司列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 97, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=97)
        return response

    def auv_param_md_41_cmd_112(self, a, b, d, e, f):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        # b	是	int	24	最新定价
        # d	是	String[]	24	小五id集合	a:小五id b:小五名称
        # e	是	int	24	报车状态	1:继续报车 2 : 加价报车
        # f	是	int	24	前线跟单id
        param = {"a": a,
                 "b": b,
                 "d": d,
                 "e": e,
                 "f": f}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_112(self, library, param):
        # 继续报车
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 112, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=112)
        return response

    def auv_param_md_41_cmd_113(self, a, b):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        # b	是	int	24	页数
        param = {"a": a,
                 "b": b}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_113(self, library, param):
        # 定价发单记录
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 113, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=113)
        return response

    def auv_param_md_41_cmd_114(self, a, b=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线跟单id
        # b	否	String	50	货品名
        param = {"a": a,
                 "b": b}
        if b is None:
            del param["b"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_114(self, library, param):
        # 常用货品名称
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 114, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=114)
        return response

    def auv_param_md_41_cmd_115(self, a=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	否	string	50	货品名称
        if a is None:
            param = {}
        else:
            param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_115(self, library, param):
        # 货品名称列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 115, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=115)
        return response

    def auv_param_md_41_cmd_116(self, a):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	string	50	货品名称
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_116(self, library, param):
        # 常用小五列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 116, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=116)
        return response

    def auv_param_md_41_cmd_117(self, a, b, c, e, d=None):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货源id
        # b	是	int	24	车辆状态	101取消 1待确认 3 (3已确认 7运输中 9运输完毕)
        # c	是	int	24	页数
        # d	否	String	24	车牌号
        # e	是	int	24	1:搜索 2:下载
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e}
        if d is None:
            del param["d"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_117(self, library, param):
        # 货源详情车辆列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 117, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=117)
        return response

    def auv_param_md_41_cmd_128(self, a):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	货单id
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_128(self, library, param):
        # 查看跟单小五
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 128, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=128)
        return response

    def auv_param_md_41_cmd_133(self, a, b, c, d):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	地址id
        # b	是	int	24	类型	1 装货 2卸货
        # c	是	String	24	三级联动地址
        # d	是	String	24	详细地址
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_133(self, library, param):
        # 编辑小五常用地址
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 133, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=133)
        return response

    def auv_param_md_41_cmd_134(self, a):
        # 参数名	必选	类型	长度	描述	取值说明
        # a	是	String	24	地址id
        param = {"a": a}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_134(self, library, param):
        # 删除前线常用地址
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 134, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=134)
        return response

    def auv_param_md_41_cmd_135(self, a, b, c, d, e):
        # 父元素	参数名	必选	类型	长度	描述	取值说明
        # a	是	int	24	前线uid
        # b	是	int	24	类型	1 装货 2卸货
        # c	是	String	24	三级联动地址
        # d	是	String	24	详细地址
        # e	是	int	24	1三级联动地址 2发货地址
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_41_cmd_135(self, library, param):
        # 前线常用地址新增
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(41, 135, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=135)
        return response

    def auv_param_md_40_cmd_1(self, d, ae, ab=None, ac=None, ad=None):
        # 参数名	必选	类型	长度	描述	取值说明
        # d	    是	int	4	类型	1:在运 2:已完成
        # ab	否	String	24	货品名称
        # ac	否	String	24	展示装货地
        # ad	否	String	24	展示卸货地
        # ae	是	int	24	起始页
        param = {"d": d,
                 "ab": ab,
                 "ac": ac,
                 "ad": ad,
                 "ae": ae}
        if ab is None:
            del param["ab"]
        if ac is None:
            del param["ac"]
        if ad is None:
            del param["ad"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def auv_md_40_cmd_1(self, library, param):
        # 货单列表
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(40, 1, 0, 0, param, c_back)
        event.wait()
        event.clear()
        response = self.get_response(iCmd=1)
        return response
