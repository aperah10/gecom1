from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from .models import *
# from .forms import *

# Register your models here.

# Custom Accounts
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "id",
        "phone",
        "email",
        "fullname",
        "is_staff",
        "password",
    )
    list_filter = (
      
        "phone",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone", "password", "fullname")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "fullname",
                
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("phone",)
    ordering = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)

# ! Mobile Otp Admin
@admin.register(MobileOtp)
class MobileAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "otp","is_phone_verfied")

# Profile ADMIN / PROFILE
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "gender",  "pic", "fullname")

# ADDRESS ADMIN
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "city", "house", "trade", "pinCode", "state")


# Product ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "title", "description", "salesPrice", "stock", "quantity", "discountPrice")



# Category ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","title")



# Cart Product ADMIN
@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("id", "upload", "product", "quantity", "shipPrice")

# Cart Profile ADMIN
@admin.register(CartProfile)
class CartProfileAdmin(admin.ModelAdmin):
      list_display = ("id", "upload", 'get_cartList' )
    # list_display = ("id", "upload",'get_category' )




# ! ALL ORDER 
@admin.register(AllOrder)
class AllOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "product",
        "address",
        "ammount",
        "quantity",
        "upload",
    )


# !CURRENT ORDER
@admin.register(CurrentOrder)
class CurrentOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderStatus",
        "product",
        "address",
        "ammount",
        "quantity",
        "upload",
    )


# ! SUCCESS ORDERKEY
@admin.register(SuccessOrder)
class SuccessOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "orderSeller",
        "product",
        "address",
        "quantity",
        "upload",
    )


# Cancel Order
@admin.register(CancelOrder)
class CancelOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "orderUser", "orderSeller", "ammount")  