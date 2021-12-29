from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import storage,firestore
import random
import string
import datetime
from links import STORAGE_BUCKET_URL


class NewProduct(APIView):
    def __init__(self):
        self.bucket = storage.bucket(STORAGE_BUCKET_URL)
        self.db = firestore.client()
        self.product_info = self.db.collection('product_info')
        
    def generate_name(self,files_list):
        length = 10
        chars = string.ascii_letters + '0123456789' + '-_'
        while True:
            file_name = ''.join(random.choices(chars, k=length))
            if file_name not in files_list:
                break
        
        return ''.join(random.choices(chars, k=length))

    def post(self,request):
                
        key_list = list(request.data.keys())

        doc_id = [doc.id for doc in self.db.collection('product_info').stream()]
        document_name = self.generate_name(doc_id)
        
        new_document = self.product_info.document(document_name)
        new_data = dict()
                
        for index in key_list[0:5]:
            new_data[index] = request.data[index]
            
        # print(new_data)
        
        new_data['id']= document_name
        
        seller_id = new_data['id']
        category = 'furniture'
        
    
        thumbnail_image = request.data['thumbnail']     
        image_content_type = thumbnail_image.content_type  # image/jpeg ['image','jpeg']  
        temp,extension = image_content_type.split('/')
        thumbnail_path = f'{seller_id}/{category}/thumbnail.{extension}' 
        thumbnail = self.bucket.blob(thumbnail_path)
        thumbnail.upload_from_string(thumbnail_image.read(),content_type = image_content_type)
        
        new_data['thumbnail_image'] = thumbnail_path
        
        new_data['images'] = list()
        
        for key_name in key_list[6:]:
            image_data = request.data[key_name]
            print(image_data)
            image_content_type = image_data.content_type
            temp,extension = image_content_type.split('/')
            
            files_list = [ 
                file.name.replace(f'{seller_id}/{category}/','') 
                for file in self.bucket.list_blobs() 
                if f'{seller_id}/{category}' in file.name
            ]
            file_name = self.generate_name(files_list)
            image_path = f'{seller_id}/{category}/{file_name}.{extension}'
            new_data['images'].append(image_path)
            new_image = self.bucket.blob(image_path)
            new_image.upload_from_string(image_data.read(),content_type = image_content_type)
        
        new_document.set(new_data)
        return Response("done dana done")
    
    
class SellerPanel(APIView):
    def __init__(self):
        self.db = firestore.client()
        self.product_info = self.db.collection('product_info')
        self.bucket = storage.bucket(STORAGE_BUCKET_URL)
        

    def get(self,request):
        doc_list = self.db.collection('product_info').stream()
        data_list = list()
        for doc_name in doc_list:
            doc = self.product_info.document(doc_name.id).get().to_dict()
            thumbnail_blob = self.bucket.blob(doc['thumbnail_image'])
            thumbnail_image = thumbnail_blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
            data = {
                'thumbnail' : thumbnail_image,
                'price' : doc['price'],
                'title' : doc['title'],
                'quantity' : doc['quantity'],
                'key': doc_name.id
            }
            data_list.append(data)
            
        return Response(data_list)
    
    
class DeleteProduct(SellerPanel):
    def post(self,request):
        doc_name = request.data['id']
        
        current_doc = self.product_info.document(doc_name)
        temp = current_doc.get().to_dict()
        thumbnail_blob = self.bucket.blob(temp['thumbnail_image'])
        thumbnail_blob.delete()
        for image_path in temp['images']:
            image_blob = self.bucket.blob(image_path)
            image_blob.delete()
        
        current_doc.delete()
    
        return Response("Product Deleted Successfully")