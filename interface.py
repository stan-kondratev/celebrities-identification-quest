
import pandas as pd
import streamlit as st
from logic import DataRetrieve
# import datetime
# import numpy as np
# import os
import unicodedata

st.set_page_config(layout="centered")
'''
# Celebrities Guessing with Images
'''

@st.cache_data
def get_data_celebrities():
    return pd.read_csv("raw_data/list_act.csv")

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

df = get_data_celebrities()
score_words = ["Frigid","Bitterly Cold","Chilling","Brisk","Refreshing","Pleasantly Mild","Balmy","Sweltering","Roasting","Scorching Hot"]


if 'score_list' not in st.session_state:
    st.session_state['score_list'] = [(0,0,0)]

hidden_celebrity, hint = DataRetrieve.celeb_selector(file_path="raw_data/metafile.csv")

df.sort_values(by="name",axis=0, ascending=True, inplace=True)

values =df['name'].tolist()
keys = df.index.to_list()

col1, col2 = st.columns([0.4,0.6],gap="small")

with col1:
    """
    #### Select a celebrity
    """
    a = st.selectbox("", values)
    a_key = df[df["name"]==a].index.values[0]
    img = DataRetrieve.get_image(a)
    st.image(img,use_column_width=True)
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        if st.button("Guess", use_container_width=True):
            hidden_celebrity = "_".join(strip_accents(hidden_celebrity.lower()).split())
            celebrity = "_".join(strip_accents(a.lower()).split())
            if hidden_celebrity==celebrity:
                score = (a,100)
                st.balloons()
            else:
                score = DataRetrieve.celeb_and_score_query(hidden_celebrity=hidden_celebrity,celebrity=celebrity,names_df=pd.read_csv("raw_data/names.csv"),score_df=pd.read_csv("raw_data/scoring.csv"))
            st.session_state["score_list"].append([a,score[1],score_words[int(score[1]/10)]])

    with col1_2:
        if st.button("Hint", use_container_width=True):
            st.write(hint[0])
    if st.button("Show answer", use_container_width=True):
        st.text(hidden_celebrity)
    else:
        st.text(" ")
with col2:
    """
    #### Score tracking
    """
    st.text(" ")
    st.text(" ")
    df_score = pd.DataFrame(st.session_state["score_list"], columns=["Name","Score","Score description"])
    st.dataframe(df_score.iloc[1:].sort_values(by="Score", ascending=False),use_container_width=True,column_config={0:"Seq",1:"Name                       ",2:"Score",3:""})
