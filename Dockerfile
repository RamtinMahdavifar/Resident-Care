# Use an official Python runtime as a parent image
FROM python:3.9.1-buster

# Set the working directory in the container
WORKDIR /usr/src/app
# Install system dependencies including g++ and curl (for downloading rustup)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libstdc++6 \
    python3-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    alsa-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Install Rust compiler using rustup
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
#
## Make sure cargo, Rust's package manager, is in the PATH
#ENV PATH="/root/.cargo/bin:${PATH}"

COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME CareBot

# Run streamlit when the container launches
CMD ["streamlit", "run", "main.py"]
