from .constants import Constants as C
import pandas as pd
from .bank import Bank
import numpy as np
import os


class Data:

    @classmethod
    def coerce_columns(cls, df:pd.DataFrame(), columns:list, fill:str=''):
        for i in set(columns).difference(set(df.columns)):
            df[i] = fill
        return df[columns]
    
    @classmethod
    def tidy_transaction_id(cls, df:pd.DataFrame()):
        mask = df[C.apiName].isna() & df[C.transactionId].isna()
        if mask.sum():
            dfg = df.loc[mask].groupby([C.bookingDate])
            ids = pd.to_datetime(df[mask][C.bookingDate]).astype(int) + dfg.cumcount()
            df.loc[mask, C.transactionId] = ids
        return df
    
    @classmethod
    def tidy_duplicated_transactions(cls, df:pd.DataFrame()):
        if df[C.transactionId].nunique() < len(df):
            aux = df[C.transactionId].value_counts()
            duplicates = aux[aux>1].index.tolist()
            mask_dup = df[C.transactionId].isin(duplicates)
            dfg = df[mask_dup].groupby([C.accountId, C.transactionId])
            first_transaction = dfg[C.createdAt].transform(np.min)
            mask_first = df.loc[mask_dup, C.createdAt] == first_transaction
            return pd.concat([df[~mask_dup], df[mask_dup][mask_first]])
        return df
   
    @classmethod
    def tidy_transactions(cls, df:pd.DataFrame()):
        df = cls.coerce_columns(df=df, columns=C.transaction_keys, fill='')
        df = cls.tidy_transaction_id(df)
        df = cls.tidy_duplicated_transactions(df)
        return df.drop_duplicates().sort_values(C.valueDate, ascending=False).reset_index(drop=True)

    @classmethod
    def read_bank_transactions(cls):
        request = Bank.transactions()
        safe =  request if request else []
        return cls.tidy_transactions(pd.DataFrame.from_records(safe))

    @classmethod
    def read_saved_transactions(cls) -> pd.DataFrame:
        if os.path.exists(C.filename_transactions):
            return cls.tidy_transactions(pd.read_feather(C.filename_transactions))
        return cls.tidy_transactions(pd.DataFrame())
    
    @classmethod
    def read_transactions(cls):
        df = pd.concat([cls.read_saved_transactions(), cls.read_bank_transactions()])
        return cls.tidy_transactions(df)

    @classmethod
    def transactions(cls) -> pd.DataFrame:
        df = cls.read_transactions()
        df.to_feather(C.filename_transactions)
        return df



