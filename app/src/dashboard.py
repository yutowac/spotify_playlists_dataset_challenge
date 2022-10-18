import json
import collections
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st

with open('../data/processed/dict_summary_playlist.json') as f:
    d_summary_playlist = json.load(f)

st.set_page_config(layout="wide")

# Data
df = pd.DataFrame(d_summary_playlist)
df_topTrack = pd.read_csv('../data/processed/df_top10Track.csv')
df_topTrack['top10_track']=df_topTrack['top10_track']+'('+df_topTrack['top10_track_artist']+')'
df_topAlbum = pd.read_csv('../data/processed/df_top10Album.csv')
df_topAlbum['top10_album']=df_topAlbum['top10_album']+'('+df_topAlbum['top10_album_artist']+')'
vars_hist = [var for var in df.columns if var.startswith('num')]

# l_num_durations = d_summary_playlist['num_durations']
# l_rate_albumsByTracks = d_summary_playlist['rate_albumsByTracks']

# Layout Sidebar
st.sidebar.markdown("## Basic Info: Numbers")
with st.sidebar.form(key='basic info'):
    # not unique
    st.sidebar.text("・Playlist: " + str(len(d_summary_playlist['names_playlist'])) + '')
    st.sidebar.text("・Tracks : " + str(sum(d_summary_playlist['num_tracks'])) + '')
    st.sidebar.text("・Albums : " + str(sum(d_summary_playlist['num_albums'])) + '')
    st.sidebar.text("・Artists: " + str(sum(d_summary_playlist['num_artists'])) + '')
    st.sidebar.text("・Follows:  " + str(sum(d_summary_playlist['num_followers'])) + '')

st.sidebar.markdown("## Settings")
hist1_selected = st.sidebar.selectbox('Variables of Histogram(left)', vars_hist, index=0)
hist2_selected = st.sidebar.selectbox('Variables of Histogram(right)', vars_hist, index=1)
cont_multi_selected = st.sidebar.multiselect('Correlation Matrix', vars_hist, default=vars_hist)

# Content Bar Chart
fig_bar1 = px.bar(df_topTrack, x='top10_track', y='num_in_playlists', labels={'top10_track':'top 10 tracks(artists)','num_in_playlists':'numbers in playlists'})
fig_bar1.update_layout(height=350,
                       margin={'l': 10, 'r': 5, 't': 0, 'b': 0},
                       showlegend=False
                       )

fig_bar2 = px.bar(df_topAlbum, x='top10_album', y='num_in_playlists', labels={'top10_album':'top 10 albums(artists)','num_in_playlists':'numbers in playlists'})
fig_bar2.update_layout(height=350,
                       margin={'l': 10, 'r': 5, 't': 0, 'b': 0},
                       showlegend=False
                       )

# Content Histogram
fig_hist1 = px.histogram(df[hist1_selected],
                        labels={'value':hist1_selected.split('_')[1]},
                        marginal='box',
                        nbins=30)
fig_hist1.update_layout(height=300,
                       margin={'l': 10, 'r': 5, 't': 0, 'b': 0},
                       showlegend=False
                       )

fig_hist2 = px.histogram(df[hist2_selected],
                        labels={'value':hist2_selected.split('_')[1]},
                        marginal='box',
                        nbins=30)
fig_hist2.update_layout(height=300,
                       margin={'l': 5, 'r': 10, 't': 0, 'b': 0},
                       showlegend=False
                       )

# Content Correlation
df_corr = df[cont_multi_selected].corr()
x = list(df_corr.columns)
y = list(df_corr.index)
z = np.array(df_corr)

fig_corr = ff.create_annotated_heatmap(
    z,
    x = x,
    y = y ,
    annotation_text = np.around(z, decimals=3),
    hoverinfo='z',
    colorscale='Magma'
    ).update_yaxes(autorange="reversed")
fig_corr.update_layout(height=300,
                       margin={'l': 20, 'r': 20, 't': 0, 'b': 0})

# Layout (Content)
st.header('Statistical Dashboard of Spotify Playlists')

st.subheader('Bar Chart')
column1, column2 = st.columns(2,gap='medium')
column1.caption('Top10 Tracks & Artists')
column2.caption('Top10 Albums & Artists')
column1.plotly_chart(fig_bar1)
column2.plotly_chart(fig_bar2)

st.subheader('Histogram')
column1, column2 = st.columns(2,gap='medium')
column1.caption('Number of ' + hist1_selected.split('_')[1] + ' in a Playlist')
column2.caption('Number of ' + hist2_selected.split('_')[1] + ' in a Playlist')
column1.plotly_chart(fig_hist1)
column2.plotly_chart(fig_hist2)
st.subheader('Correlation Matrix')
st.plotly_chart(fig_corr)
