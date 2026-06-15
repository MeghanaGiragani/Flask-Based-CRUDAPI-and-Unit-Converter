import sqlite3
from flask import Flask, request, jsonify, g
app = Flask(__name__)
database = "items.db"
def getdb():
    if "db" not in g:
        g.db = sqlite3.connect(database)
    return g.db
@app.teardown_appcontext
def close(error):
    db = g.pop("db", None)
    if db:
        db.close()
def initdb():
    db = getdb()
    db.execute("create table if not exists items (id integer primary key autoincrement, name text)")
    db.commit()
@app.beforerequest
def before():
    initdb()
# create
@app.route('/items', methods=['POST'])
def create():
    data = request.json   
    db = getdb()
    cur = db.execute("insert into items(name) values(?)", (data["name"],))
    db.commit()
    return jsonify({"id": cur.lastrowid, "name": data["name"]})
@app.route('/items', methods=['GET'])
def readall():
    db = getdb()
    rows = db.execute("select * from items").fetchall()
    result = []
    for r in rows:
        result.append({"id": r[0], "name": r[1]})   
    return jsonify(result)
@app.route('/items/<int:itemid>', methods=['GET'])
def readone(itemid):
    db = getdb()
    r = db.execute("select * from items where id=?", (itemid,)).fetchone()
    if r:
        return jsonify({"id": r[0], "name": r[1]})
    return jsonify({"error": "not found"})
# update
@app.route('/items/<int:itemid>', methods=['PUT'])
def update(itemid):
    data = request.json
    db = getdb()
    r = db.execute("select * from items where id=?", (itemid,)).fetchone()
    if not r:
        return jsonify({"error": "not found"})
    db.execute("update items set name=? where id=?", (data["name"], itemid))
    db.commit()
    return jsonify({"id": itemid, "name": data["name"]})
# delete
@app.route('/items/<int:itemid>', methods=['DELETE'])
def delete(itemid):
    db = getdb()
    r = db.execute("select * from items where id=?", (itemid,)).fetchone()
    if not r:
        return jsonify({"error": "not found"})
    db.execute("delete from items where id=?", (itemid,))
    db.commit()
    return jsonify({"message": "deleted"})
if __name__ == '__main__':
    app.run(debug=True)
