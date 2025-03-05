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

def shuffle_playlist(playlist_url):
    """
    Shuffles the order of songs in the given playlist without deleting or re-adding them.
    """
    # Extract the playlist ID
    playlist_id = extract_playlist_id(playlist_url)

    # Fetch all tracks in the playlist
    print(f"Fetching tracks from playlist ID: {playlist_id}")
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    if not tracks:
        print("The playlist is empty or invalid.")
        return

    # Generate a shuffled order of indexes
    track_uris = [item['track']['uri'] for item in tracks if item['track']]
    indexes = list(range(len(track_uris)))
    random.shuffle(indexes)

    # Apply the new order using the reorder API
    print("Shuffling playlist order...")
    for i, new_position in enumerate(indexes):
        if i != new_position:
            sp.playlist_reorder_items(playlist_id, range_start=i, insert_before=new_position)

    print("Playlist order shuffled successfully!")

# Main script
try:
    playlist_url = input("Enter the Spotify playlist URL to shuffle: ").strip()

    # Validate URL
    if "spotify.com/playlist/" not in playlist_url:
        print("Invalid Spotify playlist URL. Please try again.")
    else:
        shuffle_playlist(playlist_url)
except Exception as e:
    print(f"An error occurred: {e}")
