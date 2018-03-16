# -*- coding: UTF-8 -*-
import requests, re, hashlib, threading
import tkMessageBox, tkFont
import sys, time
from Tkinter import *
from classInfo import *
from stringFormat import *
reload(sys)
sys.setdefaultencoding('utf-8')
'''
* 一些全局变量
'''

#登录所需各个教务网站的参数
dic = {
    "202.202.1.176:8080":
    "dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz7p2B9lkx+Yq/jf62i+iqicmZx/xg==",
    "202.202.1.41":
    "dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz4b+wl1zSDOBUtpX/5BigXmPsbdDA==",
    "222.198.128.126":
    "dDw1OTgzNjYzMjM7dDw7bDxpPDE+O2k8Mz47aTw1Pjs+O2w8dDxwPGw8VGV4dDs+O2w86YeN5bqG5aSn5a2mOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBvcGVuV2luTG9nKHRoZVVSTCx3LGgpewp2YXIgVGZvcm0scmV0U3RyXDsKZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHJlc2l6YWJsZT1ubyciKVw7CnBvcD13aW5kb3cub3Blbih0aGVVUkwsJ3dpbktQVCcsVGZvcm0pXDsgLy9wb3AubW92ZVRvKDAsNzUpXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6bm9cO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwppZih0eXBlb2YocmV0U3RyKSE9J3VuZGVmaW5lZCcpIGFsZXJ0KHJldFN0cilcOwp9CmZ1bmN0aW9uIHNob3dMYXkoZGl2SWQpewp2YXIgb2JqRGl2ID0gZXZhbChkaXZJZClcOwppZiAob2JqRGl2LnN0eWxlLmRpc3BsYXk9PSJub25lIikKe29iakRpdi5zdHlsZS5kaXNwbGF5PSIiXDt9CmVsc2V7b2JqRGl2LnN0eWxlLmRpc3BsYXk9Im5vbmUiXDt9Cn0KZnVuY3Rpb24gc2VsVHllTmFtZSgpewogIGRvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7Cn0KZnVuY3Rpb24gd2luZG93Lm9ubG9hZCgpewoJdmFyIHNQQz13aW5kb3cubmF2aWdhdG9yLnVzZXJBZ2VudCt3aW5kb3cubmF2aWdhdG9yLmNwdUNsYXNzK3dpbmRvdy5uYXZpZ2F0b3IuYXBwTWlub3JWZXJzaW9uKycgU046TlVMTCdcOwp0cnl7ZG9jdW1lbnQuYWxsLnBjSW5mby52YWx1ZT1zUENcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eHRfZHNkc2RzZGpramtqYy5mb2N1cygpXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcO31jYXRjaChlcnIpe30KfQpmdW5jdGlvbiBvcGVuV2luRGlhbG9nKHVybCxzY3IsdyxoKQp7CnZhciBUZm9ybVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOiIrc2NyKyJcO3Njcm9sbGJhcnM9bm9cO2hlbHA6bm8nIilcOwp3aW5kb3cuc2hvd01vZGFsRGlhbG9nKHVybCwxLFRmb3JtKVw7Cn0KZnVuY3Rpb24gb3Blbldpbih0aGVVUkwpewp2YXIgVGZvcm0sdyxoXDsKdHJ5ewoJdz13aW5kb3cuc2NyZWVuLndpZHRoLTEwXDsKfWNhdGNoKGUpe30KdHJ5ewpoPXdpbmRvdy5zY3JlZW4uaGVpZ2h0LTMwXDsKfWNhdGNoKGUpe30KdHJ5e2V2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxzdGF0dXM9bm8scmVzaXphYmxlPXllcyciKVw7CnBvcD1wYXJlbnQud2luZG93Lm9wZW4odGhlVVJMLCcnLFRmb3JtKVw7CnBvcC5tb3ZlVG8oMCwwKVw7CnBhcmVudC5vcGVuZXI9bnVsbFw7CnBhcmVudC5jbG9zZSgpXDt9Y2F0Y2goZSl7fQp9CmZ1bmN0aW9uIGNoYW5nZVZhbGlkYXRlQ29kZShPYmopewp2YXIgZHQgPSBuZXcgRGF0ZSgpXDsKT2JqLnNyYz0iLi4vc3lzL1ZhbGlkYXRlQ29kZS5hc3B4P3Q9IitkdC5nZXRNaWxsaXNlY29uZHMoKVw7Cn0KXFwtLVw+Clw8L3NjcmlwdFw+Oz4+Ozs+O3Q8O2w8aTwxPjs+O2w8dDw7bDxpPDA+Oz47bDx0PHA8bDxUZXh0Oz47bDxcPG9wdGlvbiB2YWx1ZT0nU1RVJyB1c3JJRD0n5a2m5Y+3J1w+5a2m55SfXDwvb3B0aW9uXD4KXDxvcHRpb24gdmFsdWU9J1RFQScgdXNySUQ9J+W4kOWPtydcPuaVmeW4iFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJDlj7cnXD7nrqHnkIbkurrlkZhcPC9vcHRpb25cPgpcPG9wdGlvbiB2YWx1ZT0nQURNJyB1c3JJRD0n5biQ5Y+3J1w+6Zeo5oi357u05oqk5ZGYXDwvb3B0aW9uXD4KOz4+Ozs+Oz4+Oz4+Oz4+Oz62hRbfKCEh4NgqUfD+QNlfnJS/3A=="
}
hea = {
    'User-Agent':
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"
}

cookie = {'Fail': '0'}
target = 0
login_ip = ""
User = ""
target_list = ["  选 主 修 课 ", "  选 英 语 课 ", "  选 通 识 课 "]        #选课类型
select_list = []                                                            #选中课程列表
cookie_lock = threading.Lock()                                              #多线程锁

#======================================================= Login =========================================================
def login(address, viewstate):
    '''
    * 登录加密算法在登录网站前端JS有
    * param address: 登录地址
    * param viewstate: 对应地址参数,详见dic
    * return: Fail->0;Success->login_ip
    '''
    global cookie, cookie_lock, User, login_ip
    UID = User = str(uid.get())
    PWD = str(pwd.get())
    m = hashlib.md5()
    m.update(PWD)
    s = UID + "".join(list(m.hexdigest())[:30]).upper() + "10611"
    s_md5 = hashlib.md5()
    s_md5.update(s)
    MD5 = "".join(list(s_md5.hexdigest().upper())[:30])
    data = {
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": "CAA0A5A7",
        "Sel_Type": "STU",
        "txt_dsdsdsdjkjkjc": UID,
        "txt_dsdfdfgfouyy": PWD,
        "txt_ysdsdsdskgf": "",
        "pcInfo": "",
        "typeName": "",
        "aerererdsdxcxdfgfg": "",
        "efdfdfuuyyuuckjg": MD5
    }
    hea = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer":
        'http://' + address + '/_data/index_login.aspx'
    }

    url1 = 'http://' + address + '/_data/index_login.aspx'
    print address, "Processing"
    try:
        login_html = requests.post(url1, data=data, headers=hea, timeout=10)

    except:

        print "The address", address, "may have been closed."
        return 0
    else:
        if login_html.text.find("账号或密码不正确")!=-1:
            print address, "Faild"
            cookie = {"Fail": "1"}
            return 0
        if login_html.text.find("正在加载权限数据")!=-1:
            print address, "Login"
            if cookie_lock.acquire() and 'Fail' in cookie.keys():
                cookie = {c.name: c.value for c in login_html.cookies}
                login_ip = re.findall("http://(.*?)/_data", login_html.url)[0]
                cookie_lock.release()
            return address
        cookie = {"Fail": "1"}
        return -1
#==================================================== Check Cookie =====================================================
def checkCookie():
    '''
    * 另起一个线程用作检查cookie是否成功获取，并直接往下执行，不需等登录的三个线程都结束
    * return: 没啥用
    '''
    count = 0
    while 'Fail' in cookie.keys() and cookie['Fail'] == '0' and count < 600:        #60S超时
        time.sleep(0.1)
        count += 1
    return 0

#================================================= Login Button Submit =================================================
def login_submit(event=""):
    '''
    * 登录按钮点击后调用的函数
    * 作用： 启用多线程登录，并阻塞检查cookie
    * 不知道为啥在checkCookie线程里面检查cookie并destry root是会死锁的
    * 并且传参也是无效的,看来并不是传的引用
    * 或者说python传参说拷贝还是引用是没有意义的，2333
    * param event: Button自带参数
    * return: Fail->-1;Success->0
    '''
    global cookie
    cookie = {'Fail': '0'}
    threads = []
    for i in uid.get():
        if i not in "0123456789":
            tkMessageBox.showinfo("登录信息", "账号格式错误\n请检查后再输入")
            return -1
    for i in dic:
        t = threading.Thread(target=login, args=(i, dic[i]), name=str(i))
        threads.append(t)
    for t in threads:
        t.start()
    #当三个线程都因网站原因阻塞时，程序会无响应，直到登录成功或者登录超时(60S)
    #败笔2333
    checkThread = threading.Thread(target=checkCookie)
    checkThread.setDaemon(True)
    checkThread.start()
    checkThread.join(60)

    if 'Fail' in cookie.keys():
        tkMessageBox.showinfo("登录信息", "账号或密码错误\n或服务器正忙")
        return -1
    else:
        tkMessageBox.showinfo("登录信息", "登陆成功")
        root.destroy()
        return 0

#===================================================== Update Select ===================================================
def updateSelect(event, classOrdinal):
    '''
    * 更新选定课程控件的StringVar()
    * param event: bind 自带参数
    * param classOrdinal: 全局变量class_info_list序数
    * class_info_list结构:
    * [ [The classes in each lesson], [etc. classInfo1,classInfo2,classInfo3...],...]
    * return:
    '''
    global selectLesson1, selectLesson2, selectLesson3

    if event.widget.size() == event.widget.curselection()[0] + 1 or event.widget.curselection()[0] <= 2:
        return -1
    selectLessonClass = class_info_list[classOrdinal][
        event.widget.curselection()[0] - 3]
    if len(select_list) == 3 or selectLessonClass in select_list: return -1
    select_list.append(selectLessonClass)
    '''
    * locals()获取不到全局的StringVar()——selectLesson
    * 这里写的很臃肿
    * 如有办法简洁，plz tell me 
    '''

    #更新选定课程控件的StringVar()
    if len(select_list) == 1:
        selectLesson1.set(
            standardized(
                selectLessonClass.teacher + "[" + selectLessonClass.name +"]" +
                  selectLessonClass.id[:(selectLessonClass.id.find('[') if selectLessonClass.id.find('[') != -1 else 0)], 36))
    elif len(select_list) == 2:
        selectLesson2.set(
            standardized(
                selectLessonClass.teacher + "[" + selectLessonClass.name +"]" +
                  selectLessonClass.id[:(selectLessonClass.id.find('[') if selectLessonClass.id.find('[') != -1 else 0)], 36))
    elif len(select_list) == 3:
        selectLesson3.set(
            standardized(
                selectLessonClass.teacher + "[" + selectLessonClass.name +"]" +
                  selectLessonClass.id[:(selectLessonClass.id.find('[') if selectLessonClass.id.find('[') != -1 else 0)], 36))
    else:
        return -1
    return 0

#=================================================== Update Right Box ==================================================
def updateRightBox(event):
    '''
    * 更新右边详细信息框
    * param event: bind 自带参数
    * return: None
    '''
    Listbox_right.delete(0, END)  #clear the infoBox
    if event.widget.curselection()[0] <= 2 or event.widget.curselection()[0] >= 3 + len(class_info_list):
        Listbox_right.insert(END, " %s" % (string_ljust("_" * 50, 50)))
        Listbox_right.insert(END, "               详细说明             ")
        Listbox_right.insert(END, "  请仔细选课！！！")
        Listbox_right.insert(END, "  同一门课一次提交不同老师会被其中一个覆盖！")
        Listbox_right.insert(END, "  已经选上的课再次提交任意一个老师会退选当前老师！")
        Listbox_right.insert(END, "  并且请勿手动刷新过快")
        Listbox_right.insert(END, "  IP会被Ban掉")
        Listbox_right.insert(END, "  并且制造必要的拥堵")
        Listbox_right.insert(END, "  切勿用作非法用途")
        Listbox_right.insert(END, "   ")
        Listbox_right.insert(END, "  毕竟本菜水平有限")
        Listbox_right.insert(END, "  任何BUG请重启软件(..•˘_˘•..)")
        Listbox_right.insert(END, "                                By Wz")

        return 0
    Listbox_right.insert(END, " %s" % (string_ljust("_" * 98, 98)))
    Listbox_right.insert(END,
                         "|%s|%s|%s|%s|%s|%s|" % (string_ljust("教师", 6),
                                                  string_ljust("限选", 3),
                                                  string_ljust("已选", 3),
                                                  string_ljust("可选", 3),
                                                  string_ljust("校区", 4),
                                                  string_ljust("上课时间", 70)))
    Listbox_right.insert(END, "|%s|" % (string_ljust("-" * 97, 97)))

    #取class_info_list中的classInfo类的信息显示
    for course in class_info_list[event.widget.curselection()[0] - 3]:
        if course.teacher == "NULL":
            Listbox_right.insert(END, "正在努力爬取数据中.......")
            Listbox_right.insert(END, string_ljust("先看看别的课程吧( ˘•ω•˘ )", 50))
        else:
            text = "|%s|%s|%s|%s|%s|%s|" % (string_ljust(course.teacher, 6),
                                            string_ljust(course.limit, 4),
                                            string_ljust(course.selected, 4),
                                            string_ljust(course.optional, 4),
                                            string_ljust(course.campus, 4),
                                            string_ljust(course.schedule, 70))
            Listbox_right.insert(END, text)

    Listbox_right.insert(END, " %s" % (string_ljust("￣" * 49, 98)))

    Listbox_right.bind(
        '<Double-Button-1>',
        lambda e, i=event.widget.curselection()[0] - 3: updateSelect(e, i))         #绑定更新选择控件

#=================================================== Update Left Box ===================================================
def updateLeftBox(lesson="", lesson_teacher="", lesson_status="", **kwargs):
    '''
    * 更新左边详细信息框
    :param lesson: name
    :param lesson_teacher: teacher
    :param lesson_status: selected status
    :param kwargs: 主要为了传个noData
    :return:
    '''
    #非选课时间
    if "noData" in kwargs:
        Listbox_left.insert(5, "%s" % (string_rjust("非选课时间", 40)))
        Listbox_left.insert(6, "%s" % (string_rjust(" 等学校开了数据库再试试", 46)))
        return -1
    Listbox_left.delete(0, END)
    Listbox_left.insert(END, " %s" % (string_ljust("_" * 68, 60)))
    Listbox_left.insert(END, "|%s|%s|%s|%s|" % (string_ljust(" 序号", 3),
                                                string_ljust("课程名称", 33),
                                                string_ljust("已选老师", 22),
                                                string_ljust("状态", 5)))
    Listbox_left.insert(END, "|%s|" % (string_ljust("-" * 68, 60)))
    #显示粗略课程信息
    for i in range(len(lesson)):
        text = "|%s|%s|%s|%s|" % (string_ljust("  " + str(i + 1), 5),
                                  string_ljust(lesson[i], 33),
                                  string_ljust(lesson_teacher[i], 22),
                                  string_ljust(lesson_status[i], 5))
        Listbox_left.insert(END, text)
    Listbox_left.insert(END, " %s" % (string_ljust("￣" * 36, 60)))
    Listbox_left.bind('<Double-Button-1>', updateRightBox)                      #绑定更新右边信息框
    Listbox_left.grid_propagate(0)                                              #绝对大小

#===================================================== Main thread =====================================================
def leftInfoCrawing():
    '''
    * 主线程
    * 登录后启动
    '''
    #爬取课程简略信息
    global v
    url = "http://" + login_ip + "/wsxk/stu_btx_rpt.aspx"  #主课#英语

    data = {
        # "sel_lx":"0",#主课
        # "sel_lx":"4",#通识
        #英语加上kclb3
        # "kclb3":"60"
    }
    if v.get() == 3:
        data['sel_lx'] = "4"
    else:
        data['sel_lx'] = "0"
    if v.get() == 2:
        data["kclb3"] = "60"

    info_html = requests.post(url, data=data, cookies=cookie)
    information = info_html.text

    #如非选课时间
    if "NO_DATA" in information:
        updateLeftBox(noData=1)
        return 0

    #正则匹配
    l = re.findall("(<input name=chkKC[0-9]+.*?>)", information)
    lesson_var = re.findall("<input name=chkKC[0-9]+.*?value='(.*?)'.*?>",
                            information)                                    #课程值,用来分离课程名称
    lesson_teacher = re.findall("style='width:225px' (.*?)disabled >",
                                information)                                #老师列表
    lesson_teacher = map(fifter, lesson_teacher)                            #过滤

    #解决一个老师两个时段课的情况
    for i in range(len(lesson_teacher)):
        if lesson_teacher[i] == " ":
            lesson_teacher[i] = lesson_teacher[i - 1]

    lesson = []                                                              #课程名
    lesson_status = []                                                       #课程选择状态

    for i in lesson_var:
        lesson.extend(re.findall("\[.*?\](.*?)\$", i))
    for i in range(len(l)):
        if "checked" in l[i] and "disabled" in l[i]:
            lesson_status.append("已选")
        elif "onclick=selectSKBJ" in l[i]:
            lesson_status.append("未选")

    para_list = re.findall("type=checkbox value='(.*?)'.*?></td><td >",
                           information)                                     #选课参数
    id_list = re.findall("value='([0-9]{4}\|[0-9]+\|[0-9]{6}\|.*?)'",
                         information)                                       #详细信息网址id参数

    #填充左边信息框
    if len(lesson) != 0:
        updateLeftBox(lesson, lesson_teacher, lesson_status)

    #获取课程详细信息部分
    lesson_info_threads = []

    for i in range(len(id_list)):
        class_info_list.append([classInfo()])
        lesson_info_threads.append(
            threading.Thread(
                target=Eng_Tong_info_crawing,
                args=(id_list[i], i, para_list[i], lesson[i]),
                name="Eng_Tong_info_crawing()"))                            #开启多线程爬取每门课详细信息
    for i in lesson_info_threads:
        i.start()

#================================================ detailed Info Crawing ================================================
def Eng_Tong_info_crawing(id, ordination, para, lesson):
    id_small_list = []
    count = -1
    url = "http://" + login_ip + "/wsxk/stu_xszx_chooseskbj.aspx?id="                   #详细信息爬虫

    html = requests.post(url + id, cookies=cookie, headers=hea, timeout=10)
    html.encoding = 'gbk'
    while len(html.text) == 0 or "参数不正确" in html.text:
        html = requests.post(url + id, cookies=cookie, headers=hea, timeout=10)         #防止网站抽风

    teacher = re.findall("<a href='#' id=showD.*?>(.*?)</a>", html.text)
    num = re.findall("<td  style='height:20px' align=right.*?>(.*?)<br></td>",          #限选,可选,已选人数
                     html.text)
    sche = re.findall(
        "onclick=openWin\(this\)  value=.*?<br></td>([\s\S]*?)<a",                      #上课时间
        (html.text + "<a"))
    rowSpan = map(
        lambda x: int(x),
        re.findall(
            "<td rowspan='(\d+)' style='height:20px'><br></td>.*?onclick=selradio\(this,1\)",
            html.text))                                                                 #每个班级占表格的多少列
    id = re.findall("value='.*?\[\d{3}\].*?@(.*?)'", html.text)                         #选课参数

    for i in range(len(teacher)):  #
        schedule = re.findall(
            "<td  style='height:20px' align=left >(.*?)<br></td>",
            sche[i])[1].replace("&nbsp;", " ")
        campus = re.findall(
            "<td  style='height:20px'align=left >(.*?)<br></td>", sche[i])[1]
        #合并某些列
        if i != 0 and len(teacher[i]) == 0 and i < sum(rowSpan[:count + 1]):
            teacher[i] = teacher[i - 1]
            id_small_list[count].addSchedule(schedule)
        else:
            count += 1
            info = classInfo()
            info.setAttr(
                teacher=teacher[i],
                limit=num[i * 3],
                optional=num[i * 3 + 1],
                selected=num[i * 3 + 2],
                schedule=schedule,
                campus=campus,
                id=id[count] + "#" + para,
                name=lesson)                            #新建classInfo
            id_small_list.append(info)
    class_info_list[ordination] = id_small_list
    return

#====================================================== Clear ==========================================================
def Clear():
    '''
    * 清除已选课程
    '''
    global select_list
    select_list = []
    selectLesson1.set("")
    selectLesson2.set("")
    selectLesson3.set("")

#================================================== Change Lesson ======================================================
def changeLesson():
    '''
    * 提交修改
    '''
    global select_list
    url = "http://" + login_ip + "/wsxk/stu_btx_rpt.aspx?func=1"
    for c in select_list:
        data = {'id': "TTT," + c.id.encode('gbk')}
        submit = requests.post(url, data=data, cookies=cookie)

    Clear()                                                     #清空选择列表
    leftInfoCrawing()                                           #重新刷新左边信息框


#===================================================== Main ============================================================
if __name__ == "__main__":
    class_info_list = []

    root = Tk()
    root.title("重大选课程序      by Wz")

    Frame1 = Frame(
        root, height=50, width=100).grid(
            row=0, column=0, ipadx=50, pady=50)
    ft1 = tkFont.Font(family='', size=15, weight=tkFont.BOLD)
    ft2 = tkFont.Font(family='', size=12)
    v = IntVar()
    v.set(1)

    for i in range(3):
        Radiobutton(
            Frame1, text=target_list[i], variable=v, value=i + 1,
            font=ft2).grid(
                row=3 + i, column=0, columnspan=2, sticky=W, padx=123)

    uid = Entry(Frame1, width=30, font=tkFont.Font(family='', size=20))
    pwd = Entry(Frame1, show="●", width=30, font=tkFont.Font(family='', size=20))

    #Login Button
    Button(
        Frame1,
        text=' 登录 ',
        command=login_submit,
        height=3,
        width=15,
        font=ft1).grid(
            row=3, column=1, sticky=E, pady=40, rowspan=5)

    #unused padding label
    Label(Frame1, width=17).grid(row=0, column=2, rowspan=2)
    Label(Frame1, height=4, font=ft1).grid(row=2, column=0)
    #user & passwd label
    Label(
        Frame1, text=" 学号", width=11, font=ft1).grid(
            row=0, column=0, sticky=E)
    Label(
        Frame1, text=" 密码", width=11, font=ft1).grid(
            row=1, column=0, sticky=E)

    uid.grid(row=0, column=1)
    pwd.grid(row=1, column=1, rowspan=1)
    root.bind('<Return>', login_submit)

    #Start an thread for checking cookie
    # checkThread = threading.Thread(target=checkCookie)
    # checkThread.setDaemon(True)
    # checkThread.start()
    #Absolute size
    root.resizable(0, 0)
    root.mainloop()
    #============================================= Second root ===========================================================
    if 'Fail' not in cookie.keys():
        root = Tk()
        root.title("选课主界面      by Wz")
        MainFrame = Frame(root, height=15, width=200)
        scrollbar_right = Scrollbar(MainFrame)
        scrollbar_left = Scrollbar(MainFrame)
        scrollbar_rightButtom = Scrollbar(MainFrame, orient='horizontal')
        Listbox_left = Listbox(
            MainFrame,
            height=20,
            width=70,
            yscrollcommand=scrollbar_left.set,
            font="Momospaced")
        Listbox_right = Listbox(
            MainFrame,
            height=19,
            width=42,
            yscrollcommand=scrollbar_right.set,
            xscrollcommand=scrollbar_rightButtom.set,
            font="Momospaced")

        Label(MainFrame, text="课程列表").grid(row=0, column=0, sticky=W)
        Label(
            MainFrame, text="课程信息").grid(
                row=0, column=1, sticky=W, columnspan=2)

        Label(
            root, text="登陆IP: " + login_ip).grid(
                row=1, column=0, sticky=W + N, padx=20, ipady=12)
        Label(
            root, text="登陆账号: " + User).grid(
                row=1, column=0, sticky=W + S, padx=20, ipady=12)

        Button(
            MainFrame,
            text='手动刷新',
            command=leftInfoCrawing,
            font=tkFont.Font(family='', size=9)).grid(
                row=0, column=0, sticky=E, padx=20)
        Button(
            root, text="提交选课", height=3, width=15, command=changeLesson).grid(
                row=1, column=0, sticky=E, padx=20, pady=10)

        Listbox_left.grid(row=1, column=0)
        Listbox_right.grid(row=1, column=2, sticky=N)

        scrollbar_right.config(command=Listbox_right.yview)
        scrollbar_rightButtom.config(command=Listbox_right.xview)
        scrollbar_left.config(command=Listbox_left.yview)
        scrollbar_left.grid(row=1, column=1, sticky=N + S + W + E)
        scrollbar_right.grid(row=1, column=3, sticky=N + S + W + E)
        scrollbar_rightButtom.grid(row=1, column=2, sticky=S + W + E)

        MainFrame.grid(row=0, column=0, padx=20, pady=10)

        selectLesson1 = StringVar()
        selectLesson2 = StringVar()
        selectLesson3 = StringVar()
        selectLesson1.set("")
        selectLesson2.set("")
        selectLesson3.set("")

        Button(
            root,
            text="Clear",
            command=Clear,
            font=tkFont.Font(family='', size=10)).grid(
                row=1, column=0, sticky=S + E, padx=350, pady=10)
        #Selected widget
        Label(
            root, textvariable=selectLesson1).grid(
                row=1, column=0, sticky=N + W, padx=260)
        Label(
            root, textvariable=selectLesson2).grid(
                row=1, column=0, sticky=W, padx=260)
        Label(
            root, textvariable=selectLesson3).grid(
                row=1, column=0, sticky=S + W, padx=260)

        mainThread = threading.Thread(target=leftInfoCrawing, name="leftInfoCrawing()")
        mainThread.setDaemon(True)
        mainThread.start()

        root.resizable(0, 0)
        root.mainloop()
