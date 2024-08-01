from django.shortcuts import render, redirect
from core.models import Transaction
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@login_required
def transaction_lists(request):
    sent_transactions = Transaction.objects.filter(
        Q(sender=request.user) & Q(transaction_type="transfer")
    ).order_by("-id")
    received_transactions = Transaction.objects.filter(
        Q(reciever=request.user) & Q(transaction_type="transfer")
    ).order_by("-id")

    sent_requests = Transaction.objects.filter(
        Q(sender=request.user) & Q(transaction_type="request")
    )
    received_requests = Transaction.objects.filter(
        Q(reciever=request.user) & Q(transaction_type="request")
    )

    context = {
        "sent_transactions": sent_transactions,
        "received_transactions": received_transactions,
        "sent_requests": sent_requests,
        "received_requests": received_requests,
    }

    return render(request, "transaction-list.html", context)

@login_required
def transaction_detail(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        return render(request, "404.html", status=404)

    context = {
        "transaction": transaction,
    }

    return render(request, "transaction-detail.html", context)