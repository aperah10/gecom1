# from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import *
# from .models import CustomUser 
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# requires to define two functions authenticate and get_user

# class YourAuth:  

    # def authenticate(self, request, username=None):
    #     try:
    #         user = User.objects.get(username=username)
    #         return user
    #     except User.DoesNotExist:
    #         return None
        
    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None
# ! Working this
    # def authenticate(self, request, username=None):
    #     try:
    #         user = CustomUser.objects.get(username=username)
    #         return user
    #     except CustomUser.DoesNotExist:
    #         return None
        
    # def get_user(self, user_id):
    #     try:
    #         return CustomUser.objects.get(pk=user_id)
    #     except CustomUser.DoesNotExist:
    #         return None

    


# class PasswordlessAuthBackend(ModelBackend):
#     """Log in to Django without providing a password.

#     """
#     # def authenticate(self, username=None):
#     #     try:
#     #         return User.objects.get(username=username)
#     #     except User.DoesNotExist:
#     #         return None

#     # def get_user(self, user_id):
#     #     try:
#     #         return User.objects.get(pk=user_id)
#     #     except User.DoesNotExist:
#     #         return None
#     def authenticate(self, username=None):
#         try:
#             return CustomUser.objects.get(username=username)
#         except CustomUser.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return CustomUser.objects.get(pk=user_id)
#         except CustomUser.DoesNotExist:
#             return None