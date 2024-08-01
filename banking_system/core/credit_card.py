from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard, Notification
from account.models import Account
from decimal import Decimal
from django.http import HttpResponse
from core.models import Transaction

@login_required
def all_cards(request):
    account = get_object_or_404(Account, user=request.user)
    credit_cards = CreditCard.objects.filter(user=request.user)

    context = {
        "account": account,
        "credit_cards": credit_cards,
    }
    return render(request, "all-card.html", context)

@login_required
def card_detail(request, card_id):
    account = get_object_or_404(Account, user=request.user)
    credit_card = get_object_or_404(CreditCard, card_id=card_id, user=request.user)

    context = {
        "account": account,
        "credit_card": credit_card,
    }
    return render(request, "card-detail.html", context)

@login_required
def withdraw_fund(request, card_id):
    account = get_object_or_404(Account, user=request.user)
    credit_card = get_object_or_404(CreditCard, card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        print(f"Received withdrawal amount: {amount}")

        try:
            withdrawal_amount = Decimal(amount)
        except (ValueError, ArithmeticError):
            messages.warning(request, "Invalid amount format.")
            return redirect("core:card-detail", card_id=card_id)
        
        print(f"Parsed withdrawal amount: {withdrawal_amount}")
        print(f"Credit card amount before withdrawal: {credit_card.amount}")

        if withdrawal_amount <= credit_card.amount:
            account.account_balance += withdrawal_amount
            account.save()

            credit_card.amount -= withdrawal_amount
            credit_card.save()
            
            Notification.objects.create(
                user=request.user,
                amount=withdrawal_amount,
                notification_type="Withdrew Credit Card Funds"
            )

            messages.success(request, "Withdrawal Successful")
        else:
            messages.warning(request, "Insufficient Funds")
        
        return redirect("core:card-detail", card_id=credit_card.card_id)

    return HttpResponse("Method not allowed", status=405)

@login_required
def delete_card(request, card_id):
    credit_card = get_object_or_404(CreditCard, card_id=card_id, user=request.user)
    account = get_object_or_404(Account, user=request.user)

    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
        
    credit_card.delete()
    
    Notification.objects.create(
        user=request.user,
        notification_type="Deleted Credit Card"
    )
    
    messages.success(request, "Card Deleted Successfully")
    return redirect("account:dashboard")

@login_required
def fund_credit_card(request, card_id):
    credit_card = get_object_or_404(CreditCard, card_id=card_id, user=request.user)
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount")
        print(f"Received funding amount: {amount}")
        
        try:
            funding_amount = Decimal(amount)
        except (ValueError, ArithmeticError):
            messages.warning(request, "Invalid amount format.")
            return redirect("core:card-detail", card_id=card_id)
        
        print(f"Parsed funding amount: {funding_amount}")
        print(f"Credit Card amount before funding: {credit_card.amount}")

        if funding_amount > 0:  # Ensure the funding amount is positive
            # Увеличиваем баланс карты
            credit_card.amount += funding_amount
            credit_card.save()
            
            # Создаем уведомление
            Notification.objects.create(
                amount=funding_amount,
                user=request.user,
                notification_type="Funded Credit Card"
            )
            
            messages.success(request, "Funding Successful")
            print(f"Credit Card amount after funding: {credit_card.amount}")
        else:
            messages.warning(request, "Invalid funding amount")
        
        return redirect("core:card-detail", card_id=card_id)
    
    return HttpResponse("Method not allowed", status=405)