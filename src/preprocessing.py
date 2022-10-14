
import pandas as pd
import collections
import zipfile
import json

def get_key(val,listdata):
    for i, value in enumerate(listdata):
         if val == value:
            return i
    return "No data"

# raw data(zip)
file = '../data/raw/spotify_million_playlist_dataset.zip'
f_zip = zipfile.ZipFile(file)
l_names = f_zip.namelist()
l_names = [name for name in l_names if len(name)>20]
print('n_files:', len(l_names))
filename = l_names[0]
data = json.loads(f_zip.open(filename, 'r').read().decode())
print('keys:', data.keys())
print('keys_info:', data['info'])

# Playlist data
l_names_playlist = []
l_num_tracks = []
l_num_albums = []
l_rate_albumsByTracks = []
l_num_followers = []
l_num_durations = []
l_num_artists = []

for filename in tqdm(l_names):
    data = json.loads(f_zip.open(filename, 'r').read().decode())
    pdata = data['playlists']
    for p in pdata:
        name_playlist = p['name']
        num_tracks = p['num_tracks']
        num_albums = p['num_albums']
        num_followers = p['num_followers']
        num_durations = p['duration_ms']
        num_artists = p['num_artists']
        rate_albumsByTracks = round((num_albums/num_tracks)*100,2)
        l_names_playlist.append(name_playlist)
        l_num_tracks.append(num_tracks)
        l_num_albums.append(num_albums)
        l_num_followers.append(num_followers)
        l_num_durations.append(num_durations)
        l_num_artists.append(num_artists)
        l_rate_albumsByTracks.append(rate_albumsByTracks)

d_summary_playlist = {
    'names_playlist':l_names_playlist,
    'num_tracks':l_num_tracks,
    'num_albums':l_num_albums,
    'num_followers':l_num_followers,
    'num_durations':l_num_durations,
    'num_artists':l_num_artists,
    'rate_albumsByTracks':l_rate_albumsByTracks
}
with open('../data/processed/dict_summary_playlist.json', 'w') as f:
    json.dump(d_summary_playlist, f, indent=2)

# Track data
l_names_artist = []
l_names_track = []
l_names_albums = []
for filename in tqdm(l_names):
    data = json.loads(f_zip.open(filename, 'r').read().decode())
    pdata = data['playlists']
    for p in pdata:
        l_tracks = p['tracks']
        for track in l_tracks:
            name_artist = track['artist_name']
            name_track = track['track_name']
            name_album = track['album_name']
            l_names_artist.append(name_artist)
            l_names_track.append(name_track)
            l_names_albums.append(name_album)

d_summary_track = {
    'names_artist':l_names_artist,
    'names_track':l_names_track,
    'names_albums':l_names_albums,
}
## track info dictionary
with open('../data/processed/dict_summary_track.json', 'w') as f:
    json.dump(d_summary_track, f, indent=2)
## artist names of track info dictionary
d = {'names_artist':d_summary_track['names_artist']}
with open('../data/processed/dict_summary_track_artists.json', 'w') as f:
    json.dump(d, f, indent=2)
## track names of track info dictionary
d = {'names_track':d_summary_track['names_track']}
with open('../data/processed/dict_summary_track_tracks.json', 'w') as f:
    json.dump(d, f, indent=2)
## album names of track info dictionary
d = {'names_albums':d_summary_track['names_albums']}
with open('../data/processed/dict_summary_track_albums.json', 'w') as f:
    json.dump(d, f, indent=2)

df = pd.DataFrame(d_summary_playlist)
top10_artist = collections.Counter(d_summary_track['names_artist']).most_common()[0:10]
top10_track = collections.Counter(d_summary_track['names_track']).most_common()[0:10]
top10_album = collections.Counter(d_summary_track['names_albums']).most_common()[0:10]

## Top 10 tracks and artists
l_artistsOfTrack = []
for track in top10_track:
    t = track[0]
    i = get_key(t, d_summary_track['names_track'])
    l_artistsOfTrack.append(d_summary_track['names_artist'][i])
df_topTrack = pd.DataFrame({
    'top10_track':[t[0] for t in top10_track],
    'num_in_playlists':[t[1] for t in top10_track],
    'top10_track_artist':l_artistsOfTrack
})
df_topTrack.to_csv('../data/processed/df_topTrack.csv')

## Top 10 albums and artists
l_artistsOfAlbum = []
for album in top10_album:
    t = album[0]
    i = get_key(t, d_summary_track['names_albums'])
    l_artistsOfAlbum.append(d_summary_track['names_artist'][i])
df_topAlbum = pd.DataFrame({
    'top10_album':[t[0] for t in top10_album],
    'num_in_playlists':[t[1] for t in top10_album],
    'top10_album_artist':l_artistsOfAlbum,
})
df_topAlbum.to_csv('../data/processed/df_topAlbum.csv')

d_unique =
