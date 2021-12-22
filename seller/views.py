from rest_framework.views import APIView
from rest_framework.response import Response

class NewProduct(APIView):
    def post(self,request):
        print(request.data)
        # for item in request.data['product_images']:
        #     print("+++++++++++++++++++++++++++++++++++++++++++++")
        #     print(item)
        #     print("+++++++++++++++++++++++++++++++++++++++++++++")
          
        return Response("done dana done")
        
        
