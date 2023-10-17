FROM python:3.8

# Install system dependencies
#RUN apt-get update && apt-get install -y ffmpeg build-essential


# Set the working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system --deploy

# Copy the rest of the code
COPY . .

# Run your bot
CMD ["python", "brain_api.py"]
