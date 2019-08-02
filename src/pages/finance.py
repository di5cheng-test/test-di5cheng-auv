# coding:utf-8
import requests
from src.common import config
from src.common.logger import MyLog

global null
null = None

url_finance = config.get_finance_url()


class Finance(object):
    def finance_login(self, username, password):
        # 财务登录
        url = url_finance + "xf/sy/busi.do?md=40&cmd=1"
        json = {"username": username, "password": password}
        r = requests.post(url=url, json=json)
        response = eval(r.text)
        return response['login']

    def finance_UserInfo(self, token, admin_id):
        # 财务登录账号信息
        url = url_finance + "xf/sy/busi.do?md=40&cmd=52"
        headers = {"token": token}
        json = {"admin_id": admin_id}
        r = requests.post(url=url, headers=headers, json=json)
        response = eval(r.text)
        return response

    def finance_CheckList(self, cookie, g, h, f=None):
        # 获取财务对账单
        url = url_finance + 'cw/sy/busi.do?md=1&cmd=1'
        f_headers = {"token": cookie}
        #    f  是否为已审核列表  1是
        #    g 	状态              1待前线审核 3待财务审核 5待付款
        #    h 起始页
        json = {"f": f, "g": g, "h": h}
        if f is None:
            del json["f"]
        r = requests.post(url=url, headers=f_headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    def finance_PayMoney_param(self, a, b, c=None, d=3, e=None):
        # 财务确认付款参数
        json = {"a": a,  # a：计算单id
                "b": b,  # b：回执单链接
                "c": c,  # c：备注
                "d": d,  # d：类型(1:前线；2:复核;3:财务;4:调度)
                "e": e  # e：用户名
                }
        if c is None:
            del json["c"]
        if e is None:
            del json["e"]
        return json

    def finance_Paymoney(self, token, param):
        # 财务确认付款
        url = url_finance + "cw/sy/busi.do?md=5&cmd=5"
        headers = {"token": token}
        json = param
        r = requests.post(url=url, headers=headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        if response == {"code": 0}:
            MyLog().sendlog('财务确认付款成功！')
        else:
            MyLog().sendlog('财务确认付款失败！')
        return response

    def finance_Check(self, cookie, a, e=None, b=0, c=None, d=None):
        # 审核对账
        url = url_finance + "cw/sy/busi.do?md=4&cmd=4"
        headers = {"token": cookie}
        json = {"a": a,  # a：结算单id
                "b": b,  # b：审核结果（0 审核通过，1 审核不通过）
                "c": c,  # c：备注(审核不通过时必填)
                "d": d,  # d：类型(1:前线；2:复核;3:财务;4:调度)
                "e": e  # e：用户名
                }
        if c is None:
            del json["c"]
        if d is None:
            del json["d"]
        if e is None:
            del json["e"]
        r = requests.post(url=url, headers=headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response

    # 获取复核员已审核的对账单的详情
    def finance_getCheckDoneDetails(self, token, account_id):
        url = url_finance + "xf/sy/busi.do?md=122&cmd=122"
        headers = {"token": token}
        json = {"a": account_id}
        r = requests.post(url=url, headers=headers, json=json)
        response = eval(r.text)
        return response['data']

    # 财务系统中，获取货源详情
    def finance_getSourceDetails(self, token, source_id):
        url = url_finance + "xf/sy/busi.do?md=40&cmd=45"
        headers = {"token": token}
        json = {"a": source_id}
        r = requests.post(url=url, headers=headers, json=json)
        response = eval(r.text)
        MyLog().sendlog(response)
        return response
