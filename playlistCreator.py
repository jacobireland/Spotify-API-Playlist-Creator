!pip install requests
import requests
import numpy as np
import matplotlib.pyplot as plt
import json
from urllib.parse import urlencode



#Authenticate

# User credentials you get from registering a new application on the Spotify Developers dashboard
client_id = "<your_client_id>"
client_secret = "<your_client_secret>"
redirect_uri = '<your_redirect_uri>'

# OAuth endpoints given in the Spotify API documentation
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = [
    "user-read-email",
    "user-top-read",
    "playlist-modify-public",
    "playlist-modify-private"
]

from requests_oauthlib import OAuth2Session
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Spotify for authorization
authorization_url, state = spotify.authorization_url(authorization_base_url)
print('Please go here and authorize: ', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('\n\nPaste the full redirect URL here: ')

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(client_id, client_secret)

# Fetch the access token
token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)

user1_access_token = token['access_token']

print(token)

# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')

info = r.json()
user_id = info['id']


#send GET request for user's top artists
user_type = "artists"

endpoint = "https://api.spotify.com/v1/me/top/"

user_header =  {"Authorization": f"Bearer {user1_access_token}"}

final_url = f"{endpoint}{user_type}?limit=200"

r = requests.get(final_url, headers=user_header)


#create array of genres, based on top artists listened too
topTracks = r.json()
topGenres = []
topGenresAmt = []
y=0;
for t in topTracks['items']:
  equal = 0
  genre = t['genres']
  if y == 0:
    topGenres.append(genre[0].split().pop(-1))
    topGenresAmt.append(0)
    y = y+1

  else:
    for i in topGenres:
      if (len(genre) > 0):
        if i == genre[0].split().pop(-1):
          equal = 1;
    if equal == 0:
      if len(genre) > 0:
        topGenres.append(genre[0].split().pop(-1))
        topGenresAmt.append(0)


#create an array to keep track of commoness of each genre type
x = 0
for t in topGenres:
  for i in topTracks['items']:
    genre = i['genres']
    if len(genre) > 0:
      if t == genre[0].split().pop(-1):
        topGenresAmt[x] = topGenresAmt[x]+1
  x = x+1


print(topGenres)
print(topGenresAmt)


#edit "hop" genre name to be "hip hop" (for chart)
j=0
for i in topGenres:
  if i == 'hop':
    topGenres[j] = 'hip hop'
  j = j+1

#visualize top genres as a bar chart
plt.figure(figsize=(12, 6))
New_Colors = ['green','blue','purple','brown','teal']
plt.bar(topGenres, topGenresAmt, color=New_Colors)
plt.title('Top Genres', fontsize=14)
plt.xlabel('')
plt.ylabel('')
plt.gca().get_yaxis().set_visible(False)
plt.show()


#Genres
#get location of top 3 most listened genres in topGenres array

gen_loc1 = -1
gen_loc2 = -1
gen_loc3 = -1
for i in range(len(topGenresAmt)):
  if gen_loc3 < 0 | topGenresAmt[i] >= topGenresAmt[gen_loc3]:
    if gen_loc2 < 0 | topGenresAmt[i] >= topGenresAmt[gen_loc2]:
      if gen_loc1 < 0 | topGenresAmt[i] >= topGenresAmt[gen_loc1]:
        gen_loc3 = gen_loc2
        gen_loc2 = gen_loc1
        gen_loc1 = i
      else:
        gen_loc3 = gen_loc2
        gen_loc2 = i
    else:
      gen_loc3 = i



#Artists
#get Spotify IDs of top-2 most listened artists for each genre

#genre 1
gen1 = topGenres[gen_loc1]
genre1Artists = []
for t in topTracks['items']:
  artist = t['id']
  if len(t['genres']) > 0:
    genre = t['genres'][0].split().pop(-1)
    if genre == gen1.split().pop(-1):
      genre1Artists.append(artist)
    if len(genre1Artists) == 2:
      break

#genre 2
gen2 = topGenres[gen_loc2]
genre2Artists = []
for t in topTracks['items']:
  artist = t['id']
  if len(t['genres']) > 0:
    genre = t['genres'][0].split().pop(-1)
    if genre == gen2.split().pop(-1):
      genre2Artists.append(artist)
    if len(genre2Artists) == 2:
      break

#genre 3
gen3 = topGenres[gen_loc3]
genre3Artists = []
for t in topTracks['items']:
  artist = t['id']
  if len(t['genres']) > 0:
    genre = t['genres'][0].split().pop(-1)
    if genre == gen3.split().pop(-1):
      genre3Artists.append(artist)
    if len(genre3Artists) == 2:
      break

print(genre1Artists)
print(genre2Artists)
print(genre3Artists)


#Tracks
#get top-2 most listened tracks for each genre
#if a song in your top tracks is made by one of your top two artists (genre specific), it gets added

user_type = "tracks"

endpoint = "https://api.spotify.com/v1/me/top/"

user_header =  {"Authorization": f"Bearer {user1_access_token}"}

final_url = f"{endpoint}{user_type}?limit=200"

r = requests.get(final_url, headers=user_header)

tracks = r.json()


#genre 1 tracks
genre1Tracks = []
for t in tracks['items']:
  artist = t['artists']
  for a in artist:
    name = a['id']
    for i in genre1Artists:
      if name == i:
        song = t['id']
        genre1Tracks.append(song)
  if (len(genre1Tracks) == 2):
    break

#genre 2 tracks
genre2Tracks = []
for t in tracks['items']:
  artist = t['artists']
  for a in artist:
    name = a['id']
    for i in genre2Artists:
      if name == i:
        song = t['id']
        genre2Tracks.append(song)
  if (len(genre2Tracks) == 2):
    break

#genre 3 tracks
genre3Tracks = []
for t in tracks['items']:
  artist = t['artists']
  for a in artist:
    name = a['id']
    for i in genre3Artists:
      if name == i:
        song = t['id']
        genre3Tracks.append(song)
  if (len(genre3Tracks) == 2):
    break

#if no tracks found, that is okay, it means of your top two artists (per genre) none of your top tracks are by them

print(genre1Tracks)
print(genre2Tracks)
print(genre3Tracks)


#get recommended songs for each of top 3 genres, using users top artists (genre-specific), their top tracks, and selected genre

endpoint = "https://api.spotify.com/v1/recommendations?"
header =  {"Authorization": f"Bearer {user1_access_token}"}

#genre 1 recommendations
genre1Recs = []
data = urlencode({
    "limit": "50",
    "seed_artists": f"{','.join(genre1Artists)}",
    "seed_genres": f"{topGenres[gen_loc1]}",
    "seed_tracks": f"{','.join(genre1Tracks)}"
})
url = f"{endpoint}{data}"
r = requests.get(url, headers=header)
recs = r.json()
for r in recs['tracks']:
  song_id = (r['uri'])
  genre1Recs.append(song_id)

#genre 2 recommendations
genre2Recs = []
data = urlencode({
    "limit": "50",
    "seed_artists": f"{','.join(genre2Artists)}",
    "seed_genres": f"{topGenres[gen_loc2]}",
    "seed_tracks": f"{','.join(genre2Tracks)}"
})
url = f"{endpoint}{data}"
r = requests.get(url, headers=header)
recs = r.json()
for r in recs['tracks']:
  song_id = (r['uri'])
  genre2Recs.append(song_id)

#genre 2 recommendations
genre3Recs = []
data = urlencode({
    "limit": "50",
    "seed_artists": f"{','.join(genre3Artists)}",
    "seed_genres": f"{topGenres[gen_loc3]}",
    "seed_tracks": f"{','.join(genre3Tracks)}"
})
url = f"{endpoint}{data}"
r = requests.get(url, headers=header)
recs = r.json()
for r in recs['tracks']:
  song_id = (r['uri'])
  genre3Recs.append(song_id)

print(genre1Recs)
print(genre2Recs)
print(genre3Recs)


#create playlist for each genre, and add songs

url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

header = {
    "Authorization": f"Bearer {user1_access_token}"
}



#genre 1

#create playlist
data = {
    "name": f"Recommended {topGenres[gen_loc1]} Playlist",
    "description": f"Playlist of recommened {topGenres[gen_loc1]} songs just for you!",
    "public": "false"
}
r = requests.post(url, json=data, headers=header)
res = r.json()
gen1Playlist = res['id']

#add songs
data1 = urlencode({
    "uris": ','.join(genre1Recs),
    "position": 0
})
url1 = f"https://api.spotify.com/v1/playlists/{gen1Playlist}/tracks?{data1}"
complete = 0
while complete == 0:  #check if request succeeeded, if not, resend until it does (sometimes the API does not add the songs to the playlist)
  r1 = requests.post(url1, json=data1, headers=header)
  if (r1.status_code == 200) | (r1.status_code == 201):
    complete = 1


#genre 2
data = {
    "name": f"Recommended {topGenres[gen_loc2]} Playlist",
    "description": f"Playlist of recommened {topGenres[gen_loc2]} songs just for you!",
    "public": "false"
}
r = requests.post(url, json=data, headers=header)
res = r.json()
gen2Playlist = res['id']

data2 = urlencode({
    "uris": ','.join(genre2Recs),
    "position": 0
})
url2 = f"https://api.spotify.com/v1/playlists/{gen2Playlist}/tracks?{data2}"
complete = 0
while complete == 0:
  r2 = requests.post(url2, json=data2, headers=header)
  if (r2.status_code == 200) | (r2.status_code == 201):
    complete = 1


#genre 3
data = {
    "name": f"Recommended {topGenres[gen_loc3]} Playlist",
    "description": f"Playlist of recommened {topGenres[gen_loc3]} songs just for you!",
    "public": "false"
}
r = requests.post(url, json=data, headers=header)
res = r.json()
gen3Playlist = res['id']

data3 = urlencode({
    "uris": ','.join(genre3Recs),
    "position": 0
})
url3 = f"https://api.spotify.com/v1/playlists/{gen3Playlist}/tracks?{data3}"
complete = 0
while complete == 0:
  r3 = requests.post(url3, json=data3, headers=header)
  if (r3.status_code == 200) | (r3.status_code == 201):
    complete = 1

