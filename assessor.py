import json
from dataclasses import dataclass
from typing import Protocol

from funcutils import is_valid_function_definition


@dataclass
class Approval:
    """The proposed text meets the objective(s)."""
    pass


@dataclass
class Critique:
    """The proposed text requires refinement."""
    feedback: str


@dataclass
class Substitution:
    """The proposed text has been transformed (e.g. formatted). Substite the
    proposed text with the transformed text and continue."""
    text: str


Assessment = Approval | Critique | Substitution


class Assessor(Protocol):
    """Receives a text and returns an Assessment."""
    async def assess(self, text: str) -> Assessment:
        raise NotImplementedError()

    def reset(self):
        pass


class _JsonAssessor(Assessor):
    async def assess(self, text: str) -> Assessment:
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            return Critique("The text is not valid JSON")
        return Approval()


class _StripQuotesAssessor(Assessor):
    async def assess(self, text: str) -> Assessment:
        if text.startswith('"') and text.endswith('"'):
            try:
                value = eval(text)
            except Exception:
                return Approval()
            if isinstance(value, str):
                return Substitution(value)
        return Approval()
    

class _StripLanguageFormattingBlockAssessor(Assessor):
    async def assess(self, text: str) -> Assessment:
        if text.startswith("```") and text.endswith("```"):
            lines = text.splitlines()
            if " " not in lines[0][3:].strip():
                # If there's at most one word after the ``` then its a language name, so remove it too
                lines.pop(0)
            else:
                # Otherwise, just remove the ``` from the first line
                lines[0] = lines[0][3:]
            # Remove the ``` from the last line
            lines[-1] = lines[-1][:-3]
            return Substitution("\n".join(lines))
        return Approval()


NO_LANGUAGE_FORMATTING_BLOCK = [
    _StripLanguageFormattingBlockAssessor(),
]

NO_QUOTES = [
    _StripQuotesAssessor(),        
]


class _DefNameAssessor(Assessor):
    async def assess(self, text: str) -> Assessment:
        if not text.startswith("def "):
            return Critique("'" + text.split("\n")[0] + "' does not begin with 'def ' and a Python function name")
        return Approval()


class _ValidPythonFunctionAssessor(Assessor):
    async def assess(self, text: str) -> Assessment:
        if not is_valid_function_definition(text):
            return Critique("The text is not a single python function definition")
        return Approval()


PYTHON = [
    *NO_LANGUAGE_FORMATTING_BLOCK,
    _DefNameAssessor(),
    _ValidPythonFunctionAssessor(),
]

JSON = [
    *NO_LANGUAGE_FORMATTING_BLOCK,
    *NO_QUOTES,
    _JsonAssessor(),
]
