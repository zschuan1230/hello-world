#coding=utf-8
import time

"""
    处理接口中的数据
"""

"""
    通过saleInfo信息获取日期信息（目前获取的都是具体那天信息）
"""
def get_date(saleInfo):
    date = []
    if len(saleInfo[0]['key']) == 6:
        month = []
        for monthday in range(len(saleInfo)):
            month.append(saleInfo[monthday]['key'])
        for i in month:
            monthday = time.strptime(i, "%Y%m")
            date.append(time.strftime("%Y-%m-%d %H:%M:%S", monthday))
        # 获取当期时间，判断是否包含当月
        localtimes = time.localtime()
        localtimes_year = localtimes.tm_year
        localtimes_mon = localtimes.tm_mon
        localtimes_mday = localtimes.tm_mday

        # 把str格式转为date类型，并转换成时间戳,方便计算最后的时间值
        time1 = time.mktime(time.strptime(date[-1], "%Y-%m-%d %H:%M:%S"))
        if time.strptime(month[-1], "%Y%m").tm_mon == localtimes_mon:
            # 在原有的时间上加上当前月已过时间值，已方便查询最后一天的数据
            time2 = time.localtime(time1 + 24 * 60 * 60 * (localtimes_mday - 1))
            # 按格式，把时间戳转为字符串
            date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
        else:
            if time.strptime(month[-1], "%Y%m").tm_mon in [1, 3, 5, 7, 8, 10, 12]:
                time2 = time.localtime(time1 + 24 * 60 * 60 * 31)
                # 按格式，把时间戳转为字符串
                date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
            elif time.strptime(month[-1], "%Y%m").tm_mon in [4, 6, 9, 11]:
                time2 = time.localtime(time1 + 24 * 60 * 60 * 30)
                # 按格式，把时间戳转为字符串
                date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
            else:
                if (localtimes_year % 4 == 0 and localtimes_year % 100 != 0) or localtimes_year % 400 == 0:
                    # 闰年
                    time2 = time.localtime(time1 + 24 * 60 * 60 * 29)
                    # 按格式，把时间戳转为字符串
                    date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
                else:
                    # 闰年
                    time2 = time.localtime(time1 + 24 * 60 * 60 * 28)
                    # 按格式，把时间戳转为字符串
                    date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
    else:
        # 获取数据中的日期时间
        for i in range(len(saleInfo)):
            nowtime = saleInfo[i]['key']
            newtime = time.strptime(nowtime, "%Y%m%d")
            times = time.strftime("%Y-%m-%d %H:%M:%S", newtime)
            date.append(times)
        # 在原有的时间上加上一天，已方便查询最后一天的数据
        # 把str格式转为date类型，并转换成时间戳
        time1 = time.mktime(time.strptime(date[-1], "%Y-%m-%d %H:%M:%S"))
        # 在已有的时间戳上加上24小时
        time2 = time.localtime(time1 + 24 * 60 * 60)
        # 按格式，把时间戳转为字符串
        date.append(time.strftime("%Y-%m-%d %H:%M:%S", time2))
    print(date)
    return date


"""
    处理销售数据，按类型分开，即销售额数据归销售额数据，销量数据归销量数据，加油笔数数据归加油笔数数据
"""
def webSaleInfo(saleInfo):
    # 销量数据 单位吨
    allSaleAmount = {}
    # 销售额数据 单位万元
    allSaleMoney = {}
    # 加油笔数数据 单位笔
    allOilsNum = {}
    for date in saleInfo:
        for key in date:
            if len(date['key']) == 6:
                newkey = date['key'] + "01"
            else:
                newkey = date['key']
            if key == "saleAmount":
                allSaleAmount[newkey] = date["saleAmount"]
            if key == "saleMoney":
                allSaleMoney[newkey] = date["saleMoney"]
            if key == "oilsNum":
                allOilsNum[newkey] = date["oilsNum"]

    return allSaleAmount,allSaleMoney,allOilsNum

def webTableData(tableData):
    # 各区域销量数据 单位吨
    areaSaleAmount = {}
    # 各区域销售额数据 单位万元
    areaSaleMoney = {}
    # 各区域加油笔数数据 单位笔
    areaOilsNum = {}
    for date in tableData:
        if tableData[0]['area_name'] == "全部区域":
            areaSaleAmount[date['city_name']] = date['sale_amount']
            areaSaleMoney[date['city_name']] = date['sale_money']
            areaOilsNum[date['city_name']] = str(int(date['oil_num']))
        else:
            areaSaleAmount[date['area_name']] = date['sale_amount']
            areaSaleMoney[date['area_name']] = date['sale_money']
            areaOilsNum[date['area_name']] = str(int(date['oil_num']))
    return areaSaleAmount,areaSaleMoney,areaOilsNum





# if __name__ == "__main__":
#     allSaleAmount,allSaleMoney,allOilsNum = webSaleInfo(saleInfo)
#     print("allSaleAmount:{}".format(allSaleAmount))
#     print("allSaleMoney:{}".format(allSaleMoney))
#     print("allOilsNum:{}".format(allOilsNum))
#     get_date(saleInfo)
