from .constants import Constants as C
import pandas as pd
from .bank import Bank
import os


class Data:

    @classmethod
    def coerce_columns(cls, df:pd.DataFrame(), columns:list, fill:str=''):
        for i in set(columns).difference(set(df.columns)):
            df[i] = fill
        return df[columns]


    @classmethod
    def read_saved_transactions(cls) -> pd.DataFrame:
        if os.path.exists(C.filename_transactions):
            return cls.coerce_columns(pd.read_feather(C.filename_transactions), C.transaction_keys)
        return pd.DataFrame()

    @classmethod
    def read_bank_transaciton(cls) -> pd.DataFrame:
        transactions = Bank.transactions()
        if transactions:
            return cls.coerce_columns(pd.read_feather(C.filename_transactions), C.transaction_keys)
        return pd.DataFrame()

    @classmethod
    def transactions(cls) -> pd.DataFrame:
        df = pd.concat([cls.read_saved_transactions(), cls.read_bank_transaciton()])
        df = cls.coerce_columns(df, C.transaction_keys)
        df.drop_duplicates(inplace=True)
        df.sort_values(C.valueDate, ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_feather(C.filename_transactions)
        return df



