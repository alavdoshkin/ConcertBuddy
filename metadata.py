import gradio as gr
import requests
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
import json

def info(song_name, artist):
    # data = {
    #     'api_token': AUDD_TOKEN,
    #     'return': 'apple_music,spotify',
    # }
    # files = {
    #     'file': open(path_to_file, 'rb'),
    # }
    # result = requests.post('https://api.audd.io/', data=data, files=files)
    # return result.text

    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
    # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    if "GITHUB_TOKEN" not in os.environ:
        print("GITHUB_TOKEN environment variable is missing.")
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
    )

    response = client.complete(
        messages=[
            SystemMessage(content="You are a professor of music at Berkeley school of music. Your students are asking you questions about the historical context and musical significance of songs they listened to. Please structure the output as a json with the format {\"historical\": \"historical significance of song\", \"musical\": \"special musical characteristics of the song\", \"instrumentation\": \"[instrument 1, instrument 2, ...]\", \"tempo\": \"tempo of the song\", \"key\": \"key of the song\"}, 'genre': genre of the song}. Please do not add any text before or after this format"),
            UserMessage(content="Please explain the historical and musical significance of " + song_name + " by " + artist + ". Please also break down the instruments used in the song."),
        ],
        model="Llama-3.3-70B-Instruct",
        temperature=0.8,
        max_tokens=2048,
        top_p=0.1
    )

    print(response.choices[0])

    return response.choices[0].message.content


# demo = gr.Interface(
#     fn=greet,
#     inputs=["text"],
#     outputs=["text"],
# )

# demo.launch()
