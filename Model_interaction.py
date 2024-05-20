from openai import OpenAI
import sys
# Point to the local server
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")

print("Enter the model's behavior (Example: Answer as Homer Simpson)")
behavior = input()
messages=[
    {"role": "system", "content": behavior}, #Задает поведение модели (то, как ей надо ответить) системный промпт
  ]

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  temperature=0.7,
  messages=messages
)

while True:
    print("What's your request? (If there is none, print 'exit')")
    new_req = input()
    if (new_req == "exit"):
        sys.exit()
    messages.append(
        {"role": "user", "content": new_req}
    )
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        temperature=0.7,
        messages=messages
    )
    print(completion.choices[0].message.content)

