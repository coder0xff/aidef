import inspect
from typing import Callable, Dict, List, Optional, Tuple

from chat import Chat, ExcessContextError


class CompletionError(Exception):
    pass


async def decide(question: str, context: str="") -> Tuple[bool, str]:
    """Ask a yes/no question and return the answer."""


async def solve(
    preconditions: List[str],
    inputs: List[str],
    postconditions: List[str],
    clauseType: str,
    iterations: int = 10,
    validators: Dict[str, Callable[[str], Optional[str]]] = {},
):
    assert iterations > 0

    def format_list_item(assumption: str) -> str:
        """Given an assumption string, which may contain multiple lines, return a string
        where the first line is indented by 4 spaces and begins with an asterisk and space,
        and the rest are indented by 8 spaces. Existing indentation is preserved."""
        lines = assumption.split("\n")
        head = f"    * {lines[0]}"
        tail = [
            " " * max(8, len(line) - len(line.lstrip())) + line.strip()
            for line in lines[1:]
        ]
        return "\n".join([head] + tail) + "\n"

    def format_list(items: List[str]) -> str:
        """Given a list of assumptions, return a string where each assumption is formatted as a list item."""
        return "".join(format_list_item(assumption) for assumption in items)

    formatted_assumptions = format_list(preconditions + ["assumptions are assumed to hold true, and any verification of them is erroneous"] + inputs)
    formatted_objectives = format_list(
        postconditions + [f"The text is a {clauseType}."]
    )

    async def discriminate(candidate: str) -> Optional[str]:
        """If the candidate text is not satisfactory, return text suggestion improvements. Otherwise, return None."""
        nonlocal formatted_assumptions
        nonlocal formatted_objectives

        # First check common problems that don't require AI to detect
        for description, validator in validators.items():
            if inspect.iscoroutinefunction(validator):
                refinement = await validator(candidate)
            else:
                refinement = validator(candidate)
            if refinement:
                return f"ERROR: {description}: '{refinement}'"

        preamble = "You are a discriminator. You evaluate text against requirements. Validate the included text against the below assumptions and objectives. Ensure that complete evidence of the chain of thought is provided in the text. You will decide whether the text strictly meets these requirements.\n"
        preamble += "ASSUMPTIONS\n"
        preamble += formatted_assumptions
        preamble += "OBJECTIVES\n"
        preamble += formatted_objectives
        preamble += "TEXT_BEGINS\n"
        preamble += candidate
        preamble += "\nTEXT_ENDS\n"
        preamble += "Evaluate the text against the assumptions and objectives. They are repeated here for convenience:\n"
        preamble += "ASSUMPTIONS\n"
        preamble += formatted_assumptions

        for postcondition in postconditions:
            discriminator = Chat()
            discriminator.exposition(preamble)
            discriminator.exposition("OBJECTIVE\n")
            discriminator.exposition(format_list_item(postcondition))
            if not await discriminator.decide("Does the text meet the objective?"):
                return await discriminator.interact(
                    "What changes do you suggest to make the text meet the objective?"
                )
            else:
                pass

    generator = Chat()

    base_prompt = "You are a generator. You will produce a text that satisfies the following objectives and assumptions. You will not produce any other text such as metadata or commentary. Ensure that the output is exactly as requested, and not an unwarranted abstraction, or conversly an example of the requested abstract description.\n"
    base_prompt += "ASSUMPTIONS\n"
    base_prompt += formatted_assumptions
    base_prompt += "OBJECTIVES\n"
    base_prompt += formatted_objectives
    generator.exposition(base_prompt)
    text = await generator.interact(f"Produce a {clauseType} satisfying the objectives based on the assumptions.\n")

    while iterations > 0:
        iterations -= 1
        suggestion = await discriminate(text)
        if suggestion is None:
            break
        
        suggestion += "\nReply with a self-contained satisfication of the objectives and nothing more. Avoid other changes than those suggested.\n"
        try:
            text = await generator.interact(suggestion)
        except ExcessContextError:
            generator = Chat()
            generator.exposition("\n=== PROMPT ===\n")
            generator.exposition(base_prompt)
            generator.exposition("\n=== RESPONSE ===\n")
            generator.exposition(text)
            text = await generator.interact(suggestion)

        iterations -= 1

    if suggestion is None:
        return text

    raise CompletionError(
        "The generator was unable to produce a satisfactory result."
    )

