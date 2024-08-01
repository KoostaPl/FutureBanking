from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard, Notification, Transaction




def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("account:kyc-reg")
        
        account = Account.objects.get(user=request.user)
        credit_cards = CreditCard.objects.filter(user=request.user)

        recent_sent_transactions = Transaction.objects.filter(sender=request.user).order_by('-date')[:5]
        recent_received_transactions = Transaction.objects.filter(reciever=request.user).order_by('-date')[:5]
    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("account:sign-in")

    context = {
        "kyc": kyc,
        "account": account,
        "credit_cards": credit_cards,
        "recent_sent_transactions": recent_sent_transactions,
        "recent_received_transactions": recent_received_transactions,
    }
    return render(request, "account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submitted successfully, In review now.")
            return redirect("account:account")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "kyc-form.html", context)

def dashboard(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        messages.warning(request, "You need to submit your KYC")
        return redirect("account:kyc-reg")
    
    recent_transfer = Transaction.objects.filter(sender=request.user, transaction_type="transfer", status="completed").order_by("-id")[:1]
    recent_received_transfer = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")[:1]

    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    receiver_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")

    request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
    request_receiver_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")
    
    account = Account.objects.get(user=request.user)
    credit_cards = CreditCard.objects.filter(user=request.user).order_by("-id")

    if request.method == "POST":
        form = CreditCardForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user 
            new_form.save()
            
            Notification.objects.create(
                user=request.user,
                notification_type="Added Credit Card"
            )
            
            messages.success(request, "Card Added Successfully.")
            return redirect("account:dashboard")
    else:
        form = CreditCardForm()

    context = {
        "user": request.user,  # Добавьте это для доступа к пользователю в шаблоне
        "kyc": kyc,
        "account": account,
        "form": form,
        "credit_card": credit_cards,
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        'request_sender_transaction': request_sender_transaction,
        'request_receiver_transaction': request_receiver_transaction,
        'recent_transfer': recent_transfer,
        'recent_received_transfer': recent_received_transfer,
    }
    return render(request, "dashboard.html", context)
    
