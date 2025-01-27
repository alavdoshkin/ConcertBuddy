import gradio as gr
import requests
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
import json

def info(song_name, artist):
    if "GITHUB_TOKEN" not in os.environ:
        print("GITHUB_TOKEN environment variable is missing.")
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
    )
    response = client.complete(
        messages=[
            SystemMessage(content="You are a professor of music at Berklee College of Music. Your students are asking you questions about the historical context and musical significance of songs they listened to. Please structure the output as a json with the format {'historical': historical significance of song, 'musical': special musical characteristics of the song, 'instrumentation': [instrument 1, instrument 2, ...], 'tempo': tempo of the song, 'key': key of the song}, 'genre': genre of the song"),
            UserMessage(content="Please explain the historical and musical significance of 'Viva la Vida' by Coldplay. Please also break down the instruments used in the song."),
        ],
        model="Llama-3.3-70B-Instruct",
        temperature=0.8,
        max_tokens=2048,
        top_p=0.1
    )
    print(response.choices[0])
    return response.choices[0].message.content