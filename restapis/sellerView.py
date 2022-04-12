from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from .serializers import *  
from .models import * 
from .renders import *

from django.db.models import Q




# Product Seller
class SelProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user
        prod = Product.objects.filter(upload=usr)
        

        try:

            ser = ProductSer(prod, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc Address POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr =data.get("uplod")
       

        new_prod = {
            "title": data.get("title"),
            "description": data.get("description"),
            "salesPrice": data.get("salesPrice"),
            "discountPrice": data.get("discountPrice"),
            "stock": data.get("stock"),
            "pic": data.get("pic"),
            "category": data.get("category"),
            "offers": data.get("offers"),
            "upload": usr,
        }

        # print(new_addres)
        serializer = AddProductSer(data=new_prod)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # orc Update Adress
    def put(self, request, pk=None):
        data = request.data
        idt =data.get("id")
        usr=request.user.id
        
        cus = Product.objects.get(pk=idt)
        new_prod = {
            "title": data.get("title"),
            "description": data.get("description"),
            "salesPrice": data.get("salesPrice"),
            "discountPrice": data.get("discountPrice"),
            "stock": data.get("stock"),
            # "pic": data.get("pic"),
            # "pic":  request.FILES.getlist('pic'),
            "category": data.get("category"),
            "offers": data.get("offers"),
            "upload": usr,
        }

        # print(new_profile)
        serializer = AddProductSer(cus, data=new_prod)

        # print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            return Response(
                {
                    "stateCode": 200,
                    "msg": "enter data",
                }
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    # ! Delete 
    def delete(self, request,pk=None):
        idt = request.data.get("id")

        try:
            if Product.objects.filter(pk=idt).exists():
                prd = Product.objects.filter(pk=idt)
              
                prd.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)




class SelOrderView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    
    # ! CURRENT ORDER data
    def get(self, request):
        usr = request.user
        order =AllOrder.objects.filter(seller=request.user.id)
        try:
           ser = OrderSer(order, many=True)
           alldata = ser.data
            # print(alldata)
        except:
            alldata = ser.errors

        return Response(alldata)

    
    def put(self, request,pk=None):
        data = request.data
        idt = data.get("id")
        cus = AllOrder.objects.get(pk=idt)
       
        usr=request.user
        new_order = {
            "status":"Accept",
            "selOrderStatus":data.get("selOrderStatus")
        }
        # print(cus.customer)
        # print(cus.seller)
        if data.get("status")=="Decline":
            CancelOrder.objects.create(id=cus.id,cancelby="seller")
            Notification.objects.create(sender=cus.seller.upload, recevier=cus.customer.upload,description="Order Cancel By User")
            cus.delete()
            res = {"error": False, "msg": " data delete"}
            return Response(res)
            
        else: 
            serializer = SelOrderUpdateSer(cus,data=new_order)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = serializer.save()
                Notification.objects.create(sender=cus.seller.upload, recevier=cus.customer.upload,description=data.get("selOrderStatus"))
                return Response(
                    {
                    "stateCode": 200,
                    "msg": "enter data",
                    }
                )
        return Response(serializer.errors)
    

    