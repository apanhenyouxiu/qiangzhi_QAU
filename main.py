# -*- coding: utf-8 -*-
# @Author : apan
# @Time : 2022/01/10 15:17
# @File : main.py
# @Software: PyCharm

import requests
import os
from lxml import etree
from aip import AipOcr

# 参数配置
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG'
}

aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_cookie():
    host = 'http://jwglxt.qau.edu.cn/'
    session = requests.session()
    session.get(host, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 '
    })
    return session


def get_code(username, password, session):
    str_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon&flag=sess'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 '
    }
    r = session.get(str_url, headers=headers)
    dataStr = r.text
    scode = dataStr.split("#")[0]
    sxh = dataStr.split("#")[1]
    code = username + "%%%" + password
    encode = ""
    i = 0
    while i < len(code):
        if i < 20:
            encode += code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
            scode = scode[int(sxh[i:i + 1]):len(scode)]
        else:
            encode += code[i:len(code)]
            i = len(code)
        i += 1
    # print('encode is :', encode)
    return encode


def get_verify_code(session):
    img_url = 'http://jwglxt.qau.edu.cn/verifycode.servlet'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 '
    }
    r = session.get(img_url, headers=headers)
    # 利用百度AI识别验证码
    result = aipOcr.basicGeneral(r.content, options)
    try:
        if not os.path.exists('./result/'):
            os.makedirs('./result/')
        with open('./result/verify_code.png', 'wb') as f:
            f.write(r.content)
        text = result['words_result'][0]['words'].split()
        text = ''.join(text)
        print('AI识别的验证码为：{}'.format(text))
        if len(text) != 4:
            print("AI识别的错误验证码为{}".format(text))
            text = ""
            # if not os.path.exists('./result/'):
            #     os.makedirs('./result/')
            # with open('./result/verify_code.png', 'wb') as f:
            #     f.write(r.content)
            text = input("请打开本地图片，识别图中的验证码！\n")
            return text
        return text
    except :
        print("获取验证码失败。")

def login(encoded, verify_code, session):
    login_url = 'http://jwglxt.qau.edu.cn/Logon.do?method=logon'
    data = {
        'useDogCode': '',
        'encoded': encoded,
        'RANDOMCODE': verify_code
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36 '
    }
    r = session.post(login_url, headers=headers, data=data)
    try:
        html = etree.HTML(r.text)
        user_list = html.xpath('//div[5]/div/div[3]/text()')
        user = ''.join(user_list)
        if len(user) == 0:
            print('验证码识别错误，请重新登陆。')
        else:
            print('登陆成功，登陆用户为 : ', user)
    except:
        print('登录失败。\n')


if __name__ == '__main__':
    # username = input("请输入用户名：")
    # password = input("请输入密码：")
    username = ''
    password = ''
    session = get_cookie()
    verify_code = get_verify_code(session)
    encoded = get_code(username, password, session)
    login(encoded, verify_code, session)
