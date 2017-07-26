#!/usr/bin/python3

from flask import Flask,json
import sqlite3

app = Flask(__name__,static_url_path = '')

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/bank/dump', methods=['GET'])
def get_dump_transac():
    db = sqlite3.connect('xavbank.db')
    cu = db.cursor()
    cu.execute('select * from transac')
    rows = [x for x in cu]
    cols = [x[0] for x in cu.description]
    res = []
    for row in rows:
        line = {}
        for prop, val in zip(cols, row):
            line[prop] = val
        res.append(line)
    resJSON = json.dumps(res)
    cu.close()
    db.close()
    return resJSON

@app.route('/api/bank/accounts', methods=['GET'])
def get_accounts():
    db = sqlite3.connect('xavbank.db')
    cu = db.cursor()
    cu.execute('select id,accountid,label from account where private=?',("0",))
    rows = [x for x in cu]
    cols = [x[0] for x in cu.description]
    res = []
    for row in rows:
        line = {}
        for prop, val in zip(cols, row):
            line[prop] = val
        res.append(line)
    resJSON = json.dumps(res)
    cu.close()
    db.close()
    return resJSON
    
@app.route('/api/bank/accounts/<int:account_id>/transacs', methods=['GET'])
def get_accounts_transacs(account_id):
    db = sqlite3.connect('xavbank.db')
    cu = db.cursor()
    cu.execute('select id,transacid,date,label,amount from transac where account_id==?',(account_id,))
    rows = [x for x in cu]
    cols = [x[0] for x in cu.description]
    res = []
    for row in rows:
        line = {}
        for prop, val in zip(cols, row):
            line[prop] = val
        res.append(line)
    resJSON = json.dumps(res)
    cu.close()
    db.close()
    return resJSON




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
