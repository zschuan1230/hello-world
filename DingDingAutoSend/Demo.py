#coding=utf-8
import datetime
import json
import urllib.request

def send_msg():
    url = "https://oapi.dingtalk.com/robot/send?access_token=788bcd0e63674313f3f03b232396a212dd213aadc1cd03e55c1bf2f19d4f9c78"
    header = {
        "Content-Type":"application/json",
        "Charset":"UTF-8"
    }

    data = {
        "msgtype": "text",
        "text": {
            "content":"这是一条测试数"
        },
        "at":{
            "isAtAll":True
        }
    }

    sendData = json.dumps(data)
    sendDatas = sendData.encode("utf-8")

    request = urllib.request.Request(url=url, data=sendDatas,headers=header)
    urllib.request.urlopen(request)
    # opener = urllib.request.urlopen(request)
    #
    # print(opener.read())



if __name__ == "__main__":
    send_msg()