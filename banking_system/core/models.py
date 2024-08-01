from django.db import models
from authuser.models import User 
from account.models import Account
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal

TRANSACTION_TYPE = (
    ("transfer", "Transfer"),
    ("recieved", "Recieved"),
    ("withdraw", "Withdraw"),
    ("refund", "Refund"),
    ("request", "Payment Request"),
    ("none", "None")
)

TRANSACTION_STATUS = (
    ("failed", "Failed"),
    ("completed", "Completed"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("request_sent", "Request Sent"),
    ("request_settled", "Request Settled"),
    ("request_processing", "Request Processing"),
)

CARD_TYPE = (
    ("master", "Master"),
    ("visa", "Visa"),
    ("verve", "Verve"),
)

NOTIFICATION_TYPE = (
    ("None", "None"),
    ("Transfer", "Transfer"),
    ("Credit Alert", "Credit Alert"),
    ("Debit Alert", "Debit Alert"),
    ("Sent Payment Request", "Sent Payment Request"),
    ("Recieved Payment Request", "Recieved Payment Request"),
    ("Funded Credit Card", "Funded Credit Card"),
    ("Withdrew Credit Card Funds", "Withdrew Credit Card Funds"),
    ("Deleted Credit Card", "Deleted Credit Card"),
    ("Added Credit Card", "Added Credit Card"),
)

class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    description = models.CharField(max_length=1000, null=True, blank=True)
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_transactions")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_transactions")
    reciever_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="received_transactions")
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sent_transactions")
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"Transaction ID: {self.transaction_id} - Amount: {self.amount} - Status: {self.status}"


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=16)  # Changed to CharField
    month = models.IntegerField()
    year = models.IntegerField()
    cvv = models.IntegerField()
    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="master")
    card_status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card Number: {self.number} - User: {self.user}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="None")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"Notification for {self.user} - Type: {self.notification_type} - Amount: {self.amount}"
