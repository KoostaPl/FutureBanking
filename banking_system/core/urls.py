from django.urls import path
from core import views, transfer, transaction, payment_request, credit_card

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),

    path("search-card/", transfer.search_users_card_number, name="search-card"),
    path('amount-transfer/<slug:card_id>/', transfer.AmountTransfer, name='amount-transfer'),
    path("amount-transfer-process/<card_id>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<card_id>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<card_id>/<transaction_id>/", transfer.TransferProcess, name="transfer-process"),
    path("transfer-completed/<card_id>/<transaction_id>/", transfer.TransferCompleted, name="transfer-completed"),


    # Transactions
    path("transactions/", transaction.transaction_lists, name="transactions"),
    path('transaction-lists/', transaction.transaction_lists, name='transaction-lists'),
    path("transaction-detail/<transaction_id>/", transaction.transaction_detail, name="transaction-detail"),
    

    # Payment Request
    path("request-search-account/", payment_request.SearchUsersRequest, name="request-search-account"),
    path("amount-request/<account_number>/", payment_request.AmountRequest, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.AmountRequestProcess, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>/", payment_request.AmountRequestConfirmation, name="amount-request-confirmation"),
    path("amount-request-final-process/<account_number>/<transaction_id>/", payment_request.AmountRequestFinalProcess, name="amount-request-final-process"),
    path("amount-request-completed/<account_number>/<transaction_id>/", payment_request.RequestCompleted, name="amount-request-completed"),

    # Request Settlement
    path("settlement-confirmation/<account_number>/<transaction_id>/", payment_request.settlement_confirmation, name="settlement-confirmation"),
    path("settlement-processing/<account_number>/<transaction_id>/", payment_request.settlement_processing, name="settlement-processing"),
    path("settlement-completed/<account_number>/<transaction_id>/", payment_request.SettlementCompleted, name="settlement-completed"),
    path("delete-request/<account_number>/<transaction_id>/", payment_request.deletepaymentrequest, name="delete-request"),

    # Credit Card URLS
    path("all-cards/", credit_card.all_cards, name="all-cards"),
    path("card/<card_id>/", credit_card.card_detail, name="card-detail"),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw-fund"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete-card"),
]
