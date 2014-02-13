import json
import urllib
import subprocess


def Speak(phrase):
    googleSpeechURL = "http://translate.google.com/translate_tts?tl=en&q=" + phrase
    subprocess.call(["mplayer",googleSpeechURL], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)