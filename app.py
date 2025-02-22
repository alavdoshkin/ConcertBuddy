import gradio as gr
from gradio.themes import Soft
import os
from dotenv import load_dotenv
from transcript import transcribe_audio  # Import the transcription function
from metadata import info
import numpy as np
import requests
from scipy.io.wavfile import write
from groq import Groq
import json
from genius import get_song_info_from_lyrics

# Load environment variables from .env file
load_dotenv()
client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)

def song_history(message):
    # question = "Tell me the history or a fun fact of the song (in a single line!): " + message
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a professor of music at Berklee College of Music."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Please explain the historical and musical significance of " + message + ". Please also break down the instruments used in the song. Keep it just one line!",
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    return completion.choices[0].message.content

def analyze_song(mp3_file):
    # Call the transcription function and get the transcription
    # Pass the mp3 filename to transcript.py

    os.makedirs("out", exist_ok=True)
    write('test.wav', mp3_file[0], mp3_file[1])
    data = {
        'api_token': os.environ["AUDD_API"],
        'return': 'apple_music,spotify',
    }
    files = {
        'file': open('test.wav', 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    transcription = transcribe_audio('test.wav')
    print(result.json())
    print(transcription)
    if result.json()['result']['artist'] is not None:
        artist = result.json()['result']['artist']
        title = result.json()['result']['title']
        # genre = result.json()['result']['apple_music']['genreNames']
        try:
            genre_list = result.json()['result']['apple_music']['genreNames']
        except:
            genre_list = ['']
        genre = ", ".join(genre_list)
        try:
            image_url = result.json()['result']['spotify']['album']['images'][0]['url']
        except:
            image_url = ""
    else:
        image_url = ""
        genre = ""
        genius_response = get_song_info_from_lyrics(transcription)
        title = genius_response["title"]
        artist = genius_response["artist"]
    # else:
    song_data = json.loads(info(title, artist))
    if (genre == None):
        genre = song_data["genre"]
    # print(song_data)
    # Placeholder for song analysis logic
    instrumentation = str(song_data["instrumentation"])[1:-2].replace('\'', '')
    lyrics = transcription  # Use the transcription as lyrics
    tempo_key = song_data["tempo"] + ", " + song_data["key"]
    history = song_data["historical"]

    # instrumentation = "Sample Instrumentation"
    # lyrics = transcription  # Use the transcription as lyrics
    # tempo_key = "Sample Tempo/Key"
    # history = "History"
    # history = song_history(title)
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