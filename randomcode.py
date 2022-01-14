# -*- coding: utf-8 -*-
# @Author : apan
# @Time : 2022/01/10 16:59 
# @File : randomcode.py
# @Software: PyCharm


from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    image = get_file_content('result/verify_code.png')
    m = client.basicGeneral(image)
    text = m['words_result'][0]['words']
    print(text)
    print(type(text))