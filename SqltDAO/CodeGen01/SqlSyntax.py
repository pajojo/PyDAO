# Author: Soft9000.com
# 2018/03/08: Class Created

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from SqltDAO.CodeGen01.OrderClass import OrderClass
from SqltDAO.CodeGen01.CodeLevel import CodeLevel
from SqltDAO.CodeGen01.DaoExceptions import GenOrderError


class SqliteCrud:
    ''' Translates OrderClass + Fields into python source code. No files are created. '''

    def __init__(self, order, fields):
        ''' Set-up class with an OrderClass and SQL Table-fields.
        Will raise an exception when proper types are not provided.
        '''
        assert(isinstance(order, OrderClass))
        assert(fields)
        self.order = order
        self.fields = fields
        self.level = CodeLevel()

    def code_class_template(self, text_file, sep=','):
        ''' Translate a local order into Python code. Returns created source-code. '''
        import time
        from SqltDAO.CodeGen01.Meta import Meta
        self.level.set(0)
        result = self.level.print("#!/usr/bin/env python3\n")
        result += self.level.print("'''")
        result += self.level.print("Generated by {}".format(Meta.Title()))
        result += self.level.print("Generated @ {}".format(time.asctime()))
        result += self.level.print("'''")
        result += self.level.print("import sqlite3\n\n\nclass " + self.order.class_name + ":")
        result += self.level.print("")

        self.level.inc()
        result += self.level.print("def __init__(self):")

        self.level.inc()
        result += self.level.print("self.db = '" + self.order.db_name +"'")
        result += self.level.print("self.conn = None")
        result += self.level.print("self.curs = None")
        result += self.level.print("self.bOpen = False")
        result += self.level.print("self.fields = " + str(self.fields))
        result += self.level.print("self.table_name = '" + self.order.table_name + "'")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def open(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen is False:")
        self.level.inc();
        result += self.level.print("self.conn = sqlite3.connect(self.db)")
        result += self.level.print("self.curs = self.conn.cursor()")
        result += self.level.print("self.bOpen = True")
        self.level.dec()
        result += self.level.print("return True")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def close(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print("self.conn.commit()")
        result += self.level.print("self.bOpen = False")
        self.level.dec()
        result += self.level.print("return True")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def count(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('res = self.curs.execute("SELECT count(*) FROM ' + self.order.table_name + ';")')
        result += self.level.print("return res.fetchone()[0]")
        self.level.dec()
        result += self.level.print("return -1")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def drop_table(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("DrOp TaBLe IF EXISTS ' + self.order.table_name + ';")')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def create_table(self):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("' + self.sql_create_table() + '")')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def insert(self, fields):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("' + self.sql_insert_row() + '", fields)')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def delete(self, primary_key):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute("DELETE from ' + self.order.table_name + ' WHERE ID = ?;", [primary_key])')
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()

        result += self.level.print("def select(self, sql_select):")
        self.level.inc()
        result += self.level.print("if self.bOpen:")
        self.level.inc();
        result += self.level.print('self.curs.execute(sql_select)')
        result += self.level.print("zlist = self.curs.fetchall()")
        result += self.level.print("for ref in zlist:")
        self.level.inc();
        result += self.level.print("yield ref")
        self.level.dec()
        self.level.dec()
        result += self.level.print("return None")
        result += self.level.print("")
        self.level.dec()

        self.level.push()
        result += self.level.print("@staticmethod")
        if self.order.encoding:
            encoding = "'" + self.order.encoding + "'"
        else:
            encoding = str(self.order.encoding)
        result += self.level.print("def Import(dao, encoding=" + encoding + ", text_file='" + text_file + "', hasHeader=True, sep='" + sep + "'):")
        self.level.inc()
        result += self.level.print("try:")
        self.level.inc()
        result += self.level.print('# dao.open()')
        result += self.level.print("with open(text_file, encoding=encoding) as fh:")
        self.level.inc()
        result += self.level.print("line = fh.readline().strip()")
        result += self.level.print("if hasHeader is True:")
        self.level.inc()
        result += self.level.print("line = fh.readline().strip()")
        self.level.dec()
        result += self.level.print("while len(line) is not 0:")
        self.level.inc()
        result += self.level.print("if dao.insert(line.split(sep)) is False:")
        self.level.inc()
        result += self.level.print("return False")
        self.level.dec()
        result += self.level.print("line = fh.readline().strip()")
        self.level.dec()
        self.level.dec()
        result += self.level.print("# dao.close()")
        result += self.level.print("return True")
        self.level.dec()
        result += self.level.print("except:")
        self.level.inc()
        result += self.level.print("pass")
        self.level.dec()
        result += self.level.print("return False")
        result += self.level.print("")
        self.level.dec()
        self.level.pop()

        result += self.level.print("")
        return result


    def sql_create_table(self):
        ''' Translate the order into a field-driven SQL Table creation statement. '''
        result = "CREATE TABLE IF NOT EXISTS " + self.order.table_name
        result = result + '(ID INTEGER PRIMARY KEY AUTOINCREMENT,'
        for ss, val in enumerate(self.fields):
            result += ' '
            result += val[0] + " "
            result += val[1] + ","
        result = result[0:len(result) - 1]
        result = result + ');'
        return result


    def sql_insert_row(self):
        ''' Translate the order into a field-driven SQL Row creation statement. '''
        result = "INSERT INTO " + self.order.table_name + " ("
        for val in self.fields:
            result += ' '
            result += val[0] + ","
        result = result[0:len(result) - 1]
        result = result + ') VALUES ('
        for val in self.fields:
            result += '?,'
        result = result[0:len(result) - 1]
        result = result + ');'
        return result
