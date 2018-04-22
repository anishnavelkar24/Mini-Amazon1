from pymongo import MongoClient
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
    #
    # def delete_by_id(self, _id):
    #     self.db.products.delete_one({'_id': ObjectId(_id)})
    #
    # def update_by_id(self, _id, updated_product):
    #     condition = dict()
    #     condition['_id'] = ObjectId(_id)
    #     self.db.products.update_one(filter=condition, update={'$set': updated_product})
