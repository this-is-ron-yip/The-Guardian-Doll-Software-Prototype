import pyttsx3

def TextToSpeechAgent(text:str, input_language:str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.6)
    if input_language=="YUE":
        voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")
    else:
        #台灣發音
        voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
        #國語發音
        #voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
    engine.say(text)
    engine.runAndWait()
    return
