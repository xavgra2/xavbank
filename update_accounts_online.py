#!/usr/bin/python3

import json
import sqlite3
import subprocess

try:
    pipe = subprocess.Popen("boobank ls -n 1000 -f json_line", shell=True, stdout=subprocess.PIPE)
    try:
        db = sqlite3.connect('xavbank.db')
        cursor = db.cursor()
        new_account = 0
        
        while pipe.poll() is None:
            line = pipe.stdout.readline().decode('utf-8')
            if line != '':
                data = json.loads(line)
                cursor.execute('select count(*) from account where accountid=?',(data['id'],))
                
                res=cursor.fetchone()
                if res[0]==0:
                    cursor.execute('insert into account (accountid,label,currency,solde,type,iban,private) values (?,?,?,?,?,?,?)', (data['id'],data['label'],data['currency'],data['balance'],data['type'],data['iban'],1))
                    new_account=new_account+1

        db.commit()
        cursor.close()
        db.close()
        print (new_account)
        
    except Exception as e2:
        print ('erreur a l_insertion'.format(e2.strerror))
        exit(1)

except Exception as e:
    print ('erreur a l_execution'.format(e2.strerror))
    exit(1)


