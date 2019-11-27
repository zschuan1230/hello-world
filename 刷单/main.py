#coding=utf-8
from 刷单.goods import Goods
import time

if __name__ == "__main__":
    goods = Goods()
    goods.login()
    goods.buy_goods("11545562090","/html/body/div[4]/div[14]/div/div/div[2]/div[1]/div[2]/a[1]","/html/body/div[4]/div[14]/div/div/div[2]/div[2]/div[2]/a[1]")
    goods.pay()
    goods.buy_goods("11545562090","/html/body/div[4]/div[14]/div/div/div[2]/div[1]/div[2]/a[1]","/html/body/div[4]/div[14]/div/div/div[2]/div[2]/div[2]/a[1]")
    goods.pay()
    # goods.buy_goods("11545562090","/html/body/div[4]/div[14]/div/div/div[2]/div[1]/div[2]/a[1]","/html/body/div[4]/div[14]/div/div/div[2]/div[2]/div[2]/a[1]")
    # goods.pay()
    # time.sleep(5)
    # goods.page_back()
    # goods.Polarshadowverificationcode()