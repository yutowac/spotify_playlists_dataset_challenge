import json
import random
import collections
import numpy as np
import pandas as pd
import streamlit as st

with open('../data/processed/dict_summary_playlist.json') as f:
    d_summary_playlist = json.load(f)
with open('../data/processed/dict_summary_track_tracks.json') as f:
    d_summary_track = json.load(f)
with open('../data/processed/dict_summary_track_artists.json') as f:
    d_summary_artists = json.load(f)
with open('../data/processed/dict_summary_track_albums.json') as f:
    d_summary_albums = json.load(f)
with open('../data/processed/dict_playlist_and_tracks.json') as f:
    d_playlist_and_tracks = json.load(f)
with open('../data/processed/dict_summary_track_playlists.json') as f:
    d_track_and_playlists = json.load(f)

df_top50Track = pd.read_csv('../data/processed/df_top50Track.csv')
L_TOP50_TRACKS = df_top50Track['top50_track']
UNIQUE_TRACKS = len(list(set(d_summary_track['names_track'])))

# 今回はArmのバリエーションを固定しています。
# 本来であればArm Class作って、内部に評価値やふるまいを関数とするのが良いと思います。
# その他Arm案について：新曲、性別、年齢ラベルなど
def Arm1(track):
    """その曲が入っているプレイリスト群の中で最もたくさん出現する曲"""
    print('Arm1 chosen')
    l_playlists = d_track_and_playlists[track]
    tracks=[]
    for t_playlist in l_playlists:
        playlist = t_playlist[0]
        tracks += d_playlist_and_tracks[playlist]
    if len(tracks)==0:
        print('Arm1 other')
        r = int(abs(random.normalvariate(1, 16)))
        r = r if r<=48 else r*0
        track_next = L_TOP50_TRACKS[r]
        if track==track_next:
            track_next = L_TOP50_TRACKS[r+1]
    else:
        track_next = collections.Counter(tracks).most_common()[0][0]
        if track==track_next:
            track_next = collections.Counter(tracks).most_common()[1][0]
    return track_next

def Arm2(track):
    """その曲が入っているプレイリストで次に再生されやすい曲"""
    print('Arm2 chosen')
    l_playlists = d_track_and_playlists[track]
    tracks = []
    for t_playlist in l_playlists:
        playlist = t_playlist[0]
        pos = t_playlist[1]
        if len(d_playlist_and_tracks[playlist])<=pos:
            tracks.append(d_playlist_and_tracks[playlist][pos+1])
        else:
            tracks.append(d_playlist_and_tracks[playlist][pos-1])
    if len(tracks)==0:
        print('Arm2 other')
        r = int(abs(random.normalvariate(1, 16)))
        r = r if r<=48 else r*0
        track_next = L_TOP50_TRACKS[r]
        if track==track_next:
            track_next = L_TOP50_TRACKS[r+1]
    else:
        track_next = collections.Counter(tracks).most_common()[0][0]
    return track_next

def Arm3(track):
    """プレイリストの出現回数が多い曲Top50"""
    print('Arm3 chosen')
    r = int(abs(random.normalvariate(1, 16)))
    r = r if r<=48 else r*0
    track_next = L_TOP50_TRACKS[r]
    if track==track_next:
        track_next = L_TOP50_TRACKS[r+1]
    return track_next

def Arm4(track):
    """完全にランダム"""
    print('Arm4 chosen')
    r = random.randint(0,UNIQUE_TRACKS)
    track_next = list(d_track_and_playlists.keys())[r]
    if track==track_next:
        track_next = list(d_track_and_playlists.keys())[r+1]
    return track_next

def scoring(Scores, answer, index):
    """Armのスコアの加点減点。ユーザーの回答で決定"""
    # 良い評価
    if answer == 'like':
        Scores[index] += 1
    # goodでもbadでもない場合は評価：加点する
    elif answer == '-':
        Scores[index] += 0.4
    # 悪い評価
    else:
        Scores[index] -= 1
    return Scores

def sellect_e_greedy(Scores, epsilon=0.6):
	if np.random.binomial(n=1, p=epsilon) == 1:
		# 探索:random
		index = random.randint(0, 3)
		print('rondom')
	else:
        # 活用:Max Score Arm
		index = Scores.index(max(Scores))
	return index

Arms = [Arm1, Arm2, Arm3, Arm4]
Scores = [0,0,0,0]
r = random.randint(0,UNIQUE_TRACKS)
track = list(d_track_and_playlists.keys())[r]
index = sellect_e_greedy(Scores, 1)
A = Arms[index]
track_next = A(track)
n = d_summary_track['names_track'].index(track_next)
artist = d_summary_artists['names_artist'][n]
album = d_summary_albums['names_albums'][n]

st.text("Play This Track")
st.header('track: '+track_next)
st.subheader('artist: '+artist)
st.subheader('album: '+album)

st.text("Your Evaluation")
column1, column2, column3= st.columns(3,gap='small')
if column1.button("like"):
	Scores = scoring(Scores, "like", index)
	index = sellect_e_greedy(Scores)
	A = Arms[index]
	track_next = A(track)
if column2.button("next"):
	Scores = scoring(Scores, "-", index)
	index = sellect_e_greedy(Scores)
	A = Arms[index]
	track_next = A(track)
if column3.button("dislike"):
	Scores = scoring(Scores, "dislike", index)
	index = sellect_e_greedy(Scores)
	A = Arms[index]
	track_next = A(track)
