#coding:utf-8

'''
* 一些字符格式化方法
'''

def is_chinese(uchar):
    """判断一个unicode是否是汉字,全角字符，罗马数字1-9"""
    if (uchar >= u'\u2E80' and uchar <= u'\uFE4F') or(uchar >= u'\uFF00' and uchar <= u'\uFFEF')or(uchar >= u'\u2160' and uchar <= u'\u2168'):
        return True
    else:
        return False
def align( text, width, just ="left"):
    stext = str(text)
    utext = stext.decode("utf-8")  #对字符串进行转码
    cn_count = 0
    for u in utext:
        if is_chinese(u):
            cn_count += 2 # 计算中文字符占用的宽度
        else:
            cn_count += 1  # 计算英文字符占用的宽度
    if just == "right":
        return " " * (width - cn_count ) + stext
    elif just == "left":
        return stext + " " * ( width - cn_count )

def fifter(x):
    if len(x)>6:
        x=x[6:]
    if len(x)==1:
        x=u' '
    return x

def string_ljust( text, width ):
    return align( text, width, "left" )
def string_rjust( text, width ):
    return align( text, width, "right" )

#超长部分用...代替
def standardized(text,length):
    if len(text)>length:
        return text[:length]+"..."
    return text
