from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

llm = OllamaLLM(model="llama3.1")

# PIC: Oscar
def SpeechToTextAgent(audio) -> str:
    """a function that listen to the user, and convert the speech to text

    Args:
        inputAudio (_type_): user prompt audio (type to be identified)

    Returns:
        str: textual representation of the speech
    """

    inputText = input("human: ")
    return inputText


# PIC: Oscar
def TextToSpeechAgent(outputText: str) -> None:
    """a function that say out the generated response

    Args:
        outputText (str): textual representation of the expected output
    """
    return


# PIC: Ron
def ThreatDetectionAgent(inputText: str) -> bool:
    """a function that detect whether the user has suicidal thoughts / experienced bullying / harrassment

    Args:
        inputText (str): user prompt

    Returns:
        bool: flag indicating if the user is facing any threat 
    """

    return False


# PIC: Ron
def TranslatorAgent(text: str, output_language: str) -> str:
    """a function that translate between Cantonese and English

    Args:
        text (str): target content
        output_language (str): "CAN" for Cantonese, "ENG" for english

    Returns:
        str: translated text
    """
    if output_language == "CAN":
        system_message = "你是一個翻譯員。你的職責是將輸入的英語原句翻譯成廣東話。"
    elif output_language == "ENG":
        system_message = "Your role is to translate Cantonese text to English accurately. Translate the provided phrase only without extra notes. Indicate unclear inputs with 'ERROR: I don't understand' only. You are expected not to show the thinking process."
    else:
        raise ValueError()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_message}"),
            ("human", "{text}")
        ]
    )
    chain = prompt_template | llm
    response = chain.invoke(input={"system_message": system_message, "text": f"'{text}'"})

    return response


# PIC: Ron
def ResponseAgent(inputText: str, chat_history: list) -> tuple[str, list]:
    """a function that send the user prompt to the GenAI, and pass the GenAI response out as string

    Args:
        inputText (str): user prompt
        chat_history (list): updated chat_history

    Returns:
        tuple[str, list]: GenAI response, chat_history
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a emotionaless Chatbot called Mike. You are talking to a child. Please use simple wordings and do not use contractions."),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    chain = prompt_template | llm
    chat_history.append(HumanMessage(content=inputText))
    response = chain.invoke({"chat_history": chat_history})
    chat_history.append(AIMessage(content=response))

    return response, chat_history


# PIC: Davis
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
            rawOutput = thirdPartyBlackBox(inputAudio=audio)
        else:
            rawInput = SpeechToTextAgent(audio)
            translatedInput = TranslatorAgent(text=rawInput, output_language="ENG")
            print("translated: " + translatedInput)
            is_danger = ThreatDetectionAgent(translatedInput)
            if is_danger:
                rawOutput = thirdPartyBlackBox(inputText=translatedInput)
            else:
                rawOutput, chat_history = ResponseAgent(translatedInput, chat_history)
            print("rawOutput: " + rawOutput)
            translatedOutput = TranslatorAgent(text=rawOutput, output_language="CAN")
        TextToSpeechAgent(translatedOutput)
        print("assistant: " + translatedOutput)
        print()


if __name__ == "__main__":
    main()