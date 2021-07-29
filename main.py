import os
import streamlit as st

from money_tracker import Data

os.environ.update({i[0]: i[1] for i in [i.split('=') for i in open('.env').read().split()]})

df = Data.transactions()
st.write(df)
