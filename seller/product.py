from firebase_admin import storage,firestore
from links import STORAGE_BUCKET_URL
import random
import string
import datetime


class Product:
    bucket = storage.bucket(STORAGE_BUCKET_URL)
    db = firestore.client()
    # product_info = db.collection('product_info')
    
    def generate_name(self,files_list):
        length = 10
        chars = string.ascii_letters + '0123456789' + '-_'
        while True:
            file_name = ''.join(random.choices(chars, k=length))
            if file_name not in files_list:
                break
        
        return ''.join(random.choices(chars, k=length))
    
    
    def add_new_product(self,request_data):
        key_list = list(request_data.data.keys())
        # print(key_list)
        category = request_data.data["category"]
        product_info = self.db.collection(category)
        
        doc_id = [doc.id for doc in product_info.stream()]
        document_name = self.generate_name(doc_id)
        
        new_document = product_info.document(document_name)
        new_data = dict()
        
        new_data['reviews']=[]
                
        for index in key_list[0:5]:
            new_data[index] = eval(request_data.data[index]) if request_data.data[index].isnumeric() else request_data.data[index]
            
        
        new_data['id']= document_name
        
    
        thumbnail_image = request_data.data['thumbnail']     
        image_content_type = thumbnail_image.content_type  # image/jpeg ['image','jpeg']  
        temp,extension = image_content_type.split('/')
        thumbnail_path = f'{document_name}/thumbnail.{extension}' 
        thumbnail = self.bucket.blob(thumbnail_path)
        thumbnail.upload_from_string(thumbnail_image.read(),content_type = image_content_type)
        
        new_data['thumbnail_image'] = thumbnail_path
        
        new_data['images'] = list()
        
        for key_name in key_list[7:]:
            image_data = request_data.data[key_name]
            # print(image_data)
            image_content_type = image_data.content_type
            temp,extension = image_content_type.split('/')
            
            files_list = [ 
                file.name.replace(f'{document_name}/','') 
                for file in self.bucket.list_blobs() 
                if f'{document_name}' in file.name
            ]
            file_name = self.generate_name(files_list)
            image_path = f'{document_name}/{file_name}.{extension}'
            new_data['images'].append(image_path)
            new_image = self.bucket.blob(image_path)
            new_image.upload_from_string(image_data.read(),content_type = image_content_type)
        
        new_document.set(new_data)
        return True
    
    def get_product_list(self,category):
        product_info = self.db.collection(category)
        doc_list = product_info.stream()
        data_list = list()
        for doc_name in doc_list:
            doc = product_info.document(doc_name.id).get().to_dict()
            thumbnail_blob = self.bucket.blob(doc['thumbnail_image'])
            thumbnail_image = thumbnail_blob.generate_signed_url(datetime.timedelta(seconds=500), method='GET')
            data = {
                'thumbnail' : thumbnail_image,
                'price' : doc['price'],
                'title' : doc['title'],
                'quantity' : doc['quantity'],
                'key': doc_name.id
            }
            data_list.append(data)
            
        return data_list
    
    
    def update_product(self,request_data):
        # print(request_data.data['thumbnail'])
        product_info = self.db.collection(request_data.data["category"])
        doc_id = request_data.data['id']
        
        doc = product_info.document(doc_id)
        doc_data=doc.get().to_dict()

        doc.update({
            'title':request_data.data['title'] if request_data.data['title'] !='' else doc_data['title'],
            'description':request_data.data['description'] if request_data.data['description'] !='' else doc_data['description'],
            'price':request_data.data['price'] if request_data.data['price'] !='' else doc_data['price'],
            'discount_price':request_data.data['discount_price'] if request_data.data['discount_price'] !='' else doc_data['discount_price'],
            'quantity':request_data.data['quantity'] if request_data.data['quantity'] !='' else doc_data['quantity']
        })
        
        
    def delete_product(self,request_data):
        product_info = self.db.collection(request_data.data["category"])
        doc_name = request_data.data['id']
        
        current_doc = product_info.document(doc_name)
        temp = current_doc.get().to_dict()
        thumbnail_blob = self.bucket.blob(temp['thumbnail_image'])
        thumbnail_blob.delete()
        for image_path in temp['images']:
            image_blob = self.bucket.blob(image_path)
            image_blob.delete()
        
        current_doc.delete()
        
        
    def get_info_by_id(self,key,is_history,category):
        product_info = self.db.collection(category)
        info = product_info.document(key).get().to_dict()

        data = {
            'category':category,
            'title': info['title'],
            'description' : info['description'],
            'price':info['price'],
            'discount_price': info['discount_price'],
            'quantity': info['quantity']
        }
        
        if is_history:
            data['images']=[]
            for image_path in info['images']:
                blob = self.bucket.blob(image_path)
                product_image = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
                data['images'].append(product_image)
        else:
            blob = self.bucket.blob(info['thumbnail_image'])
            thumbnail_image = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
            data['thumbnail'] = thumbnail_image
            
        return data