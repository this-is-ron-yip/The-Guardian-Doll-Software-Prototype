def speechToText():
    text = input()
    return text


def getLLMOutput():
    return "response"


def processLLMOutput():
    text = ""
    return text


def seekAssistance():
    return


def textToSpeech():
    return


chat_history = list()
while True:
    input = speechToText()
    output = getLLMOutput()
    is_danger, text = processLLMOutput()
    chat_history.append(text)
    if is_danger:
        seekAssistance(chat_history)
    
    textToSpeech()
        
