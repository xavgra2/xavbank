#!/usr/bin/python3

import sqlite3

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


try:
    db2 = sqlite3.connect('bigdata.db')
    cursor2 = db2.cursor()
except Exception as e1:
    print('erreur de connection a bigdata')
    print ('erreur message'.format(e.strerror))

### Update la table bigdata avec les donnees validees
try:
    db = sqlite3.connect('xavbank.db')
    cursor = db.cursor()
    cursor.execute('select id,label,category_id from transac where valid=1')

    transacs=cursor.fetchall()
    for transac in transacs:
        cursor2.execute('select count(*) from bigdata where label=?',(transac[1],))
        res=cursor2.fetchone()
        if res[0]==0:
            cursor2.execute('insert into bigdata (label,category_id) values (?,?)', (transac[1], transac[2]))
        db2.commit()
   
except Exception as e:
    print('error pour ajouter les transac valide a bigdata')
    print ('erreur message'.format(e.strerror))


## update transac pas validees
try:
    cursor.execute('select id,label from transac where valid=0')
    transacs = cursor.fetchall()
    for transac in transacs:
        cursor2.execute('select id,label,category_id from bigdata')
        transRefs=cursor2.fetchall()
        dist=0
        category_id=0
        for transRef in transRefs:
            transDist=similar(transac[1],transRef[1])
            if transDist>dist :
                dist=transDist
                category_id=transRef[2]
        if dist>0.7 :
            try:
                cursor.execute('update transac set category_id=?,valid=2 where id=?', (category_id,transac[0]))
            except Exception as e2:
                print ('erreur update'.format(e2.strerror))
                exit(1)
            print ('UPDATE ' + str(transac[1]) + " *-* " + str(category_id))
            db.commit()
        else:
            print (' ** NO UPDATE ' + str(transac[1]) + " ** " )
    cursor2.close()
    db2.close()
    cursor.close()
    db.close()

except Exception as e:
    print('Erreur pour recuperer le compte')
    print ('erreur message'.format(e.strerror))

