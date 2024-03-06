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

1. Download and extract a vosk model from [Vosk Models](https://alphacephei.com/vosk/models). \
   It is recommended to use `vosk-model-en-us-0.42-gigaspeech.zip` for the highest accuracy.
2. Move the extracted folder to the root folder of the Python project.

### Environment Configuration

Create a `.env` file in the project root with the following content:

```plaintext
# Open API
OPENAI_API_KEY='Your Open API Key'

# Twilio
ACCOUNT_SID='Your ACCOUNT_SID'
AUTH_TOKEN='Your AUTH_TOKEN'
TWILIO_PHONE_NUMBER='Twilio's phone number assigned to your account'
CAREGIVER_PHONE_NUMBER='The phone number of the caregiver who will receive alerts'

Ensure that the phone numbers are in full international format, starting with 
the '+' sign followed by the country code and the full phone number. This number must
be verified in your Twilio account to recieve messages.

For example:

In Canada, the country code is +1, so the format will be +1XXXXXXXXXX.
If you are using a phone number from another country, replace +1 with the 
appropriate country code for that number.

# Vosk
VOSK_MODEL_PATH='Path to your downloaded Vosk model'

# TTS
TTS_MODEL_NAME='tts_models/en/ljspeech/tacotron2-DDC_ph' 

You can replace the TTS Model with another if you prefer.
```

## Running the Program

### Running as a Terminal Application

To run the program as a terminal application, use the following command:

```bash
python3 main.py
```

### Running as a Web Application with a User Interface

To run the program as a web application with a user interface, use the command:

```bash
streamlit run /path/to/your/main.py
```

Please adjust the `/path/to/your/main.py` with the actual path to your `main.py` file on your system.
