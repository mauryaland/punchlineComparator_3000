# coding: utf-8

# Import modules
import os
import lyricsgenius as genius
import pandas as pd

def get_artist_lyrics(artist, client_access_token, keep_data=True):
    
    """
    
    This function takes as input an artist name and will request the Genius 
    API obtained thanks to lyricsgenius package and returns a pandas dataframe
    
    INPUTS:
        1) artist: artist name
        2) client_access_token: client access token from Genius API
        3) keep_data: if True, keep the json file on disk
        
    OUTPUTS:
        Format pandas dataframe with all songs from the artist
        
    """
    # Get the data
    api = genius.Genius(client_access_token)
    artist_guy = api.search_artist(artist, max_songs=3)
    data = artist_guy.save_lyrics()
         
    # Remove json file or not
    if keep_data != True:
        os.remove('Lyrics_' + artist + '.json')
    
    # Parse the json
    infos = []
    for song in range(len(data['songs'])):
        infos.append(list(data['songs'][song].values()))
        
    # Save as pandas Dataframe and do some cleaning
    df = pd.DataFrame(infos, columns=list(data['songs'][0].keys()))
    df.drop(['image', 'raw'], axis=1, inplace=True)
    for column in df.columns:
        df[column] = df[column].str.replace('\n', ' ')
        df[column] = df[column].str.replace(r"\[[^\[\]]*\]", ' ')
        
    
    return df