from firebase_admin import firestore,auth
from seller.product import Product
import datetime
from email_service.send_email import send_dispatch_email,send_delivered_email

db = firestore.client()
user_data = db.collection('user_data')
payment_data = db.collection('payment_data')



def update_cart_to_pending(payment_id,shipping_address,uid):
    global db
    global user_data
    global payment_data
    
    user_info = user_data.document(uid)
    user_doc = user_info.get().to_dict()
    
    total = float(user_doc["total"]) + 50
    current_cart = user_doc["cart"]
    current_shipping_address = user_doc["addresses"][shipping_address]
        
    current_transaction = {
        "total":total,
        "products":list(),
        "shipping_address":current_shipping_address,
        "payment_id":payment_id,
        "payment_date":datetime.datetime.now().strftime("%d-%m-%Y")
    }
    
    
    if(len(user_doc["cart"])>0):
        for product in user_doc['cart']:
                product_info = db.collection(product["category"]).document(product["product_id"]).get().to_dict()
                current_transaction["products"].append(product_info["title"])
                
               
        current_transaction["uid"] = uid 
        user_doc["pending"].append(current_transaction)
        current_index = user_doc["pending"].index(current_transaction)
        user_doc["pending"][current_index]["index"] = current_index
        
        user_info.update({
            "total":0,
            "cart":list(),
            "pending":user_doc["pending"]
        })
        
        pending_data = payment_data.document("pending")
        pending_doc = pending_data.get().to_dict()
        
        
            
        pending_doc["users"].append(current_transaction)
        pending_data.update({
            "users":pending_doc["users"]
        })
        
        
def update_pending_to_dispatch(data,uid):
    
    global user_data
    global payment_data
    
    user_info = user_data.document(uid)
    user_info_doc = user_info.get().to_dict()
    pending_info = payment_data.document("pending")
    pending_info_doc = pending_info.get().to_dict()
    
    pending_info_doc["users"].remove(data["user_info"])
    user_info_doc["pending"].remove(data["user_info"])
    
    current_transaction = dict()
    
    current_transaction["user_info"] = data["user_info"]
    current_transaction["delivery_date"] = data["order_date_by_seller"]
    
    user_info_doc["dispatched"].append(current_transaction)
    
    payment_info = payment_data.document("dispatched")
    payment_info_dict = payment_info.get().to_dict()
    
    payment_info_dict["users"].append(current_transaction)
    
    user_info.update({
        "pending":user_info_doc["pending"],
        "dispatched":user_info_doc["dispatched"]
    })
    
    pending_info.update({
        "users":pending_info_doc["users"]
    })
    
    payment_info.update({
        "users":payment_info_dict["users"]
    })
    
    user_email = auth.get_user(uid).email
    send_dispatch_email(
        info=current_transaction,
        email=user_email
    )
    
    
def update_dispatch_to_delivered(uid,data):
    
    global user_data
    global payment_data
    
    current_transaction = data["user_data"]
        
    user_uid = uid
    user_info = user_data.document(user_uid)
    user_info_doc = user_info.get().to_dict()
    
    dispatched_info = payment_data.document("dispatched")
    dispatched_info_doc = dispatched_info.get().to_dict()
    
    dispatched_info_doc["users"].remove(current_transaction)
    user_info_doc["dispatched"].remove(current_transaction)
    
    delivered_info = payment_data.document("delivered")
    delivered_info_doc = delivered_info.get().to_dict()
    
    delivered_info_doc["users"].append(current_transaction)
    user_info_doc["delivered"].append(current_transaction)
    
    user_info.update({
        "dispatched":user_info_doc["dispatched"],
        "delivered":user_info_doc["delivered"]
    })
    
    dispatched_info.update({
        "users":dispatched_info_doc["users"]
    })
    
    delivered_info.update({
        "users": delivered_info_doc["users"]
    })
    
    user_email = auth.get_user(user_uid).email
    
    send_delivered_email(
        info = current_transaction,
        email = user_email
    )