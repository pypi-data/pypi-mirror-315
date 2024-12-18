# -*- coding: utf-8 -*-
# @Date     : 2024-11-30 10:37:27
# @Author   : WANGKANG
# @Blog     : https://wangkang1717.github.io
# @Email    : 1686617586@qq.com
# @Filepath : WkMysql.py
# @Brief    : WkMysql封装类
# Copyright 2024 WANGKANG, All Rights Reserved.

""" 
项目地址：https://gitee.com/purify_wang/wk-mysql
"""

""" 
使用示例
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "123456"
DATABASE = "myproject"
TABLE = "test_table"

db = WkMysql(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
db.set_table(TABLE).create_table(
    {
        "id": "INT PRIMARY KEY AUTO_INCREMENT",
        "key": "varchar(255)",
        "sno": "varchar(255)",
        "role": "varchar(255)",
    },
    delete_if_exists=False,
)
"""

import atexit
from contextlib import contextmanager
import pymysql
from pymysql.cursors import Cursor
import sys
import time
from threading import Lock, Thread
import traceback
from WkLog import WkLog


class WkMysql:
    def __init__(
        self,
        host,
        user,
        password,
        database,
        port=3306,
        time_interval=60,  # 设置每隔多长时间进行一次连接测试，单位秒，目的是保持连接不断开
        **kwargs,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.time_interval = time_interval
        self.kwargs = kwargs

        self.table: str = None
        self.time_interval = time_interval
        self.last_connect_time = None  # 上次连接时间
        self.close_flag: bool = False

        self._log = WkLog()
        self.lock = Lock()

        self.conn: pymysql.Connection = self.connect_db()
        atexit.register(self.close)

        self.new_thread(self.keep_connect, self.time_interval)

    def connect_db(self) -> pymysql.Connection:
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                autocommit=True,
                **self.kwargs,
            )
            self._log.debug("Successfully connected to database!")
            self.last_connect_time = time.time()
            return conn
        except Exception as e:
            msg = f"Failed to connect to database! -> {str(e)}"
            self._log.error(msg)
            raise Exception(msg)

    def close(self):
        self._log.debug("Close database connection!")
        with self.lock:
            try:
                if self.close_flag:
                    return
                self.conn.close()
                self.close_flag = True
            except Exception as e:
                self._log.error(f"Failed to close database connection! -> {str(e)}")

    def before_execute(func):
        def wrapper(self, *args, **kwargs):
            if self.table is None:
                raise Exception("table is not set!")
            with self.lock:
                self.__test_conn()
                result = func(self, *args, **kwargs)
            return result

        return wrapper

    def new_thread(self, func, *args):
        # print(args)
        t = Thread(target=func, args=args)
        t.daemon = True
        t.start()

    def keep_connect(self, time_interval):
        self._log.debug(f"Keep connect to database every {time_interval} seconds!")
        while True:
            time.sleep(time_interval)
            with self.lock:
                self._log.debug("Keep connect to database!")
                self.__test_conn()

    def __test_conn(self):
        """
        长连接时，如果长时间不进行数据库交互，连接就会关闭，再次请求就会报错
        每次使用游标的时候，都调用下这个方法
        """
        try:
            if self.close_flag:
                return
            current_time = time.time()
            if current_time - self.last_connect_time >= self.time_interval:
                print("__test_conn")
                with self.get_cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.last_connect_time = current_time
        except:
            print(traceback.format_exc())
            self.conn = self.connect_db()

    def __get_query_params(self, obj: dict | list):
        if isinstance(obj, dict):
            return " AND ".join([f"`{column_name}` {'=' if obj[column_name] is not None else 'is'} %s" for column_name in obj.keys()])
        elif isinstance(obj, list):
            return " AND ".join([f"`{column_name}` {'=' if column_name is not None else 'is'} %s" for column_name in obj])

    def __get_set_params(self, obj: dict):
        return ", ".join([f"`{column_name}` {'=' if obj[column_name] is not None else 'is'} %s" for column_name in obj.keys()])

    def __get_col_params(self, obj: dict | list):
        if isinstance(obj, dict):
            return ", ".join([f"`{column_name}`" for column_name in obj.keys()])
        elif isinstance(obj, list):
            return ", ".join([f"`{column_name}`" for column_name in obj])

    def __get_values(self, obj: dict | list):
        if isinstance(obj, dict):
            return list(obj.values())
        elif isinstance(obj, list):
            res = []
            for o in obj:
                res.append(self.__get_values(o))
            return res

    def __get_placeholders(self, length):
        return ", ".join(["%s"] * length)

    def __validate_args(self, args, kwargs):
        """
        验证参数是否正确
        """
        if not args and not kwargs:
            raise Exception("args or kwargs must be used!")
        if args and kwargs:
            raise Exception("args and kwargs cannot be used together!")
        if args:
            if len(args) > 1 or not isinstance(args[0], dict):
                raise Exception("args's length must be 1 and the type must be dict!")

    def __package_data(self, data: list | tuple | None, cursor: Cursor):
        """用来封装数据: 把数据封装为json数据"""
        json_data = []
        try:
            if data is None:
                return None

            column_names = [desc[0] for desc in cursor.description]  # 获取列名
            if type(data) == list:
                for d in data:
                    json_data.append(dict(zip(column_names, d)))
                return json_data
            elif type(data) == tuple:
                return dict(zip(column_names, data))
            else:
                raise TypeError("data类型错误，应为列表或元组")
        except Exception as e:
            self._log.error(f"封装数据失败 -> {str(e)}")
            return None

    def __print_info(self, func_name, sql=None, values=None, success=True, error_msg=None, cursor: Cursor = None):
        if success:
            self._log.debug(f"Success: {func_name} -> {sql} -> {values} -> Rows affected: {cursor.rowcount}")
        else:
            self._log.error(f"Failure: {func_name} -> {sql} -> {values} -> {error_msg}")

    def set_table(self, table):
        self.table = table
        return self

    @contextmanager
    def get_cursor(self):
        try:
            cursor = self.conn.cursor()
            yield cursor
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def create_table(self, obj: dict, delete_if_exists=False):
        """
        创建表
        :param obj: 字典对象，键为列名，值为列类型
        :param delete_if_exists: 是否删除原有表
        :return: True/False
        """
        if delete_if_exists:
            self.delete_table()
        return self.__create_table(obj)

    @before_execute
    def __create_table(self, obj: dict):
        self.__get_set_params(obj)
        col_params = ", ".join([f"`{column_name}` {column_type}" for column_name, column_type in obj.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {self.table} ({col_params})"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql)
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, cursor=cursor)
                return True
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, success=False, error_msg=str(e))
            return False

    @before_execute
    def delete_table(self):
        """
        删除表
        :return: True/False
        """
        sql = f"DROP TABLE IF EXISTS {self.table}"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql)
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, cursor=cursor)
                return True
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, success=False, error_msg=str(e))
            return False

    @before_execute
    def get_column_names(self):
        sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s"
        try:
            values = (self.database, self.table)
            with self.conn.cursor() as cursor:
                cursor.execute(sql, values)
                res = []
                for row in cursor.fetchall():
                    res.append(row[0])
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
            return res
        except pymysql.Error as e:
            self.__print_info(sys._getframe().f_code.co_name, success=False, error_msg=str(e))
            return []

    @before_execute
    def exists(self, *args, **kwargs):
        """
        根据字典对象判断元素是否存在
        - demo:
            - exists({"id": 1, "name": "wangkang"})
            - exists({id=1, name=wangkang})
        """
        self.__validate_args(args, kwargs)
        obj = args[0] if args else kwargs

        values = self.__get_values(obj)
        params = self.__get_query_params(obj)
        sql = f"SELECT 1 FROM {self.table} WHERE {params} LIMIT 1"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                flag = cursor.fetchone() != None
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return flag
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return False

    @before_execute
    def insert_row(self, *args, **kwargs):
        """
        插入一行数据
        :return: True/False, insert_id
        - demo:
            - insert_row({"id": 1, "name": "wangkang"})
            - insert_row(id=1, name=wangkang)
        """
        self.__validate_args(args, kwargs)
        obj = args[0] if args else kwargs

        values = self.__get_values(obj)
        col_params = self.__get_col_params(obj)
        placeholders = self.__get_placeholders(len(obj))
        sql = f"INSERT INTO {self.table}({col_params}) VALUES({placeholders})"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount, cursor.lastrowid  # 获取插入数据的自增ID,如果没有自增ID，则返回0
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return -1

    def insert_rows(self, obj_list: list[dict]):
        """
        插入多行数据，不会因为个别数据的添加失败导致后面的所有数据都插入失败
        :param obj_list: 列表，元素为字典对象，键为列名，值为列值
        :return: 字典对象，键为success和fail，值为成功和失败次数
        """
        if not obj_list:
            return None
        success = 0
        fail = 0
        for obj in obj_list:
            flag, _ = self.insert_row(obj)
            if flag > 0:
                success += 1
            else:
                fail += 1
        return {"success": success, "fail": fail}

    @before_execute
    def insert_many(self, obj_list: list[dict]):
        """
        使用executemany来批量插入数据 此操作具有原子性
        obj_list: 列表，元素为字典对象，键为列名，值为列值
        :return: True/False
        """
        if not obj_list:
            self._log.warn("要插入的数据为空!")
            return
        values = self.__get_values(obj_list)
        col_params = self.__get_col_params(obj_list[0])
        placeholders = self.__get_placeholders(len(obj_list[0].keys()))
        sql = f"INSERT INTO {self.table}({col_params}) VALUES({placeholders})"
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return False

    @before_execute
    def delete_row(self, *args, **kwargs):
        """
        根据条件删除一行数据
        - demo:
            - delete_row({"id": 1, "name": "wangkang"})
            - delete_row(id=1, name=wangkang)
        """
        self.__validate_args(args, kwargs)
        obj = args[0] if args else kwargs

        values = self.__get_values(obj)
        params = self.__get_query_params(obj)
        sql = f"DELETE FROM {self.table} WHERE {params}"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return -1

    def delete_rows(self, obj_list: list):
        """
        :param obj_list: 列表，元素为字典对象，键为列名，值为列值
        :return: 字典对象，键为success和fail，值为成功和失败次数
        """
        if not obj_list:
            return None
        success = 0
        fail = 0
        for obj in obj_list:
            if self.delete_row(obj) > 0:
                success += 1
            else:
                fail += 1
        return {"success": success, "fail": fail}

    @before_execute
    def delete_many(self, obj_list: list[dict]):
        """
        使用executemany来批量插入数据 此操作具有原子性
        :param obj_list: 列表，元素为字典对象，键为列名，值为列值
        :return: True/False
        """
        if not obj_list:
            self._log.warn("要删除的数据为空!")
            return
        values = self.__get_values(obj_list)
        params = self.__get_query_params(obj_list[0])
        # print(params)
        sql = f"DELETE FROM {self.table} WHERE {params}"
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return -1

    @before_execute
    def select_all(self):
        """
        查询所有数据
        :return: 列表，元素为字典对象，键为列名，值为列值
        """
        sql = f"SELECT * FROM {self.table}"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, cursor=cursor)
                return self.__package_data(list(data), cursor)
        except Exception as e:
            print(traceback.format_exc())
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, success=False, error_msg=str(e))
            return None

    @before_execute
    def select(self, *args, **kwargs):
        """
        根据条件进行查询
        :return: 列表，元素为字典对象，键为列名，值为列值
        - demo:
            - select({"id": 1, "name": "wangkang"})
            - select(id=1, name=wangkang)
        """
        self.__validate_args(args, kwargs)
        obj = args[0] if args else kwargs

        values = self.__get_values(obj)
        param = self.__get_query_params(obj)
        # print(f"|{col_names}|{col_params}|{values}|{param}|")
        sql = f"SELECT * FROM {self.table} where {param}"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                data = cursor.fetchall()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return self.__package_data(list(data), cursor)
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return None

    @before_execute
    def select_one(self, *args, **kwargs):
        """
        根据条件进行查询，只返回第一条数据
        :return: 字典对象，键为列名，值为列值
        - demo:
            - select_one({"id": 1, "name": "wangkang"})
            - select_one(id=1, name=wangkang)
        """
        self.__validate_args(args, kwargs)
        obj = args[0] if args else kwargs

        values = self.__get_values(obj)
        param = self.__get_query_params(obj)
        sql = f"SELECT * FROM {self.table} where {param} LIMIT 1"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                data = cursor.fetchone()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return self.__package_data(data, cursor)
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return None

    @before_execute
    def update(self, target_obj: dict, new_obj: dict):
        """
        根据条件更新数据
        :param target_obj: 字典对象，键为列名，值为列值 作为更新条件
        :param new_obj: 字典对象，键为列名，值为列值 作为更新内容
        :return: True/False
        """
        values = self.__get_values(new_obj) + self.__get_values(target_obj)
        set_params = self.__get_set_params(new_obj)
        query_params = self.__get_query_params(target_obj)
        sql = f"UPDATE {self.table} set {set_params} where {query_params}"
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return -1

    @before_execute
    def execute(self, sql, values=None):
        """
        执行SQL语句
        :param sql: SQL语句
        :param values: 列表，元素为SQL语句中占位符对应的值
        :return: 影响行数

        - demo:
            - execute("INSERT INTO table_name(col1, col2) VALUES(?, ?)", [1, "test"])
            - execute("UPDATE table_name SET col1=? WHERE col2=?", [2, "test"])
        """
        try:
            with self.get_cursor() as cursor:
                # raise Exception("1")
                if values is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, values)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values, success=False, error_msg=str(e))
            return -1

    @before_execute
    def execute_many(self, sql, values_list):
        """
        批量执行SQL语句
        :param sql: SQL语句
        :param values_list: 列表，元素为列表，每个子列表为SQL语句中占位符对应的值
        :return: 影响行数

        - demo:
            - execute_many("INSERT INTO table_name(col1, col2) VALUES(?, ?)", [[1, "test"], [2, "test2"]])
            - execute_many("UPDATE table_name SET col1=? WHERE col2=?", [[2, "test"], [3, "test2"]])
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(sql, values_list)
                self.conn.commit()
                self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values_list, cursor=cursor)
                return cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            self.__print_info(sys._getframe().f_code.co_name, sql=sql, values=values_list, success=False, error_msg=str(e))
            return -1
