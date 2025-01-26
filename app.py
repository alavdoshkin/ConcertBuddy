import gradio as gr
from gradio.themes import Soft
import os
# from dotenv import load_dotenv
from transcript import transcribe_audio  # Import the transcription function
from genius_api import get_song_info_from_lyrics
from metadata import info
import json
import numpy as np
import requests
from scipy.io.wavfile import write
from groq import Groq

# Load environment variables from .env file
# load_dotenv()

client = Groq(
    api_key=os.getenv("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"),
)

# def song_history(message):
#     question = "Tell me the history or a fun fact of the song (in a single line!): " + message
#     completion = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[question],
#         temperature=1,
#         max_completion_tokens=1024,
#         top_p=1,
#         stream=True,
#         stop=None,
#     )
#     for chunk in completion:
#         return chunk.choices[0].delta.content or ""

def analyze_song(mp3_file):
    # Call the transcription function and get the transcription
    os.makedirs("out", exist_ok=True)
    write('test.wav', mp3_file[0], mp3_file[1])
    data = {
        'api_token': '171afdabea68ffcdbd7f102b8611ac63',
        'return': 'apple_music,spotify',
    }
    files = {
        'file': open('test.wav', 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    transcription = transcribe_audio('test.wav')
    if result is not None:
        artist = result.json()['result']['artist']
        title = result.json()['result']['title']
        # genre = result.json()['result']['apple_music']['genreNames']
        genre_list = result.json()['result']['apple_music']['genreNames']
        genre = ", ".join(genre_list)
        image_url = result.json()['result']['spotify']['album']['images'][0]['url']
    else:
        image_url = None
        genre = None
        genius_response = get_song_info_from_lyrics(transcription)
        title = genius_response["title"]
        artist = genius_response["artist"]
    song_data = json.loads(info(title, artist))
    if (genre == None):
        genre = song_data["genre"]
    print(song_data)
    # Placeholder for song analysis logic
    instrumentation = str(song_data["instrumentation"])[1:-2].replace('\'', '')
    lyrics = transcription  # Use the transcription as lyrics
    tempo_key = song_data["tempo"] + ", " + song_data["key"]
    history = song_data["historical"]
    
    return title, artist, genre, instrumentation, lyrics, tempo_key, history, image_url  # Return the mp3 file for replay


# Custom CSS to set a fun musical theme image as background
css = """
body {
    background-image: url('https://example.com/path/to/your/musical-theme-image.jpg'); /* Replace with your image URL */
    background-size: cover; /* Cover the entire background */
    background-repeat: no-repeat; /* Prevent repeating the image */
    background-position: center; /* Center the image */
}
"""

demo = gr.Interface(
    fn=analyze_song,
    inputs=gr.Audio(label="Record Audio", sources=["upload", "microphone"],
    waveform_options=gr.WaveformOptions(
        waveform_color="#01C6FF",
        waveform_progress_color="#0066B4",
        skip_length=2,
        show_controls=False,
        ),
    ),  # Record audio in MP3 format
    
    outputs=[
        gr.Textbox(label="Title"),
        gr.Textbox(label="Artist"),
        gr.Textbox(label="Genre"),
        gr.Textbox(label="Instrumentation"),
        gr.Textbox(label="Lyrics"),
        gr.Textbox(label="Tempo/Key"),
        gr.Textbox(label="History"),
        # gr.Audio(label="Replay Recorded Audio"),  # Add an output for replaying the recorded audio
        gr.Image(label="Cover")  # Gives the Cover image
    ],
    theme=Soft(),  # Apply the Soft theme
    title="Concert Buddy 😄🎵🪩"  # Apply custom CSS for background image
)

demo.launch()
