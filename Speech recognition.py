# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 13:30:35 2025

@author: THINKPAD
"""

import nltk
import streamlit as st
import os


nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_dir):
    os.mkdir(nltk_data_dir)


nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('punkt_tab', download_dir=nltk_data_dir)
nltk.data.path.append(nltk_data_dir)


try:
    import speech_recognition as sr
    speech_enabled = True
except:
    speech_enabled = False


with open("chatbot.txt", "r") as file:
    raw_data = file.read()


sent_tokens = nltk.sent_tokenize(raw_data)
word_tokens = nltk.word_tokenize(raw_data)


def transcribe_speech():
    if not speech_enabled:
        return "Speech recognition not available online."
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."


def chatbot_response(user_input):
    return "You said: " + user_input


def handle_input(input_type):
    if input_type == "Text":
        user_text = st.text_input("Type your message:")
        if st.button("Send") and user_text:
            st.write(chatbot_response(user_text))
    elif input_type == "Speech" and speech_enabled:
        if st.button("Speak"):
            speech_text = transcribe_speech()
            st.write("Transcribed: " + speech_text)
            st.write(chatbot_response(speech_text))
    else:
        st.warning("Speech input is only available when running locally.")


def main():
    st.title("Speech-Enabled Chatbot")

   
    if "STREAMLIT_RUNTIME" in os.environ and not speech_enabled:
        st.info("Speech input disabled online. Please use Text mode.")
        input_type = "Text"
    else:
        input_type = st.radio("Choose input type:", ("Text", "Speech"))

    handle_input(input_type)

if __name__ == "__main__":
    main()