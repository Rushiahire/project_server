from firebase_admin import firestore
from seller.product import Product

db = firestore.client()

class User():
    
    user_data = db.collection('user_data')
    
    def __init__(self,uid=''):
        self.uid = uid  
        
    def add_new_user(self):
        new_document = self.user_data.document(self.uid)
        new_data = {
            "uid" : self.uid,
            "addresses" : list(),
            "cart" : list(),
            "purchase_history" : list(),
            "is_seller" : False,
            "seller_id" : None
        }
        new_document.set(new_data)
        
    def fetch_info_by_id(self):
        user_data_document = self.user_data.document(self.uid).get().to_dict()
        return user_data_document
    
    def delete_by_id(self):
        self.user_data.document(self.uid).delete()
        return "deleted"
    
    def update_address_id(self,value,add,index=-1):
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        
        if add:
            user_doc['addresses'].append(value)
        else:
            del(user_doc['addresses'][index])
        
        user_info.update({
                'addresses':user_doc['addresses']
        })
        
        
    def update_cart(self,product_info,add,index=-1,is_qty=False):
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        print(user_doc)
        if add:
            user_doc['cart'].append(product_info)
        else:
            if is_qty:
                user_doc['cart'][index]['quantity'] = product_info["quantity"]
            else:
                del(user_doc['cart'][index])
            
        user_info.update({
                'cart':user_doc['cart']
        })
        
    def get_cart_by_id(self):
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        cart_info = list()
        product = Product()
        for prod_info in user_doc['cart']:
            info = product.get_info_by_id(key=prod_info['product_id'],is_history=False)
            info['quantity'] = prod_info['quantity']
            info['key'] = prod_info['product_id']
            cart_info.append(info)
            
        return cart_info
        