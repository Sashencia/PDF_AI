# %%
# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")


messages=[
    {"role": "system", "content": "Answer as Homer Simpson"}, #Задает поведение модели (то, как ей надо ответить) системный промпт
    {"role": "user", "content": "Introduce yourself."} #Вопрос пользователя к модели
    #есть еще роль ассистент (ai/bot), которая обозначает ответ модельки
  ]

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  temperature=0.7,
  messages=messages
)

print(completion.choices[0].message)

# %%
for i in range(5):
    print(messages[i:i+2])
    print("-"*40)

# %%
messages.append(dict(completion.choices[0].message))

# %%
print(messages)

# %%
messages.append(
    {"role": "user", "content":"Who is your wife?"}
)
messages = messages[-3:]

# %%
#Метод, который передает запрос к хосту: обработать список сообщений
completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  temperature=0.7,
  messages=messages
)


# %%
print(completion.choices[0].message)

# %%
messages.append(
    {"role": "assistant", "content" :"I have no wife" }
)

# %%
print(messages)

# %%
messages.append(
    {"role":"user", "content":"Who is your wife?"}
)

# %%
#Добавили в историю подмененныый ответ (придумали ответ за систему)
completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  temperature=0.7,
  messages=messages
)


# %%
print(completion.choices[0].message)





