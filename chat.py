import os
from functools import cache
from typing import Tuple

from openai import AsyncOpenAI

@cache
def _remote_client():
    return AsyncOpenAI(        
        organization='org-pcWedsce1WajPvgssuP1Ub0A',
        api_key=os.environ['OPENAI_API_KEY'],
    )


class ExcessContextError(Exception):
    pass


async def _complete(prompt: str) -> str:
    task = _remote_client().chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    response = await task
    return response.choices[0].message.content


class Chat:
    def __init__(self, context: str = ""):
        self.context = context

    def exposition(self, txt: str):
        self.context += txt

    async def interact(self, prompt: str, delimiters: Tuple[str, str] = ("\n=== PROMPT ===\n", "\n=== RESPONSE ===\n")):
        self.context += delimiters[0]
        self.context += prompt
        self.context += delimiters[1]
        if len(self.context) > 100000:
            raise ExcessContextError("Context too long.")
        new_text = await _complete(self.context)
        self.context += new_text
        return new_text

    async def decide(self, question: str):
        await self.interact(question + " Explain your reasoning.")
        self.context += "\n=== QUESTION (YES/NO) ===\n"
        self.context += question
        self.context += "\n=== ANSWER (YES/NO)===\n"
        for _ in range(3):
            new_text = await _complete(self.context)
            if new_text.upper() == "YES":
                self.context += new_text
                return True
            elif new_text.upper() == "NO":
                self.context += new_text
                return False
        raise Exception(f"Could not decide: {question}.")
