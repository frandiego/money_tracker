from types import SimpleNamespace
import os


class Constants:
    path_data = './data'
    filename_transactions = os.path.join(path_data, 'transactions.fth')

    requisition = 'requisition'
    requisitions = 'requisitions'
    transactions = 'transactions'

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
    createdAt = 'createdAt'

    transactionType = 'transactionType'
    accountId = 'accountId'
    valueDate = 'valueDate'
    
    transactionId = 'transactionId'
    bookingDate = 'bookingDate'
    createdAt = 'createdAt'
    
    transaction_keys = [accountId, transactionId, 'mandateId',
                        bookingDate, valueDate, 'remittanceInformationUnstructured',
                        transactionType, transactionAmount, transactionCurrency, 'balance',
                        creditorAccount, 'creditorName', 'ultimateCreditor',
                        debtorAccount, 'debtorName', 'ultimateDebtor',
                        'bankTransactionCode', 'apiName', createdAt]

    environment_variables = SimpleNamespace(**{i: i for i in ['REQUISITION', 'TOKEN']})

    url = SimpleNamespace(**{
        requisitions: 'https://ob.nordigen.com/api/requisitions/{}/',
        transactions: 'https://ob.nordigen.com/api/accounts/{}/transactions/'
    })
