#!/usr/bin/python3

import sqlite3



try:
    db2 = sqlite3.connect('bigdata.db')
    cursor2 = db2.cursor()

    cursor2.execute('''create table bigdata (id integer primary key,label text, category_id integer)''')
    db2.commit()

except Exception as e1:
    print('erreur de creation bigdata')
    print ('erreur message'.format(e.strerror))



#try:
#    db = sqlite3.connect('xavbank.db')
#    cursor = db.cursor()
#    cursor.execute('select id,label,category_id from transac where valid=1')
#
#    transacs=cursor.fetchall()
#    for transac in transacs:
#        cursor2.execute('select count(*) from bigdata where label=?',(transac[1],))
#        res=cursor2.fetchone()
#        if res[0]==0:
#            cursor2.execute('insert into bigdata (label,category_id) values (?,?)', (transac[1], transac[2]))
#        db2.commit()
#    cursor2.close()
#
#except Exception as e:
#    print('error pour ajouter les transac')
#    print ('erreur message'.format(e.strerror))

db2.close()
#cursor.close()
#db.close()