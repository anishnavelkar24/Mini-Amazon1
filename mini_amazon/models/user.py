from pymongo import MongoClient
from bson.objectid import ObjectId
class UserModel:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.tvb_amazon

    def add_new_user(self,name,email,username,password):
        user = {

            'name': name,
            'email':email,
            'username':username,
            'password':password

        }
        self.db.users.insert_one(user)

    def authenticate(self,username,password):
        query = {
            'username':username,
            'password':password
        }
        cursor=self.db.users.find(query)
        if cursor.count() == 0:
            return False
        else:
            return True

    def get_user_by_username(self, username):
        query = {
            'username': username
        }
        cursor = self.db.users.find(query)

        if cursor.count() == 0:
            return None

        for user in cursor:
            return user

    def add_product_to_cart(self,user_id,product_id):
        print(user_id)
        #print(ObjectId(user_id))
        condition = {'_id': ObjectId(user_id)}

        cursor = self.db.users.find(condition)

        user_data = cursor[0] if cursor.count > 0 else None
        if user_data is None:
            return False
        if 'cart' not in user_data:
            user_data['cart'] = []

        if ObjectId(product_id) not in user_data['cart']:
            user_data['cart'].append(ObjectId(product_id))
            self.db.users.update_one(filter=condition, update={'$set': user_data})

            return True

    def get_by_id(self, _id):
        query = {
                    '_id': ObjectId(_id)
            }
        cursor = self.db.users.find(query)
        user = cursor[0] if cursor.count() > 0 else None
        return user
