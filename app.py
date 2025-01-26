import gradio as gr
from gradio.themes import Soft
import os
from dotenv import load_dotenv
from transcript import transcribe_audio  # Import the transcription function
from genius_api import get_song_info_from_lyrics
from metadata import info
import json

# Load environment variables from .env file
load_dotenv()

def analyze_song(mp3_file):
    # Call the transcription function and get the transcription
    transcription = transcribe_audio(mp3_file)  # Pass the mp3 filename to transcript.py
    print(transcription)
    genius_response = get_song_info_from_lyrics(transcription)
    print(genius_response)
    print(genius_response["title"])
    print(genius_response["artist"])
    song_data = json.loads(info(genius_response["title"], genius_response["artist"]))
    print(song_data)
    # Placeholder for song analysis logic
    title = genius_response["title"]
    artist = genius_response["artist"]
    genre = song_data["genre"]
    instrumentation = str(song_data["instrumentation"])[1:-2].replace('\'', '')
    lyrics = transcription  # Use the transcription as lyrics
    tempo_key = song_data["tempo"] + ", " + song_data["key"]
    
    return title, artist, genre, instrumentation, lyrics, tempo_key, mp3_file  # Return the mp3 file for replay

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
    inputs=gr.Audio(label="Record Audio", type="filepath", format="mp3"),  # Record audio in MP3 format
    outputs=[
        gr.Textbox(label="Title"),
        gr.Textbox(label="Artist"),
        gr.Textbox(label="Genre"),
        gr.Textbox(label="Instrumentation"),
        gr.Textbox(label="Lyrics"),
        gr.Textbox(label="Tempo/Key"),
        gr.Audio(label="Replay Recorded Audio")  # Add an output for replaying the recorded audio
    ],
    theme=Soft(),  # Apply the Soft theme
    css=css  # Apply custom CSS for background image
)

demo.launch()
