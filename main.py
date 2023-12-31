import database
import transcribe_speech
import generate_reply
import generate_audio
import asyncio
import argparse

from random         import choices
from config         import NAME
from pydub          import AudioSegment
from pydub.playback import play
from io             import BytesIO


# Set the language as English for all models
LANGUAGE = "en"

def output(text: str, audio_file: BytesIO) -> None:
    """
    Prints the text and plays back the audio file.

    Parameters:
    text (str): The text to be printed.
    audio_file (BytesIO): The audio file to be played.
    """
    # print the text
    print("\nELOQUI: " + text + "\n\n----------------------------------------\n")

    # load the audio from the BytesIO object using pydub
    audio_segment = AudioSegment.from_file(audio_file, format='mp3')

    # play the audio
    play(audio_segment)


def process_voice_question(whisper_model: str, gender: str, language_level: str) -> None:
    """
    Handles the user's button click event by capturing the spoken input,
    transcribing it, generating a response, converting the response to speech,
    and displaying the text response while playing the audio output.

    Args:
        whisper_model (str): The whisper model to be used.
        gender (str): The desired gender of the generated voice.
        language_level (str): The target grade level (1, 5, 10, etc)
    """
    # Capture user's spoken input and transcribe it
    transcript = transcribe_speech.main(whisper_model, LANGUAGE)
    if transcript is not None:
        transcript = transcript.strip()
    else:
        print("Error: Transcript is empty.")
        return
    print("ME: " + transcript + "\n")
    
    # Generate a response using NLP
    response_text = generate_reply.converse(transcript, language_level)

    # Convert the response text to speech
    audio_file = asyncio.run(get_audio_file(response_text, LANGUAGE, gender))

    # Display the text response and play the audio
    output(response_text, audio_file)


async def get_audio_file(text, gender):
    return await generate_audio.generate_audio(text, LANGUAGE, gender)


def process_text_question(text: str, gender: str, language_level: str) -> None:
    """
    Handles the user's typed input, generating a response, converting the response to speech,
    and displaying the text response while playing the audio output.

    Args:
        text (str): The input text from the user.
        gender (str): The desired gender of the generated voice.
        language_level (str): The target grade level (K3, 1, 5, 10, etc)
    """
    
    # Generate a response using NLP
    response_text = generate_reply.converse(text, language_level)

    # Convert the response text to speech
    audio_file = asyncio.run(get_audio_file(response_text, LANGUAGE, gender))

    # Display the text response and play the audio
    output(response_text, audio_file)


def main(whisper_model: str, gender: str, language_level: str) -> None:
    """
    The main loop of the application that waits for the user's button press
    (Enter key) and starts the recording process.

    Args:
        whisper_model (str): The whisper model to use for transcription.
        language_level (str): The target grade level (1, 5, 10, etc)
    """
    database.initialize_memory()

    global NAME     
    NAME = input("Please enter your name: ")

    while True:
        # Wait for the user to press a button (Enter key in this case)
        user_input = input("Press Enter to speak, or type your question... (type 'goodbye' to quit)")
        
        if user_input.lower() == "":
            # Start the recording process
            process_voice_question(whisper_model, LANGUAGE, gender, language_level)
        elif user_input.lower() == "goodbye":
            # Call a different function to handle the "exit" command
            generate_reply.exit_program()
            break  # exit the loop and terminate the program
        else:
            process_text_question(user_input, LANGUAGE, gender, language_level)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--whisper_model', type=str, help='Whisper model to be used.', choices= ["tiny", "tiny.en", "base", "base.en", "small", "small.en"], default="base")
    parser.add_argument('--gender', type=str, help='The desired gender of the voice. (M or F)', nargs='?', default='F', choices=["M", "F"])
    parser.add_argument('--grade_level', type=str, help='The target grade level (K3, 1, 5, 10, etc)', nargs='?', default='3', choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    
    args           = parser.parse_args()
    whisper_model  = args.whisper_model
    gender         = args.gender
    language_level = args.grade_level
    main(whisper_model, gender, language_level)
