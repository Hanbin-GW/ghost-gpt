from openai import OpenAI
from color_ansi import Color
client = OpenAI(api_key="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")

completion = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    #{"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "discord.py wavelink example code"}
  ]
)

print(f"{Color.MAGENTA}{completion.choices[0].message.content}{Color.RESET}")