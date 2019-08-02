# coding:utf-8
import pytest
import random
from src.common import random_param
from config import global_parameter
from src.pages import shipper
from src.pages import dispatch
from src.pages import service
from src.pages import finance
import requests

global null
null = None


class Test_case(object):
    def setup_class(self):
        self.financial = finance.Financial()
        self.financial_token = self.financial.financial_login(username=global_parameter.financial_account['username'],
                                                              password=global_parameter.financial_account['password'])

        # self.financial_admin_id = self.financial_login['admin_id']

    # def teardown_class(self):
    #     print("teardown_class(self)：每个类之后执行一次")
    #
    # def setup_method(self):
    #     print("setup_method(self):在每个方法之前执行")
    #
    # def teardown_method(self):
    #     print("teardown_method(self):在每个方法之后执行")

    def test_01_financialCheckPass(self):
        # # 获取财务管理员信息
        # financialUserInfo = self.financial.financial_UserInfo(self.financial_token, self.financial_admin_id)
        # print(financialUserInfo)
        print("- - - 财务待审核列表 - - -")
        # 获取财务待审核列表
        financialCheckList = self.financial.financial_CheckList(self.financial_token)
        for financialCheck in financialCheckList:
            print(financialCheckList)

        # 复核员随机获取一条数据A
        reCheckData = random.choice(financialCheckList)
        print(reCheckData)
        account_Oder_id = reCheckData['a']

        # # 复核员审核数据A
        # self.financial.reCheck(self.financial_token,account_Oder_id)

        print("- - - 财务已审核列表 - - -")
        # 获取财务已审核列表
        financialCheckDoneList = self.financial.financial_CheckList(self.financial_token)
        print(financialCheckDoneList)
        # 校验数据A 是否存在于复核员的已审核列表中
        for financialCheckDoneA in financialCheckDoneList:
            if financialCheckDoneA['a'] == account_Oder_id:
                reCheckState = financialCheckDoneA['m']
                if reCheckState == 5:
                    print("已找到数据A，状态为“待财务审核”")
            else:
                continue

        print("- - - 财务待付款列表 - - -")
        # 获取财务待付款列表
        financialPaymentList = self.financial.financial_PaymentList(self.financial_token)
        for financialPayment in financialPaymentList:
            if financialPayment['a'] == account_Oder_id and financialPayment['m'] == reCheckState:
                print("已找到数据A，状态为“待财务审核”")
        # print("- - - 财务已付款列表 - - -")
        # # 获取财务已付款列表
        # financialPaymentDoneList = self.financial.financialPaymentList(self.financial_token)
        # for financialPaymentDone in financialPaymentDoneList:
        #     print(financialPaymentDone)
        # print("- - - 生成财务付款参数 - - -")
        # # 生成财务付款参数
        # financialPayMoney_params = self.financial.financialPayMoney_params('5cec9bb6743a4937883d2845')
        # print(financialPayMoney_params)
        # print("- - - 财务确认付款 - - -")
        # # 财务确认付款
        # financialPayMoney = self.financial.financialPaymoney(self.financial_token,financialPayMoney_params)
        # print("- - - 生成财务打回对账的参数 - - -")

    def test_02_financialCheckFail(self):
        # 获取财务待审核列表
        financialCheckList = self.financial.financial_CheckList(self.financial_token)
        for financialCheck in financialCheckList:
            print(financialCheckList)

        # 复核员随机获取一条数据A
        reCheckData = random.choice(financialCheckList)
        print(reCheckData)
        account_Oder_id = reCheckData['a']
        # 生成财务打回对账的参数
        disCheckParams = self.financial.financial_disCheck_params(account_Oder_id)
        print(disCheckParams)
        print("- - - 财务打回对账 - - -")
        disCheck = self.financial.financial_disCheck(self.financial_token, disCheckParams)
        financialCheckDoneList = self.financial.financial_CheckDoneList(self.financial_token)
        print(financialCheckDoneList)
        # 校验数据A 是否存在于复核员的已审核列表中
        for financialCheckDoneA in financialCheckDoneList:
            if financialCheckDoneA['a'] == account_Oder_id:
                print(financialCheckDoneA['m'])
            else:
                continue

    def test_03_financialCheckSourceDetails(self):
        # 获取复核员已审核的对账单的详情
        account_id = "5cff6ff2743a4915e2671a97"
        financialWaitCheckDetails = self.financial.financial_getCheckDoneDetails(token=self.financial_token,
                                                                                 account_id="5cff6ff2743a4915e2671a97")
        print(financialWaitCheckDetails)
        # 拿到详情中的数据
        source_price = financialWaitCheckDetails['ac']  # 货品单价
        transport_price = financialWaitCheckDetails['i']  # 运价
        carNum = financialWaitCheckDetails['j']  # 待对账车数
        checkState = financialWaitCheckDetails['q']  # 对账状态
        trueMoney = int(financialWaitCheckDetails['z'] / 1000)  # 实付费用
        allMoney = int(financialWaitCheckDetails['p'] / 1000)  # 应付运费
        messagePrice = financialWaitCheckDetails['p'] / 100  # 信息费
        otherMoney = financialWaitCheckDetails['o']  # 其他费用
        allLossMoney = int(financialWaitCheckDetails['n'] / 1000)  # 损耗赔偿
        allLossNum = financialWaitCheckDetails['m']  # 损耗数量（kg）
        allLoadNum = financialWaitCheckDetails['m']  # 损耗数量（吨）
        start_address = financialWaitCheckDetails['a']  # 装货地
        end_address = financialWaitCheckDetails['b']  # 卸货地
        order_id = financialWaitCheckDetails['c']  # 运单编号
        source_id = financialWaitCheckDetails['ag']  # 货单id
        account_order_id = financialWaitCheckDetails['s']  # 对账单id
        lossPercent = financialWaitCheckDetails['ad']  # 承担损耗
        start_time = financialWaitCheckDetails['h']  # 发起时间
        remark = financialWaitCheckDetails['af']  # 付款备注

        # 根据运单编号，获取货源详情
        sourceDetails = self.financial.financial_getSourceDetails(token=self.financial_token, source_id=source_id)
        print(sourceDetails)
        # print(sourceDetails['a'])
        # print(sourceDetails['b'])
        assert start_address == sourceDetails['a']
        assert end_address == sourceDetails['b']

