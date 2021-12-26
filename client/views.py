from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import storage,firestore
import base64

class FetchProduct(APIView):
    def __init__(self):
        self.bucket = storage.bucket('shopheaven-ccc82.appspot.com')
        self.db = firestore.client()
        self.product_info = self.db.collection('product_info')
        self.doc_id = [doc.id for doc in self.product_info.stream()]
    
    def get(self,request):
        product_list = []
        
        for doc_name in self.doc_id:
            info = self.product_info.document(doc_name).get().to_dict()
            
            thumbnail_image = base64.b64encode(self.bucket.blob(info['thumbnail_image']).download_as_bytes()).decode('utf-8')
            product_list.append({
                'id': info['id'],
                'title': info['title'],
                'price': info['discount_price'],
                'thumbnail': thumbnail_image
            })
            if len(product_list)==6:
                break
        # print(product_list)
        return Response(product_list)
    
    
class ProductDetails(FetchProduct):
    def get(self,request,key):
        info = self.product_info.document(key).get().to_dict()
        print(info)
        data = {
            'title': info['title'],
            'description' : info['description'],
            'price':info['price'],
            'discount_price': info['discount_price'],
            'quantity': info['quantity'],
            'images':[]
        }
        
        for image_path in info['images']:
            product_image = base64.b64encode(self.bucket.blob(image_path).download_as_bytes()).decode('utf-8')
            data['images'].append(product_image)
        return Response(data)
    
    
    
    
