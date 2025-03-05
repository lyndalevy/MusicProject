import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random  # For shuffling

# Spotify API credentials
SPOTIPY_CLIENT_ID = '0314a2282eb3470d9ab666ac305108a3'
SPOTIPY_CLIENT_SECRET = 'a74e9a59716e45628c08a706614c671d'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='playlist-modify-public playlist-read-private'
))

def extract_playlist_id(playlist_url):
    """
    Extracts the playlist ID from a full Spotify playlist URL.
    """
    return playlist_url.split('/')[-1].split('?')[0]

def get_playlist_tracks(playlist_id):
    """
    Fetches all track URIs from the specified playlist.
    """
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [track['track']['uri'] for track in tracks if track['track']]

def zipper_merge_playlists(playlist1_url, playlist2_url, new_playlist_name):
    """
    Combines two playlists in a shuffled zipper pattern and creates a new playlist.
    """
    # Extract playlist IDs
    playlist1_id = extract_playlist_id(playlist1_url)
    playlist2_id = extract_playlist_id(playlist2_url)

    # Fetch tracks from both playlists
    playlist1_tracks = get_playlist_tracks(playlist1_id)
    playlist2_tracks = get_playlist_tracks(playlist2_id)

    # Shuffle the tracks
    random.shuffle(playlist1_tracks)
    random.shuffle(playlist2_tracks)

    # Perform zipper merge
    max_len = max(len(playlist1_tracks), len(playlist2_tracks))
    combined_tracks = []
    for i in range(max_len):
        if i < len(playlist1_tracks):
            combined_tracks.append(playlist1_tracks[i])
        if i < len(playlist2_tracks):
            combined_tracks.append(playlist2_tracks[i])

    # Create a new playlist
    user_id = sp.me()['id']
    new_playlist = sp.user_playlist_create(user_id, new_playlist_name)
    new_playlist_id = new_playlist['id']

    # Add tracks to the new playlist in batches
    for i in range(0, len(combined_tracks), 100):
        sp.playlist_add_items(new_playlist_id, combined_tracks[i:i + 100])

    print(f"New playlist created: {new_playlist['external_urls']['spotify']}")

playlist1_url = input("Link of playlist 1: ")
playlist2_url = input("Link of playlist 2: ")
zipper_merge_playlists(playlist1_url, playlist2_url, "Zipper Merged Playlist")

