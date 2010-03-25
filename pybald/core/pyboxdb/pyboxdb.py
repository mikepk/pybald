#!/usr/bin/env python
# encoding: utf-8
"""
pyboxdb.py

An object to simplify SQL access to a mysql database. Eliminates some of the sources of error
normally in dealing with MySQLdb directly. Also protects against some unsafe mysql (deletes w/out
where clauses etc...)

Created by mikepk on 2009-07-07.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest
import time

import sqlalchemy.pool as pool
# from MySQLdb import OperationalError
import MySQLdb as mysqldb
# wrap MySQLdb with sqlalchemy's connection pooling
mysqldb = pool.manage(mysqldb)

# exception for unsafe SQL statements
class UnsafeSQL(Exception): pass

class Pyboxdb:
    '''Simple PyBox database wrapper class.'''
    IntegrityError = mysqldb.IntegrityError
    def __init__(self):
        pass

    def set_connection_string(self,config):
        self.connect_config = config

    def connect(self):
        self.db = mysqldb.connect(**self.connect_config)

    def close(self):
        self.db.close()


    def sqlInsert(self,table,params):
        '''DB insert using simple DBAPI interface.'''
        placeholders,fields,values = self.gen_params_list(params)
        fields = ', '.join(fields)
        sql_statement = '''INSERT INTO %s (%s) VALUES (%s)''' % (table, fields, placeholders)
        return self.sqlExecute(sql_statement, tuple(values))

    def sqlRaw(self,sql_statement,values=None):
        '''Pass an escaped statement directly.'''
        return self.sqlExecute(sql_statement, tuple(values), cursor_type=mysqldb.cursors.DictCursor)

    def sqlSelect(self,cols,table,where=None,opt=None):
        '''DB select function.'''
        if isinstance(table,list):
            table = ' JOIN '.join(table)

        if where:
            where_list,values = self.gen_where_list(where)
            where_list = ' WHERE '+where_list
        else:
            values = []
            where_list = ''

        if opt:
            sql_statement = '''SELECT %s FROM %s%s%s''' % (cols,table, where_list, opt)
        else:
            sql_statement = '''SELECT %s FROM %s%s''' % (cols,table, where_list)

        # for selects, return dicitonaries?
        return self.sqlExecute(sql_statement, tuple(values), cursor_type=mysqldb.cursors.DictCursor)
        
    def sqlDelete(self,table,where=None):
        '''DB delete rows from a table'''
        # safety, requires where clause
        if not where:
            raise UnsafeSQL()
        
        where_list,values = self.gen_where_list(where)
        sql_statement = '''DELETE FROM %s WHERE %s''' % (table, where_list)
        return self.sqlExecute(sql_statement, tuple(values))
        
    def sqlUpdate(self,table,params,where=None):
        '''DB update rows in a table'''
        # safety, requires where clause
        if not where:
            raise UnsafeSQL()

        where_list,where_values = self.gen_where_list(where)
        placeholders,fields,param_values = self.gen_params_list(params)
        fields = ', '.join([f+'=%s' for f in fields])

        sql_statement = '''UPDATE %s SET %s WHERE %s''' % (table, fields, where_list)
        return self.sqlExecute(sql_statement, tuple(param_values)+tuple(where_values))

    def sqlGetColumns(self,table):
        '''Get the column names from a table'''
        sql_statement = '''SHOW COLUMNS FROM %s''' % (table)
        rows = self.sqlExecute(sql_statement)
        rows = [item[0] for item in rows]
        return rows

    def sqlLastInsertId(self):
        '''Retrieve the last insert ID for auto-inc tables.'''
        sql_statement = '''SELECT LAST_INSERT_ID()'''
        rows = self.sqlExecute(sql_statement)[0][0]
        return rows


    def queryTracer(func):
        '''Function decorator to add debug information to the SQL statements.'''
        def replacement(self, statement, values=None, cursor_type=None):        
            import inspect
            stack = inspect.stack()
            # get the calling frame for the method/function calling
            # the sql command (taking into account the sql+execute functions)
            frame = stack[4][0]
            frame_info = inspect.getframeinfo(frame)
            debug = 'method:'+str(frame_info[2])+' file:'+str(frame_info[0])+' line:'+str(frame_info[1])
            statement += ' -- '+debug
            return func(self, statement, values, cursor_type)
        return replacement

    # Uncomment this decorator to add debug information to trace where queries are originating. 
    # Very useful for slow queries (look in mysql slow query log to get pointers to the code
    # issuing the slow queries)
    @queryTracer
    def sqlExecute(self, statement, values=None, cursor_type=None):
        '''Execute a sql statement + values'''
        # sometimes mysql 'goes away' so this retries the statment several times
        # to try reconnecting
        # if project.debug:
        #print '''Statement: %s   Values: %s''' % (statement,values)
        retry = 20
        while retry > 0:
            try:
                #self.connect()
                if cursor_type:
                    cursor = self.db.cursor(cursor_type)
                else:
                    cursor = self.db.cursor()
                cursor.execute(statement, values)
                
            # retry the statement
            except (mysqldb.OperationalError,mysqldb.ProgrammingError),e:
                try:
                    print "Retrying %d..." % (retry)
                    cursor.close()
                    self.close()
                    time.sleep(0.1)
                    self.connect()
                    retry = retry -1
                except (mysqldb.OperationalError,mysqldb.ProgrammingError),e:
                    time.sleep(0.1)
                    print "Retry failed..."
                if retry == 0:
                    raise
            else:  
                self.db.commit()
                rows = cursor.fetchall()
                cursor.close()
                retry = 0
                #self.close()
                return list(rows)

       
    def gen_where_list(self,where):
        '''Take a where dictionary and create a where clause as well as a list of fields and placeholders'''
        fields = where.keys()        
        values = where.values()
        where_list = ' AND '.join([f+"=%s" for f in fields])
        return where_list,values
        
    def gen_params_list(self,params):
        '''Create a list of fields and values as well as a string of '\%s' placeholders'''
        placeholders = ', '.join(['%s'] * len(params))
        fields = params.keys()
        values = params.values()
        return placeholders,fields,values


pdb = Pyboxdb()
        
class PyboxdbTests(unittest.TestCase):
    '''Database access unit tests.'''        
    def setUp(self):
        self.pdb = Pyboxdb()
        self.pdb.set_connection_string({'host':'localhost', 'user':'test', 'passwd':'test', 'db':'test'})
        self.pdb.connect()

    def testCRUD(self):
        '''Test Insert,Select,Update and Delete to database.'''
        self.pdb.sqlInsert('sessions',{'session_id':'DEADBEEF6','cache':'Im JUST TESTING'})
        rows = self.pdb.sqlSelect('*','sessions',{'session_id':'DEADBEEF6'})
        record = rows[0]
        self.assertEqual(record['session_id'], 'DEADBEEF6')
        self.pdb.sqlUpdate('sessions',{'cache':'ANOTHER TEST'},{'session_id':'DEADBEEF6'})
        self.pdb.sqlDelete('sessions',{'session_id':'DEADBEEF6'})
        rows = self.pdb.sqlSelect('*','sessions',{'session_id':'DEADBEEF6'})
        self.assertTrue(len(rows) == 0)

    def testInjection(self):
        '''Try to inject some simple SQL into a value parameter.'''
        self.pdb.sqlInsert('sessions',{'session_id':'DEADBEEF6','cache':'Im JUST TESTING'})
        self.pdb.sqlSelect('*','sessions',{'cache':'BOB; UPDATE sessions SET cache="INJECTED"s;'})
        rows = self.pdb.sqlSelect('*','sessions',{'cache':'INJECTED'})
        self.pdb.sqlDelete('sessions',{'session_id':'DEADBEEF6'})
        self.assertTrue(len(rows) == 0)
        

    def testUnsafe(self):
        '''Make sure that Delete and Update require a Where clause.'''
        self.assertRaises(UnsafeSQL, self.pdb.sqlDelete, 'sessions')
        self.assertRaises(UnsafeSQL, self.pdb.sqlUpdate, 'sessions', {'cache':'test'})

    def testColCheck(self):
        '''Check whether column name select works.'''
        rows = self.pdb.sqlGetColumns('sessions')
        self.assertTrue(len(rows) == 3)
        
if __name__ == '__main__':
    unittest.main()
