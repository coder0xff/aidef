import json
from dataclasses import dataclass
from typing import Protocol

from funcutils import is_valid_function_definition


@dataclass
class Ready:
    """The text is ready for the next step in the process. It meets the objective."""
    pass


@dataclass
class Refine:
    """The text refined requires a change that could impact other Critiques. Ask the generator to
    refine the text, and reset the refinement process. Refinement will call all Critics again."""
    correction: str


@dataclass
class Substitute:
    """The text being refined needs a simple change that does not require resetting the refinement
    process because it changes trivial aspected, for example quotation marks. Replace the working
    text with the new text and continue refining."""
    text: str


Critique = Ready | Refine | Substitute


# A Critic is a function that takes a text and returns one of three things:
# - True if the text meets the objective
# - False if this Critic should be called again
# - A string with a suggestion for a refinement
class Critic(Protocol):
    async def test(self, text: str) -> Critique:
        raise NotImplementedError()

    def reset(self):
        pass


class _JsonCritic(Critic):
    async def test(self, text: str) -> Critique:
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            return Refine("The text is not valid JSON")
        return Ready()


class _StripQuotesCritic(Critic):
    async def test(self, text: str) -> Critique:
        if text.startswith('"') and text.endswith('"'):
            try:
                value = eval(text)
            except Exception:
                return Ready()
            if isinstance(value, str):
                return Substitute(value)
        return Ready()
    

class _StripLanguageFormattingBlockCritic(Critic):
    async def test(self, text: str) -> Critique:
        if text.startswith("```") and text.endswith("```"):
            lines = text.splitlines()
            if " " not in lines[0][3:].strip():
                # If there's a zero or one words after the ``` then its a language name, so remove it too
                lines.pop(0)
            else:
                # Otherwise, just remove the ``` from the first line
                lines[0] = lines[0][3:]
            # Remove the ``` from the last line
            lines[-1] = lines[-1][:-3]
            return Substitute("\n".join(lines))
        return Ready()


NO_LANGUAGE_FORMATTING_BLOCK = [
    _StripLanguageFormattingBlockCritic(),
]

NO_QUOTES = [
    _StripQuotesCritic(),        
]


class _DefNameCritic(Critic):
    async def test(self, text: str) -> Critique:
        if not text.startswith("def "):
            return Refine("'" + text.split("\n")[0] + "' does not begin with 'def ' and a Python function name")
        return Ready()


class _ValidPythonFunctionCritic(Critic):
    async def test(self, text: str) -> Critique:
        if not is_valid_function_definition(text):
            return Refine("The text is not a single python function definition")
        return Ready()


PYTHON = [
    *NO_LANGUAGE_FORMATTING_BLOCK,
    _DefNameCritic(),
    _ValidPythonFunctionCritic(),
]

JSON = [
    *NO_LANGUAGE_FORMATTING_BLOCK,
    *NO_QUOTES,
    _JsonCritic(),
]
