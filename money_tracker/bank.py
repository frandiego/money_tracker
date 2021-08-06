import os
from itertools import chain

import requests

from .tidy import TidyTransaction
from .constants import Constants as C

class Bank:

    @classmethod
    def headers(self):
        return {'accept': 'application/json', 'Authorization': f"Token {os.getenv(C.environment_variables.TOKEN)}"}

    @classmethod
    def get(cls, url):
        return requests.get(url, headers=cls.headers())

    @classmethod
    def _requisition(cls):
        return cls.get(C.url.requisitions.format(os.getenv(C.environment_variables.REQUISITION)))

    @classmethod
    def accounts(cls):
        return cls._requisition().json().get(C.accounts, [])

    @classmethod
    def _transactions(cls):
        return {i: cls.get(C.url.transactions.format(i)).json().get(C.transactions, {}) for i in cls.accounts()}

    @classmethod
    def _balances(cls):
        return {i: cls.get(C.url.balances.format(i)).json().get(C.balances, {}) for i in cls.accounts()}

    @classmethod
    def _merge(cls, transaction: dict, transaction_type: str, account_id: id):
        return {**transaction, **{C.transactionType: transaction_type, C.accountId: account_id}}

    @classmethod
    def nested_transactions(cls):
        return [[[cls._merge(i, t, k) for i in j] for t, j in v.items()] for k, v in cls._transactions().items()]

    @classmethod
    def flat_transactions(cls):
        return list(chain(*chain(*cls.nested_transactions())))

    @classmethod
    def transactions(cls):
        return list(map(TidyTransaction.tidy, cls.flat_transactions()))
