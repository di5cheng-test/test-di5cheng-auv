# coding:utf-8
'''
description:公共的随机方法类
'''

import random
import datetime
from src.common import config
import xlrd
import json

areaCodeDict = r'地区编码'
user_name = r'姓名'
workbook = xlrd.open_workbook(config.get_excel())
sheet_car = workbook.sheet_by_name('车牌区号')
prelist_car = sheet_car.col_values(0)
sheet_area = workbook.sheet_by_name(r'地区编码')
prelist_area = sheet_area.col_values(1)
sheet = workbook.sheet_by_name(r'姓名')
first_name = sheet.col_values(0)
second_name = sheet.col_values(1)
pic = random.choice(random.choice(config.get_picture()))


class Random_param(object):
    # 随机N位数字
    def random_num(self, num):
        ret = ""
        for i in range(num):
            num1 = random.randint(0, 9)
            s = str(random.choice([num1]))
            ret += s
        return ret

    # 随机车牌区号
    def car_areaCode(self):
        a = ""
        while a == "":
            a = random.choice(prelist_car)
        return a

    '''
    排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位校验码:
    1、地址码 
    表示编码对象常住户口所在县(市、旗、区)的行政区域划分代码，按GB/T2260的规定执行。
    2、出生日期码 
    表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。 
    3、顺序码 
    表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。 
    4、校验码计算步骤
        (1)十七位数字本体码加权求和公式 
        S = Sum(Ai * Wi), i = 0, ... , 16 ，先对前17位数字的权求和 
        Ai:表示第i位置上的身份证号码数字值(0~9) 
        Wi:7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 （表示第i位置上的加权因子）
        (2)计算模 
        Y = mod(S, 11)
        (3)根据模，查找得到对应的校验码 
        Y: 0 1 2 3 4 5 6 7 8 9 10 
        校验码: 1 0 X 9 8 7 6 5 4 3 2
    '''

    def getCheckBit(self, num17):
        """
        获取身份证最后一位，即校验码
        :param num17: 身份证前17位字符串
        :return: 身份证最后一位
        """
        Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        checkCode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        zipWiNum17 = zip(list(num17), Wi)
        S = sum(int(i) * j for i, j in zipWiNum17)
        Y = S % 11
        return checkCode[Y]

    def getAddrCode(self):
        """
        获取身份证前6位，即地址码
        :return: 身份证前6位
        """
        addrIndex = random.choice(prelist_area)
        return addrIndex

    def getBirthday(self, start="1900-01-01", end="2018-12-30"):
        """
        获取身份证7到14位，即出生年月日
        :param start: 出生日期合理的起始时间
        :param end: 出生日期合理的结束时间
        :return: 份证7到14位
        """
        days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
        birthday = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days))
        return datetime.datetime.strftime(birthday, "%Y%m%d")

    def create_IDcard(self, sex=1):
        """
        获取随机身份证
        :param sex: 性别，默认为男
        :return: 返回一个随机身份证
        """
        idNumber = int(self.getAddrCode())
        idCode = str(idNumber) + self.getBirthday()
        for i in range(2):
            idCode += str(random.randint(0, 9))
        idCode += str(random.randrange(sex, 9, 2))
        idCode += self.getCheckBit(idCode)
        return idCode

    # 生成随机2-3位姓名
    def create_name(self):
        a = ""
        while a == "":
            a = random.choice(first_name)
        b = ""
        while b == "":
            b = random.choice(second_name)
        full_name = a + "".join(b for i in range(random.randint(1, 2)))
        return full_name

    # 生成随机手机号
    def create_Phone(self):
        a = str(random.randint(130, 199)) + "".join(random.choice("0123456789") for i in range(8))
        return a

    # 生成随机车牌号
    def create_carNumber(self, length):
        area_code = self.car_areaCode()
        length_num = self.random_num(length)
        if length == 4:
            car_num = area_code + length_num + "挂"
        else:
            car_num = area_code + length_num
        return car_num

    def create_car_param(self, fleet_id):
        # web车辆信息
        param = {
            "fleet_id": fleet_id,
            "car_number": self.create_carNumber(5),
            "gua_number": self.create_carNumber(4),
            "car_ton": random.randint(0, 100) * 1000,
            "m_user": self.create_name(),
            "m_mobile": self.create_Phone(),
            "m_id_card": self.create_IDcard(),
            "status": 0,
            "region_source": 5,
            "first_people": 252
        }
        return param

    def create_addBank_param(self, enterprise):
        # app 添加收款账户
        pic_id = random.choice(config.get_picture())
        account_name = "中国银行" + self.random_num(2) + "号分行"
        cardnumber = self.random_num(16)
        cardaddress = "中山北路" + self.random_num(2) + "号"
        param = {"a": enterprise,  # 车队id
                 "b": pic_id,  # 图片id
                 "c": account_name,  # 开户名称
                 "d": cardnumber,  # 开户账号
                 "e": cardaddress,  # 开户行
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_enter_driver_info_param(self, enterprise):
        # app 添加车辆 （旧，已弃用）
        param = {"a": enterprise,  # 车队id
                 "b": self.create_name(),  # 司机姓名
                 "c": self.create_Phone(),  # 手机号码
                 "d": self.create_IDcard(),  # 身份证
                 "e": self.create_carNumber(5),  # 车牌号码
                 "f": self.create_carNumber(4),  # 挂车牌号码
                 "g": random.randint(10, 99) * 1000  # 荷载吨数
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_app_car_info(self, fleet_id):
        # app 添加车辆
        param = {"a": self.create_carNumber(length=5),
                 "b": random.randint(1, 3),
                 "c": pic,
                 "d": pic,
                 "e": pic,
                 "f": 1563984000000,
                 "o": 1563984000000,
                 "g": pic,
                 "h": pic,
                 "i": pic,
                 "j": pic,
                 "k": self.random_num(5),
                 "l": 1563984000000,
                 "p": 1563984000000,
                 "n": fleet_id,
                 "r": random.choice([0, 2]),
                 "q": random.randint(1, 2)}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_app_gua_car_info(self, fleet_id):
        # app 添加挂车
        param = {"a": self.create_carNumber(4),
                 "b": random.randint(1, 4),
                 "c": pic,
                 "d": pic,
                 "e": pic,
                 "f": 1563984000000,
                 "o": 1563984000000,
                 "g": pic,
                 "h": pic,
                 "i": pic,
                 "j": pic,
                 "k": self.random_num(5),
                 "l": 1563984000000,
                 "p": 1563984000000,
                 "n": fleet_id,
                 "r": random.choice([0, 2]),
                 "m": random.randint(10, 99) * 1000,
                 "q": random.choice([1, 2]),
                 "t": random.choice(["1", "2", "1,2"])}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_app_driver_info(self, fleet_id, switch=0):
        # app 添加司机
        param = {"a": self.create_name(),
                 "b": self.create_IDcard(),
                 "c": int(self.create_Phone()),
                 "d": pic,
                 "e": pic,
                 "f": 1563984000000,
                 "g": 1563984000000,
                 "h": pic,
                 "i": self.random_num(6),
                 "j": 1563984000000,
                 "k": 1563984000000,
                 "l": fleet_id,
                 "m": pic,
                 "n": pic,
                 "o": pic,
                 "r": random.choice(["1", "2", "1,2"])
                 }
        if switch != 0:
            del param["m"]
            del param["n"]
            del param["o"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_app_driver_ya_info(self, fleet_id):
        param = {"a": self.create_name(),
                 "b": int(self.create_Phone()),
                 "c": pic,
                 "d": 1563984000000,
                 "e": 1563984000000,
                 "f": fleet_id,
                 "r": random.choice(["1", "2", "1,2"])
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param

    def create_fleet_info_param(self, admin_id, admin_name, admin_user_id):
        # 小五注册直接认证通过的车队参数
        name_1 = self.create_name()
        name_2 = self.create_name()
        phone = self.create_Phone()
        id_card = self.create_IDcard()
        company_id_number = self.random_num(num=15)
        param = {
            "fleet_name": ("南京" + name_1 + "股份有限公司"),
            "address": ("南京市浦口区团结路" + str(random.randint(1, 10000)) + "号"),
            "contact": name_2,
            "contact_phone": phone,
            "admin_id": admin_id,
            "region_source": 5,
            "id_card": id_card,
            "company_id_number": company_id_number,
            "id_card_pic_m": random.choice(config.get_picture()),
            "id_card_pic_p": random.choice(config.get_picture()),
            "business": random.choice(config.get_picture()),
            "business_2": random.choice(config.get_picture()),
            "status": 1,
            "car_type": random.randint(1, 4),
            "password": "123456",
            "first_people": "252",
            "admin_name": admin_name,
            "admin_user_id": admin_user_id
        }
        print(param)
        return param

    def create_finance_PayMoney_params(self, a, e):
        # 财务确认付款参数
        # a：计算单id
        # b：回执单链接
        # c：备注
        # d：类型(1:前线；2:复核;3:财务;4:调度)
        # e：用户名
        param = {"a": a,
                 "b": random.choice(config.get_picture()),
                 "c": "付款完成啦啦啦！",
                 "d": 3,
                 "e": e
                 }
        return param

    def create_apply_uncontract_param(self, a, d, i, s, u, v, z):
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
        param = {"a": a,
                 "b": 2,
                 "d": d,
                 "f": 0,
                 "i": i,
                 "j": 2,
                 "k": random.choice(config.get_picture()),
                 "m": 1,
                 "n": 1,
                 "o": 2,
                 "s": s,
                 "u": u,
                 "v": v,
                 "w": 2,
                 "z": z,
                 }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        return c_param
