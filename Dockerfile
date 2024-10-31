# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY main.py .

# Set environment variables (optional: replace with Docker secrets for production)
ENV DISCORD_BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
ENV AZURE_API_KEY="YOUR_AZURE_API_KEY"
ENV AZURE_ENDPOINT="YOUR_AZURE_ENDPOINT"
ENV DEPLOYMENT_NAME="YOUR_DEPLOYMENT_NAME"

# Run the bot
CMD ["python", "main.py"]
