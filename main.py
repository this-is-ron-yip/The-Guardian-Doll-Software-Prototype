from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from deep_translator import (GoogleTranslator)

llm = OllamaLLM(model="llama3.1")

# PIC: Oscar
def SpeechToTextAgent(audio, input_language: str) -> str:
    """a function that listen to the user, and convert the speech to text

    Args:
        audio (_type_): user prompt audio (type to be identified)
        input_language (str): "EN" for english, "YUE" for Cantonese, "CN" for Mandarin

    Returns:
        str: textual representation of the speech
    """

    inputText = input("human: ")
    return inputText


# PIC: Oscar
def TextToSpeechAgent(outputText: str, input_language: str) -> None:
    """a function that say out the generated response

    Args:
        outputText (str): textual representation of the expected output
        input_language (str): "EN" for english, "YUE" for Cantonese, "CN" for Mandarin
    """
    return


# PIC: Ron
def ThreatDetectionAgent(text: str) -> bool:
    """a function that detect whether the user has suicidal thoughts / experienced bullying / harrassment

    Args:
        text (str): user prompt

    Returns:
        bool: flag indicating if the user is facing any threat 
    """
    system_message = "You are a threat detector for individuals with intellectual disabilities or autism. If you receive user prompt that may directly or indirectly contain emotional distress, violence, sexual-content and self-harm implications, reply 'DANGER' only. otherwise respond 'SAFE' only. You do not have the third option. Categorize as DANGER for marginal case"

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_message}"),
            ("human", "{text}")
        ]
    )
    chain = prompt_template | llm
    response = chain.invoke(
        input={"system_message": system_message, "text": f"'{text}'"})
    
    print(f"threat: {response}")
    if "DANGER" in response:
        return True
    else:
        system_message = "You are analysing the AI-generated response. If the response is a suicide prevention message, or mentioned about cannot create content related to harrassement, violence, danger or sexual-content, or about cannot engagereply 'DANGER' only, else reply 'SAFE' only"

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                ("human", "{text}")
            ]
        )
        chain = prompt_template | llm
        response = chain.invoke(input={"system_message": system_message, "text": f"'{response}'"})
        print(f"suicidal: {response}")
        if "DANGER" in response:
            return True
    return False


# PIC: Ron
def TranslatorAgent(text: str, input_language: str = "EN", output_language: str = "EN") -> str:
    """a function that translate between Cantonese and English

    Args:
        text (str): target content
        input_language (str): "EN" for english, "YUE" for Cantonese, "CN" for Mandarin
        output_language (str): "EN" for english, "YUE" for Cantonese, "CN" for Mandarin

    Returns:
        str: translated text
    """
    language_code = {"EN": "en", "YUE": "zh-CN", "CN": "zh-CN"}

    if input_language == "YUE":
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "請將廣東話口語翻譯成書面語，請不要添加額外句子"),
                ("human", "{text}")
            ]
        )
        chain = prompt_template | llm
        text = chain.invoke({"text": text})
        print("cantonese: " + text)

    text = GoogleTranslator(
        source=language_code[input_language], 
        target=language_code[output_language]).translate(text)


    if output_language == "YUE":
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "請將書面語翻譯成廣東話口語，請不要添加額外句子"),
                ("human", "{text}")
            ]
        )
        chain = prompt_template | llm
        print("cantonese before: " + text)
        text = chain.invoke({"text": text})

    return text


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
    
    print("Welcome to the program. Please select a language to start with: (1)English, (2)Cantonese, (3)Mandarin")
    print("歡迎嚟到呢個程式，請選擇語言：（1）英文，（2）廣東話，（3）普通話")
    print("欢迎来到这个程式，请选择语言：（1）英语，（2）广东话，（3）普通话")
    language = {'1': 'EN', '2': 'YUE', '3': 'CN'}.get(input(">> "))
    if not language:
        raise ValueError()
    
    while True:
        audio = ""
        if is_danger:
            rawOutput = thirdPartyBlackBox(inputAudio=audio)
        else:
            rawInput = SpeechToTextAgent(audio, input_language=language)
            translatedInput = TranslatorAgent(text=rawInput, input_language=language)
            print("translated: " + translatedInput)
            is_danger = ThreatDetectionAgent(translatedInput)
            if is_danger:
                rawOutput = thirdPartyBlackBox(inputText=translatedInput)
            else:
                rawOutput, chat_history = ResponseAgent(translatedInput, chat_history)
            print("rawOutput: " + rawOutput)
            translatedOutput = TranslatorAgent(text=rawOutput, output_language=language)
        TextToSpeechAgent(translatedOutput, input_language=language)
        print("assistant: " + translatedOutput)
        print()


if __name__ == "__main__":
    main()