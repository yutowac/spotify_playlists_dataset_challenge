
import pandas as pd
import collections
import zipfile
import json

def get_key(val,listdata):
    for i, value in enumerate(listdata):
         if val == value:
            return i
    return "No data"

def main():
    # raw data(zip)
    file = '../data/raw/superlight_spotify_million_playlist_dataset.zip'
    f_zip = zipfile.ZipFile(file)
    l_names = f_zip.namelist()
    l_names = [name for name in l_names if len(name)>20]
    print('n_files:', len(l_names))
    filename = l_names[0]
    data = json.loads(f_zip.open(filename, 'r').read().decode())
    print('keys:', data.keys())
    print('keys_info:', data['info'])

    # Playlist data
    print('processing playlist data')
    l_names_playlist = []
    l_num_tracks = []
    l_num_albums = []
    l_rate_albumsByTracks = []
    l_num_followers = []
    l_num_durations = []
    l_num_artists = []
    for filename in l_names:
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

    # Track data
    print('processing track data')
    l_names_artist = []
    l_names_track = []
    l_names_albums = []
    for filename in l_names:
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

    d_playlist_and_tracks={}
    for pdata in data['playlists']:
        playlist = pdata['name']
        l_tracks = []
        for track in pdata['tracks']:
            l_tracks.append(track['track_name'])
        d_playlist_and_tracks.update({playlist:l_tracks})

    l_unique_tracks = list(set(d_summary_track['names_track']))
    d_track_and_playlists={}
    for u_track in l_unique_tracks:
        l_playlist_and_pos = []
        for pdata in data['playlists']:
            playlist = pdata['name']
            tracks = pdata['tracks']
            for track in tracks:
                if track['track_name']==u_track:
                    pos = track['pos']
                    l_playlist_and_pos.append((playlist, pos))
                    break
                else:
                    pass
        d_track_and_playlists.update({u_track:l_playlist_and_pos})

    ## playlist dictionary
    with open('../data/processed/dict_summary_playlist.json', 'w') as f:
        json.dump(d_summary_playlist, f, indent=2)
    ## playlist and tracks dictionary
    with open('../data/processed/dict_playlist_and_tracks.json', 'w') as f:
        json.dump(d_playlist_and_tracks, f, indent=2)
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
    ## track and playlists dictionary
    with open('../data/processed/dict_summary_track_playlists.json', 'w') as f:
        json.dump(d_track_and_playlists, f, indent=2)
    print('processed dictionary')

    print('make top tracks')
    # df = pd.DataFrame(d_summary_playlist)
    # top10_artist = collections.Counter(d_summary_track['names_artist']).most_common()[0:10]
    top10_track = collections.Counter(d_summary_track['names_track']).most_common()[0:10]
    top10_album = collections.Counter(d_summary_track['names_albums']).most_common()[0:10]
    top50_track = collections.Counter(d_summary_track['names_track']).most_common()[0:50]

    ## Top 10 tracks and artists
    l_artistsOfTrack = []
    for track in top10_track:
        t = track[0]
        i = get_key(t, d_summary_track['names_track'])
        l_artistsOfTrack.append(d_summary_track['names_artist'][i])
    df_top10Track = pd.DataFrame({
        'top10_track':[t[0] for t in top10_track],
        'num_in_playlists':[t[1] for t in top10_track],
        'top10_track_artist':l_artistsOfTrack
    })
    df_top10Track.to_csv('../data/processed/df_top10Track.csv')
    ## Top 50 tracks and artists
    l_artistsOfTrack = []
    for track in top50_track:
        t = track[0]
        i = get_key(t, d_summary_track['names_track'])
        l_artistsOfTrack.append(d_summary_track['names_artist'][i])
    df_top50Track = pd.DataFrame({
        'top50_track':[t[0] for t in top50_track],
        'num_in_playlists':[t[1] for t in top50_track],
        'top50_track_artist':l_artistsOfTrack
    })
    df_top50Track.to_csv('../data/processed/df_top50Track.csv')

    ## Top 10 albums and artists
    l_artistsOfAlbum = []
    for album in top10_album:
        t = album[0]
        i = get_key(t, d_summary_track['names_albums'])
        l_artistsOfAlbum.append(d_summary_track['names_artist'][i])
    df_top10Album = pd.DataFrame({
        'top10_album':[t[0] for t in top10_album],
        'num_in_playlists':[t[1] for t in top10_album],
        'top10_album_artist':l_artistsOfAlbum,
    })
    df_top10Album.to_csv('../data/processed/df_top10Album.csv')
    print('processed done')
if __name__ == '__main__':
    main()


