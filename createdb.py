#!/usr/bin/python3

import sqlite3

##commetn git

try:
    db = sqlite3.connect('xavbank.db')

    cursor = db.cursor()

    cursor.execute('''create table account (id integer primary key,accountid text, label text, currency text, solde real, type text, iban text, private text)''')
    cursor.execute('''create table transac (id integer primary key,transacid text, date text, label text, amount real, raw text, account_id integer)''')

    db.commit()

    cursor.close()
    db.close()

except:
    print('Une erreur a la creation')
    exit(1)

print('Db creee')

