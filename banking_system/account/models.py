from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from authuser.models import User
from django.db.models.signals import post_save


ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    account_number = ShortUUIDField(unique=True,length=10, max_length=25, prefix="217", alphabet="1234567890") 
    account_id = ShortUUIDField(unique=True,length=7, max_length=25, prefix="DEX", alphabet="1234567890") 
    pin_number = ShortUUIDField(unique=True,length=4, max_length=7, alphabet="1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'account'


    def __str__(self):
        return f"{self.user}"

class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    account =  models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    marrital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="user_identity_images", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}"    

    
    class Meta:
        db_table = 'kyc'



def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(sender, instance,**kwargs):
    instance.account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)


