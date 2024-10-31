import os
import discord
import requests

from dotenv import load_dotenv

load_dotenv()


bot_token = os.getenv("DISCORD_BOT_TOKEN")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
azure_api_key = os.getenv("AZURE_API_KEY")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

headers = {"Ocp-Apim-Subscription-Key": azure_api_key, "Content-Type": "application/json"}

# Initialize Discord client
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        query = message.content[5:]

        # Request to Azure Cognitive Services
        payload = {
            "prompt": query,
            "max_tokens": 100
        }
        response = requests.post(
            f"{azure_endpoint}/openai/deployments/{deployment_name}/completions?api-version=2023-05-15",
            headers=headers, json=payload
        )

        # Get response text from Azure's response
        if response.status_code == 200:
            try:
                answer = response.json()["choices"][0]["text"].strip()
                await message.channel.send(answer)
            except (KeyError, IndexError):
                await message.channel.send("Could not retrieve a valid answer. Please try again.")
        else:
            await message.channel.send(f"Error {response.status_code}: {response.text}")

client.run(bot_token)
