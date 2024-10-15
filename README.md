# Welcome to the Repository
Heyy Oscar Davis!! Welcome to the Project!! I have setup the basic structure of the project and we can just start working on our respective function! One point to note is that the how to pick up the audio is still unresolved. probably the one handling the text-speech conversion can also see how we can pick up that audio! (eg. pressing the space bar idk haha) also for better development purpose, if you have to push unfinished code, please start a new branch!! it would be better to not push the code to main branch until it is completed!! Gayao and have fun (probably)!!

# Ollama setup
1. To install Ollama, please select the installation package as provided [here](https://github.com/ollama/ollama?tab=readme-ov-file#ollama)

2. After successfully installing Ollama, open the terminal and run 
```
ollama pull llama3.1
```
then
```
ollama run llama3.1
```
You should then be able to interact with the model through the terminal

3. Check pulled model by ```ollama list```. Make sure that it matched the model name of 
```python
llm = OllamaLLM(model="llama3.1")
```
4. Try to run the code!!

### Reference
[GitHub](https://github.com/ollama/ollama?tab=readme-ov-file#ollama)

[LangChain](https://python.langchain.com/docs/integrations/llms/ollama/#setup)