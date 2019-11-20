#coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

"""
    账号 ：13057523552 密码：qiujikai4971113
    易付宝支付
    支付密码203479
"""


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://m.suning.com/?utm_source=direct&utm_midium=direct&utm_content=&utm_campaign=&minip_origin=SNPG')
time.sleep(2)

driver.find_element_by_xpath('//*[@id="searchFixed"]/div[2]/div[1]/a[3]').click()
time.sleep(3)

driver.find_element_by_xpath('/html/body/div[1]/div[6]/a[2]').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys('17626022721')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="password"]').send_keys('zsc17626022721')
time.sleep(1)
ele = driver.find_element_by_xpath('//*[@id="siller2_dt_child_content_containor"]/div[3]')
print(ele)
lc = ele.location
print(lc)
# ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
# ActionChains(driver).move_to_element_with_offset(ele,1,1).
# driver.find_element_by_xpath('/html/body/div[2]/div[6]/a[1]').click()
