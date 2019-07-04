# encoding: utf-8
import os
import requests
import base64
import re
import hashlib
import time

def create_dir(dir_path):
    if os.path.isdir(dir_path):
        pass
    else:
        os.mkdir(dir_path)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def change_config_file(path, string, replace_str):
    """
    替换文件中的str变为replace_str
    :param path: 文件地址
    :param string: 准备替换的string
    :param replace_str: 替换的string
    :return:
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            if string in line:
                line = line.replace(string, replace_str)
            f.write(line)
        f.close()

def replace_str(target, string, replace_str):
    """
    替换字符串中的str变为replace_str
    :type target: str
    :type string: str
    :type replace_str: str
    :rtype: str
    """
    new_str = re.sub(re.compile(string), replace_str, target)
    return new_str


def decode_base64_string(string):
    """
    :param string: base64编码的字符串
    :return: base64解码的字符串
    """
    return base64.b64decode(str(string)).decode('utf-8')

def get_content_by_auth(username, password, url):
    auth = (username, password)
    res = requests.get(url, auth=auth).content
    return res

def change_str_by_list(str, array, replace_array):
    """

    :param str:
    :param array:
    :param replace_array:
    :return:
    """
    if len(array) != len(replace_array):
        raise Exception("Error")
    for idx in range(len(array)):
        string = '\${' + array[idx] + '}'
        replace_string = replace_array[idx]
        str = replace_str(str, string, replace_string)
    return str

def check_email(email):
    """
    检测邮箱格式
    :param email:
    :return:
    """
    if not isinstance(email, str):
        raise Exception("Input email need a string type")

    if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', email):
        return False
    return True

def check_phone(phone):
    """
    检测手机号格式
    :param phone:
    :return:
    """
    if not isinstance(phone, str):
        raise Exception("Input email need a string type")

    if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', phone):
        return False
    return True

def sha_256(string):
    string = str(string)
    return hashlib.sha256(string.encode(encoding='utf-8')).hexdigest()

def get_current():
    return time.time()


