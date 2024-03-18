# Resident-Care

## Project Files

Access the project files and documentation through this [Google Drive link](https://drive.google.com/drive/folders/10UkNdUlFrZ7Nbwz7XC6iyy3upMq62CyO?usp=sharing).

## Hardware Requirements
1. 25Gb Free Disk Space
2. 16Gb Ram
3. Network Card or Ethernet port
4. Stereo Output
5. Microphone Input
6. x86 CPU Architecture

## Software Requirements
1. Python 3.9.x (We have tested on Python 3.9.18)
2. Debian Linux (We have tested on Ubuntu 22.0.4 Operating System)

## Setup Instructions

### Building and Installing Requirements

1. Ensure that you have a version of python 3.9 installed on your system. \
   We have used Python 3.9.18.

2. Run the provided bash script setup_project.sh to install the required packages, and setup the virtual environment. 

    ```bash
    ./setup_project.sh 
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


# Resident Details
These environment variables are used to personalize the experience based on the resident's details.

RESIDENT_FIRST_NAME='The first name of the resident'
RESIDENT_LAST_NAME='The last name of the resident'
RESIDENT_AGE_YEARS='The age of the resident in years (1-130)'
RESIDENT_SEX='The sex of the resident ("Male" or "Female")'
RESIDENT_MEDICAL_CONDITIONS='A comma seperated list of known medical conditions of the resident'

# Setting Resident Details
Set these variables to reflect the resident's personal information. 
Ensure that the age is an integer between 1 and 130, and the sex is 
specified as either "Male" or "Female" (case insensitive). 
The medical conditions should be a comma-separated list of 
conditions without any special characters.

For example:

RESIDENT_FIRST_NAME='John'
RESIDENT_LAST_NAME='Doe'
RESIDENT_AGE_YEARS=85
RESIDENT_SEX='male'
RESIDENT_MEDICAL_CONDITIONS='mild dementia, mobility issues.'

These details will be used to tailor the interaction and alerts for the resident's specific needs and conditions.

```

## Running the Program
1. Ensure you have completed the setup instructions above.
2. Ensure your virtual environment is activated. If it is not activated run the following command.
```bash
source venv/bin/activate
```

### Running as a Terminal Application

To run the program as a terminal application, use the following command: 

```bash
python3 /path/to/your/main.py
```

### Running as a Web Application with a User Interface

To run the program as a web application with a user interface, use the command:

```bash
streamlit run /path/to/your/main.py
```

Please adjust the `/path/to/your/main.py` with the actual path to your `main.py` file on your system.
