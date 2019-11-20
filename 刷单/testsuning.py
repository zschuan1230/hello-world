#coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import pymysql
import random
import re

"""

    账号 ：13057523552 密码：qiujikai4971113
    易付宝支付
    支付密码203479
"""


# 浏览器页面高度,可以打开百度，元素选择body，查看下浏览去页面高度数据
bodyhight = 937
# x坐标系数 实际屏幕宽度/分辨率 例如：实际屏幕大小( window_size = driver.get_window_size()) {'width': 1936, 'height': 1056}  分辨率1920-1080 1920/1936
ratioX = 0.991
# y坐标系数 1080/1056
ratioY = 1.0227
# 用户/密码设置
user = '13057523552'
pwd = 'qiujikai4971113'
# 付款密码 - 一定要是字符串格式
password = ['2', '0', '3', '4', '7', '9']
# 数据库 相关设置
mysqlIp = '192.168.10.64'
mysqlUser = 'root'
mysqlPwd = 'tang123456'
mysqlDb = 'spcard'


def get_driver():
    """
    获取浏览器驱动
    :return:
    """
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\dell\AppData\Local\Google\Chrome\User Data"

    # zsc script
    # os.system(r'chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\dell\AppData\Local\Google\Chrome\User Data"')
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print(driver.title)
    return driver

def login(driver):
    """
    登录
    :param driver:
    :return:
    """
    # 打开url
    driver.get('https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
    time.sleep(2)
    # 点击登录按钮跳转到登录页面
    driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[1]/a[3]').click()
    time.sleep(3)
    try:
        # 点击账号密码登录,如果找不到则认为，已登录
        # /html/body/div[1]/div[7]/a[2]
        driver.find_element_by_xpath('/html/body/div[1]/div[7]/a[2]').click()
    except:
        time.sleep(1.5)
        # 退出登录
        log_out(driver)
        login(driver)
        return None
        # time.sleep(1.5)
        # # 返回上个页面，并结束登录操作
        # driver.back()
        # time.sleep(1.5)
        # return None
    # 输入用户名或者密码
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(user)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    time.sleep(2)
    # 判断是否有验证码出现
    try:
        # 循环2次破解拖拽验证码，验证通过点击登录，如果4次都没有验证通过，则程序抛异常停止
        for i in range(3):
            verify_code_drag(driver)
            # 获取 验证码框旁的文字信息
            ele = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div[2]').text
            print("%%%-ele",ele)
            if ele == u'验证通过':
                print("开始点击登录")
                # 点击登录 /html/body/div[2]/div[7]/a[1]
                driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
                print("准备跳出循环")
                break
            if i == 2:
                raise Exception("验证码未出现，可直接点击登录")
    except Exception as e:
        print(e)

def log_out(driver):
    """
    退出登录，从我的易购页面开始退出
    :param driver:
    :return:
    """
    # 点击设置按钮
    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/a').click()
    time.sleep(2)
    # 页面下滑 200 ，以方便找到退出登录按钮
    page_drag(200)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/a[8]').click()
    time.sleep(2)
    # 点击确定
    driver.find_element_by_xpath('//*[@id="alertBox_0"]/div[3]/a[2]').click()
    time.sleep(2)





def get_track(distance):
    """
    拖拽距离随机切割，以创建不同的运动轨迹，应为相同的运动轨迹会被认为是机器在操作，导致校验不过
    :param distance:
    :return:
    """
    res = []
    # 随机切割3-6段
    n = random.randint(3,8)
    for i in range(0,n):
        f = random.randint(2,9)
        dis = distance / f
        res.append(round(dis))
        distance -= round(dis)
    res.append(distance)
    return res


def verify_code_drag(driver):
    """
    实现拖拽验证码的验证
    :param driver:
    :return:
    """
    # 找到滑块元素
    ele = driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]/div[3]')
    time.sleep(3)
    # 获取滑块元素位置
    lc = ele.location
    if lc == {'x': 0, 'y': 0}:
        print("验证码未出现，直接点击登录")
        # 点击登录
        driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
        time.sleep(2)
        return None
    # 滑块大小
    sliderSize=ele.size
    print(lc)
    # 获取屏幕大小
    window_size = driver.get_window_size()
    print(window_size)
    # 获取拖拽框元素
    el = driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]')
    # 获取拖拽框的大小
    s = el.size
    print(s['width'])
    print(ele.size)
    # 获取移动轨迹
    track = get_track(s['width'])
    print(track)
    # 计算滑块元素在屏幕中的实际位置 X
    t_x = lc['x']*ratioX
    # 鼠标移动滑块上 设备不同肯能有偏差请根据实际情况调试
    pyautogui.dragTo(x=t_x+sliderSize['width']*ratioX/2,
                     y=lc['y']*ratioY+window_size['height']-bodyhight,
                     duration=1, tween=pyautogui.easeInOutQuad)
    # 按下鼠标
    pyautogui.mouseDown(x=t_x+sliderSize['width']*ratioX/2,
                     y=lc['y']*ratioY+window_size['height']-bodyhight-3)
    # 按之前获取的轨迹拖拽移动鼠标
    for x in track:
        pyautogui.moveRel(xOffset=x*ratioX,
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

def buy_something(driver):
    """
    购买商品 【洽洽】山核桃味葵花籽坚果零食炒货批500g
    :param driver:
    :return:
    """
    windowSize = driver.get_window_size()
    print(windowSize)
    driver.get('https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
    # 点击搜索 并输入收搜 内容
    # 点击首页中的搜索
    driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[2]/div/a').click()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="searchAssInp"]').send_keys('三体')
    time.sleep(1)
    # 点击收搜
    driver.find_element_by_xpath('//*[@id="wapSearchURL"]').click()
    # 页面下滑100
    page_drag(dis=100)
    time.sleep(1)
    # 选择目标商品
    #  //*[@id="wapssjgy_search_pro_baoguang-1-0-1_1_1_0070718561_11025632299_0__"]/div[2]/p
    driver.find_element_by_xpath(
        '//*[@id="wapssjgy_search_pro_baoguang-1-0-1_1_1_0070718561_11025632299_0__"]/div[2]/p').click()
    time.sleep(1)
    try:
        # 处理页面提示 如果有则点击继续浏览
        driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/span').click()
    except:
        pass
    # 点击立即抢购
    driver.find_element_by_xpath('//*[@id="buyNow"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tbuyNow"]').click()
    time.sleep(1.5)
    # 滑动页面 200
    page_drag(dis=200)

    # 选择苏宁支付 的方式支付
    # //*[@id="app"]/div/div/div[3]/div[4]/div/div[1]/div/p
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div[4]/div/div[1]/div/p').click()
    time.sleep(1)
    # 短信验证码部分
    try:
        # 点击获取验证码按钮
        driver.find_element_by_xpath('//*[contains(@id,"am-modal-container")]/div/div[2]/div/div/div[1]/div/div/div').click()
        # 点击获取后 获取当前时间用于判断短信验证码是否是最新的
        time_pay = time.strftime('%Y-%m-%d %H:%M:%S')
        # 获取验证码
        for i in range(4):
            time.sleep(30)
            result = get_verification_code(time_pay, user)
            # 判断是否获取到验证码
            if result == None or result == []:
                continue
                if i == 3:
                    raise Exception("验证码发送失败")
            break
        # 输入之前的验证码
        driver.find_element_by_xpath(
            '//*[contains(@id, "am-modal-container")]/div/div[2]/div/div/div[1]/div/div/input').send_keys(result)
        time.sleep(0.7)
        # 点击确定
        driver.find_element_by_xpath(
            '//*[contains(@id, "am-modal-container")]/div/div[2]/div/div/div[2]/div/a[2]').click()
        time.sleep(1)
    except Exception as e:
        print(e)
    time.sleep(2)

def pay():
    """
    付款方法
    :return:
    """
    # 切换ua为正常的chrome -default模式
    chang_UA()
    print("UA changed")
    time.sleep(1.5)
    # 打开pc版的苏宁
    driver.get('https://my.suning.com/?safp=d488778a.homepage1.P5ptt.1')
    time.sleep(1)
    # 点击我的订单
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[3]/a/span').click()
    time.sleep(1)
    # 点击代付款
    driver.find_element_by_xpath('//*[@id="li_status_wait_pay"]/a').click()
    time.sleep(1.5)
    # 点击马上支付 [contains(@id, "am-modal-container")]
    ele = driver.find_element_by_xpath('//*[contains(@id, "operation")]/div[2]/a')
    time.sleep(1)
    if ele.text == u'马上支付':
        ele.click()
        time.sleep(5)
        # 鼠标移动第一个密码输入框上
        pyautogui.moveTo(x=500, y=580, duration=1)
        # 鼠标点击
        pyautogui.click()
        # 模拟输入密码
        pyautogui.typewrite(password)
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
    chang_UA(dis=72)

def chang_UA(dis=0):
    """
    模拟人操作切换user agent，不同的设备需要调试下距离
    :param dis: dis=0切换到chrome-default模式；dis =72 切换到android-android kitkat模式
    :return:
    """
    time.sleep(5)
    # 鼠标移动插件控制按钮上，并点击
    pyautogui.moveTo(1820,50,duration=1)
    time.sleep(1)
    pyautogui.click()
    # 鼠标移动到chrome上并点击
    pyautogui.moveTo(1700, 80+dis,duration=1)
    # time.sleep(10)
    pyautogui.click()
    time.sleep(1)
    # 鼠标移动到default上，并点击
    pyautogui.moveTo(1600,80,duration=1)
    pyautogui.click()
    time.sleep(1)
    # 鼠标移动插件控制按钮上，并点击 关闭插件控制按钮
    pyautogui.moveTo(1820, 50, duration=1)
    time.sleep(1)
    pyautogui.click()

def page_drag(dis=0):
    """
    页面滑动
    :param dis:
    :return:
    """
    windowSize = driver.get_window_size()
    print(windowSize)
    # 移动到页面滑条位置
    pyautogui.moveTo(1910, windowSize['height'] - bodyhight + 30, duration=1)
    # 往下滑动页面dis距离
    pyautogui.dragTo(1910, windowSize['height'] - bodyhight + 30 + dis, duration=1)

"""
mysqlIp = '192.168.10.64'
mysqlUser = 'root'
mysqlPwd = 'tang123456'
mysqlDb = 'spcard'
"""

def get_verification_code(time_pay,phonum):
    """
    链接数据库，在数据库中查找短信验证信息
    :param time_pay:
    :param phonum:
    :return:
    """
    # 数据库链接
    db = pymysql.connect(mysqlIp, mysqlUser, mysqlPwd, mysqlDb, charset='utf8')
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


if __name__ == "__main__":
    driver = get_driver()
    login(driver)
    buy_something(driver)
    # pay()
    # buy_something_gui(driver)
    # chang_UA(dis=72)
