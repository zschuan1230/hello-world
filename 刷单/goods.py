#coding=utf-8
import time
import pyautogui
from .operation import Operation


class Goods(Operation):
    """
        商品类
    """
    def __init__(self):
        super(Goods,self).__init__()

    def buy_goods(self,goodId,parm1=None,parm2=None):
        """
        该方法是用于购买商品，最多可以选择两个属性，如果没有两个属性则parm设置为None即可
        特征：
            1.需拼团购买
            2.购买商品时，商品特性<=2
            3.没有对应特性时，设置特性为None
        :return:
        """
        # 点击拼购，进入品购页面
        self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/ul[1]/li/a[3]').click()
        time.sleep(1.5)
        window_size = self.driver.get_window_size()
        print(window_size)
        # 鼠标移动到搜索栏上并点击
        pyautogui.moveTo(x=1920/2, y=window_size['height']*1.0227-937, duration=1)
        time.sleep(0.5)
        pyautogui.click()
        # 进入收索页面，在搜索收入框中输入目标商编编码信息
        self.driver.find_element_by_xpath('//*[@id="search-input"]').send_keys(goodId)
        # 移动鼠标到搜索按钮上并点击
        search_btn_ele = self.driver.find_element_by_xpath('//*[@id="search-btn"]')
        # 获取元素位置信息
        search_btn_location = search_btn_ele.location
        # 获取搜索按钮大小信息
        search_btn_size = search_btn_ele.size
        print(search_btn_location)
        pyautogui.moveTo(x=search_btn_location['x']+search_btn_size['width']/2, y=window_size['height']*1.0227-937+search_btn_location['y'], duration=1)
        pyautogui.click()
        time.sleep(1.5)
        # 鼠标移动到商品图片上并点击 根据实际情况调试下坐标点
        pyautogui.moveTo(x=606 + 240 / 2,
                         y=1056 * 1.0227 - 937 + 222)
        pyautogui.click()
        # 页面下滑擦看是否由拼团信息
        self.page_drag(200)
        time.sleep(1)
        # 找到 直接参与可快速成团 标签在页面中的位置，方便定位立即参团的位置
        add_tearm = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]')
        add_tearm_location = add_tearm.location
        add_tearm_size = add_tearm.size
        print(add_tearm_location,add_tearm_size,sep=":")
        # 鼠标移动到第一个参团的商品上
        pyautogui.moveTo(x=add_tearm_location['x']+add_tearm_size['width']*0.991/2,
                         y=add_tearm_location['y'] - (add_tearm_location['y']+(window_size['height']*1.0227-937)-937)-200+add_tearm_size["height"])
        pyautogui.click()
        time.sleep(1.5)
        # 点击我也要参团 /html/body/div[5]/div/div/div[5]
        pyautogui.moveTo(x=window_size['width']/2, y=window_size['height']/2+200, duration=1)
        pyautogui.click()
        # self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[5]').click()
        time.sleep(1.5)
        if parm1 !=None:
            # 选择第一个属性 如购买鞋子时，选择颜色
            self.driver.find_element_by_xpath(parm1).click()
            time.sleep(0.5)
        if parm2 !=None:
            # 选择第二个属性 如购买鞋子时，选择尺寸
            self.driver.find_element_by_xpath(parm2).click()
            time.sleep(0.5)
        if parm1 != None or parm2 != None:
            # 点击确定
            self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/a[2]').click()
            time.sleep(1)
        # 页面滑动
        self.page_drag(200)
        # 点击提交按钮 可能需要自己调试下坐标位置
        pyautogui.moveTo(x=1936 - 160, y=1056 - 70)
        pyautogui.click()
        # 提交验证码破解
        for i in range(3):
            try:
                time.sleep(1.5)
                # 查找滑块元素，如果有则调用验证码破解方法，如果没有则会报错，并终止该for循环
                # self.driver.find_element_by_xpath('//*[@id="view"]/div[2]/div[2]/div[2]/div[1]/div[3]/img')
                self.driver.find_element_by_xpath('//*[@id="view"]/div[2]/div[2]/div[1]/div[2]/img').click()
                self.page_back()
            except:
                break
            self.Polarshadowverificationcode()




