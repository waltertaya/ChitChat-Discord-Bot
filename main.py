import os
import discord
import requests

from dotenv import load_dotenv

load_dotenv()


bot_token = os.getenv("DISCORD_BOT_TOKEN")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
azure_api_key = os.getenv("AZURE_API_KEY")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")

headers = { "api-key": azure_api_key, "Content-Type": "application/json"}

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

client = discord.Client(intents=intents)
# client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        query = message.content.replace(f"<@{client.user.id}>", "").strip()

        if query:
            # payload = {
            #     "prompt": query,
            #     "max_tokens": 100
            # }
            payload = {
                "messages": [
                    {"role": "user", "content": query}
                ],
                "max_tokens": 500
            }
            response = requests.post(
                # f"{azure_endpoint}/openai/deployments/{deployment_name}/completions?api-version=2023-05-15",
                f"{azure_endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version=2024-02-15-preview",
                headers=headers, json=payload
            )

            # Get response text from Azure's response
            if response.status_code == 200:
                try:
                    answer = response.json()["choices"][0]["message"]["content"]

                    # print(f"Question: {query}")
                    # print(f"Answer: {answer}")

                    await message.channel.send(f"<@{message.author.id}> {answer}")
                except (KeyError, IndexError):
                    await message.channel.send(f"<@{message.author.id}> Could not retrieve a valid answer. Please try again.")
            else:
                await message.channel.send(f"<@{message.author.id}> Error {response.status_code}: {response.text}")
        else:
            await message.channel.send(f"<@{message.author.id}> Please ask me something!")



client.run(bot_token)
