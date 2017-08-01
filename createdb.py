#!/usr/bin/python3

import sqlite3

##le comment pour GIT / bash_win


try:
    db = sqlite3.connect('xavbank.db')

    cursor = db.cursor()

    cursor.execute('''create table account (id integer primary key,accountid text, label text, currency text, solde real, type text, iban text, private text)''')
    cursor.execute('''create table transac (id integer primary key,transacid text, date text, label text, amount real, raw text, account_id integer, category_id integer, valid integer )''')
    cursor.execute('''create table category (id integer primary key,cat_name text)''')
    db.commit()

    cursor.execute('''insert into category values(0,"Other")''')
    db.commit()

    cursor.close()
    db.close()

except:
    print('Une erreur a la creation')
    exit(1)

print('Db creee')

