import gradio as gr
from gradio.themes import Soft
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def analyze_song(mp3_file):
    # Placeholder for song analysis logic
    # Here you would implement the logic to extract song information
    title = "Sample Title"
    artist = "Sample Artist"
    genre = "Sample Genre"
    instrumentation = "Sample Instrumentation"
    lyrics = "Sample Lyrics"
    tempo_key = "Sample Tempo/Key"
    
    return title, artist, genre, instrumentation, lyrics, tempo_key

# Custom CSS for bright and colorful theme
css = """
#component-0 {
    background-color: #ffcc00; /* Bright yellow for the button */
    border-radius: 50%; /* Round button */
    padding: 20px;
    font-size: 20px;
    color: white;
    text-align: center;
}

#component-0:hover {
    background-color: #ff9900; /* Darker yellow on hover */
}

.output-textbox {
    background-color: #e0f7fa; /* Light cyan for output boxes */
    border: 2px solid #00796b; /* Dark teal border */
    color: #004d40; /* Darker text color */
    font-weight: bold;
}

.output-textbox:hover {
    border-color: #004d40; /* Darker border on hover */
}
"""

demo = gr.Interface(
    fn=analyze_song,
    inputs=gr.Audio(label="Upload MP3"),
    outputs=[
        gr.Textbox(label="Title"),
        gr.Textbox(label="Artist"),
        gr.Textbox(label="Genre"),
        gr.Textbox(label="Instrumentation"),
        gr.Textbox(label="Lyrics"),
        gr.Textbox(label="Tempo/Key"),
    ],
    theme=Soft()  # Apply custom CSS
)

demo.launch()
