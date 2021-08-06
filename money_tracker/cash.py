import re
from .constants import Constants as C
from .data import Data

class Cash:

    @classmethod
    def transactions(cls):
        df = Data.transactions()[C.cash_keys]
        df.columns = [re.sub('([A-Z]+)', r'_\1',i).lower() for i in df.columns]
        return df.drop_duplicates()
