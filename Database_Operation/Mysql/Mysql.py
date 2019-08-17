#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/8/17 17:07
# @FileName: Mysql.py
import mysql.connector

if __name__ == '__main__':
    # 连接数据库,此处连接本机的库，所以没有指定库的IP
    try:
        conn = mysql.connector.connect(user='root', password='123456', host='localhost', port='3306',
                                       database='test_database', use_unicode=True)
    except:
        print('连接失败')
    # 获取游标
    else:
        c = conn.cursor()

        # 将autocommit设置True，关闭事务,这样程序就无须调用连接对象的 commit() 方法来提交事务了,若没有就必须使用conn.commit()
        # SQLite库是没有此功能模块,这种方法不利于事物操作，一半不用
        # conn.autocommit = True

        # 执行DDL语句创建数据表
        c.execute('''create table user_tb(
            user_id int primary key auto_increment,
            name varchar(255),
            pass varchar(255),
            gender varchar(255))''')
        c.execute('''create table order_tb(
        order_id integer primary key auto_increment,
        item_name varchar(255),
        item_price double,
        item_number double,
        user_id int,
        foreign key(user_id) references user_tb(user_id) )''')
        conn.commit()
        print('创建成功')

        # 数据表中插入数据
        c.execute('insert into user_tb values(null, %s, %s, %s)',
                  ('孙悟空', '123456', 'male'))
        c.execute('insert into order_tb values(null, %s, %s, %s, %s)',
                  ('鼠标', '34.2', '3', 1))
        conn.commit()
        print('插入成功')

        # 重复执行一条SQL语句（即：多次插入不同的数据）
        c.executemany('insert into user_tb values(null, %s, %s, %s)',
                      (('sun', '123456', 'male'),
                       ('bai', '123456', 'female'),
                       ('zhu', '123456', 'male'),
                       ('niu', '123456', 'male'),
                       ('tang', '123456', 'male')))
        conn.commit()
        print('多条插入成功')

        # 更新数据
        c.executemany('update user_tb set name=%s where user_id=%s',
                      (('小孙', 2),
                       ('小白', 3),
                       ('小猪', 4),
                       ('小牛', 5),
                       ('小唐', 6)))
        # 通过rowcount获取被修改的记录条数
        print('修改的记录条数：', c.rowcount)
        conn.commit()
        print('修改成功')

        # 查询语句
        c.execute('select * from user_tb where user_id > %s', (2,))
        # 通过游标的description属性获取列信
        for col in (c.description):
            print(col[0], end='\t')
        print()
        # 直接使用for循环来遍历游标中的结果集
        for row in c:
            print(row)
        # 使用while遍历结果，此方法栈内存较大，MySQL 数据库模块的游标对象同样支持 fetchone()、fetchmany()、fetchall() 方法
        # while True:
        #     row = c.fetchone()
        #     if not row:
        #         break
        #     print(row)

        ''' 存储过程：
        delimiter $$
        create procedure add_pro(a int, b int, out sum int) /
        begin 
            set sum = a + b; 
        end $$
        '''
        # callproc(self, procname, args=())方法:调用数据库存储过程
        # procname 参数代表存储过程的名字，而 args 参数则用于为存储过程传入参数
        reslut = c.callproc('add_pro', (5, 6, 0))
        # 返回的result_args既包含了传入参数的值，也包含了传出参数的值
        print(reslut)
        # 如果只想访问传出参数的值，可直接访问result_args的第3个元素，如下代码
        print(reslut[2])

        # 删除数据表,要先删除具有外键的数据表后才可以删除关联表
        c.execute('drop table order_tb')
        c.execute('drop table user_tb')
    finally:
        c.close()
        conn.close()
