# coding=utf-8

import os
import json


# 返回全部三方库的路径，并将点分分隔的路径，转换为/分隔的路径，作为在zip文件中的相对路径
def load_3rd_lib(_3rd_file_name):
    packages = []
    try:
        fi = open(_3rd_file_name, 'r')
        buffer = fi.read()
        _3rd_lict = json.loads(buffer.strip('\r\n'))
    except Exception as e:
        print(e)
        return []
    for _3rd_dict in _3rd_lict:
        # 压缩包中前两级为src/sources/，这里补全文件在压缩包的完整路径
        packages.append('src/sources/' + _3rd_dict['Package'][1:])
    return packages


# 返回全部三方库的路径，并保留原始的点分隔的格式
def load_3rd_lib_dot(_3rd_file_name):
    packages_dot = []
    try:
        fi = open(_3rd_file_name, 'r')
        buffer = fi.read()
        _3rd_lict = json.loads(buffer.strip('\r\n'))
    except Exception as e:
        print(e)
        return []
    for _3rd_dict in _3rd_lict:
        # 压缩包中前两级为src/sources/，这里补全文件在压缩包的完整路径
        packages_dot.append(_3rd_dict['Package'][1:].replace('/', '.'))
        # packages_slash.append('src/sources/' + _3rd_dict['Package'][1:])
    return packages_dot


if __name__ == '__main__':
    packages = load_3rd_lib('/home/alvin/Desktop/ffd5efd46b2b861b8b11e71c6ba00ea891c854029ebb407500c38aed86e9e880.3rd')
    print(packages)
