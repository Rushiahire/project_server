from firebase_admin import firestore
from seller.product import Product
import datetime
from payment.payment_status import update_cart_to_pending

db = firestore.client()

class User():
    
    user_data = db.collection('user_data')
    payment_data = db.collection('payment_data')
    
    def __init__(self,uid=''):
        self.uid = uid  
        
    def add_new_user(self):
        print("creating new user")
        new_document = self.user_data.document(self.uid)
        new_data = {
            "uid" : self.uid,
            "addresses" : list(),
            "cart" : list(),
            "purchase_history" : list(),
            "dispatched":list(),
            "delivered":list(),
            "cancled":list(),
            "pending":list(),
            "total" : 0
        }
        new_document.set(new_data)
        
        
    def if_user_exists_in_db(self):
        return self.uid in [k.id for k in self.user_data.stream()]
        
    def fetch_info_by_id(self):
        if not self.if_user_exists_in_db():
            self.add_new_user()
        user_data_document = self.user_data.document(self.uid).get().to_dict()
        return user_data_document
    
    def delete_by_id(self):
        if self.if_user_exists_in_db():
            self.user_data.document(self.uid).delete()
        return "deleted"
    
    def update_address_id(self,value,add,index=-1):
        if not self.if_user_exists_in_db():
            self.add_new_user()
            
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
        if not self.if_user_exists_in_db():
            self.add_new_user()
            
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        if add:
            if len(user_doc['cart']) > 0 and product_info['product_id'] in [product['product_id'] for product in user_doc['cart']]:
                for index in range(len(user_doc['cart'])):
                    if user_doc['cart'][index]['product_id'] == product_info['product_id']:
                        user_doc['total']+=float(product_info['price'])*float(user_doc['cart'][index]['quantity'])
                        user_doc['cart'][index]['quantity'] = int(user_doc['cart'][index]['quantity']) + 1
                        break
            else:    
                user_doc['total']+=float(product_info['price'])*float(product_info["quantity"])
                user_doc['cart'].append(product_info)
        elif is_qty:
            qty = int(user_doc['cart'][index]['quantity'])
            new_qty = int(product_info["quantity"])
            price = float(product_info["price"])
            user_doc['total'] = user_doc['total'] -  qty * price
            user_doc['total'] = user_doc['total'] + new_qty * price
            user_doc['cart'][index]['quantity'] = new_qty
        else:
            qty = int(user_doc['cart'][index]['quantity'])
            price = float(user_doc["cart"][index]["price"])
            amount = qty * price
            user_doc['total'] = user_doc['total'] - amount
            del(user_doc['cart'][index])
            
        user_info.update({
                'cart':user_doc['cart'],
                'total':user_doc['total']
        })
        
    def get_cart_by_id(self):
        if not self.if_user_exists_in_db():
            self.add_new_user()
        
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        cart_info = list()
        product = Product()
        for prod_info in user_doc['cart']:
            info = product.get_info_by_id(
                    category=prod_info["category"],
                    key=prod_info['product_id'],
                    is_history=False
                )
            info['quantity'] = prod_info['quantity']
            info['key'] = prod_info['product_id']
            cart_info.append(info)
            
        return cart_info
    
    
    def get_total_by_id(self):
        
        if not self.if_user_exists_in_db():
            self.add_new_user()
        
        user_info = self.user_data.document(self.uid)
        user_doc = user_info.get().to_dict()
        delivery_charges = 50
        data = {
            'charges':delivery_charges,
            'subTotal':user_doc['total'],
            'total':user_doc['total']+delivery_charges
        }
        return data
    
    def move_cart_to_pending(self,payment_id,payment_id_local,shipping_address):
        
        if not self.if_user_exists_in_db():
            self.add_new_user()
        
        update_cart_to_pending(
            payment_id=payment_id,
            payment_id_local=payment_id_local,
            shipping_address=shipping_address,
            uid=self.uid
        )
        
        
            
            
        
        
        

        
        