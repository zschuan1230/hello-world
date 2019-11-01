#coding=utf-8
import MySQLdb

""""
    销量统计（吨）
"""

db = MySQLdb.connect("47.103.96.253", "root", "yssMysqlQa1$", "smp", charset='utf8' )

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
# 查询时间
date = ['2019-09-16 00：00：00','2019-09-17 00：00：00','2019-09-18 00：00：00','2019-09-19 00：00：00',
        '2019-09-20 00：00：00','2019-09-21 00：00：00','2019-09-22 00：00：00','2019-09-23 00：00：00',
        '2019-09-24 00：00：00','2019-09-25 00：00：00','2019-09-26 00：00：00','2019-09-27 00：00：00']

for i in range(len(date)-1):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    newsql = sql.format(date[i], date[i + 1])
    # 使用execute方法执行SQL语句
    cursor.execute(newsql)
    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()

    # 打印数据
    print(" {}: {} ".format(date[i][0:10], data))

# 关闭数据库连接
db.close()