#coding=utf-8
import MySQLdb
import time
import interfacedata

# 省级权限sql查询语句模板
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
            sql = """
                select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
                -- 省名称
                and p.name='江苏省'
            """
            newsql = sql.format(date[i], date[i + 1])
        elif len(tableData) == 1:
            # sql语句 -- 长字符串
            sql = """
                    select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        else:
            sql = """
                    select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
            sql = """
                SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
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
            newsql = sql.format(date[i], date[i + 1])
        # 权限为区
        elif len(tableData) == 1:
            sql = """
                    SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
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
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        # 权限为市
        else:
            sql = """
                    SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
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
            sql = """
                select count(*) as "加油笔数（笔）" from `smp`.order t 
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
                -- 省名称
                and p.name='江苏省'
            """
            newsql = sql.format(date[i], date[i + 1])
        # 权限为区
        elif len(tableData) == 1:
            # sql语句 -- 长字符串
            sql = """
                    select count(*) as "加油笔数（笔）" from `smp`.order t 
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
                    -- 省名称
                    and p.name='江苏省'
                    and c.name='{}'
                    and a.name='{}'
                """
            newsql = sql.format(date[i], date[i + 1],tableData[0]["city_name"],tableData[0]["area_name"])
        else:
            # sql语句 -- 长字符串
            sql = """
                     select count(*) as "加油笔数（笔）" from `smp`.order t 
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
                     -- 省名称
                     and p.name='江苏省'
                     and c.name='{}'
                 """
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
            sql = """
                    select count(*) as "加油笔数（笔）" from `smp`.order t 
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
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = """
                    select count(*) as "加油笔数（笔）" from `smp`.order t 
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
            sql = """
                    SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
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
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = """
                    SELECT SUM(w.`油品销售量(吨)`) as "油品总销量（吨）" from (select t.goods_code,sum(t.goods_amount) * d.density/1000000 as "油品销售量(吨)" from order_goods t 
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
            sql = """
                    select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
            newsql = sql.format(date[0], date[-1], tableData[i]['city_name'])
        else:
            sql = """
                    select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
    # 定义空字典，存储数据， 时间-销售额
    totalSaleMoney_q = {}
    if tableData[0]['area_name'] == "全部区域":
        # sql语句 -- 长字符串
        sql = """
                select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
        newsql = sql.format(date[0], date[-1])
    elif len(tableData) == 1:
        # sql语句 -- 长字符串
        sql = """
                select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"], tableData[0]["area_name"])
    else:
        # sql语句 -- 长字符串
        sql = """
                select sum(b.need_pay_amount)/1000000 as "油品销售额" from `smp`.order_goods t 
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
        newsql = sql.format(date[0], date[-1], tableData[0]["city_name"])
    # 使用execute方法执行SQL语句
    cursor.execute(newsql)
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    # 数据处理 保留两位小数，并四舍五入
    newdate = int((float(data[0]) + 0.005) * 100) / 100
    totalSaleMoney_q['saleMoney'] = newdate
    print(totalSaleMoney_q)
    # 关闭数据库连接
    db.close()
    return totalSaleMoney_q

if __name__ == "__main__":
    all_data = {"code":"0","msg":"","data":{"totalData":11,"tableData":[{"area_name":"六合区","city_name":"南京市","oil_num":7560.0,"sale_money":2109.68,"sale_amount":2160.74},{"area_name":"下关区","city_name":"南京市","oil_num":5040.0,"sale_money":1417.03,"sale_amount":1451.79},{"area_name":"秦淮区","city_name":"南京市","oil_num":5040.0,"sale_money":1407.61,"sale_amount":1441.66},{"area_name":"高淳县","city_name":"南京市","oil_num":5040.0,"sale_money":1411.92,"sale_amount":1445.68},{"area_name":"建邺区","city_name":"南京市","oil_num":5040.0,"sale_money":1493.66,"sale_amount":1442.74},{"area_name":"浦口区","city_name":"南京市","oil_num":5040.0,"sale_money":1414.54,"sale_amount":1448.97},{"area_name":"白下区","city_name":"南京市","oil_num":2520.0,"sale_money":703.31,"sale_amount":719.82},{"area_name":"雨花台","city_name":"南京市","oil_num":2520.0,"sale_money":703.53,"sale_amount":720.34},{"area_name":"溧水县","city_name":"南京市","oil_num":2520.0,"sale_money":702.39,"sale_amount":719.39},{"area_name":"鼓楼区","city_name":"南京市","oil_num":2520.0,"sale_money":701.71,"sale_amount":718.28},{"area_name":"玄武区","city_name":"南京市","oil_num":2520.0,"sale_money":703.72,"sale_amount":720.79}],"saleStatistics":{"saleAmount":12990.21,"saleMoney":12769.1,"oilsNum":45360.0},"saleInfo":[{"saleAmount":3795.44,"saleMoney":3706.64,"oilsNum":"13284","key":"201906"},{"saleAmount":4212.26,"saleMoney":4113.01,"oilsNum":"14688","key":"201907"},{"saleAmount":2885.89,"saleMoney":2902.4,"oilsNum":"10044","key":"201908"},{"saleAmount":2096.62,"saleMoney":2047.05,"oilsNum":"7344","key":"201909"}]}}


    saleInfo = all_data["data"]["saleInfo"]
    saleStatistics = all_data["data"]["saleStatistics"]
    tableData = all_data["data"]["tableData"]

    # 获取查询时间
    date = interfacedata.get_date(saleInfo)

    # 页面数据处理 销售数据
    allSaleAmount, allSaleMoney, allOilsNum = interfacedata.webSaleInfo(saleInfo)

    try:
        print("===销售额数据正确性验证开始===")
        # 数据库查询 销售额数据
        allSaleMoney_q = querySalesMoney(tableData,date)
        if allSaleMoney_q == allSaleMoney:
            print("销售额测试通过")
        else:
            print("allSaleMoney_q: {}".format(allSaleMoney_q))
            print("allSaleMoney: {}".format(allSaleMoney))
    except:
        print("###销售额测试过程中出现问题了，请检查。。。")

    try:
        print("===油品销量数据正确性验证开始===")
        # 数据库查询销量数据
        allSaleAmount_q = querySaleAmount(tableData,date)
        if allSaleAmount_q == allSaleAmount:
            print("油品销量测试通过")
        else:
            print("allSaleAmount_q: {}".format(allSaleAmount_q))
            print("allSaleAmount: {}".format(allSaleAmount))
    except:
        print("###油品销量测试过程代码出问题了，请检查。。。")

    try:
        print("===加油笔数数据正确性验证开始===")
        # 加油笔数数据查询
        allOilsNum_q = queryOilsNum(tableData,date)
        if allOilsNum_q == allOilsNum:
            print("加油笔数测试通过")
        else:
            print("allOilsNum_q: {}".format(allOilsNum_q))
            print("allOilsNum: {}".format(allOilsNum))
    except:
        print("###加油笔数测试过程中代码出问题了，请检查。。。")

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
            print("areaSaleAmount_q: {}".format(areaSaleAmount_q))
            print("areaSaleAmount: {}".format(areaSaleAmount))
    except:
        print("###表单销量测试过程中代码出现问题，请检查。。。")

    try:
        print("===表单销售额数据正确性验证开始===")
        # 各区销售额数据查询
        areaSaleMoney_q = querySaleMoneyByArea(tableData,date)
        if areaSaleMoney_q == areaSaleMoney:
            print("表单销售额测试通过")
        else:
            print("areaSaleMoney_q: {}".format(areaSaleMoney_q))
            print("areaSaleMoney: {}".format(areaSaleMoney))
    except:
        print("###表单销售额测试过程中代码出现了问题，请检查。。。")

    try:
        print("===表单加油笔数数据正确性验证开始===")
        # 各区加油笔数数据查询
        areaOilsNum_q = queryOilsNumByArea(tableData,date)
        if areaOilsNum_q == areaOilsNum:
            print("表单加油笔数测试通过")
        else:
            print("areaOilsNum_q: {}".format(areaOilsNum_q))
            print("areaOilsNum: {}".format(areaOilsNum))
    except:
        print("###表单加油笔数测试过程中代码出现了问题，请检查。。。")