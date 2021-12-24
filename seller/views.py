from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import storage,firestore
import random
import string
import base64

# gs://shopheaven-ccc82.appspot.com



class NewProduct(APIView):
    # def __init__(self):
    #     self.bucket = storage.bucket('shopheaven-ccc82.appspot.com')
    #     db = firestore.client()
    #     product_info = db.collection('product_info')
        
    def generate_name(self,files_list):
        length = 10
        chars = string.ascii_letters + '0123456789' + '-_'
        while True:
            file_name = ''.join(random.choices(chars, k=length))
            if file_name not in files_list:
                break
        
        return ''.join(random.choices(chars, k=length))

    def post(self,request):
        print(request.data)
    #     doc_id = [doc.id for doc in self.db.collection('product_info').stream()]
    #     document_name = self.generate_name(doc_id)
        
    #     new_document = self.product_info(document_name)
    #     new_data = dict()
    #     new_data['title'] = request.data['title']
    #     new_data['description'] = request.data['description']
    #     new_data['discount_price'] = request.data['discount_price']
    #     new_data['quantity'] = request.data['quantity']
        
    #     new_data['id']= document_name
    #     seller_name = 'Rushikesh'
    #     category = 'electronics'
    #     thumbnail_image = request.data        
    #     image_content_type = thumbnail_image.content_type  # image/jpeg ['image','jpeg']  
    #     temp,extension = image_content_type.split('/')
        
        
    #     thumbnail_path = f'{seller_name}/{category}/thumbnail.{extension}' 
    #     thumbnail = self.bucket.blob(thumbnail_path)
    #     thumbnail.upload_from_string(thumbnail_image.read(),content_type = image_content_type)
        
        return Response("done dana done")
    
            
        
