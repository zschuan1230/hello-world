#coding=utf-8
import time
import pyautogui


class Goods:
    """
        商品类
    """
    def __init__(self, driver):
        self.driver = driver

    def page_drag(self,dis=0):
        """
        页面滑动
        :param dis:
        :return:
        """
        windowSize = self.driver.get_window_size()
        print(windowSize)
        # 移动到页面滑条位置
        pyautogui.moveTo(1910, windowSize['height'] - 937 + 30, duration=1)
        # 往下滑动页面dis距离
        pyautogui.dragTo(1910, windowSize['height'] - 937 + 30 + dis, duration=1)

    def buy_Guer(self):
        """
        购买Guer围巾
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
        self.driver.find_element_by_xpath('//*[@id="search-input"]').send_keys("11347263649")
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
        # 鼠标移动到商品图片上并点击
        # //*[@id="lpgjgwapss_11353907740_pro_baoguang-1-0_1_1_0070750814_11353907740_0"]/div[1]
        img_ele = self.driver.find_element_by_xpath('//*[@id="lpgjgwapss_11347263649_pro_baoguang-1-0_1_1_0070178365_11347263649_0"]/div[1]')
        img_ele_localtion = img_ele.location
        img_ele_size = img_ele.size
        print(img_ele_localtion,img_ele_size,sep="   ")
        pyautogui.moveTo(x=img_ele_localtion['x']+img_ele_size['width']/2, y=window_size['height']*1.0227-937+img_ele_localtion['y'])
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
                         y=add_tearm_location['y'] - (add_tearm_location['y']+(window_size['height']*1.0227-937)-937)-200+add_tearm_size["height"]*2)
        # pyautogui.click()
        # time.sleep(1.5)
        # # 点击我也要参团 /html/body/div[5]/div/div/div[5]
        # pyautogui.moveTo(x=window_size['width']/2, y=window_size['height']/2+200, duration=1)
        # pyautogui.click()
        # # self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[5]').click()
        # time.sleep(1.5)
        # # 选择颜色
        # self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/div[2]/div[1]/div[2]/a[1]').click()
        # time.sleep(0.5)
        # # 选择尺码
        # self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/div[2]/div[2]/div[2]/a[6]').click()
        # time.sleep(0.5)
        # # 点击确定
        # self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/a[2]').click()
        # time.sleep(1)
        # # 页面滑动
        # self.page_drag(200)
        # # 点击提交按钮
        # pyautogui.moveTo(x=1936 - 160, y=1056 - 70)
        # pyautogui.click()

    def buy_shoes(self,goodId,parm1,parm2):
        """
        该方法是用于购买类似与鞋类的商品
        特征：
            1.需拼团购买
            2.购买时需要选择两个属性，例如：颜色 & 尺码
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
        # 鼠标移动到商品图片上并点击
        # //*[@id="lpgjgwapss_11353907740_pro_baoguang-1-0_1_1_0070750814_11353907740_0"]/div[1]
        # img_ele = self.driver.find_element_by_xpath('//*[@id="lpgjgwapss_11347263649_pro_baoguang-1-0_1_1_0070178365_11347263649_0"]/div[1]')
        # img_ele_localtion = img_ele.location
        # img_ele_size = img_ele.size
        # print(img_ele_localtion,img_ele_size,sep="   ")
        # pyautogui.moveTo(x=img_ele_localtion['x']+img_ele_size['width']/2, y=window_size['height']*1.0227-937+img_ele_localtion['y'])
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
                         y=add_tearm_location['y'] - (add_tearm_location['y']+(window_size['height']*1.0227-937)-937)-200+add_tearm_size["height"]*2)
        pyautogui.click()
        time.sleep(1.5)
        # 点击我也要参团 /html/body/div[5]/div/div/div[5]
        pyautogui.moveTo(x=window_size['width']/2, y=window_size['height']/2+200, duration=1)
        pyautogui.click()
        # self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[5]').click()
        time.sleep(1.5)
        # 选择颜色
        self.driver.find_element_by_xpath(parm1).click()
        time.sleep(0.5)
        # 选择尺码
        self.driver.find_element_by_xpath(parm2).click()
        time.sleep(0.5)
        # 点击确定
        self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/a[2]').click()
        time.sleep(1)
        # 页面滑动
        self.page_drag(200)
        # 点击提交按钮
        pyautogui.moveTo(x=1936 - 160, y=1056 - 70)
        pyautogui.click()


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
        # 鼠标移动到商品图片上并点击
        # //*[@id="lpgjgwapss_11353907740_pro_baoguang-1-0_1_1_0070750814_11353907740_0"]/div[1]
        # img_ele = self.driver.find_element_by_xpath('//*[@id="lpgjgwapss_11347263649_pro_baoguang-1-0_1_1_0070178365_11347263649_0"]/div[1]')
        # img_ele_localtion = img_ele.location
        # img_ele_size = img_ele.size
        # print(img_ele_localtion,img_ele_size,sep="   ")
        # pyautogui.moveTo(x=img_ele_localtion['x']+img_ele_size['width']/2, y=window_size['height']*1.0227-937+img_ele_localtion['y'])
        pyautogui.moveTo(x=606 + 240 / 2,
                         y=1056 * 1.0227 - 937 + 240)
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
        # pyautogui.click()
        # time.sleep(1.5)
        # # 点击我也要参团 /html/body/div[5]/div/div/div[5]
        # pyautogui.moveTo(x=window_size['width']/2, y=window_size['height']/2+200, duration=1)
        # pyautogui.click()
        # # self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[5]').click()
        # time.sleep(1.5)
        # if parm1 !=None:
        #     # 选择第一个属性 如购买鞋子时，选择颜色
        #     self.driver.find_element_by_xpath(parm1).click()
        #     time.sleep(0.5)
        # if parm2 !=None:
        #     # 选择第二个属性 如购买鞋子时，选择尺寸
        #     self.driver.find_element_by_xpath(parm2).click()
        #     time.sleep(0.5)
        # if parm1 != None or parm2 != None:
        #     # 点击确定
        #     self.driver.find_element_by_xpath('/html/body/div[4]/div[14]/div/div/a[2]').click()
        #     time.sleep(1)
        # # 页面滑动
        # self.page_drag(200)
        # # 点击提交按钮
        # pyautogui.moveTo(x=1936 - 160, y=1056 - 70)
        # pyautogui.click()

