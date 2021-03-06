import gzip
import ssl
import urllib.request
import http.cookiejar

import re
from urllib.parse import urlencode

import json

from bs4 import BeautifulSoup

#自行添加帐号密码或是输入change之后添加
user = ""
password = ""
TOKEN = ""
TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3"
INDEX_URL = "http://www.baidu.com/"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"
TIEBA_URL = "http://tieba.baidu.com"
LIKE_URL = "http://tieba.baidu.com/f/like/mylike"
SIGN_URL = "http://tieba.baidu.com/sign/add"
# 跳过证书验证
ssl._create_default_https_context = ssl._create_unverified_context

loginHeaders = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
    "Host":"passport.baidu.com",
    'Upgrade-Insecure-Requests':'1',
    "Origin":"http://www.baidu.com",
    "Referer":"http://www.baidu.com/",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
}

bdData = {
    "staticpage":"https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
    "token":"",
    "tpl":"pp",
    "username":user,
    "password":password,
    "loginmerge":"true",
    "mem_pass":"on",
    "logintype":"basicLogin",
    "logLoginType":"pc_loginBasic",
}

signData = {
    "ie":"utf-8",
    "kw":"",
    "tbs":""
}

def setUser(userName):
    global user
    user = userName
    bdData["username"] = user

def setPassword(passWord):
    global password
    password = passWord
    bdData["password"] = password

def start():
    cj = http.cookiejar.LWPCookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    try:
        opener.open(INDEX_URL)
    except:
        print("网络问题 无法为您获取token,正在退出...")
        return
    return opener

def main():
    try:
        opener = start()
    except:
        return
    #get TOKEN
    print("Loading...正在获取token:")
    try:
        data = opener.open(TOKEN_URL).read()
        TOKEN = re.compile("\"token\"\s+:\s+\"(\w+)\"").findall(str(data))[0]
        bdData["token"] = TOKEN
        print("token获取成功:" + TOKEN)
    except:
        print("网络问题 无法为您获取token,正在退出...")
        return
    #login
    request = urllib.request.Request(LOGIN_URL, headers=loginHeaders)
    print("正在为" + user + "进行登录操作")
    try:
        result = opener.open(request, urlencode(bdData).encode('utf-8')).read()
        result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
    except:
        print("网络问题,无法登录,正在退出...")
        return
    result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
    ##judge
    try:
        if result["no"] == 0:
            print(user + "登录成功!")
        else:
            print("反正我不知道哪里挂了不上去!正在退出...")
            return
    except:
        print("帐号或密码错误,正在退出...")
        return
    #get my bars
    LIKE_LIST = []
    print("\n待签贴吧:")
    for ba in re.compile("<a href=\"([^\"]+)\" title=\"([^\"]+)\">").findall(opener.open(LIKE_URL).read().decode('gbk')):
        LIKE_LIST.append((ba[0], ba[1]))
        print(ba[1])

    #aoto sign
    print("\n正在为您自动签到...")
    for bar in LIKE_LIST:
        try:
            data = opener.open(TIEBA_URL + bar[0]).read().decode('utf-8')
            tbs = re.compile("'tbs': \"(\w+)\"").findall(data)
            signData["tbs"] = tbs
            signData["kw"] = bar[1]
            result = json.loads(opener.open(SIGN_URL, urlencode(signData).encode('utf-8')).read().decode("utf-8"))
            if  result["no"] == 0:
                print(bar[1] + "吧 签到成功!")
            if result["no"] == 1101:
                print(bar[1] + "吧 今天已经签到了!")
        except:
            print(bar[1] + "遇到细节问题,签到失败!")
            continue
    print("签到完毕\n")

if __name__ == "__main__":
    main()
    while True:
        print("输入exit退出脚本,输入change进行注销!\n")
        command = input()
        if command == 'exit':
            print("Good-bye")
            exit(0)
        if command == 'change':
            print("帐号:")
            user = input()
            setUser(user)
            print("密码:")
            password = input()
            setPassword(password)
            main()
            continue
        print("输入有误!")