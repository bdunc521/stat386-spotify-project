#Load in Libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Plot formatting
#plt.rcParams.update({
#    "figure.facecolor": (0, 0, 0, 0),  # (R, G, B, Alpha)
#    "axes.facecolor": (0, 0, 0, 0),
#    "savefig.transparent": True
#})
plt.style.use('dark_background')

st.set_page_config(page_title="Artist Exploration")

#Load in data and section off by artist
DATA_PATH = 'app_artists.csv'
df = pd.read_csv(DATA_PATH)
artist_list = df['artists'].unique().tolist()
acous_avg = df.groupby('year')['acousticness'].mean().reset_index()
durat_avg = df.groupby('year')['duration_s'].mean().reset_index()

#Dropdown to select an artist
artist = st.selectbox('Select an artist:', options = [artist_list, 'all artists'])

if artist == 'all':

    tab1, tab2 = st.tabs(['Average Song Length','Average Song Acousticness'])
    with tab2:
    
        fig, ax = plt.subplots()
        ax.scatter(durat_avg['year'], durat_avg['duration_s'] , color='red')
        ax.set_title('Song Length by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Length (s)')
        ax.patch.set_alpha(0)
        st.pyplot(fig)

    with tab1:
        fig, ax = plt.subplots()
        ax.scatter(acous_avg['year'], acous_avg['acousticness'] , color='purple')
        ax.set_title('Average Acousticness by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Acousticness')
        ax.patch.set_alpha(0)
        st.pyplot(fig)
    
#Reduces the DataFrame to just the selected artist
df_selected = df[df['artists'] == artist].reset_index()
#Must have at least 3 songs in the year to count
df_selected = df_selected.groupby('year').filter(lambda x: len(x) >= 3).reset_index(drop = True)
#Calculate averages to simplify graphing
acous_avg = df_selected.groupby('year')['acousticness'].mean().reset_index()
durat_avg = df_selected.groupby('year')['duration_s'].mean().reset_index()

#Display dataframe on the app
st.dataframe(df_selected)

tab1, tab2 = st.tabs(['Average Song Length','Average Song Acousticness'])
with tab2:
  
        fig, ax = plt.subplots()
        ax.scatter(durat_avg['year'], durat_avg['duration_s'] , color='red')
        ax.set_title('Average Song Length by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Length (s)')
        ax.patch.set_alpha(0)
        st.pyplot(fig)

with tab1:
    fig, ax = plt.subplots()
    ax.scatter(acous_avg['year'], acous_avg['acousticness'] , color='purple')
    ax.set_title('Average Acousticness by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Acousticness')
    ax.patch.set_alpha(0)
    st.pyplot(fig)
    
    
