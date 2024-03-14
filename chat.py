import logging
import os
from functools import cache

from openai import AsyncOpenAI

from log import getlogger


log = getlogger(__name__)
log.setLevel(logging.DEBUG)


@cache
def _remote_client():
    return AsyncOpenAI(
        organization=os.environ["OPENAI_API_ORG"],
        api_key=os.environ["OPENAI_API_KEY"],
    )


class ExcessContextError(Exception):
    pass


async def complete(content: str) -> str:
    """Use the LLM API to complete the given content."""
    if len(content) > 100000:
        raise ExcessContextError("Context too long.")
    task = _remote_client().chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": content}],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    response = await task
    reply = response.choices[0].message.content
    return reply


class Chat:
    def __init__(self, context: str = ""):
        self.context = context

    async def prompt(self, prompt: str):
        self.section("PROMPT")
        self.append(prompt)
        self.section("REPLY")
        new_text = await complete(self.context)
        self.append(new_text)
        return new_text

    async def test(self, question: str) -> bool:
        """Ask a YES/NO question"""
        self.section("PROMPT")
        self.append(question + " (YES/NO)\n")
        self.section("REPLY")
        for _ in range(3):
            new_text = (await complete(self.context)).strip()
            if new_text.upper() == "YES":
                self.append(new_text + "\n")
                return True
            elif new_text.upper() == "NO":
                self.append(new_text + "\n")
                return False
            else:
                log.error("Invalid YES/NO response from Chat")

        raise Exception(f"Could not decide: {question}.")

    async def pretest(self, question: str):
        """Call before test to get the AI to think about the question."""
        await self.prompt(question + " Show your step-by-step reasoning.")

    def append(self, txt: str):
        self.context += txt

    def section(self, title: str):
        if not self.context.endswith("\n"):
            self.context += "\n"
        self.append(f"\n=== {title} ===\n\n")
