from SpeechToTextAgent import SpeechToTextAgent
from TextToSpeechAgent import TextToSpeechAgent
from blackbox import thirdPartyBlackBox  # Handles sending text/audio to an external service
from recording import record
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from deep_translator import GoogleTranslator
import logging
import os

# Initialize the LLM model
llm = OllamaLLM(model="llama3.1")

# Function to detect threats in the input text
def ThreatDetectionAgent(text: str) -> bool:
    system_message = "You are a threat detector for individuals with intellectual disabilities or autism. If you receive a prompt that may directly or indirectly contain emotional distress, violence, sexual-content, and self-harm implications, reply 'DANGER' only. Otherwise, respond 'SAFE' only. Categorize as DANGER for marginal cases."

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_message}"),
            ("human", "{text}")
        ]
    )
    chain = prompt_template | llm
    response = chain.invoke(
        input={"system_message": system_message, "text": f"'{text}'"}
    )
    
    if "DANGER" in response:
        return True
    else:
        return False

# Function to translate between languages
def TranslatorAgent(text: str, input_language: str = "EN", output_language: str = "EN") -> str:
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
        text = chain.invoke({"text": text})

    return text

# Function to handle bot responses
def ResponseAgent(inputText: str, chat_history: list) -> tuple[str, list]:
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an emotionless chatbot called Mike. You are talking to a child. Please use simple wordings and do not use contractions."),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    chain = prompt_template | llm
    chat_history.append(HumanMessage(content=inputText))
    response = chain.invoke({"chat_history": chat_history})
    chat_history.append(AIMessage(content=response))

    return response, chat_history
def main():
    chat_history = []
    is_danger = False
    
    # Select language
    print("Welcome to the program. Please select a language to start with: (1)English, (2)Cantonese, (3)Mandarin")
    print("歡迎嚟到呢個程式，請選擇語言：（1）英文，（2）廣東話，（3）普通話")
    print("欢迎来到这个程式，请选择语言：（1）英语，（2）广东话，（3）普通话")
    language = {'1': 'EN', '2': 'YUE', '3': 'CN'}.get(input(">> "))
    
    if not language:
        raise ValueError("Invalid language selection")
    
    # Store recorded responses
    recorded_responses = []
    output_list = thirdPartyBlackBox(inputText=None, inputAudio=None, output_list=None)
    
    while True:
        print("Recording your input... (press Ctrl+C to stop)")
        audio = record()  # Record audio and return the filename

        if is_danger:
            # Send the recorded audio to the external service via thirdPartyBlackBox
            output_list = thirdPartyBlackBox(inputText=None, inputAudio=audio, output_list=output_list)
            raw_output = " ".join([response['content'] for response in output_list if response not in recorded_responses])
            recorded_responses.extend(output_list)

            if not raw_output:
                raw_output = "Waiting for help..."
            
            translated_output = TranslatorAgent(text=raw_output, output_language=language)
        else:
            # Convert recorded audio to text
            raw_input = SpeechToTextAgent(audio)  
            
            if raw_input == "":
                print("No speech detected, please try again.")
                continue  # Skip to the next iteration if transcription fails

            # Translate the input text
            translated_input = TranslatorAgent(text=raw_input, input_language=language)
            print(f"Translated Input: {translated_input}")
            
            # Detect threats in the translated input
            is_danger = ThreatDetectionAgent(translated_input)
            
            if is_danger:
                # If danger is detected, notify through thirdPartyBlackBox
                thirdPartyBlackBox(inputText=translated_input, inputAudio=audio)
                raw_output = "Please wait a moment, I'm getting help"
            else:
                # Get response from chatbot
                raw_output, chat_history = ResponseAgent(translated_input, chat_history)
            
            print(f"Raw Output: {raw_output}")
            # Translate the response back to the selected language
            translated_output = TranslatorAgent(text=raw_output, output_language=language)

        # Convert the translated text back to speech
        TextToSpeechAgent(translated_output, input_language=language)
        print(f"Assistant: {translated_output}")

if __name__ == "__main__":
    main()
