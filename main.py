from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel, ValidationError
app = Flask(__name__)
DATABASE_URL = "sqlite:///items.db"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
Base.metadata.create_all(engine)
class ItemSchema(BaseModel):
    name: str
class ItemService:
    def __init__(self):
        self.db = Session()
    def create_item(self, data):
        try:
            item = Item(name=data.name)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except:
            self.db.rollback()
            raise
    def get_all_items(self):
        return self.db.query(Item).all()
    def get_item(self, item_id):
        return self.db.query(Item).filter(Item.id == item_id).first()
    def update_item(self, item_id, data):
        item = self.get_item(item_id)
        if not item:
            return None
        try:
            item.name = data.name
            self.db.commit()
            return item
        except:
            self.db.rollback()
            raise
    def delete_item(self, item_id):
        item = self.get_item(item_id)
        if not item:
            return False
        try:
            self.db.delete(item)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            raise
class ItemAPI(MethodView):
    def get(self):
        try:
            service = ItemService()
            itemid = request.args.get('id')
            if itemid:
                item = service.get_item(int(itemid))
                if not item:
                    return jsonify({"error": "not found"})
                return jsonify({"id": item.id, "name": item.name})
            items = service.get_all_items()
            return jsonify([{"id": i.id, "name": i.name} for i in items])
        except Exception as e:
            return jsonify({"error": str(e)})
    def post(self):
        try:
            data = ItemSchema(**request.json)
            service = ItemService()
            item = service.create_item(data)
            return jsonify({"id": item.id, "name": item.name})
        except ValidationError as ve:
            return jsonify({"error": ve.errors()})
        except Exception as e:
            return jsonify({"error": str(e)})
    def put(self):
        try:
            itemid = request.args.get('id')
            if not itemid:
                return jsonify({"error": "id required"})
            data = ItemSchema(**request.json)
            service = ItemService()
            item = service.update_item(int(itemid), data)
            if not item:
                return jsonify({"error": "not found"})
            return jsonify({"id": item.id, "name": item.name})
        except ValidationError as ve:
            return jsonify({"error": ve.errors()})
        except Exception as e:
            return jsonify({"error": str(e)})
    def delete(self):
        try:
            itemid = request.args.get('id')
            if not itemid:
                return jsonify({"error": "id required"})

            service = ItemService()
            success = service.delete_item(int(itemid))

            if not success:
                return jsonify({"error": "not found"})
            return jsonify({"message": "deleted"})
        except Exception as e:
            return jsonify({"error": str(e)})
item_view = ItemAPI.as_view('item_api')
app.add_url_rule(
    '/items',
    view_func=item_view,
    methods=['GET', 'POST', 'PUT', 'DELETE']
)
if __name__ == '__main__':
    app.run(debug=True)
