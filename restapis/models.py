from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import uuid
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password


 



# MY CUSTOMUSER
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    phone = models.CharField(
        unique=True, max_length=15, validators=[RegexValidator("^[789]\d{9}$")]
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130, null=True,blank=True,
    )
    email = models.EmailField(_("emailaddress"), unique=True,null=True,blank=True)
    # otp=models.CharField(max_length=6)
    is_phone_verfied=models.BooleanField(default=False)

    is_staff = models.BooleanField(_("is_staff"), default=False)
    is_active = models.BooleanField(_("is_active"), default=True)
    date_joined = models.DateField(_("date_joined"), default=date.today)
    change_pw = models.BooleanField(default=True)
    isCustomer = models.BooleanField(default=False,null=True,
        blank=True,)
    isSeller = models.BooleanField(default=False,null=True,
        blank=True,)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("Accounts")
        verbose_name_plural = _("Acconts")

    def get_short_name(self):
        """
        Returns the display name.
        If full name is present then return full name as display name
        else return username.
        """
        if self.fullname != "":
            return self.fullname
        else:
            return str(self.phone) 


class MobileOtp(models.Model):
    phone = models.CharField(unique=True,
         max_length=15, validators=[RegexValidator("^[789]\d{9}$")]
    )
    otp=models.CharField(max_length=6)
    is_phone_verfied=models.BooleanField(default=False)



class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    isCustomer = models.BooleanField(default=True)
    fullname = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(_("emailaddress"), unique=True, null=True, blank=True)
    upload = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200,
        null=True,
        blank=True,
    )
    pic = models.ImageField(upload_to="CustomerImg", blank=True, null=True)

    # @permalink
    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.upload.id)


# ! Seller Profile 
class SellerProfile(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    isSeller = models.BooleanField(default=False)
    fullname = models.CharField(max_length=100, null=True,blank=True)
    email = models.EmailField(_("emailaddress"), unique=True, null=True, blank=True)
    upload = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200,
        null=True,
        blank=True,
    )
    businesspic = models.ImageField(upload_to="SellerImg", blank=True, null=True)
    businessname=models.CharField(max_length=100, null=True,
        blank=True,)
    pic = models.ImageField(upload_to="SellerImg", blank=True, null=True)

    # @permalink
    def get_absolute_url(self):
        return reverse("", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.upload.id)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    upload = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="addressuser"
    )
    fullname = models.CharField(
        _("full name"),
        max_length=130,
    )
    phone = models.CharField(max_length=15, validators=[RegexValidator("^[789]\d{9}$")])
    email = models.EmailField(_("emailaddress"), null=True, blank=True)
    house = models.CharField(max_length=300, null=True, blank=True)
    trade = models.CharField(max_length=200, null=True, blank=True)
    area = models.CharField(max_length=200,  null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pinCode = models.CharField(
        max_length=100,
        validators=[RegexValidator("^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$")],
    )
    delTime = models.CharField(max_length=100,  default="AnyTime")
    state = models.CharField(max_length=200)
    

    def __str__(self):
        return str(self.upload)



# ! Category 
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# ! Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    salesPrice = models.FloatField()
    discountPrice = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField()
    pic=models.FileField(upload_to='ProdcutImg',blank=True,null=True)
    # pic = models.ImageField(upload_to="ProdcutImg", blank=True)
    offers = models.IntegerField(default=1, null=True, blank=True)
    upload = models.ForeignKey(
        # to=CustomUser,
        to=SellerProfile,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,null=True,blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField(default=0)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:  # Check for create
            self.ammount = self.discountPrice * self.quantity
        else:

            self.ammount = self.discountPrice * self.quantity
        return super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("product", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title




# !  Cart In Product
class CartProduct(models.Model):
    class Meta:
        unique_together = (("upload"), ("product"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    upload = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField(default=0)
    shipPrice = models.PositiveIntegerField(default=50)
    totalAmmount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def user_id(self):
     return self.id.__str__()
    
    
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice
        else:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice

        return super().save(*args, **kwargs)

# !Cart Profile
class CartProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    upload=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    cartUpload = models.JSONField(default={})
    
    
    
    # def __str__(self):
    #     return str(self.upload)
    def __str__(self):
        return f"cartID ={self.id}user={self.upload}| cartList={len(self.cartUpload)}"
    def save(self, *args, **kwargs):
       return super().save(*args, **kwargs)
    
    def get_cartList(self):
        usr=self.upload
        prodList = CartProduct.objects.filter(upload=self.upload) 
        for p in prodList:
            print(p)
        return f' {list(prodList).__len__() } {list(prodList)}'
        # return prodList
    # def get_category(self):
    #     return "\n".join([p.cartUpload for p in self.cartUpload.all()])





# ------------------ORDER MODEL ------------------------------
OrderStateT = (
    ("Dispatch", "Dispatch"),
    ("Shipment", "Shipment"),
    ("Arrives at", "Arrives at"),
    ("Complete", "Complete"),
)

StateT = (("Pending", "Pending"), ("Accept", "Accept"), ("Decline", "Decline"))


# !ORDER BASE CLASS
class BaseOrder(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    seller=models.ForeignKey(SellerProfile, on_delete=models.CASCADE, null=True,
        blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    ammount = models.PositiveIntegerField()
    shipPrice = models.PositiveIntegerField(default=50)
    totalAmmount = models.PositiveIntegerField(default=0)

    # ! this method add ammount value is
    def save(self, *args, **kwargs):
        if not self.pk:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice
        else:
            self.ammount = self.product.discountPrice * self.quantity
            if self.ammount > 499:
                self.shipPrice = 0
                self.totalAmmount = self.ammount + self.shipPrice
            else:
                self.shipPrice = 70
                self.totalAmmount = self.ammount + self.shipPrice

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True



# ! All Order 
class AllOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    status = models.CharField(max_length=100, default='Pendiing')
    selOrderStatus = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

# ! CURRENT ORDER
class CurrentOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(AllOrder, on_delete=models.CASCADE)
    orderStatus = models.CharField(
        max_length=100,
        choices=OrderStateT,
        default="OrderConfirm",
        null=True,
        blank=True,
    )


#! Success ORDER
class SuccessOrder(BaseOrder):
    id = models.UUIDField(
        primary_key=True,
    )
    orderSeller = models.ForeignKey(CurrentOrder, on_delete=models.CASCADE)


# !CANCEL ORDER
class CancelOrder(models.Model):
    id = models.UUIDField(
        primary_key=True,
    )
    # upload = models.ForeignKey(
    #     AllOrder, on_delete=models.CASCADE, null=True, blank=True
    # )
    cancelby = models.CharField(max_length=50,null=True, blank=True)
   





# ! NOTIFICATION MODEl
class Notification(models.Model):
    id = models.UUIDField( primary_key=True, editable=False,default=uuid.uuid4)
    sender=models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name="customer")
    recevier = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name="seller")
    checked=models.BooleanField(default=False)
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField()