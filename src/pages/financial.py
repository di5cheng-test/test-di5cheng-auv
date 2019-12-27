import requests
from src.common.logger import MyLog 
from src.common import config
import random

global null
null = None
url_finance = config.get_finance_url()


class Financial(object):
    def financial_login(self, username, password):
        url = url_finance + "xf/sy/busi.do?md=40&cmd=1"
        params = {"username": username, "password": password}
        r = requests.post(url=url, json=params)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response['login']

    def financial_UserInfo(self, token, admin_id):
        url = url_finance + "xf/sy/busi.do?md=40&cmd=52"
        headers = {"token": token}
        params = {"admin_id": admin_id}
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def financial_CheckList(self, cookie, status, page, check=None):
        # 获取财务对账单
        url = url_finance + 'cw/sy/busi.do?md=1&cmd=1'
        f_headers = {"token": cookie}
        #    f  是否为已审核列表  1是
        #    g 	状态              1待前线审核 3待财务审核 5待付款
        #    h 起始页
        param = {"f": check, "g": status, "h": page}
        if check is None:
            del param["f"]
        r = requests.post(url=url, headers=f_headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    # 复核员审核对账，审核通过
    # a：结算单id  b：审核结果（0 审核通过，1 审核不通过）
    def financial_reCheck(self, cookie, account_Oder_id, status):
        url = url_finance + "cw/sy/busi.do?md=4&cmd=4"
        headers = {"token": cookie}
        params = {"a": account_Oder_id, "b": status}
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        print(response)
        if response == {"code": 0}:
            print('复核员审核通过成功！')
        else:
            print('复核员审核通过失败！')
        return response

    # 财务确认付款参数
    # a：计算单id  b：回执单链接  c：备注  d：类型(1:前线；2:复核;3:财务;4:调度)  e：用户名
    def financial_PayMoney_params(self, account_Oder_id):
        params = {}
        params['a'] = account_Oder_id
        params['b'] = random.choice(config.get_picture())
        params['c'] = "付款完成啦啦啦！"
        params['d'] = 3
        params['e'] = "test004"
        return params

    # 财务确认付款
    def financial_Paymoney(self, token, financialPayMoney_params):
        url = url_finance + "cw/sy/busi.do?md=5&cmd=5"
        headers = {"token": token}
        params = financialPayMoney_params
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        print(response)
        if response == {"code": 0}:
            print('财务确认付款成功！')
        else:
            print('财务确认付款失败！')
        return response

    # 生成打回对账参数
    # a：结算单id  b：审核结果（0 审核通过，1 审核不通过）  c：备注(审核不通过时必填)  d：类型(1:前线；2:复核;3:财务;4:调度)  e：用户名
    def financial_disCheck_params(self, account_Oder_id):
        params = {}
        params['a'] = account_Oder_id
        params['b'] = 1
        params['c'] = "你的对账信息有误，请重新发起！"
        params['d'] = 3
        params['e'] = "test004"
        print(params)
        return params

    # 财务打回对账
    def financial_disCheck(self, token, disCheck_params):
        url = url_finance + "cw/sy/busi.do?md=4&cmd=4"
        headers = {"token": token}
        params = disCheck_params
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        print(response)
        if response == {"code": 0}:
            print('打回对账成功！')
        else:
            print('打回对账失败！')
        return response

    # 获取复核员已审核的对账单的详情
    def financial_getCheckDoneDetails(self, token, account_id):
        url = url_finance + "xf/sy/busi.do?md=122&cmd=122"
        headers = {"token": token}
        params = {"a": account_id}
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        return response['data']

    # 财务系统中，获取货源详情
    def financial_getSourceDetails(self, token, source_id):
        url = url_finance + "xf/sy/busi.do?md=40&cmd=45"
        headers = {"token": token}
        params = {"a": source_id}
        r = requests.post(url=url, headers=headers, json=params)
        response = eval(r.text)
        print(response)
        return response
