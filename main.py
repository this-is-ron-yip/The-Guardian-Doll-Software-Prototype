

# PIC: 
def speechToText(audio) -> str:
    """a function that listen to the user, and convert the speech to text

    Args:
        inputAudio (_type_): user prompt audio (type to be identified)
        
    Returns:
        str: textual representation of the speech
    """
    
    inputText = input()
    return inputText


# PIC: 
def textToSpeech(outputText: str) -> None:
    """a function that say out the generated response

    Args:
        outputText (str): textual representation of the expected output
    """
    
    return


# PIC: Ron
def threatDetection(inputText: str) -> bool:
    """a function that detect whether the user has suicidal thoughts / experienced bullying / harrassment

    Args:
        inputText (str): user prompt

    Returns:
        bool: flag indicating if the user is facing any threat 
    """

    return False


# PIC: Ron
def getLLMResponse(inputText: str) -> str:
    """a function that send the user prompt to the GenAI, and pass the GenAI response out as string

    Args:
        inputText (str): user prompt

    Returns:
        str: GenAI response
    """
    response = "LLM response"
    
    return response


# PIC: 
def thirdPartyBlackBox(inputText: str = None, inputAudio=None) -> str:
    """a blackbox that send user prompt (and possibly chat history) to third party (eg. psychiatrist / parent) and get textual response

    Args:
        inputText (str, optional): user prompt text
        inputAudio (_type_, optional): user prompt audio (type to be identified)

    Returns:
        str: response provided by third party user
    """
    response = "manual response"

    return response


def main():
    chat_history = list()
    is_danger = False
    while True:
        audio = ""
        if is_danger:
            outputText = thirdPartyBlackBox(inputAudio=audio)
        else:
            inputText = speechToText(audio)
            is_danger = threatDetection(inputText)
            if is_danger:
                outputText = thirdPartyBlackBox(inputText=inputText)
            else:
                outputText = getLLMResponse(inputText)
        textToSpeech(outputText)
            

if __name__ == "__main__":
    main()