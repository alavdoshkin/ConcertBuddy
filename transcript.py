import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def transcribe_audio(filename):
    """Transcribe the audio file and return the transcription text."""
    # Open the audio file
    with open(filename, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),  # Required audio file
            model="whisper-large-v3",  # Required model to use for transcription
            prompt="",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        
        # Return the transcription text
        return transcription.text  # Access the 'text' property

# Example usage (you can remove this part later)
if __name__ == "__main__":
    filename = "/Users/sydneydu/Projects/ConcertBuddy/blankspacetrimmed.mp3"
    transcription_text = transcribe_audio(filename)
    print(transcription_text)  # Print the extracted text for testing
