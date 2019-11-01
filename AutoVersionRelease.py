#coding=utf-8
import urllib.request
import jenkins
import time
import json

class AutoVersionRelease():
    # 信息发送方法 钉钉接口消息发送需要与关键字匹配，改接口的关键字为 测试，所以所有的消息体中都要包含 测试 关键字
    def send_msg(self,msg):
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
        # 目标消息体 塞到data中
        data['text']['content']=msg
        # 转格式
        sendData = json.dumps(data)
        sendDatas = sendData.encode("utf-8")
        # 消息发送
        request = urllib.request.Request(url=url, data=sendDatas,headers=header)
        opener = urllib.request.urlopen(request)
        # 打印 发送结果
        # print(opener.read())

    def objectBuild(self):
        # jenkins 的地址
        url = 'http://jenkins.ysskj.com/'
        # 工程名称
        objectName = 'qa-supervise-eeop'
        # 创建jenkins对象
        jenkinsObject = jenkins.Jenkins(url=url, username='liyuan', password='liyuan')
        self.send_msg("测试：{}工程开始构建。".format(objectName))
        # 获取工程构建的信息
        objectInfo = jenkinsObject.get_job_info(objectName)
        # 获取下次构建的数值
        nextBulitTime = objectInfo['nextBuildNumber']
        # 构建工程 “qa-supervise-eeop”
        jenkinsObject.build_job(objectName)
        # 添加等待时间 确认工程确实构建中
        time.sleep(30)
        self.send_msg("测试：{}工程正在构建中".format(objectName))
        # 获取正在运行中的工程名称
        runningObjects = jenkinsObject.get_running_builds()
        # 判断工程是否在构建中，如果在构建中，则等待30s
        while True:
            for runningObject in runningObjects:
                if runningObject['name'] == objectName:
                    time.sleep(30)
                    continue
            break

        # 获取工程构建的信息
        objectInfoNew = jenkinsObject.get_job_info(objectName)
        # 获取最近构建数值 lastBuildNum
        lastBuildNum = objectInfoNew['lastBuild']['number']

        if lastBuildNum == nextBulitTime:
            while True:
                buliding = jenkinsObject.get_build_info(objectName,lastBuildNum)['building']
                if buliding:
                    time.sleep(5)
                else:
                    break
            result = jenkinsObject.get_build_info(objectName,lastBuildNum)['result']
            if result == 'SUCCESS':
                self.send_msg("测试：{}工程构建成功，可以测试了".format(objectName))
            else:
                self.send_msg("测试：工程{}构建失败，请查看原因:{}".format(objectName, url))
        else:
            self.send_msg("测试：{}工程构建异常,请查看：{}".format(objectName, url))


if __name__ == "__main__":
    avr = AutoVersionRelease()
    avr.objectBuild()




