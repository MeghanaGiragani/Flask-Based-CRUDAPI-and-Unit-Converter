from flask import Flask, request, jsonify
app = Flask(__name__)
items = []
#create
@app.route('/items', methods=['POST'])
def create():
    data = request.json
    item = {
        "id": len(items) + 1,
        "name": data["name"]
    }
    items.append(item)
    return jsonify(item)
@app.route('/items', methods=['GET'])
def readall():
    return jsonify(items)
@app.route('/items/<int:itemid>', methods=['GET'])
def readone(itemid):
    for i in items:
        if i["id"] == itemid:
            return jsonify(i)
    return jsonify({"error": "not found"})
# update
@app.route('/items/<int:itemid>', methods=['PUT'])
def update(itemid):
    data = request.json
    for i in items:
        if i["id"] == itemid:
            i["name"] = data["name"]
            return jsonify(i)
    return jsonify({"error": "not found"})
# delete
@app.route('/items/<int:itemid>', methods=['DELETE'])
def delete(itemid):
    for i in items:
        if i["id"] == itemid:
            items.remove(i)
            return jsonify({"message": "deleted"})
    return jsonify({"error": "not found"})
if __name__ == '__main__':
    app.run(debug=True)
