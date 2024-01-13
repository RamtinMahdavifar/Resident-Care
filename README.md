# Resident-Care

## Project Files

Access the project files through this [Google Drive link](https://drive.google.com/drive/folders/10UkNdUlFrZ7Nbwz7XC6iyy3upMq62CyO?usp=sharing).

## Setup Instructions

### Virtual Environment Setup

1. Set up your Python virtual environment.
2. Install the required packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

### Vosk Setup (Local Voice Recognition)

1. Download and extract the `vosk-model-en-us-0.42-gigaspeech.zip` file from [Vosk Models](https://alphacephei.com/vosk/models).
2. Move the extracted folder to the root folder of the Python project.

### Environment Configuration

Create a `.env` file in the project root with the following content:

```plaintext
# Open API
OPENAI_API_KEY='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'

# Twilio
ACCOUNT_SID='AC5c1208d0ab1d092a1bfc3e8c151fd265'
AUTH_TOKEN='ef08d29b88b0d9af6caf15333ebdc13d'
