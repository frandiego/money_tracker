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
    def tidy_transactions(cls, df:pd.DataFrame()):
        df = cls.coerce_columns(df=df, columns=C.transaction_keys, fill='')
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



