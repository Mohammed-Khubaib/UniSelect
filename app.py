import streamlit as st
import pandas as pd
from st_on_hover_tabs import on_hover_tabs
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title='University Short Listing',page_icon='🏫',layout='wide',initial_sidebar_state='expanded')

hide_streamlit_style="""
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    h1 {
        color: #01FFB3 ;
    }
    h2 {
        color: darkorange;
    }
    h3 {
        color: red;
        # color: #12FFE2;
    }
    h4 {
        color: coral;
        # color: #12FFE2;
    }
    /* The progress bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(to right, #00EEFF, #01FFB3);
            border-radius: 10px;
        }
        /* The text inside the progress bars */
        .stProgress > div > div > div > div > div {
            color: white;
        }
    </style>
    """
st.markdown(hide_streamlit_style,unsafe_allow_html=True)
def load_lottie_file(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
lottie_file1 =load_lottie_file('./Gloab.json')
lottie_file2 =load_lottie_file('./uni.json')
with st.sidebar:
    st_lottie(lottie_file1,speed=0.5,reverse=False,height=100,width=260)
    tabs = on_hover_tabs(tabName=['Dashboard'],  
                         iconName=['bar_chart_4_bars'], default_choice=0,
                         styles = {'navtab': {'background-color':'#272731',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                    'tabOptionsStyle': {':hover :hover': {'color': 'orangered',
                                                                      'cursor': 'pointer'}},              
                                                  
                                                  },
                         )
if tabs == "Dashboard":
    c1,c2,c3= st.columns([0.25,0.15,0.5])
    with c2:
        st_lottie(lottie_file2,speed=0.5,reverse=False,height=100,width=260)
    with c3:
        st.title("Short Listing University")

    merged_df = pd.read_csv('./merged.csv')
    chances = merged_df['% Chance'].unique()
    States_and_Territories = merged_df['State'].unique()
    selected_States_and_Territories=st.multiselect('Please select one or more U.S.🇺🇸 states and territories',States_and_Territories)

    public_vs_private = merged_df['Private / Public'].unique()
    selected_public_vs_private = st.multiselect('Select Private or Public University',public_vs_private)

    category = merged_df['Category'].unique()
    selected_category = st.multiselect('Select Regional or National University',category)

    Ranking = merged_df['Rank Class (Estimated)'].unique()
    selected_ranking = st.multiselect('Select The Ranking you prefer from the following ',Ranking)
    st.divider()
    filtered_df = merged_df[
        (merged_df['State'].isin(selected_States_and_Territories)) &
        (merged_df['Private / Public'].isin(selected_public_vs_private)) &
        (merged_df['Category'].isin(selected_category)) &
        (merged_df['Rank Class (Estimated)'].isin(selected_ranking))
    ]
    if filtered_df.empty != True:
        st.dataframe(filtered_df[['University','% Chance','Private / Public','F1 Slots Ranking','General Rank', 'US News Ranking', 'Regional Ranking','Category','State','City']], use_container_width=True)
        options_count = r'''\large \color{limegreen}\text{Total Available Options : }\color{goldenrod}'''+f'''{filtered_df.shape[0]}'''+f'''\\\\🎉🥳👏'''
        st.latex(options_count)
    else:
        states_count = r'''\large \color{limegreen}\text{Total U.S.🇺🇸 states and territories : }\color{goldenrod}'''+f'''{merged_df['State'].nunique()}'''
        st.latex(states_count)
        city_count = r'''\large \color{cyan}\text{Total U.S.🇺🇸 Cities with Universities : }\color{limegreen}'''+f'''{merged_df['City'].nunique()}'''
        st.latex(city_count)
        University_count = r'''\large \color{orange}\text{Total Universities in the U.S.🇺🇸 : }\color{orangered}'''+f'''{merged_df['University'].nunique()}'''
        st.latex(University_count)