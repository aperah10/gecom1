import requests
import random 

from django.conf import settings
# ! Send Otp
def send_otp_to_phone(phoneNum):
    try:
        otp=random.randint(1000, 9999) 
        
        # url=f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phoneNum}/{otp}'
        # response =requests.get(url)
        # print(response)
        return otp
    except Exception as e:
        return None