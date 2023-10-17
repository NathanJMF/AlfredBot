FROM python:3.8

# Install system dependencies
#RUN apt-get update && apt-get install -y ffmpeg build-essential
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Set the working directory
WORKDIR /app

# Install dependencies

# Copy the rest of the code
COPY . .

# Run your bot
CMD ["python", "main.py"]
