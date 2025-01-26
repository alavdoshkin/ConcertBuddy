import gradio as gr
from gradio.themes import Soft
import os
from dotenv import load_dotenv
from transcript import transcribe_audio  # Import the transcription function

# Load environment variables from .env file
load_dotenv()

def analyze_song(mp3_file):
    # Call the transcription function and get the transcription
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
    title="Concert Buddy 😄🎵🪩"  # Apply custom CSS for background image
)

demo.launch()
