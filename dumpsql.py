#!/usr/bin/python

import sqlite3

def getTableDump(db_file, table_to_dump):
    conn = sqlite3.connect(':memory:')    
    cu = conn.cursor()
    cu.execute("attach database '" + db_file + "' as attached_db")
    cu.execute("select sql from attached_db.sqlite_master "
               "where type='table' and name='" + table_to_dump + "'")
    sql_create_table = cu.fetchone()[0]
    cu.execute(sql_create_table);
    cu.execute("insert into " + table_to_dump +
               " select * from attached_db." + table_to_dump)
    conn.commit()
    cu.execute("detach database attached_db")
    return "\n".join(conn.iterdump())

print "ACCOUNT"

TABLE_TO_DUMP = 'account'
DB_FILE = 'xavbank.db'

print getTableDump(DB_FILE, TABLE_TO_DUMP)

print "TRANSAC"

TABLE_TO_DUMP = 'transac'
DB_FILE = 'xavbank.db'

print getTableDump(DB_FILE, TABLE_TO_DUMP)
