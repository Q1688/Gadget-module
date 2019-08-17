#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Author : lianggq
# @Time  : 2019/8/17 9:49
# @FileName: SQLite.py
import sqlite3


# 定义一个普通函数
def reverse_ext(st):
    # 对字符串反转，前后加方括号
    return '[' + st[::-1] + ']'


class MinLen:
    """
    聚集函数的实现类,该类必须实现 step(self, params...) 和 finalize(self) 方法，
    其中 step() 方法对于查询所返回的每条记录各执行一次；finalize(self) 方法只在最后执行一次
    """

    def __init__(self):
        self.min_len = None

    def step(self, value):
        if self.min_len is None:
            self.min_len = value
            return
        if len(self.min_len) > len(value):
            self.min_len = value

    def finalize(self):
        return self.min_len


def my_collate(st1, st2):
    if st1[1:-1] == st2[1:-1]:
        return 0
    elif st1[1: -1] > st2[1: -1]:
        return 1
    else:
        return -1


if __name__ == '__main__':
    # conn = sqlite3.connect(':first.db:') # 创建内存数据库
    try:
        # 连接数据库名
        conn = sqlite3.connect('first.db')
    except:
        print('连接失败')
    else:
        # 获取游标
        c = conn.cursor()

        # 执行DDL操作创建数据表
        c.execute('create table user_tb(_id integer primary key autoincrement, name text,\
                  pass text, gender text)')
        # 执行DDL操作创建数据表
        c.execute('create table order_tb(_id integer primary key autoincrement,\
                    item_name text, item_price real, item_number real, user_id inteter,\
                    foreign key(user_id) references user_tb(_id))')
        print('创建成功')

        # 插入一条数据
        c.execute('insert into user_tb values(null, ?,?,?)', ('孙悟空', '123456', 'male'))
        c.execute('insert into order_tb values (null, ?,?,?,?)', ('鼠标', '34.2', '3', 1))
        conn.commit()
        print('插入成功')

        # 一条SQL插入多条数据
        c.executemany('insert into user_tb values(null, ?, ?, ?)',
                      (('sun', '123456', 'male'),
                       ('bai', '123456', 'female'),
                       ('zhu', '123456', 'male'),
                       ('niu', '123456', 'male'),
                       ('tang', '123456', 'male')))
        conn.commit()
        print('多条插入成功')

        # 一条SQL语句进行更新数据
        c.execute('update user_tb set name=? where _id=?', ('小孙', 2))
        conn.commit()
        print('更新成功')

        # 更新多条数据（重复执SQL 语句）
        c.executemany('update user_tb set name=? where _id=?',
                      (('小白', 3),
                       ('小猪', 4),
                       ('小牛', 5),
                       ('小唐', 6)))
        # 通过rowcount获取被修改的记录条数
        print('修改的记录条数：', c.rowcount)
        conn.commit()

        # 进行语句查询
        c.execute('select * from user_tb where _id > ?', (2,))
        # 通过游标的description属性获取列信息,对表字段的描述
        for col in c.description:
            print(col[0], end='\t')
        print()
        while True:
            # 每次获取一行记录及对应的数据，每行数据都是一个元组
            row = c.fetchone()
            # 若抓取的row为one，退出循环
            if not row:
                break
            print(row)
            # 获取字段对应的数据
            print(row[1] + '-->' + row[2])

        while True:
            # 每次抓取3条记录,该方法返回一个由3条记录组成的列表
            rows = c.fetchmany(3)
            if not rows:
                break
            # 再次时使用遍历获取具体的列表
            for r in rows:
                print(r)

        # 避免使用 fetchall() 来获取查询返回的全部记录,记录数量太多,可能导致系统崩溃
        while True:
            # 每次抓取3条记录,该方法返回一个由3条记录组成的列表
            rows = c.fetchall()
            if not rows:
                break
            # 再次时使用遍历获取具体的列表
            for r in rows:
                print(r)

        # executescript()方法执行SQL脚本（即多条不同的sql语句）
        c.executescript('''insert into user_tb values(null,'武松', '3444', 'male');
                            insert into user_tb values(null, '林冲', '44444', 'male');
                            create table item_tb(_id integer primary key autoincrement, name, price);''')
        conn.commit()
        print('脚本执行成功')

        # 删除数据
        c.execute('''delete from user_tb where name='武松';''')
        conn.commit()
        print('删除数据成功')

        # 删除数据表
        c.execute('drop table user_tb')
        c.execute('drop table order_tb')
        print('删除成功')

        # 调用create_function注册自定义函数，
        # name 参数：指定注册的自定义函数的名字。
        # num_params：指定自定义函数所需参数的个数。
        # func：指定自定义函数对应的函数。
        conn.create_function('enc', 1, reverse_ext)
        c.execute('insert into user_tb values(null, ?, enc(?), ?)', ('贾宝玉', '123456', 'male'))
        conn.commit()
        print('函数调用成功')

        # 调用create_aggregate聚集函数注册自定义聚集函数：min_len
        # name：指定自定义聚集函数的名字。
        # num_params：指定聚集函数所需的参数。
        # aggregate_class：指定聚集函数的实现类
        conn.create_aggregate('min_len', 1, MinLen)
        c.execute('select min_len(pass) from user_tb')
        print(c.fetchone()[0])
        conn.commit()

        # create_collation(name, callable)
        # name：指定自定义比较函数的名字。
        # callable：指定自定义比较函数对应的函数。该函数包含两个参数，并对这两个参数进行大小比较，如果该方法返回正整数，系统认为第一个参数更大；如果返回负整数，系统认为第二个参数更大；如果返回
        # 0，系统认为两个参数相等。
        # 调用自定义的比较函数：my_collate
        conn.create_collation('sub_cmp', my_collate)
        c.execute('select * from user_tb order by pass collate sub_cmp')
        # 进行遍历
        for row in c:
            print(row)
        conn.commit()

    finally:
        c.close()
        conn.close()
