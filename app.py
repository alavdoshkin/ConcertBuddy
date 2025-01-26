import gradio as gr
from gradio.themes import Soft
import os
from dotenv import load_dotenv
from transcript import transcribe_audio  # Import the transcription function
from genius_api import get_song_info_from_lyrics
from metadata import greet
# Load environment variables from .env file
load_dotenv()

def analyze_song(mp3_file):
    # Call the transcription funçction and get the transcription
    transcription = transcribe_audio(mp3_file)  # Pass the mp3 filename to transcript.py

    # Placeholder for song analysis logic
    title = "Sample Title"
    artist = "Sample Artist"
    genre = "Sample Genre"
    instrumentation = "Sample Instrumentation"
    lyrics = transcription  # Use the transcription as lyrics
    tempo_key = "Sample Tempo/Key"
    
    return title, artist, genre, instrumentation, lyrics, tempo_key, mp3_file  # Return the mp3 file for replay

# Custom CSS to set a fun musical theme image as background
css = """
body {
    background-image: url('https://png.pngtree.com/thumb_back/fh260/background/20210918/pngtree-note-music-logo-watercolor-background-image_903000.png'); /* Replace with your image URL */
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
