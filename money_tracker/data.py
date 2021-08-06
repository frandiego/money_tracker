from .constants import Constants as C
import pandas as pd
from .bank import Bank
import numpy as np
import os
import datetime

class Data:

    @classmethod
    def coerce_columns(cls, df:pd.DataFrame(), columns:list, fill:str=''):
        for i in set(columns).difference(set(df.columns)):
            df[i] = fill
        return df[columns]

    @classmethod
    def columns_to_string(cls, df:pd.DataFrame()):
        for i in df.columns:
            df[i] = df[i].astype(str).fillna('')
        return df

   
    @classmethod
    def tidy_transactions(cls, df:pd.DataFrame()):
        df = cls.coerce_columns(df=df, columns=C.transaction_keys, fill='')
        df = cls.columns_to_string(df=df)
        df = df.drop_duplicates(subset=C.transactionId, keep='first')
        df = df.drop_duplicates().sort_values(C.valueDate, ascending=False).reset_index(drop=True)
        return df

    @classmethod
    def read_bank_transactions(cls):
        request = Bank.transactions()
        safe =  request if request else []
        return cls.tidy_transactions(pd.DataFrame.from_records(safe))

    @classmethod
    def read_feather(cls, filename:str) -> pd.DataFrame:
        if os.path.exists(filename):
            return cls.tidy_transactions(pd.read_feather(filename))
        return pd.DataFrame()

    @classmethod
    def read_saved_transactions(cls) -> pd.DataFrame:
        return cls.tidy_transactions(cls.read_feather(C.filename_transactions))
    
    @classmethod
    def read_transactions(cls):
        df = pd.concat([cls.read_saved_transactions(), cls.read_bank_transactions()])
        return cls.tidy_transactions(df)

    @classmethod
    def transactions(cls) -> pd.DataFrame:
        df = cls.read_transactions()
        df.to_feather(C.filename_transactions)
        return df

    @classmethod
    def balance_amount(cls, balance:dict) -> float:
        return float([i.get(C.balanceAmount) for i in balance if i.get(C.balanceType) == C.closingBooked][0].get(C.amount))

    @classmethod
    def balances(cls) -> dict:
        balances = Bank._balances()
        details = Bank._details()
        
        balances_dict =  {k: cls.balance_amount(v) for k, v in balances.items()}
        details_dict = {k:v.get(C.resourceId) for k, v in details.items()}

        df =  pd.DataFrame(balances_dict.keys(), columns=[C.accountId])
        df[C.iban] = df[C.accountId].map(details_dict)
        df[C.balance] = df[C.accountId].map(balances_dict)
        df[C.dateStamp] = str(datetime.datetime.utcnow().date())
        df = pd.concat([cls.read_feather(C.filename_balances), df])
        df = df.drop_duplicates(keep='last')
        df = cls.columns_to_string(df).drop_duplicates().reset_index(drop=True)
        df.to_feather(C.filename_balances)
        return df
        



