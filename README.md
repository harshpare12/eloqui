# Eloqui
Eloqui is a Conversational AI tool for learning the English language. Eloqui is designed to provide casual conversation for practicing language skills. One can think of it in a similar way as DuoLingo.

## Features
Users spoken input is transcribed using the [Whisper]([url](https://github.com/openai/whisper)) library.
Uses [ChatGPT API]([url](https://platform.openai.com/docs/guides/gpt)) (GPT3.5 Turbo model) to generate responses for the user's input
The generated responses are converted to speech using the library [edge-tts]([url](https://pypi.org/project/edge-tts/))
Provides options for different language proficiency levels. The user can select a level from grades 1-12, and the model will behave accordingly.
Remembers the previous conversations made with the user. Uses the library [ChromaDB]([url](https://www.trychroma.com/)) for storing the old conversations.

## Run Eloqui
In order to run the app, run the python script main.py. It takes the following command-line arguments:

1. whisper_model: Whisper model to be used. Choices: "tiny", "tiny.en", "base", "base.en", "small", "small.en". Default: "base"
2. gender: The desired gender of the voice. Choices: "M", "F". Default: "F"
3. grade_level: The target grade level. Choices: "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12". Default: 10

Example
'''python main.py --whisper_model tiny --gender F --grade_level 10'''
