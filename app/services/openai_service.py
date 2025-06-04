import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def generar_mensaje(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content