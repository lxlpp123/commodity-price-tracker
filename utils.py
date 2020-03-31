# -*- coding: utf-8 -*-
import datetime
import platform
import time


# 检查当前操作系统版本信息
def check_os():
    system = platform.system()
    if system == SYSTEM_WINDOWS:
        return SYSTEM_WINDOWS
    if system == SYSTEM_LINUX:
        return SYSTEM_LINUX
    if system == SYSTEM_JAVA:
        return SYSTEM_JAVA
    return SYSTEM_UNKNOWN


# 获取当前屏幕尺寸
def get_screen_size():
    width  = int(1366 * 0.95)
    height = int(768 * 0.95)
    return (width, height)


# 获取当前系统时间
def get_system_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


# 获取当前系统日期
def get_system_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


# 生成指定范围内的日期序列
def gen_range_date(s, e):
    date_s = datetime.date(*s)
    date_e = datetime.date(*e)
    if date_s > date_e:
        return []

    range_date = []
    curr = date_s
    while curr != date_e:
        range_date.append(curr)
        curr += datetime.timedelta(1)
    range_date.append(curr)
    return range_date


if __name__ == "__main__":
    for d in gen_range_date((2020, 4, 1), (2020, 4, 7)):
        print(d)
    