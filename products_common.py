from firebase_admin import firestore
import random

categories = [
    'laptop','iphone','clock','watch','camera'
]

laptops = []
iphone = []
clock = []
watch = []
camera = []

db = firestore.client()

print("executing this file")
for index,category in enumerate(categories):
    category_collection = db.collection(category)
    product_list = category_collection.stream()
    for product_doc in product_list:
        doc = product_doc.to_dict()
        data = {
            'thumbnail' : doc['thumbnail_image']['url'],
            'price' : doc['price'],
            'title' : doc['title'],
            # 'category':category,
            # 'quantity' : doc['quantity'],
            'key': product_doc.id
            }
        if index == 0: # laptop
            laptops.append(data)
        elif index == 1: # iPhone
            iphone.append(data)
        elif index == 2: # clock 
            clock.append(data)
        elif index == 3: # watch 
            watch.append(data)
        elif index == 4: # camera
            camera.append(data)
        # else:
        #     pass

