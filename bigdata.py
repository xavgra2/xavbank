#!/usr/bin/python3

import sqlite3

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


db = sqlite3.connect('xavbank.db')
cursor = db.cursor()
cursor.execute('select id,label from transac where valid=0 order by id desc limit 1')

try:
    transac = cursor.fetchone()
    cursor.execute('select id,label,category_id from transac where valid=1')

    transRefs=cursor.fetchall()
    dist=0
    category_id=0
    for transRef in transRefs:
        transDist=similar(transac[1],transRef[1])
        print( "RRR " + str(transDist))
        if transDist>dist :
            dist=transDist
            category_id=transRef[2]
            print(" ----------- " + transac[1] + " ++ " + transRef[1] + " = " + str(dist))
    if dist>0.7 :
        print( "FOURTE")
        try:
            cursor.execute('update transac set category_id=?,valid=2 where id=?', (category_id,transac[0]))
        except Exception as e2:
            print ('erreur update'.format(e2.strerror))
            exit(1)
        print ('UPDATE ' + str(category_id) + " *-* " + str(transac[0]))
        db.commit()
    cursor.close()

except Exception as e:
    print('Erreur pour recuperer le compte')
    print ('erreur message'.format(e.strerror))


db.close()