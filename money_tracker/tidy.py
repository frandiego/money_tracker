import datetime
from .constants import Constants as C


class TidyTransaction:

    @classmethod
    def tidy_account_iban(cls, transaction: dict, key: str, iban_key: str = C.iban) -> dict:
        if key in transaction:
            if isinstance(transaction[key], dict):
                iban = transaction[key].get(iban_key)
                transaction[key] = iban
        return transaction

    @classmethod
    def tidy_transaction_amount(cls, transaction: dict) -> dict:
        if C.transactionAmount in transaction:
            if isinstance(transaction[C.transactionAmount], dict):
                amount = transaction[C.transactionAmount].get(C.amount)
                currency = transaction[C.transactionAmount].get(C.currency)
                transaction[C.transactionAmount] = amount
                transaction[C.transactionCurrency] = currency
        return transaction

    @classmethod
    def merge(cls, transaction: dict, metadata: dict) -> dict:
        return {**transaction, **metadata}

    @classmethod
    def tidy(cls, transaction: dict) -> dict:
        for i in [C.debtorAccount, C.creditorAccount]:
            transaction = cls.tidy_account_iban(transaction, i)
        transaction = cls.tidy_transaction_amount(transaction)
        transaction = cls.merge(transaction, {C.apiName: C.nordigen})
        transaction = cls.merge(transaction, {C.createdAt: str(datetime.datetime.utcnow())})
        transaction = {i: transaction.get(i) for i in C.transaction_keys}
        return transaction
