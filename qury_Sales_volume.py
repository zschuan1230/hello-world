#coding=utf-8
import MySQLdb
import time
import interfacedata

#########################################销售额查询模板#################################################################
# 省级权限sql查询语句模板 --销售额查询
moneySqlP = """select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join `smp`.data_station_info s on  b.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
"""
# 市级权限sql查询语句模板 --销售额查询
moneySqlC = """select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join `smp`.data_station_info s on  b.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
"""
# 区级权限sql查询语句模板 --销售额查询
moneySqlA ="""select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join `smp`.data_station_info s on  b.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
    and a.name='{}'
"""

##########################################销量查询模板##################################################################
# 省级权限sql查询语句模板 --销量查询
amountSqlP = """SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join data_station_info s on  b.oil_station_id = s.id 
    left join sys_city_info p on p.id = s.province_code
    left join sys_city_info c on c.id = s.city_code
    left join sys_city_info a on a.id = s.area_code
    left join data_product d on d.code = t.goods_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
    GROUP BY t.goods_code) w
"""

# 市级权限sql查询语句模板 --销量查询
amountSqlC = """SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join data_station_info s on  b.oil_station_id = s.id 
    left join sys_city_info p on p.id = s.province_code
    left join sys_city_info c on c.id = s.city_code
    left join sys_city_info a on a.id = s.area_code
    left join data_product d on d.code = t.goods_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
    GROUP BY t.goods_code) w
"""

# 区级权限sql查询语句模板 --销量查询
amountSqlA = """SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
    LEFT JOIN `smp`.order b on b.id = t.order_id
    left join data_station_info s on  b.oil_station_id = s.id 
    left join sys_city_info p on p.id = s.province_code
    left join sys_city_info c on c.id = s.city_code
    left join sys_city_info a on a.id = s.area_code
    left join data_product d on d.code = t.goods_code
    where 
    b.is_delete='0'
    AND s.is_delete='0'
    AND t.is_delete='0'
    AND b.create_time >='{}'
    and b.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
    and a.name='{}'
    GROUP BY t.goods_code) w
"""

##########################################加油笔数查询模板##################################################################
# 省级权限sql查询语句模板 --加油笔数查询
oilNumSqlP = """select count(*) as "加油笔数（笔）" from `smp`.order t 
    left join `smp`.data_station_info s on  t.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where
    t.is_delete='0' 
    AND
    s.is_delete='0'
    AND
    t.create_time >='{}'
    and t.create_time<'{}'
    and p.name='江苏省'
"""

# 市级权限sql查询语句模板 --加油笔数查询
oilNumSqlC = """select count(*) as "加油笔数（笔）" from `smp`.order t 
    left join `smp`.data_station_info s on  t.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where
    t.is_delete='0' 
    AND
    s.is_delete='0'
    AND
    t.create_time >='{}'
    and t.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
"""

# 区级权限sql查询语句模板 --加油笔数查询
oilNumSqlA = """select count(*) as "加油笔数（笔）" from `smp`.order t 
    left join `smp`.data_station_info s on  t.oil_station_id = s.id 
    left join `smp`.sys_city_info p on p.id = s.province_code
    left join `smp`.sys_city_info c on c.id = s.city_code
    left join `smp`.sys_city_info a on a.id = s.area_code
    where
    t.is_delete='0' 
    AND
    s.is_delete='0'
    AND
    t.create_time >='{}'
    and t.create_time<'{}'
    and p.name='江苏省'
    and c.name='{}'
    and a.name='{}'
"""
##################################################以上是SQL模板区#######################################################

"""
    城市销售数据数据校验脚本（按天统计数据）
    按天统计数据校验
"""

def querySalesMoney(tableData,date):
    # 数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    allSaleMoney_q = {}
    for i in range(len(date)-1):
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = moneySqlP
            newsql = sql.format(date[i], date[i + 1])
        elif len(tableData) == 1:
            # sql语句 -- 长字符串
            sql = moneySqlA
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        else:
            sql = moneySqlC
            newsql = sql.format(date[i], date[i + 1], tableData[0]["city_name"])
        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        dateTime = time.strptime(date[i][0:10],"%Y-%m-%d")
        timeKey = time.strftime("%Y%m%d",dateTime)
        # 数据处理 保留两位小数，并四舍五入
        newdate = int((float(data[0])+0.005)*100)/100
        allSaleMoney_q[timeKey] = newdate
        # 打印数据
        # print(" {}: {} ".format(date[i][0:10], data))
        print(allSaleMoney_q)
    # 关闭数据库连接
    db.close()
    return allSaleMoney_q

"""
    统计加油量 单位吨
"""
def querySaleAmount(tableData,date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    allSaleAmount_q = {}
    for i in range(len(date) - 1):
        # 权限为省
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = amountSqlP
            newsql = sql.format(date[i], date[i + 1])
        # 权限为区
        elif len(tableData) == 1:
            sql = amountSqlA
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        # 权限为市
        else:
            sql = amountSqlC
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"])

        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        dateTime = time.strptime(date[i][0:10], "%Y-%m-%d")
        timeKey = time.strftime("%Y%m%d", dateTime)
        # 数据处理 保留两位小数，并四舍五入
        newdate = int((float(data[0]) + 0.005) * 100) / 100
        allSaleAmount_q[timeKey] = newdate
        print(allSaleAmount_q)
    # 关闭数据库连接
    db.close()
    return allSaleAmount_q

"""
    统计加油笔数 单位笔
"""
def queryOilsNum(tableData,date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    allOilsNum_q = {}
    for i in range(len(date) - 1):
        # 权限为省
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = oilNumSqlP
            newsql = sql.format(date[i], date[i + 1])
        # 权限为区
        elif len(tableData) == 1:
            # sql语句 -- 长字符串
            sql = oilNumSqlA
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        else:
            # sql语句 -- 长字符串
            sql = oilNumSqlC
            newsql = sql.format(date[i], date[i + 1], tableData[0]["city_name"])

        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        dateTime = time.strptime(date[i][0:10], "%Y-%m-%d")
        timeKey = time.strftime("%Y%m%d", dateTime)
        # 加油数据接口返回的是字符串，所以该处也转换成功字符串
        newdate = str(data[0])
        allOilsNum_q[timeKey] = newdate
        print(allOilsNum_q)
    # 关闭数据库连接
    db.close()
    return allOilsNum_q

"""
    按区域查询加油笔数数据
"""
def queryOilsNumByArea(tableData, date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    OilsNum_q = {}

    for i in range(len(tableData)):
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = oilNumSqlC
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = oilNumSqlA
            newsql = sql.format(date[0], date[-1],tableData[i]['city_name'],tableData[i]['area_name'])

        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        # 加油数据接口返回的是字符串，所以该处也转换成功字符串
        newdate = str(data[0])
        if tableData[0]['area_name'] == "全部区域":
            OilsNum_q[tableData[i]['city_name']] = newdate
        else:
            OilsNum_q[tableData[i]['area_name']] = newdate
        print(OilsNum_q)
    # 关闭数据库连接
    db.close()
    return OilsNum_q

"""
    按区域查询销量（加油量）， 单位吨
"""
def querySaleAmountByArea(tableData, date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    SaleAmount_q = {}
    for i in range(len(tableData)):
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = amountSqlC
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = amountSqlA
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'], tableData[i]['area_name'])

        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        # 数据处理 保留两位小数，并四舍五入
        newdate = int((float(data[0]) + 0.005) * 100) / 100
        if tableData[0]['area_name'] == "全部区域":
            SaleAmount_q[tableData[i]['city_name']] = newdate
        else:
            SaleAmount_q[tableData[i]['area_name']] = newdate
        print(SaleAmount_q)
    # 关闭数据库连接
    db.close()
    return SaleAmount_q

"""
    按区域查询销售额， 单位 万元
"""
def querySaleMoneyByArea(tableData, date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 定义空字典，存储数据， 时间-销售额
    SaleMoney_q = {}
    for i in range(len(tableData)):
        if tableData[0]['area_name'] == "全部区域":
            # sql语句 -- 长字符串
            sql = moneySqlC
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = moneySqlA
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'], tableData[i]['area_name'])

        # 使用execute方法执行SQL语句
        cursor.execute(newsql)
        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()
        # 数据处理 保留两位小数，并四舍五入
        newdate = int((float(data[0]) + 0.005) * 100) / 100
        if tableData[0]['area_name'] == "全部区域":
            SaleMoney_q[tableData[i]['city_name']] = newdate
        else:
            SaleMoney_q[tableData[i]['area_name']] = newdate
        print(SaleMoney_q)
    # 关闭数据库连接
    db.close()
    return SaleMoney_q

"""
    所选区域，所选时间总销售额查询
"""
def queryAllSaleMoney(tableData,date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if tableData[0]['area_name'] == "全部区域":
        # sql语句 -- 长字符串
        sql = moneySqlP
        newsql = sql.format(date[0], date[-1])
    elif len(tableData) == 1:
        # sql语句 -- 长字符串
        sql = moneySqlA
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"], tableData[0]["area_name"])
    else:
        # sql语句 -- 长字符串
        sql = moneySqlC
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"])
    # 使用execute方法执行SQL语句
    cursor.execute(newsql)
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    # 数据处理 保留两位小数，并四舍五入
    newdate = int((float(data[0]) + 0.005) * 100) / 100
    saleMoney = newdate
    print("saleMoney: {}".format(saleMoney))
    # 关闭数据库连接
    db.close()
    return saleMoney

"""
    所选区域，所选时间总销量查询
"""
def queryAllSaleAmount(tableData,date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if tableData[0]['area_name'] == "全部区域":
        sql = amountSqlP
        newsql = sql.format(date[0], date[-1])
    elif len(tableData) == 1:
        sql = amountSqlA
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"], tableData[0]["area_name"])
    else:
        sql = amountSqlC
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"])
    # 使用execute方法执行SQL语句
    cursor.execute(newsql)
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    # 数据处理 保留两位小数，并四舍五入
    newdate = int((float(data[0]) + 0.005) * 100) / 100
    saleAmount = newdate
    print("saleAmount: {}".format(saleAmount))
    # 关闭数据库连接
    db.close()
    return saleAmount

"""
    所选区域，所选时间加油笔数查询
"""
def queryAllOilsNum(tableData,date):
    # 创建数据库链接
    db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if tableData[0]['area_name'] == "全部区域":
        sql = oilNumSqlP
        newsql = sql.format(date[0], date[-1])
    elif len(tableData) == 1:
        sql = oilNumSqlA
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"], tableData[0]["area_name"])
    else:
        sql = oilNumSqlC
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"])
    # 使用execute方法执行SQL语句
    cursor.execute(newsql)
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    newdate = str(data[0])
    oilsNum = newdate
    print("oilsNum: {}".format(oilsNum))
    # 关闭数据库连接
    db.close()
    return oilsNum


if __name__ == "__main__":
    # 江苏省的数据 常州数据少0.01是应为sql统计时进行了计算，结果自动四舍五入引起，去掉/1000000验证就ok了
    # all_data = {"code":"0","msg":"","data":{"totalData":13,"tableData":[{"area_name":"全部区域","city_name":"宿迁市","oil_num":7974.0,"sale_money":2227.78,"sale_amount":2281.02},{"area_name":"全部区域","city_name":"盐城市","oil_num":2520.0,"sale_money":708.9,"sale_amount":726.05},{"area_name":"全部区域","city_name":"南京市","oil_num":2052.0,"sale_money":572.41,"sale_amount":586.06},{"area_name":"全部区域","city_name":"淮安市","oil_num":1890.0,"sale_money":528.88,"sale_amount":541.32},{"area_name":"全部区域","city_name":"徐州市","oil_num":1368.0,"sale_money":382.17,"sale_amount":391.26},{"area_name":"全部区域","city_name":"南通市","oil_num":1008.0,"sale_money":279.74,"sale_amount":286.31},{"area_name":"全部区域","city_name":"扬州市","oil_num":882.0,"sale_money":246.55,"sale_amount":252.37},{"area_name":"全部区域","city_name":"连云港市","oil_num":882.0,"sale_money":247.69,"sale_amount":253.49},{"area_name":"全部区域","city_name":"常州市","oil_num":861.0,"sale_money":241.54,"sale_amount":247.26},{"area_name":"全部区域","city_name":"镇江市","oil_num":756.0,"sale_money":211.53,"sale_amount":216.54},{"area_name":"全部区域","city_name":"无锡市","oil_num":684.0,"sale_money":190.55,"sale_amount":195.18},{"area_name":"全部区域","city_name":"苏州市","oil_num":756.0,"sale_money":211.82,"sale_amount":217.03},{"area_name":"全部区域","city_name":"泰州市","oil_num":504.0,"sale_money":139.14,"sale_amount":142.51}],"saleStatistics":{"saleAmount":6336.4,"saleMoney":6188.72,"oilsNum":22137.0},"saleInfo":[{"saleAmount":952.08,"saleMoney":929.96,"oilsNum":"3330","key":"20190926"},{"saleAmount":958.69,"saleMoney":936.15,"oilsNum":"3330","key":"20190927"},{"saleAmount":949.72,"saleMoney":927.46,"oilsNum":"3330","key":"20190928"},{"saleAmount":952.09,"saleMoney":929.68,"oilsNum":"3330","key":"20190929"},{"saleAmount":956.84,"saleMoney":934.74,"oilsNum":"3330","key":"20190930"},{"saleAmount":318.84,"saleMoney":311.32,"oilsNum":"1110","key":"20191022"},{"saleAmount":317.44,"saleMoney":310.03,"oilsNum":"1110","key":"20191023"},{"saleAmount":314.79,"saleMoney":307.44,"oilsNum":"1110","key":"20191024"},{"saleAmount":615.91,"saleMoney":601.96,"oilsNum":"2157","key":"20191025"}]}}
    # 扬州市数据
    all_data = {"code":"0","msg":"","data":{"totalData":3,"tableData":[{"area_name":"广陵区","city_name":"扬州市","oil_num":384.0,"sale_money":105.56,"sale_amount":108.22},{"area_name":"邗江区","city_name":"扬州市","oil_num":192.0,"sale_money":52.12,"sale_amount":53.32},{"area_name":"宝应县","city_name":"扬州市","oil_num":96.0,"sale_money":26.39,"sale_amount":26.94}],"saleStatistics":{"saleAmount":188.48,"saleMoney":184.07,"oilsNum":672.0},"saleInfo":[{"saleAmount":12.33,"saleMoney":12.03,"oilsNum":"42","key":"20191022"},{"saleAmount":11.29,"saleMoney":10.99,"oilsNum":"42","key":"20191023"},{"saleAmount":11.56,"saleMoney":11.31,"oilsNum":"42","key":"20191024"},{"saleAmount":35.2,"saleMoney":34.46,"oilsNum":"126","key":"20191025"},{"saleAmount":35.69,"saleMoney":34.87,"oilsNum":"126","key":"20191026"},{"saleAmount":34.62,"saleMoney":33.84,"oilsNum":"126","key":"20191027"},{"saleAmount":47.8,"saleMoney":46.56,"oilsNum":"168","key":"20191028"}]}}


    saleInfo = all_data["data"]["saleInfo"]
    saleStatistics = all_data["data"]["saleStatistics"]
    tableData = all_data["data"]["tableData"]

    # 获取查询时间
    date = interfacedata.get_date(saleInfo)

    try:
        print("===销售总金额数据正确性验证开始")
        saleMoney = queryAllSaleMoney(tableData,date)
        if saleMoney == saleStatistics["saleMoney"]:
            print("销售总金额测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("saleStatistics：{}".format(saleStatistics))
    except Exception as e:
        print("###销售总金额测试过程中代码出现了问题，请检查。。。\n{}".format(e))

    try:
        print("===总销量数据正确性验证开始")
        saleAmount = queryAllSaleAmount(tableData,date)
        if saleAmount == saleStatistics["saleAmount"]:
            print("总销量测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("saleStatistics：{}".format(saleStatistics))
    except Exception as e:
        print("###总销量测试过程中代码出现了问题，请检查。。。\n".format(e))

    try:
        print("===加油总笔数数据正确性验证开始")
        oilsNum = queryAllOilsNum(tableData,date)
        if oilsNum == str(int(saleStatistics["oilsNum"])):
            print("加油总笔数测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("saleStatistics：{}".format(saleStatistics))
    except Exception as e:
        print("###加油总笔数测试过程中代码出现了问题，请检查。。。\n{}".format(e))

    # 页面数据处理 销售数据
    allSaleAmount, allSaleMoney, allOilsNum = interfacedata.webSaleInfo(saleInfo)

    try:
        print("===销售额数据正确性验证开始===")
        # 数据库查询 销售额数据
        allSaleMoney_q = querySalesMoney(tableData,date)
        if allSaleMoney_q == allSaleMoney:
            print("销售额测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("allSaleMoney_q: {}".format(allSaleMoney_q))
            print("allSaleMoney: {}".format(allSaleMoney))
    except Exception as e:
        print("###销售额测试过程中出现问题了，请检查。。。\n{}".format(e))

    try:
        print("===油品销量数据正确性验证开始===")
        # 数据库查询销量数据
        allSaleAmount_q = querySaleAmount(tableData,date)
        if allSaleAmount_q == allSaleAmount:
            print("油品销量测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("allSaleAmount_q: {}".format(allSaleAmount_q))
            print("allSaleAmount: {}".format(allSaleAmount))
    except Exception as e:
        print("###油品销量测试过程代码出问题了，请检查。。。\n{}".format(e))

    try:
        print("===加油笔数数据正确性验证开始===")
        # 加油笔数数据查询
        allOilsNum_q = queryOilsNum(tableData,date)
        if allOilsNum_q == allOilsNum:
            print("加油笔数测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("allOilsNum_q: {}".format(allOilsNum_q))
            print("allOilsNum: {}".format(allOilsNum))
    except Exception as e:
        print("###加油笔数测试过程中代码出问题了，请检查。。。\n{}".format(e))

    # 按区域查询数据测试开始，即表单数据验证
    print("*****开始验证表单数据*****")

    areaSaleAmount, areaSaleMoney, areaOilsNum = interfacedata.webTableData(tableData)

    try:
        print("===表单销量数据正确性验证开始===")
        # 各区域销量数据查询
        areaSaleAmount_q = querySaleAmountByArea(tableData,date)
        if areaSaleAmount_q == areaSaleAmount:
            print("表单销量测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("areaSaleAmount_q: {}".format(areaSaleAmount_q))
            print("areaSaleAmount: {}".format(areaSaleAmount))
    except Exception as e:
        print("###表单销量测试过程中代码出现问题，请检查。。。\n{}".format(e))

    try:
        print("===表单销售额数据正确性验证开始===")
        # 各区销售额数据查询
        areaSaleMoney_q = querySaleMoneyByArea(tableData,date)
        if areaSaleMoney_q == areaSaleMoney:
            print("表单销售额测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("areaSaleMoney_q: {}".format(areaSaleMoney_q))
            print("areaSaleMoney: {}".format(areaSaleMoney))
    except Exception as e:
        print("###表单销售额测试过程中代码出现了问题，请检查。。。\n{}".format(e))

    try:
        print("===表单加油笔数数据正确性验证开始===")
        # 各区加油笔数数据查询
        areaOilsNum_q = queryOilsNumByArea(tableData,date)
        if areaOilsNum_q == areaOilsNum:
            print("表单加油笔数测试通过")
        else:
            print("###测试不通过，请查看原因")
            print("areaOilsNum_q: {}".format(areaOilsNum_q))
            print("areaOilsNum: {}".format(areaOilsNum))
    except Exception as e:
        print("###表单加油笔数测试过程中代码出现了问题，请检查。。。\n{}".format(e))