import os
import requests
from itertools import chain


class Bank:

    url = {
        'requisition': 'https://ob.nordigen.com/api/requisitions/{}/',
        'transactions': 'https://ob.nordigen.com/api/accounts/{}/transactions/'
    }

    @classmethod
    def headers(self):
        return {'accept': 'application/json', 'Authorization': f"Token {os.getenv('TOKEN')}"}

    @classmethod
    def get(cls, url):
        return requests.get(url, headers=cls.headers())

    @classmethod
    def _requisition(cls):
        return cls.get(cls.url.get('requisition').format(os.getenv('REQUISITION')))

    @classmethod
    def accounts(cls):
        return cls._requisition().json().get('accounts', [])

    @classmethod
    def _transactions(cls):
        return {i:cls.get(cls.url.get('transactions').format(i)).json().get('transactions', {}) for i in cls.accounts()}

    @classmethod
    def _merge(cls,transaction:dict,  transaction_type:str, account_id:id):
        return {**transaction, **{'transaction_type':transaction_type, 'account_id': account_id}}

    @classmethod
    def nested_transactions(cls):
        return [[[cls._merge(i, t, k) for i in j] for t, j in v.items()] for k, v in cls._transactions().items()]

    @classmethod
    def flat_transactions(cls):
        return list(chain(*chain(*cls.nested_transactions())))


