from email import message
from django.core.mail import send_mail
from keys import EMAIL_HOST_USER



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

    send_mail(subject,message,email_from,recipient_list)
    print("email sent")
    
    
def send_delivered_email(email,info):
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
    
    