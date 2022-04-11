from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
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
from .helpers import send_otp_to_phone 
from django.db.models import Q
# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySer


# ! Register View 
class RegisterView(APIView):
    def post(self, request, format=None):
        data = request.data
        if CustomUser.objects.filter(Q(phone__exact=data.get('phone')) | Q(email__exact=data.get('email'))):
            return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        
        if not MobileOtp.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400, "msg": "Phone Verify First"}, 201)
      
        
        if MobileOtp.objects.get(phone__exact=data.get('phone')).is_phone_verfied ==True:
          new_user = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email":data.get("email"),
            "password": make_password(data.get("password")),
            "is_phone_verfied":True
          }
          print(new_user)

          serializer = RegisterSer(data=new_user)
          if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            username = data.get("phone")
            raw_password = data.get("password")

            cur_user = authenticate(username=username, password=raw_password)

            #   token, _ = Token.objects.get_or_create(user=cur_user)
            token = get_tokens_for_user(cur_user)
            return Response(
                {
                    'token':token,
                     'msg':'Registration Successful'}, status=status.HTTP_201_CREATED
                )
          return Response(
                {
                   'msg':'Verify Mobile First'},
                )
        return Response(
                {
                   'msg':'Verify Mobile First'},
                )
        
        
       
        

        
       

# =============================== LOGIN   =====================================
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def loginView(request):
    data=request.data
    username = data.get("phone")
    password = data.get("password")
    if not CustomUser.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400, "msg": "User is Not Existes"}, 201)
    print(request.user.is_authenticated)
    
    if not MobileOtp.objects.filter(phone__exact=data.get('phone')).exists(): 
          return Response({"stateCode": 400, "msg": "Phone Verify First"}, 201)
    
    if MobileOtp.objects.get(phone__exact=data.get('phone')).is_phone_verfied ==True:
      
        user = CustomUser.objects.get(phone=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
    else:
      user = authenticate(username=username, password=password)

   
    

    print(request.user.is_authenticated)
    
  
   
    
   
    # user = authenticate(username={data.get('phone')})
    # login(request, user)


  
    # try:
    #   # if 
    #     # user = authenticate(
    #     #     username=CustomUser.objects.get(email__iexact=username), password=password
    #     # )

    # except:
    #     user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid Credentials"},)
   
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    

# ! Profile 
class ProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    # print(request.user)
    # print(request.user.id)
    profile = Profile.objects.filter(upload=request.user)
    try:
            serializer = ProfileSer(profile, many=True)
            alldata = serializer.data

    except:
           
            alldata = ser.errors
    return Response(alldata,status=status.HTTP_200_OK)
    # serializer = ProfileSer(profile)
    # return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self,request,format=None):
       serializer = ProfileSer(data=request.data)
       serializer.is_valid(raise_exception=True)
    #    print(serializer)
       fullname = serializer.data.get('fullname')
       gender = serializer.data.get('gender')
       pic = serializer.data.get('pic')
      #  print(request.user)
      #  print(request.user.id)
       if pic is not None:
          mat = Profile.objects.update_or_create(id=request.user.id,upload= request.user, defaults={'fullname':fullname,'gender':gender})
       else:
         mat = Profile.objects.update_or_create(id=request.user.id,upload=request.user, defaults={'fullname':fullname,})
       return Response(serializer.data, status=status.HTTP_200_OK)


# ! ADDRESS View 
# ---------------------------------------------------------------------------- #
#                   ! ADDRESS POST & GET  METHOD                                     #
# ---------------------------------------------------------------------------- #
class AddressView(APIView):

    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # todo  GET METHOD
    def get(self, request):
        usr = request.user
        addres = Address.objects.filter(upload=usr)
        

        try:

            ser = AddressSer(addres, many=True)
            alldata = ser.data

        except:
            alldata = ser.errors

        return Response(alldata)

    # orc Address POST METHOD

    def post(self, request, pk=None):
        data = request.data
        usr = str(request.user.id)
        # usr =data.get("uplod")
       

        new_addres = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "upload": usr,
        }

        # print(new_addres)
        serializer = AddAddressSer(data=new_addres)

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
        
        cus = Address.objects.get(pk=idt)
        new_address = {
            "fullname": data.get("fullname"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "house": data.get("house"),
            "trade": data.get("trade"),
            "area": data.get("area"),
            "city": data.get("city"),
            "pinCode": data.get("pinCode"),
            "delTime": data.get("delTime"),
            "state": data.get("state"),
            "upload": usr
            
        }

        # print(new_profile)
        serializer = AddAddressSer(cus, data=new_address)

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
            if Address.objects.filter(pk=idt).exists():
                adr = Address.objects.filter(pk=idt)
              
                adr.delete()
                res = {"error": False, "msg": "data delete"}
            else:
                res = {"error": True, "msg": " not have any data"}

        except:
            res = {"error": True}
        return Response(res)





    
# ---------------------------------------------------------------------------- #
#                                 ! CART METHOD                                 #
# ---------------------------------------------------------------------------- #
class CartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # ! get cart data 
    def get(self, request):
        data = request.data
        usr = str(request.user.id)
        
        
        usrCart = CartProduct.objects.filter(upload=usr)

        try:
            ser = CartSer(usrCart, many=True)
            alldata = ser.data

        except:
           
            alldata = ser.errors
        return Response(alldata)
    
    # ! post cart data .get
     # orc PROFILE POST METHOD

    def post(self, request):
        data = request.data
        usr = str(request.user.id) 
        # usr= data.get("customerCart")
        newCart = {
            "quantity": data.get("quantity"),
            "product": data.get("product"),
            "upload": str(usr),
            
        }

        if CartProduct.objects.filter(
            Q(upload__exact=usr)
            & Q(product__exact=data.get("product"))
        ):
            return Response({"stateCode": 201, "msg": "User Exits"}, 201)
        
        serializer = AddCartSer(data=newCart)
        
      
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

    # orc QUANTITY UPDATE 
    def put(self, request, pk=None):
        data = request.data
        idt = request.data.get("id")
        cus = CartProduct.objects.get(pk=idt)
        
        new_cartu = {
            "quantity": data.get("quantity"),
        }
        serializer = UpdateCartSer(cus, data=new_cartu)

      
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
    


    def delete(self, request,pk=None):
        idt= request.data.get("id") 
        cus = CartProduct.objects.get(pk=idt)
        print(cus)
        if CartProduct.objects.filter(pk=idt).exists():
                card = CartProduct.objects.get(pk=idt)
                
                card.delete()
                res = {"error": False, "msg": "data delete"}
                return Response(res)
        
        else:
            res = {"error": True, "msg": " not have any data"}
        return Response(res)






# ---------------------------------------------------------------------------- #
#                                 ! ORDER PAGE                                 #
# ---------------------------------------------------------------------------- #
class OrderView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    # !  ORDER REQUEST DATA
    def post(self, request):
        data = request.data
        # usr = str(request.user.id)
        # usr=data.get("upload")
        usr=request.user.id
        # adr=data.get("address")
        # adrs=Address.objects.filter(upload=usr)
        # prod=Product.objects.get(pk=data.get("product"))
        # prod=Product.objects.filter(pk=data.get("product"))
        # adr=Address.objects.get(upload=usr)
        # print(prod)
        # print(data)
        # print(adr2)
        # print(adrs.id)
        

        if Address.objects.filter(Q(upload=usr)) :
            new_order = {
               "product": data.get("product"),
                "address": data.get("address"),
                "quantity": data.get("quantity"),
                "upload": usr,
                }

            serializer = AllOrderSer(data=new_order)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = serializer.save()
                return Response(
                    {
                    "stateCode": 200,
                    "msg": "enter data",
                    }
                )
            return Response(serializer.errors, )

        return Response('Order Wrong', )

    # ! CURRENT ORDER data
    def get(self, request):
        usr = request.user
        # order = CurrentOrder.objects.filter(upload=usr)
        order =AllOrder.objects.filter(upload=usr)
        

        try:
            ser = CurrentOrderSer(order, many=True)
            alldata = ser.data
            print(alldata)

        except:
            alldata = ser.errors

        return Response(alldata)