from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from account.models import Account
from core.models import Transaction, Notification, CreditCard

@login_required
def search_users_card_number(request):
    query = request.POST.get("card_number", '')
    cards = CreditCard.objects.all()

    if query:
        cards = cards.filter(Q(number__icontains=query)).distinct()

    context = {
        "accounts": cards,
        "query": query,
    }
    return render(request, "search-user-by-card-number.html", context)

@login_required
def AmountTransfer(request, card_id):
    print(f"Received card_id: {card_id}")
    card = get_object_or_404(CreditCard, id=card_id)
    print(f"Found card: {card}")
    
    context = {
        "card": card,
    }
    return render(request, "amount-transfer.html", context)

@login_required
def AmountTransferProcess(request, card_id):
    try:
        receiver_card = CreditCard.objects.get(card_id=card_id)
    except CreditCard.DoesNotExist:
        messages.warning(request, "Credit Card does not exist.")
        return redirect("core:search-card")

    sender_account = request.user.account
    receiver_account = receiver_card.user.account

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get("amount-send"))
            description = request.POST.get("description")

            if sender_account.account_balance >= amount:
                new_transaction = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    description=description,
                    reciever=receiver_card.user,
                    sender=request.user,
                    sender_account=sender_account,
                    reciever_account=receiver_account,
                    status="processing",
                    transaction_type="transfer"
                )

                sender_account.account_balance -= amount
                receiver_account.account_balance += amount

                sender_account.save()
                receiver_account.save()

                return redirect("core:transfer-confirmation", card_id=card_id, transaction_id=new_transaction.transaction_id)
            else:
                messages.warning(request, "Insufficient funds.")
                return redirect("core:amount-transfer", card_id=card_id)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("core:amount-transfer", card_id=card_id)
    else:
        messages.warning(request, "Invalid request method.")
        return redirect("account:account")

@login_required
def TransferConfirmation(request, card_id, transaction_id):
    card = get_object_or_404(CreditCard, card_id=card_id)
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    context = {
        'transaction': transaction,
        'card': card,
    }
    return render(request, 'transfer-confirmation.html', context)

@login_required
def TransferProcess(request, card_id, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    sender_account = request.user.account
    receiver_card = get_object_or_404(CreditCard, card_id=card_id)
    receiver_account = receiver_card.user.account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            receiver_account.account_balance += transaction.amount

            sender_account.save()
            receiver_account.save()

            Notification.objects.create(
                amount=transaction.amount,
                user=receiver_card.user,
                notification_type="Credit Alert"
            )
            Notification.objects.create(
                user=request.user,
                notification_type="Debit Alert",
                amount=transaction.amount
            )

            messages.success(request, "Transfer successful.")
            return redirect("core:transfer-completed", card_id=card_id, transaction_id=transaction_id)
        else:
            messages.warning(request, "Incorrect PIN.")
            return redirect('core:transfer-confirmation', card_id=card_id, transaction_id=transaction_id)
    else:
        messages.warning(request, "Invalid request method.")
        return redirect('core:transfer-confirmation', card_id=card_id, transaction_id=transaction_id)

@login_required
def TransferCompleted(request, card_id, transaction_id):
    card = get_object_or_404(CreditCard, card_id=card_id)
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    context = {
        "card": card,
        "transaction": transaction
    }
    return render(request, "transfer-completed.html", context)
