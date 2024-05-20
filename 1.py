'''from llama_cpp import Llama

llm = Llama(
    model_path="C:/Users/msof2/Downloads/Meta-Llama-3-8B-Instruct-IQ1_S.gguf",
    chat_format="llama-3",
    # n_gpu_layers=-1, # для использования GPU
    # seed=1337, # установить конкретный seed
    # n_ctx=8192, # установить размер контекста
)
messages = [
    { "role": "system", "content": "Ты полезный ИИ помощник." },
    { "role": "user", "content": "Привет! Ты кто?" },
]

output = llm.create_chat_completion(messages)
print(output)
'''
import LMstudio_model
import sys
while True:
    print("Enter your request: ")
    request = input()
    LMstudio_model.messages.append(
        {"role": "user", "content": request}
    )
    LMstudio_model.messages = LMstudio_model.messages[-3:]
    print("-"*40)
    print(LMstudio_model.messages)
    print(LMstudio_model.completion.choices[0].message)

    if (request == "exit"):
        sys.exit()
