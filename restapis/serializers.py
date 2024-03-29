from rest_framework import serializers

# MY IMPORT FOR ALL FIELS
from .models import *


# ================

# make accounts in
class RegisterSer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["phone", "password","email","fullname","isSeller","isCustomer"]

        def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            return user


class LoginSer(serializers.ModelSerializer):
 
  class Meta:
    model = CustomUser
    fields = [ 'phone', 'password']

# ---------------------------------------------------------------------------- #
#                    orc ProfilePage GET AND POST SERILIZER                    #
# ---------------------------------------------------------------------------- #

# ! PROFILE POST METHOD
class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "fullname",
            "pic",
            "gender",
        ]

# ALL PRODUCT SHOW DATA
class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class AddProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "salesPrice",
            "discountPrice",
            "stock",
            "pic",
            "upload",
            "category","offers"
        ]

# ALL PRODUCT SHOW DATA
class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        depth = 1
# ---------------------------------------------------------------------------- #
#                       ! ADDRESS METHOD POST AND GET SERILIZER                                         #
# ---------------------------------------------------------------------------- #
class AddressSer(serializers.ModelSerializer):
    # class Meta:
    #     model = Address
    #     fields = "__all__"
    class Meta:
        model =  Address
        fields = "__all__"
        depth = 2


class AddAddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "fullname",
            "phone",
            "email",
            "house",
            "trade",
            "area",
            "city",
            "pinCode",
            "delTime",
            "state",
            "upload",
        ]




# # ALL PRODUCT SHOW DATA
# class AllProductSer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"
#         depth = 1
# ---------------------------------------------------------------------------- #
#                           orc CART ADDED SERILIZER                           #
# ---------------------------------------------------------------------------- #

# CART FOR DATA
class CartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        # fields=["id","product","quantity"]
        depth = 3

class AddCartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ["product", "quantity", "upload"]

class UpdateCartSer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [ "quantity",]

# ! ORDER PAGE METHOD
class AddOrderSer(serializers.ModelSerializer):
    class Meta:
        model = AllOrder
        # fields = ['quantity','product']
        fields = ['quantity','address', "customer",'seller','product']
        # depth = 2



# ! Seller Order Update
class SelOrderUpdateSer(serializers.ModelSerializer):
    class Meta:
        model = AllOrder
        fields = ['status','selOrderStatus']


class OrderSer(serializers.ModelSerializer):
    class Meta:
        model = AllOrder
        fields = "__all__"
        depth = 3


class NotificationSer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        depth = 1



class AddNotificationSer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["sender","recevier","description","title"]
       