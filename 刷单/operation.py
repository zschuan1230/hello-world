#coding=utf-8
import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import pymysql
import random
import re
from PIL import Image
import pandas as pd
import cv2


class Operation:
    """
    该类是个操作类，用于存放相关操作的方法
    """
    def __init__(self):
        self.suning_config = yaml.load(open('config.yaml', "r", encoding='utf8'))
        print("suning_config:{}".format(self.suning_config))
        # 初始化浏览器
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # 获取全屏下浏览器长宽
        self.chromesize = self.driver.get_window_size()
        # 获取全屏下浏览器的初始位置
        self.chromelocation = self.driver.get_window_position()

    def login(self):
        """
        登录
        :param driver:
        :return:
        """
        # 打开url
        self.driver.get(
            'https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
        time.sleep(2)
        # 点击登录按钮跳转到登录页面
        self.driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[1]/a[3]').click()
        time.sleep(3)
        try:
            # 点击账号密码登录,如果找不到则认为，已登录
            # /html/body/div[1]/div[7]/a[2]
            self.driver.find_element_by_xpath('/html/body/div[1]/div[7]/a[2]').click()
        except:
            time.sleep(1.5)
            # 退出登录
            self.log_out()
            self.login()
            return None
            # time.sleep(1.5)
            # # 返回上个页面，并结束登录操作
            # driver.back()
            # time.sleep(1.5)
            # return None
        # 输入用户名或者密码
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.suning_config['userInfo']['user'])
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.suning_config['userInfo']['pwd'])
        time.sleep(2)
        # 判断是否有验证码出现
        try:
            # 循环2次破解拖拽验证码，验证通过点击登录，如果4次都没有验证通过，则程序抛异常停止
            for i in range(3):
                self.verify_code_drag()
                # 获取 验证码框旁的文字信息
                ele = self.driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[2]').text
                print("%%%-ele", ele)
                if ele == u'验证通过':
                    print("开始点击登录")
                    # 点击登录 /html/body/div[2]/div[7]/a[1]
                    self.driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
                    print("准备跳出循环")
                    break
                if i == 2:
                    raise Exception("验证码未出现，可直接点击登录")
        except Exception as e:
            print(e)

    def log_out(self):
        """
        退出登录，从我的易购页面开始退出
        :param driver:
        :return:
        """
        # 点击设置按钮
        self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/a').click()
        time.sleep(2)
        # 页面下滑 200 ，以方便找到退出登录按钮
        self.page_drag(100)
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/a[8]').click()
        time.sleep(2)
        # 点击确定
        self.driver.find_element_by_xpath('//*[@id="alertBox_0"]/div[3]/a[2]').click()
        time.sleep(2)

    def get_track(self,distance):
        """
        拖拽距离随机切割，以创建不同的运动轨迹，应为相同的运动轨迹会被认为是机器在操作，导致校验不过
        :param distance:
        :return:
        """
        res = []
        # 随机切割3-6段
        n = random.randint(3, 8)
        for i in range(0, n):
            f = random.randint(2, 9)
            dis = distance / f
            res.append(round(dis))
            distance -= round(dis)
        res.append(distance)
        return res

    def verify_code_drag(self):
        """
        实现拖拽验证码的验证
        :param driver:
        :return:
        """
        # 找到滑块元素
        ele = self.driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]/div[3]')
        time.sleep(3)
        # 获取滑块元素位置
        lc = ele.location
        print("滑块位置信息：{}".format(lc))
        if lc == {'x': 0, 'y': 0}:
            print("验证码未出现，直接点击登录")
            # 点击登录
            self.driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
            time.sleep(2)
            return None
        # 滑块大小
        sliderSize = ele.size
        print(lc)
        # 获取屏幕大小
        window_size = self.driver.get_window_size()
        print(window_size)
        # 获取拖拽框元素
        el = self.driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]')
        # 获取拖拽框的大小
        s = el.size
        print(s['width'])
        print(ele.size)
        # 获取移动轨迹
        track = self.get_track(s['width'])
        print(track)
        # 计算滑块元素在屏幕中的实际位置 X
        t_x = lc['x'] * self.suning_config['parm']['ratioX']
        # 鼠标移动滑块上 设备不同肯能有偏差请根据实际情况调试
        pyautogui.dragTo(x=t_x + sliderSize['width'] * self.suning_config['parm']['ratioX'] / 2,
                         y=lc['y'] * self.suning_config['parm']['ratioY'] + window_size['height'] - self.suning_config['parm']['bodyhight'],
                         duration=1, tween=pyautogui.easeInOutQuad)
        # 按下鼠标
        pyautogui.mouseDown(x=t_x + sliderSize['width'] * self.suning_config['parm']['ratioX'] / 2,
                            y=lc['y'] * self.suning_config['parm']['ratioY'] + window_size['height'] - self.suning_config['parm']['bodyhight'] - 3)
        # 按之前获取的轨迹拖拽移动鼠标
        for x in track:
            pyautogui.moveRel(xOffset=x * self.suning_config['parm']['ratioX'],
                              yOffset=0,
                              duration=1, tween=pyautogui.easeInOutQuad)
            time.sleep(0.3)
        # 移动鼠标防止之前获取的距离过短
        pyautogui.moveRel(xOffset=20,
                          yOffset=3,
                          duration=1, tween=pyautogui.easeInOutQuad)
        # 鼠标抬起
        pyautogui.mouseUp()
        time.sleep(2)

    def pay(self):
        """
        付款方法
        :return:
        """
        # 切换ua为正常的chrome -default模式
        self.chang_UA()
        print("UA changed")
        time.sleep(1.5)
        # 打开pc版的苏宁
        self.driver.get('https://my.suning.com/?safp=d488778a.homepage1.P5ptt.1')
        time.sleep(1)
        # 点击我的订单
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/a/span').click()
        time.sleep(1)
        # 点击代付款
        self.driver.find_element_by_xpath('//*[@id="li_status_wait_pay"]/a').click()
        time.sleep(1.5)
        # 点击马上支付 [contains(@id, "am-modal-container")]
        ele = self.driver.find_element_by_xpath('//*[contains(@id, "operation")]/div[2]/a')
        time.sleep(1)
        if ele.text == u'马上支付':
            ele.click()
            time.sleep(5)
            # 鼠标移动第一个密码输入框上
            pyautogui.moveTo(x=500, y=590, duration=1)
            # 鼠标点击
            pyautogui.click()
            # 模拟输入密码
            pyautogui.typewrite(self.suning_config['userInfo']['password'])
            time.sleep(2)
            # 点击确认付款
            # driver.find_element_by_xpath('//*[@id="confirmPay"]').click()

            # # 付款完成后获取当前时间用于判断短信验证码是否是最新的
            # time_pay = time.strftime('%Y-%m-%d %H:%M:%S')
            # # 获取验证码
            # for i in range(4):
            #     time.sleep(30)
            #     result = get_verification_code(time_pay,'13057523552')
            #     # 判断是否获取到验证码
            #     if result == None or result == []:
            #         continue
            #         if i == 3:
            #             raise Exception("验证码发送失败")
            #     break

        # UA切换为手机版本
        self.chang_UA(dis=72)
        # 付完款返回易购登录页面
        self.driver.get(
            'https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
        time.sleep(1.5)

    def chang_UA(self,dis=0):
        """
        模拟人操作切换user agent，不同的设备需要调试下距离
        :param dis: dis=0切换到chrome-default模式；dis =72 切换到android-android kitkat模式
        :return:
        """
        time.sleep(1)
        # 鼠标移动插件控制按钮上，并点击
        pyautogui.moveTo(1820, 50, duration=1)
        time.sleep(1)
        pyautogui.click()
        # 鼠标移动到chrome上并点击
        pyautogui.moveTo(1700, 80 + dis, duration=1)
        # time.sleep(10)
        pyautogui.click()
        time.sleep(1)
        # 鼠标移动到default上，并点击
        pyautogui.moveTo(1600, 80, duration=1)
        pyautogui.click()
        time.sleep(1)
        # 鼠标移动插件控制按钮上，并点击 关闭插件控制按钮
        pyautogui.moveTo(1820, 50, duration=1)
        time.sleep(1)
        pyautogui.click()

    def page_drag(self,dis=0):
        """
        页面滑动
        :param dis:
        :return:
        """
        windowSize = self.driver.get_window_size()
        print(windowSize)
        # 移动到页面滑条位置
        pyautogui.moveTo(1910, windowSize['height'] - self.suning_config['parm']['bodyhight'] + 30, duration=1)
        # 往下滑动页面dis距离
        pyautogui.dragTo(1910, windowSize['height'] - self.suning_config['parm']['bodyhight'] + 30 + dis, duration=1)
    def page_back(self):
        """
        页面滑条回到最上方,试用与滑条较长的 要是滑条较度，该方法精度可能不够，需要自己调试下
        :return:
        """
        windowSize = self.driver.get_window_size()
        # 移动到页面滑条位置
        pyautogui.moveTo(1910, windowSize['height'] - self.suning_config['parm']['bodyhight'] + 30, duration=1)
        pyautogui.click()

    def get_verification_code(self,time_pay, phonum):
        """
        链接数据库，在数据库中查找短信验证信息
        :param time_pay:
        :param phonum:
        :return:
        """
        # 数据库链接
        db = pymysql.connect(self.suning_config['mysqlInfo']['mysqlIp'],
                             self.suning_config['mysqlInfo']['mysqlUser'],
                             self.suning_config['mysqlInfo']['mysqlPwd'],
                             self.suning_config['mysqlInfo']['mysqlDb'], charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 查询sql
        sql = "select smsContent,smsDate from sms_recv where PhoNum = '{}' order by smsDate desc ".format(phonum)
        print(sql)
        # 使用execute方法执行SQL语句
        cursor.execute(sql)
        # 使用 fetchone() 方法获取一条数据 获取的是该手机号的最新一条信息
        data = cursor.fetchone()
        print(data)
        # 关闭链接
        cursor.close()
        # 未匹配的内容返回None
        if data == None:
            return None
        # 短信接收时间
        sms_date = data[1]
        # 最新短信时间小于支付时间，该短信不是最新验证码，返回None
        if time_pay > sms_date:
            return None
        # 正则匹配 匹配出六位数字的验证码信息
        pattern = re.compile(r'\d{4}')
        result = pattern.findall(data[0])
        print(result)
        return result

    # todo 验证码识别函数
    def Polarshadowverificationcode(self):

        # # 获取 全屏下网页的长和宽
        # websize = driver.find_element_by_xpath('/html/body').size
        # 保存 chrome页面截图
        time.sleep(1)
        self.driver.save_screenshot('screenshot.png')
        # todo 将数据移到小滑块中心位置 滑块元素 /html/body/div[5]/div[2]/div[2]/div[1]/div[3]/img
        self.drag_source('//*[@id="view"]/div[2]/div[2]/div[2]/div[1]/div[3]/img')
        # 获取验证码大图片的的元素大小和位置 图的元素
        image = self.driver.find_element_by_xpath('//*[@id="view"]/div[2]/div[2]/div[2]/div[1]/div[3]/canvas')
        # 获取验证码滑块拖动图标的的元素大小和位置 滑块元素
        smallimage = self.driver.find_element_by_xpath('//*[@id="view"]/div[2]/div[2]/div[2]/div[1]/div[3]/img')
        imagesize = image.size
        imagelocation = image.location
        smallimagesize = smallimage.size
        smallimagelocation = smallimage.location
        # print(imagesize, imagelocation, smallimagesize, smallimagelocation)

        # 定义验证码大图片的四个顶点的位置
        left = imagelocation['x']
        top = imagelocation['y']
        right = imagelocation['x'] + imagesize['width']
        bottom = imagelocation['y'] + imagesize['height']

        # 计算验证码小图片在大图片中的相对位置
        x1 = smallimagelocation['x'] - imagelocation['x'] + 12
        y1 = smallimagelocation['y'] - imagelocation['y'] + 12
        x2 = x1
        y2 = y1 + 40
        x3 = x1 + 40
        y3 = x1
        x4 = x1 + 40
        y4 = x1 + 40
        # 对验证码图片进行截图并保存
        im = Image.open('screenshot.png')
        im = im.crop((left + 5, top + y1 + 1, right - 5, top + y2 - 1))
        im.save('screenshot.png')

        # 读取截取到的验证码图片
        img = cv2.imread('screenshot.png')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aims_gray = gray

        # 将验证码灰度图矩阵转换为DataFrame
        data = pd.DataFrame(aims_gray)
        # 获取每一列的统计信息
        dataimage = data.describe().T
        # 得到 初始拖动验证码没有缺口边的x位置
        dataimage1 = dataimage.iloc[:47, :]
        # print(dataimage1)

        smallimagecompletesideX = dataimage1['std'].idxmin()
        # 获取验证码阴影没有缺口边的x位置
        dataimage = dataimage.iloc[50:249, :]
        dataimage = dataimage[dataimage['std'] < 20]
        # 之前的最优是100 todo
        dataimage = dataimage[dataimage['mean'] < 100]
        # print(dataimage)
        imagecompletesideX = dataimage['std'].idxmin()
        # 根据边的位置不同 确定中心点x坐标
        if smallimagecompletesideX < 30:
            imagecompletesideX = imagecompletesideX + 20
        else:
            imagecompletesideX = imagecompletesideX - 20
            # print(smallimagecompletesideX, imagecompletesideX)
        # 按下鼠标
        pyautogui.mouseDown()
        track = self.get_track(imagecompletesideX + 5 - 32 - self.chromelocation['x'])
        #  进行鼠标相对移动
        for i in track:
            pyautogui.moveRel(xOffset=i,
                              yOffset=0,
                              duration=1, tween=pyautogui.easeInOutQuad)
        time.sleep(1)
        pyautogui.mouseUp()

    def drag_source(self,xpath):
        '''
        找到元素 鼠标移动过去
        :param xpath:
        :return:
        '''
        element = self.driver.find_element_by_xpath(xpath)
        # print(element.size)
        # print(element.location)

        pyautogui.moveTo(x=element.location['x'] + element.size['width'] / 2,
                         y=element.location['y'] + element.size['height'] / 2 + self.chromelocation['y'] * 2 + self.chromesize[
                             'height'] - self.suning_config['parm']['bodyhight'],
                         duration=1, tween=pyautogui.easeInOutQuad)
        time.sleep(1)

