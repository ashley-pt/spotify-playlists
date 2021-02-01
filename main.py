import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import csv

scope="playlist-read-collaborative playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret= cred.client_SECRET, redirect_uri=cred.redirect_url, scope=scope))

results = sp.current_user_playlists()

items = results.get('items') # list of items from each dictionary entry

playlists = []

csv_columns = ['PLAYLIST', 'ALBUM', 'ARTIST', 'NAME']

def write_playlist_tracks(tracks):
    trackitems = tracks.get('items')
    for trackitem in trackitems:
        track_album = trackitem.get('track').get('album').get('name')
        track_artist = trackitem.get('track').get('artists')[0].get('name')
        track_name = trackitem.get('track').get('name')
        playlists.append({'PLAYLIST': playlist_name, 'ALBUM': track_album, 'ARTIST': track_artist, 'NAME': track_name})

for item in items:
    playlist_name = item.get('name')
    playlist_id = item.get('id')

    # get the playlist tracks
    tracks = sp.playlist_tracks(playlist_id)
    tracktotal = tracks.get('total')

    if tracktotal > 100:
        offset = 0
        while tracktotal > 0:
            tracks = sp.playlist_tracks(playlist_id, offset=offset)
            write_playlist_tracks(tracks)
            tracktotal -= 100
            offset += 100

    else:
        write_playlist_tracks(tracks)

try:
    with open("playlists.csv", 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for playlist in playlists:
            writer.writerow(playlist)
except IOError:
    print ("I/O error")

#each item in the list is a dictionary
# so for each item in items, 
# name = item.get('name') and 
# playlist_id = item.get('id')
# tracks = sp.playlist_tracks(playlist_id)
# tracksitems = tracks.get('items') which is a list so for each tracksitem in the list
# trackdetails = trackitem.get('track') which gives a dictionary
# track_album =  trackdetails.get('album').get('name')
# track_artist = trackdetails.get('album').get('artists')[0].get('name')
# track_name =  trackdetails.get('name')