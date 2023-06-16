
import pandas as pd
import streamlit as st
from logic import DataRetrieve

'''
# Celebrities Guessing with Images
'''
df = DataRetrieve.get_data_celebrities()

df.sort_values(by="name",axis=0, ascending=True, inplace=True)

values =df['name'].tolist()
keys = df.index.to_list()

score = {
    "Name": [],
    "Score": []
}

# def guess(name, score):

#     return df.iloc[id]


col1, col2 = st.columns(2,gap="large")

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
        st.button("Guess", use_container_width=True)
    with col1_2:
        st.button("Hint", use_container_width=True)
    st.button("Show answer", use_container_width=True)

with col2:
    """
    #### Score tracking
    """
    st.text(" ")
    st.text(" ")
    df_score = pd.DataFrame(score)
    st.dataframe(df_score,width=300, hide_index=True)
