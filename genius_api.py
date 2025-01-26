import requests

def get_song_info_from_lyrics(lyrics, genius_api_token):
    """
    Fetch song information from Genius API using lyrics.

    Args:
        lyrics (str): A snippet of the song lyrics.
        genius_api_token (str): Your Genius API token.

    Returns:
        dict: Information about the song (e.g., title, artist, URL) or None if not found.
    """
    base_url = "https://api.genius.com/search"
    headers = {
        "Authorization": f"Bearer {genius_api_token}"
    }
    
    params = {
        "q": lyrics
    }

    try:
        # Make the API call
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        data = response.json()

        # Check if there are hits in the response
        if data.get("response") and data["response"].get("hits"):
            hits = data["response"]["hits"]
            if hits:
                # Return the first song match's details
                song = hits[0]["result"]
                print(song)
                return {
                    "title": song["title"],
                    "artist": song["primary_artist"]["name"],
                    "url": song["url"]
                }
        return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API call: {e}")
        return None

# Example usage
# Replace "your_genius_api_token" with your actual Genius API token.
# lyrics_snippet = "And I'm here to remind you of the mess you left when you went away"
# api_token = "stPiAOUb80jj_AngLAAioCwSqcUkuVLqMs3cDNdpG2QF1L9UAygAkevXWFcMurwZ"
# song_info = get_song_info_from_lyrics(lyrics_snippet, api_token)
# print(song_info)
