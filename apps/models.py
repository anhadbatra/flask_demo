from flask_login import UserMixin
from bson import ObjectId


class User(UserMixin):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        from . import mongo
        mongo.db.users.insert_one({'username': self.username, 'password': self.password})

    @staticmethod
    def load_by_id(user_id):
        from . import mongo
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        print(user_data)
        if user_data:
            return User(user_data['username'], user_data['password'])
        return None
    def get_id(self):
        return self.username
    
class Product:
    def __init__(self,name,description,owner_id):
        self.name=name
        self.description=description
        self.owner_id=owner_id

    def save(self):
        from . import mongo
        mongo.db.product.insert_one({
            'name':self.name,
            'description':self.description,
            'owner_id':self.owner_id

        })