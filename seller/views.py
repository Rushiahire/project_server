from rest_framework.views import APIView
from rest_framework.response import Response
from .product import Product


class NewProduct(APIView):

    def post(self,request):
        new_product = Product()
        new_product.add_new_product(request_data=request)
        return Response("done dana done")
    
class SellerPanel(APIView):
        
    def get(self,request):
        products = Product()
        product_list = products.get_product_list()
        return Response(product_list)
    
    
class DeleteProduct(APIView):
    def post(self,request):
        product = Product()
        product.delete_product(request_data=request)
        return Response("Product Deleted Successfully")
    

class UpdateProduct(APIView):
    def post(self,request):     
        current_product = Product()
        current_product.update_product(request_data=request)
        return Response("updated")
