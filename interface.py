
import pandas as pd
import streamlit as st
from wikidata import Tools
# Draw a title and some text to the app:
'''
# Celebrities Guessing wtih Images
'''
df = pd.read_csv("raw_data/list_act.csv")

df.sort_values(by="name",axis=0, ascending=True, inplace=True)

values = tuple(df['name'].tolist())

a = st.sidebar.selectbox('Select a Celebrity', values)

img = Tools.get_image(a)
st.sidebar.image(img,width=300)

