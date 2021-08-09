import re
from .constants import Constants as C
from .data import Data
import numpy as np
import pandas as pd

class Cash:

    @classmethod
    def clean_columns(cls, df:pd.DataFrame):
        return [re.sub('([A-Z]+)', r'_\1',i).lower() for i in df.columns]

    @classmethod
    def tidy_data(cls, df:pd.DataFrame):
        df.columns = cls.clean_columns(df)
        return df.drop_duplicates()

    @classmethod
    def transactions(cls):
        return cls.tidy_data(Data.transactions()[C.cash_keys])

    @classmethod
    def balances(cls):
        df = Data.balances()
        max_dates = df.groupby([C.accountId])[C.dateStamp].transform(np.max)
        df = df[df[C.dateStamp] == max_dates]
        return cls.tidy_data(df)


