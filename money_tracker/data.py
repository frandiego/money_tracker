from .constants import Constants as C
import pandas as pd
from .bank import Bank
import numpy as np
import os
from datetime import datetime

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
    def feather_path(cls, filename:str) -> str:
        return os.path.join(C.path_data, filename + C.feather_extension)

    @classmethod
    def read_feather(cls, filename:str) -> pd.DataFrame:
        path = cls.feather_path(filename)
        if os.path.exists(path):
            return pd.read_feather(path)
        return pd.DataFrame()
    
    @classmethod
    def save_feather(cls, df:pd.DataFrame, filename:str):
        path = cls.feather_path(filename)
        df = cls.columns_to_string(df).drop_duplicates().reset_index(drop=True)
        df.to_feather(path)

    @classmethod
    def update_feather(cls, df:pd.DataFrame, filename:str, output:bool=True) -> pd.DataFrame:
        df = pd.concat([df, cls.read_feather(filename)])
        cls.save_feather(df, filename)
        if output:
            return df

    @classmethod
    def shoud_call_api(cls, filename:str) -> dict:
        path = cls.feather_path(filename)
        if os.path.exists(path):
            last_creation = datetime.fromtimestamp(os.path.getmtime(path))
            return (datetime.now() - last_creation).total_seconds() / 60**2>1

    @classmethod
    def transactions(cls):
        if cls.shoud_call_api(C.transactions):
            request = Bank.transactions()
            safe =  request if request else []
            df =  cls.tidy_transactions(pd.DataFrame.from_records(safe))
            return cls.tidy_transactions(cls.update_feather(df, C.transactions))
        return cls.tidy_transactions(cls.read_feather(C.transactions))


    @classmethod
    def balance_amount(cls, balance:dict) -> float:
        return float([i.get(C.balanceAmount) for i in balance if i.get(C.balanceType) == C.closingBooked][0].get(C.amount))

    @classmethod
    def get_balances(cls) -> pd.DataFrame:
        balances = Bank._balances()
        details = Bank._details()
        balances_dict =  {k: cls.balance_amount(v) for k, v in balances.items()}
        details_dict = {k:v.get(C.resourceId) for k, v in details.items()}
        df =  pd.DataFrame(balances_dict.keys(), columns=[C.accountId])
        df[C.iban] = df[C.accountId].map(details_dict)
        df[C.balance] = df[C.accountId].map(balances_dict)
        df[C.dateStamp] = str(datetime.utcnow().date())
        return df
        
    @classmethod
    def balances(cls):
        if cls.shoud_call_api(C.balances):
            df = cls.get_balances()
            return cls.update_feather(df, C.balances)
        return cls.read_feather(C.balances)



