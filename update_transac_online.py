#!/usr/bin/python3

import json
import sqlite3
import subprocess

try:
    db = sqlite3.connect('xavbank.db')
    cursor = db.cursor()
    new_transac=0
    
    cursor.execute('select id,accountid from account where private=?',("0",))
    accounts = cursor.fetchall()
    for account in accounts:
        try:
            pipe = subprocess.Popen("boobank history "+account[1]+" -n 1000 -f json_line", shell=True, stdout=subprocess.PIPE)
            while pipe.poll() is None:
                line = pipe.stdout.readline().decode('utf-8')
                if line != '':
                    data = json.loads(line)
                    cursor.execute('select count(*) from transac where date=? and raw=?',(data['date'],data['raw'],))
                    
                    res=cursor.fetchone()
                    if res[0]==0:
                        cursor.execute('insert into transac (transacid,date,label,amount,raw,account_id,category_id,valid) values (?,?,?,?,?,?,0,0)', (data['id'],data['date'],data['label'],data['amount'],data['raw'],account[0]))
                        new_transac=new_transac+1
                        print('New Transac : '+data['label']+' amount= '+data['amount'])

        except Exception as e:
            print('Erreur de lecture'.format(e.strerror))
#            exit(3)

    db.commit()
    cursor.close()
    db.close()
    print (str(new_transac)+" nouvelles transactions")
                        
except Exception as e2:
    print ('erreur DB'.format(e2.strerror))
    exit(1)
