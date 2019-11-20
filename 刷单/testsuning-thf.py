# coding=utf-8
import time

import pyautogui as pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
import random


def randomSplit(M, N, minV, maxV):
    '''
    数字随机切割函数
    :param M:
    :param N:
    :param minV:
    :param maxV:
    :return:
    '''
    res = []
    while N > 0:
        l = max(minV, M - (N - 1) * maxV)
        r = min(maxV, M - (N - 1) * minV)
        num = random.randint(l, r)
        N -= 1
        M -= num
        res.append(num)
    return res


"""
    账号 ：13057523552 密码：qiujikai4971113
    易付宝支付
    支付密码203479    
"""

# options = Options()
# options.add_argument("--user-data-dir=" + r"C:\Users\dell\AppData\Local\Google\Chrome\User Data")
#
# # options.add_experimental_option("debuggerAddress", "localhost:10000")
# driver = webdriver.Chrome(options=options, desired_capabilities=dcap)
# print(driver.title)
# driver.maximize_window()

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(chrome_options=chrome_options)
print(driver.title)


# driver.maximize_window()
try:
    driver.get('https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[1]/a[3]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/a[2]').click()
    driver.find_element_by_xpath('//*[@id="username"]').send_keys('13057523552')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('qiujikai4971113')
    time.sleep(1)
    ele = driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]/div[3]')
    print(ele)
    lc = ele.location
    print(lc)
    # 点击并按住滑块
    # ActionChains(driver).click_and_hold(ele).perform()
    # 获取屏幕宽度 及X值
    # scren_x = GetSystemMetrics(0)
    # scren_y = GetSystemMetrics(1)
    # print(scren_x)
    # print(scren_y)
    window_size = driver.get_window_size()
    print(window_size)
    el = driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]')
    s = el.size
    print(s['width'])
    print(ele.size)
    # track = get_track(s["width"])
    track = randomSplit(
        10 + 20 + 30 + 50 + 80 + 100 + 100 + 100 + 200 + 200 + 100 + 100 + 100 + 50 + 50 + 30 + 30 + 200 + 200, 5, 100,
        1000)
    print(track)
    t_x = lc['x']
    pyautogui.dragTo(x=t_x + ele.size['width'] / 2,
                     y=lc['y'] + window_size['height'] - 900,
                     duration=1, tween=pyautogui.easeInOutQuad)
    pyautogui.mouseDown(x=t_x + ele.size['width'] / 2,
                        y=lc['y'] + window_size['height'] - 900)
    for x in track:
        pyautogui.moveRel(xOffset=x,
                          yOffset=0,
                          duration=1, tween=pyautogui.easeInOutQuad)
        time.sleep(1)
    pyautogui.mouseUp()
    # 手动拖拽验证码
    time.sleep(3)
    # 点击登录
    driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
    time.sleep(1)
except Exception as e:
    try:
        driver.find_element_by_xpath('/html/body/div[2]/div[7]/a[1]').click()
    except:
        pass
    print(e)
    pass
# 点击搜索 并输入收搜 内容
# 点击首页中的搜索
try:
    driver.find_element_by_xpath('/html/body/div[3]/a[1]/img').click()
except:
    pass
driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[2]/div/a').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="searchAssInp"]').send_keys('【洽洽】山核桃味葵花籽坚果零食炒货批500g')
time.sleep(1)
# 点击搜索

driver.find_element_by_xpath('//*[@id="wapSearchURL"]').click()
driver.execute_script("window.scrollTo(0,-{})".format(random.randint(5, 10)))
time.sleep(1)
driver.find_element_by_xpath('//*[@id="productsList"]/li[1]').click()

time.sleep(1)
try:
    # 处理页面提示 如果有则点击继续浏览
    driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/span').click()
except:
    pass
# 点击单独购买
# driver.find_element_by_xpath('//*[@id="toCommonPage"]').click()
# time.sleep(1.5)
# driver.execute_script("window.scrollTo(0,-{})".format(random.randint(10,90)))
# 点击立即抢购
driver.find_element_by_xpath('//*[@id="toCommonPage"]').click()
time.sleep(1.5)
driver.find_element_by_xpath('//*[@id="buyNow"]').click()

# 滑动页面到底部
time.sleep(1)
driver.execute_script("window.scrollTo(0,-100)")
time.sleep(0.5)
driver.execute_script("window.scrollTo(0,-130)")
time.sleep(1)

pyautogui.moveTo(x=1910,
                 y=200,
                 duration=1, tween=pyautogui.easeInOutQuad)

pyautogui.click(1910, 200, button='left')
pyautogui.dragRel(xOffset=0,
                  yOffset=250,
                  duration=2, tween=pyautogui.easeInOutQuad)
time.sleep(1)

# 选择苏宁支付 的方式支付

pyautogui.moveTo(x=1000, y=1000, duration=1, tween=pyautogui.easeInOutQuad)
time.sleep(1)

# driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[4]/div/div[1]/div/p')
pyautogui.click()
time.sleep(2)
try:
    # 输入之前的验证码
    driver.find_element_by_xpath(
        '//*[contains(@id, "am-modal-container")]/div/div[2]/div/div/div[1]/div/div/input').send_keys('3334')
    driver.find_element_by_xpath('//*[contains(@id, "am-modal-container")]/div/div[2]/div/div/div[2]/div/a[2]').click()
    # time.sleep(1)
except Exception as e:
    print(e)
    # time.sleep(10)
time.sleep(2)

driver.get('https://www.suning.com/?utm_source=baidu&utm_medium=brand&utm_campaign=title')
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[3]/a/span').click()
time.sleep(1)
driver.find_element_by_xpath('//*[contains(@id, "operation")]/div[2]/a').click()
time.sleep(2)
password = [2, 0, 3, 4, 7, 9]

element = driver.find_element_by_xpath('//*[@id="simplePassword"]/li[1]')

pyautogui.moveTo(x=500,
                 y=700,
                 duration=1, tween=pyautogui.easeInOutQuad)

pyautogui.click()
pyautogui.typewrite(['2', '0', '3', '4', '7', '9'])
time.sleep(1)
# driver.find_element_by_xpath('//*[@id="confirmPay"]').click()

'''
从手机端获取到订单号以后 ，进入苏宁网页版支付页面 进行模拟鼠标操作支付
https://payment.suning.com/epps-pppm/miniGateway/show.htm?payOrderId=1911148783382544777&cashierType=01&sourceUrl4Sa=https://order.suning.com/order/orderList.do

'''
