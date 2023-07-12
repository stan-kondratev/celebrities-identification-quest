
import pandas as pd
import streamlit as st
from celebrity import DataRetrieval
import unicodedata
import plotly.express as px


# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state, page_title='CIQ', page_icon='⭐')

# Define page width
page_width = 75
css=f'''
<style>
    section.main > div {{max-width:{page_width}rem}}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

st.title('Celebrity Identification Quest')
# Caching data for a better performance
@st.cache_data
def get_data_celebrities():
    return pd.read_csv("raw_data/list_act.csv")

df = get_data_celebrities()

# Function to remove all letter modifications that could obstruct names processing
def remove_diacritics(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
# Scoring
score_words = ["Freezing","Very Cold","Cold","Cool","Mild","Warm","Hot","Very Hot",\
    "Scorching","You Won!"]

# Streamlit session_state intialization

if 'score_list' not in st.session_state:
    st.session_state['score_list'] = [(0,0,0,0)]
if 'hint_counter' not in st.session_state:
    st.session_state['hint_counter'] = 0
if 'game_mode' not in st.session_state:
    st.session_state['game_mode'] = 'daily'
if 'test_index' not in st.session_state:
    st.session_state['test_index'] = 0
if 'test_celebrity' not in st.session_state:
    st.session_state['test_celebrity'] = 'not chosen'

# Get a celebrity to guess and corresponding hint

hidden_celebrity, hint, selection_df = DataRetrieval.celeb_selector(file_path="raw_data/metafile_complete.csv", mode = st.session_state['game_mode'], test_index = st.session_state['test_index'])

# Hint intialization
hint_df = pd.DataFrame.from_dict(hint, orient='index')


df.sort_values(by="name",axis=0, ascending=True, inplace=True)

values =df['name'].tolist()
keys = df.index.to_list()


with st.sidebar:
    """
    # About the Game:
    Celebrity Identification Quest is game that tests your memory on faces of film celebrities
    # Rules of the Game:
    ### Objective:
    The main objective of the game is to correctly identify the hidden celebrity by making educated guesses
    based on the provided images.
    ### How it works:
    To make a guess, you need to select from our list of celebrities the one that you believe
    resemble the hidden personality. The game will analyze your choice and provide you with a score of similarity,
    indicating how close your guess is to the correct answer. This score will help you refine your future guesses.
    ### Visual progress:
    You can track your progress not only in the table but also with our radar-like map. It's a polar plot where
    radius is the similarity of celebrity to a hidden celebrity and angle is shows how other celebrities are different
    from each other. Red points represent celebrities you have already tried and the blue points represent the rest of
    our celebrity database. The closer a point to the centre the higher the resemblence. It is normal that at some point
    there is a huge gap betweeen the hidden celebrity and other celebrities as not every person has a famous sibling or
    a doppelganger.
    ### Hint Button:
    If you stack you can use our hints.
    Every time you click hint button you get a piece of information about the hidden celebrity: first gender then occupation,
    citizenship, and age.

    ### Further ideas:
    Currently the celebrities databse is rather scanty and limited to only a small set of celebrities that is
    mostly formed from top-100 actors and actresses of all time. So later on we will add more celebrities to make it easier to play.


    **Good luck and have fun!**

    **Author**: Stanislav Kondratev\n
    **Development**: Stanislav Kondratev and Joaquim Albuquerque\n
    **Test**: Carlota Armero and Hena Tabassum
    """
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')

## Developer mode
    st.session_state['game_mode'] = st.selectbox('Game mode', ['daily', 'test'])

    st.session_state['test_celebrity']  = st.selectbox("hidden celebrity choice", selection_df['Celebrity'])
    st.session_state['test_index'] = selection_df[selection_df['Celebrity']==st.session_state['test_celebrity']].index.values[0]
    st.button('Confirm')
    st.write(st.session_state['test_celebrity'], hidden_celebrity)


col1, col2, col3 = st.columns([0.25,0.35,0.4],gap="small")

with col1:
    """#### Select a celebrity"""
    selected_celebrity = st.selectbox("", values)
    selected_celebrity_key = df[df["name"]==selected_celebrity].index.values[0]
    selected_celebrity_image = DataRetrieval.get_celeb_image(selected_celebrity)
    st.image(selected_celebrity_image,use_column_width=True)

with col2:
    """#### Score tracking"""
    st.text(" ")
    st.text(" ")

    col2_1, col2_2 = st.columns([0.5,0.5])
    with col2_1:
        if st.button("Guess", use_container_width=True):
            hidden_celebrity = "_".join(remove_diacritics(hidden_celebrity.lower()).split())
            selected_celebrity_cleaned = "_".join(remove_diacritics(selected_celebrity.lower()).split())
            if hidden_celebrity==selected_celebrity_cleaned:
                score = (selected_celebrity,100)
                st.balloons()
                st.session_state["score_list"].append([selected_celebrity,score[1], score_words[-1], selected_celebrity_key])
            else:
                score = DataRetrieval.celeb_and_score_query(hidden_celebrity=hidden_celebrity,selected_celebrity=selected_celebrity_cleaned,\
                    names_df=pd.read_csv("raw_data/names.csv"),score_df=pd.read_csv("raw_data/scoring.csv"))
                st.session_state["score_list"].append([selected_celebrity,int(100-score[1]*100),score_words[int(int((100-score[1]*100))/10)],selected_celebrity_key])
    with col2_2:
        # Toggle sidebar state between 'expanded' and 'collapsed'.
        if st.button('Rules', use_container_width=True):
            st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
            # Force an app rerun after switching the sidebar state.
            st.experimental_rerun()

    score_table_df = pd.DataFrame(st.session_state["score_list"], columns=["Name","Score","Score description","key"])
    score_table_df.drop(columns="key", inplace=True)
    st.dataframe(score_table_df.iloc[1:].sort_values(by="Score", ascending=False),use_container_width=True, height=143, \
    column_config={0:"Seq",1:"Name                       ",2:"Score",3:""})

    if st.button("Hint", use_container_width=True):
        st.session_state['hint_counter'] += 1
    if st.session_state['hint_counter'] > len(hint):
        st.session_state['hint_counter'] = 0
    if st.session_state['hint_counter'] > 0:
        st.dataframe(hint_df.head(st.session_state['hint_counter']), use_container_width=True,column_config=\
            {0:"Hint",1:"Value"})



    if st.button("Give up", use_container_width=True):
        st.text(hidden_celebrity)
    else:
        st.text(" ")


with col3:
    '''#### Visual progress'''

    ### Plotting block ###
    hidden_celebrity_ = "_".join(remove_diacritics(hidden_celebrity.lower()).split())
    names_df=pd.read_csv("raw_data/names.csv")
    indices_df=pd.read_csv("raw_data/indices.csv")
    scoring_df=pd.read_csv("raw_data/scoring.csv")
    projections_df=pd.read_csv("raw_data/projections.csv")

    # Compilation of a df for plotting with plotly
    plotting_df = pd.concat([names_df[hidden_celebrity_], indices_df[hidden_celebrity_], scoring_df[hidden_celebrity_], projections_df[hidden_celebrity_]], axis=1)
    plotting_df.columns = ['names','indices', 'distances', 'projections']

    # Retrieval of celebrities that are already guessed
    guessed_celebrities = ["_".join(remove_diacritics(a.lower()).split()) for a in pd.DataFrame(st.session_state["score_list"])[1:][0]]

    # Reveal the names of celebrities that have been tried on the plot
    plotting_df['guessed'] = plotting_df["names"].apply(lambda x: "Guessed" if x in  guessed_celebrities else "Unknown")
    plotting_df['Celebrity Name'] = plotting_df["names"].apply(lambda x: x if x in guessed_celebrities else "Unknown")
    # Distribute projections evenly across 360 degrees of the polar plot
    plotting_df['radial_projections'] = plotting_df['projections'].apply(lambda x: (x- plotting_df['projections'].max())/(plotting_df['projections'].min()-plotting_df['projections'].max())*360)

    # Plot the scatter polar plot with plotly express
    fig = px.scatter_polar(plotting_df, r='distances', theta="radial_projections", color="guessed", \
                           color_discrete_map={"Guessed":"red", "Unknown":"blue"}, hover_name="Celebrity Name", \
                               hover_data={ 'distances':False, 'radial_projections':False, 'guessed': False } )
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.2,
    xanchor="left",
    x=0),
    legend_title_text='')
    fig.update_layout(polar = dict(radialaxis = dict(showticklabels = False)))
    fig.update_layout(polar = dict(angularaxis = dict(showticklabels = False)))
    st.plotly_chart(fig, use_container_width=True)

    ### End of plotting block ###
