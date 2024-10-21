import pyttsx3

def TextToSpeechAgent(text: str, input_language: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speech speed
    engine.setProperty('volume', 0.6)  # Voice volume

    try:
        # Select voice based on input language
        if input_language == "YUE":
            # Set Cantonese voice (ensure this voice is available on the system)
            engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")
        elif input_language == "CN":
            # Set Mandarin voice
            engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting")
        else:
            # Default to an English voice
            engine.setProperty('voice', "com.apple.speech.synthesis.voice.alex")

        # Speak the provided text
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"Error in TextToSpeechAgent: {str(e)}")
