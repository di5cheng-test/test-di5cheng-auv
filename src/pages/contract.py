# coding:utf-8
import requests
from src.common import config
from src.common.logger import MyLog

global null
null = None

url_contract = config.get_contract_url()


class Contract(object):
    def contract_md_40_cmd_1(self, username, password):
        # 电子合同登录
        url = url_contract + "xf/sy/busi.do?md=40&cmd=1"
        param = {"username": username, "password": password, "region_source": 3}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response["data"]["token"]

    def contract_md_48_cmd_13(self, cookie, a, c, d, b=None):
        # 线下合同列表
        # 参数名	必选	类型	长度	说明
        # a	是	int	8	页码
        # b	否	String	64	公司名称
        # c	是	int	8	0待审核 1已审核
        # d	是	int	8	1长约 2短约
        url = url_contract + "ect/sy/busi.do?md=48&cmd=13"
        param = {"a": a, "b": b, "c": c, "d": d}
        f_headers = {"token": cookie}
        if b is None:
            del param["b"]
        r = requests.post(url=url, json=param, headers=f_headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def contract_md_48_cmd_12(self, cookie, a, b, e, f, g, h, c=None, d=None):
        # 线下合同编辑（审核）
        # 上级元素	参数名	必选	类型	长度	说明
        # a	是	String	8	乙方公司
        # b	是	String	64	合同url
        # c	否	long	64	生效时间
        # d	否	long	64	失效时间
        # e	是	String	8	乙方公司id
        # f	是	int	8	主键id
        # g	是	int	8	1通过 -2驳回
        # h	是	int	8	审核备注
        url = url_contract + "ect/sy/busi.do?md=48&cmd=12"
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h}
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        f_headers = {"token": cookie}
        r = requests.post(url=url, json=param, headers=f_headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def contract_md_48_cmd_18(self, cookie, a):
        # 线下合同详情
        # 上级元素	参数名	必选	类型	长度	说明
        # a	是	int	64	主键id
        url = url_contract + "ect/sy/busi.do?md=48&cmd=18"
        param = {"a": a}
        f_headers = {"token": cookie}
        r = requests.post(url=url, json=param, headers=f_headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response
