from email import message
from django.core.mail import send_mail
from keys import EMAIL_HOST_USER


# subject = 'welcome to ShopHeaven world'
# message = f'Hello brother\n,Bhava skype var ye na\nha email django ne send kelay :)'
# email_from = EMAIL_HOST_USER
# recipient_list = ['rushiahire9567@gmail.com','amanshukla33317@gmail.com']
# send_mail( subject, message, email_from, recipient_list )


# {
#     'user_info': {
#         'payment_date': '17-03-2022', 
#         'total': 170, 
#         'payment_id': '6068eebc394447d4a7931d2d9465a9cf', 
#         'payment_id_local': '6068eebc394447d4a7931d2d9465a9cf', 
#         'uid': 'Cv3mKxfaCAVDf8QZDNkC8ukCkRy2', 
#         'products': ['Laptop 1'], 
#         'index': 0, 'shipping_address': {
#             'state': 'hahaha', 
#             'district': 'weq', 
#             'city': 'hahahah', 
#             'pin': '123123', 
#             'line1': 'hahaha', 
#             'line2': 'hahahah'
#             }
#         }, 
#     'delivery_date': '2022-03-20'
# }




def send_dispatch_email(email,info):
    subject = "Product Dispatch Info"
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    message =  f'''
    Dear user,
    Your Order has been dispatched\n
    Following are details : 
    payment date: {info["user_info"]["payment_date"]}\n
    payment id : {info["user_info"]["payment_id"]}\n
    products : { ",".join(info["user_info"]["products"]) }\n
    Delivery Date : {info["delivery_date"]}\n
    shipping address : \n
        Address Line 1 : {info["user_info"]["shipping_address"]["line1"]}\n
        Address Line 2 : {info["user_info"]["shipping_address"]["line2"]}\n
        City : {info["user_info"]["shipping_address"]["city"]}\n
        District : {info["user_info"]["shipping_address"]["district"]}\n
        State : {info["user_info"]["shipping_address"]["state"]}\n
        Pincode : {info["user_info"]["shipping_address"]["pin"]}\n
    
    '''
    # print(message)
    # print(email)
    send_mail(subject,message,email_from,recipient_list)
    print("email sent")
    
    
    
    
# {
#     'user_info': 
#         {
#             'index': 0, 
#             'payment_id': 'e008148f8c1748ca97f14720e7727b12', 
#             'shipping_address': {
#                 'pin': '123123', 
#                 'district': 'weq', 
#                 'state': 'hahaha', 
#                 'line1': 'hahaha', 
#                 'line2': 'hahahah', 
#                 'city': 'hahahah'
#             }, 
#             'total': 170, 
#             'payment_date': '17-03-2022', 
#             'payment_id_local': 'e008148f8c1748ca97f14720e7727b12', 
#             'uid': 'Cv3mKxfaCAVDf8QZDNkC8ukCkRy2', 
#             'products': ['Laptop 1']
#         }, 
#         'delivery_date': '2022-03-26'
# }

def send_delivered_email(email,info):
    # print(info)
    subject = "Product Deliverd Info"
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    message =  f'''
    Dear user,
    Your Order has been delivered\n
    Following are details :
    payment date: {info["user_info"]["payment_date"]}\n
    payment id : {info["user_info"]["payment_date"]}\n
    products : { ",".join(info["user_info"]["products"]) }\n
    Delivery Date : {info["delivery_date"]}\n
    shipping address : \n
        Address Line 1 : {info["user_info"]["shipping_address"]["line1"]}\n
        Address Line 2 : {info["user_info"]["shipping_address"]["line2"]}\n
        City : {info["user_info"]["shipping_address"]["city"]}\n
        District : {info["user_info"]["shipping_address"]["district"]}\n
        State : {info["user_info"]["shipping_address"]["state"]}\n
        Pincode : {info["user_info"]["shipping_address"]["pin"]}\n
    '''
    send_mail(subject,message,email_from,recipient_list)