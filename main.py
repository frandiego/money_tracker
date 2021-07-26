import os
import pandas as pd
import streamlit as st

from bank import Bank

os.environ.update({i[0]: i[1] for i in [i.split('=') for i in open('.env').read().split()]})

st.write(pd.DataFrame(Bank.flat_transactions()))
