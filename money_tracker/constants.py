from types import SimpleNamespace
import os


class Constants:
    path_data = './data'
    transactions = 'transactions'
    balances = 'balances'
    feather_extension = '.fth'
    requisition = 'requisition'
    requisitions = 'requisitions'
    transactions = 'transactions'
    balances = 'balances'
    details = 'details'
    account = 'account'
    accounts = 'accounts'
    amount = 'amount'
    currency = 'currency'

    nordigen = 'nordigen'
    iban = 'iban'

    transactionAmount = 'transactionAmount'
    transactionCurrency = 'transactionCurrency'
    debtorAccount = 'debtorAccount'

    creditorAccount = 'creditorAccount'
    apiName = 'apiName'

    transactionType = 'transactionType'
    accountId = 'accountId'
    valueDate = 'valueDate'
    
    transactionId = 'transactionId'
    bookingDate = 'bookingDate'

    mandateId = 'mandateId'
    remittanceInformationUnstructured = 'remittanceInformationUnstructured'
    balance = 'balance'

    creditorName = 'creditorName'
    ultimateCreditor = 'ultimateCreditor'
    debtorName = 'debtorName'

    ultimateDebtor = 'ultimateDebtor'
    bankTransactionCode = 'bankTransactionCode'
    apiName = 'apiName'

    balanceAmount = 'balanceAmount'
    balanceType = 'balanceType'
    closingBooked = 'closingBooked'
    amount = 'amount'
    dateStamp = 'dateStamp'
    resourceId = 'resourceId'
    
    transaction_keys = [accountId, transactionId, mandateId,
                        bookingDate, valueDate, remittanceInformationUnstructured,
                        transactionType, transactionAmount, transactionCurrency, balance,
                        creditorAccount, creditorName, ultimateCreditor,
                        debtorAccount, debtorName, ultimateDebtor,
                        bankTransactionCode, apiName]

    cash_keys = [accountId, transactionId, bookingDate, valueDate,  remittanceInformationUnstructured, 
                 transactionAmount, transactionCurrency, creditorAccount, creditorName, 
                 debtorAccount, debtorName]
    

    environment_variables = SimpleNamespace(**{i: i for i in ['REQUISITION', 'TOKEN']})
    
    base_url = 'https://ob.nordigen.com/api'
    url = SimpleNamespace(**{
        requisitions: base_url + '/requisitions/{}/',
        transactions: base_url + '/accounts/{}/transactions/',
        balances : base_url + '/accounts/{}/balances/', 
        details : base_url + '/accounts/{}/details/', 
    })
