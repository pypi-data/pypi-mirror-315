import spotipy
from spotipy.oauth2 import SpotifyOAuth

class ApiHandler:
    def __init__(self, client_id, client_secret, redirect_uri='http://localhost:8888/callback', scope='playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative'):
        self.identity = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope   
        ))
    
    def get_playlist_id(self, playlist_url):
        if str(playlist_url).__contains__('playlist/'):
            splitted = str(playlist_url).split('playlist/')
            
            if len(splitted) > 0 and splitted[1].__contains__('?'):
                return splitted[1].split('?')[0]
            else:
                return None
        else:
            return None
        
    def get_album_id(self, playlist_url):
        if str(playlist_url).__contains__('album/'):
            splitted = str(playlist_url).split('album/')
            
            if len(splitted) > 0 and splitted[1].__contains__('?'):
                return splitted[1].split('?')[0]
            else:
                return None
        else:
            return None
        
    def get_track_id(self, playlist_url):
        if str(playlist_url).__contains__('track/'):
            splitted = str(playlist_url).split('track/')
            
            if len(splitted) > 0 and splitted[1].__contains__('?'):
                return splitted[1].split('?')[0]
            else:
                return None
        else:
            return None
    
    def get_playlist_tracks(self, playlist_id):
        results = self.identity.playlist_items(playlist_id=playlist_id, limit=None)
        tracks = results['items']
        
        uri_list = []
        for track in tracks:
            if 'track' in track.keys():
                if 'uri' in track['track'].keys():
                    uri_list.append(track['track']['uri'])
        
        return uri_list
    
    def get_album_tracks(self, album_id):
        results = self.identity.album_tracks(album_id=album_id, limit=None)
        tracks = results['items']
        
        uri_list = []
        for track in tracks:
            if 'uri' in track.keys():
                uri_list.append(track['uri'])
        
        return uri_list

    
    def create_playlist(self, tracks, playlist_name='Shuffled!', description='created by shuffleify', public=True):
        playlist = self.identity.user_playlist_create(
            user=self.identity.current_user()['id'],
            name=playlist_name,
            public=public,
            description=description
        )
        
        self.identity.playlist_add_items(
            playlist_id=playlist['id'],
            items=tracks
        )