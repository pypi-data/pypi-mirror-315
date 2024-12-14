#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/25 10:51
fileName    : allure_config.py
'''

from ..common.Network import get_local_ip #, get_ip

class Allure(object):
    PATH    : str = r'E:\allure-2.13.8\bin\allure.bat'
    IP      : str = get_local_ip()
    PORT    : int = 9797