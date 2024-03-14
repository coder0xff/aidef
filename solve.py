import logging
from typing import List, assert_never

from chat import Chat
from assessor import Assessor, Assessment, Approval, Critique, Substitution
from format import format_list, format_list_item
from log import getlogger

log = getlogger(__name__)
log.setLevel(logging.DEBUG)


class CompletionError(Exception):
    pass


class Generator:
    """Generates text using an LLM"""
    def __init__(self, assumptions: List[str], objectives: List[str], clauseType: str):
        """Create a generator primed with the given assumptions and objectives."""
        self.chat = Chat()
        self.clauseType = clauseType

        # Prepare the initial prompt
        self.chat.append("You are a generator. You will produce a text that satisfies the following ")
        self.chat.append("objectives and assumptions. Don't produce any other text such as metadata ")
        self.chat.append("or commentary. Ensure that the output is exactly as requested, avoiding ")
        self.chat.append("abstractions and stearing clear of distractions.\n")
        self.chat.section("ASSUMPTIONS")
        self.chat.append(format_list(assumptions))
        self.chat.section("OBJECTIVES")
        self.chat.append(format_list(objectives))

    async def first_shot(self) -> str:
        """Make the first attempt at producing text of the desired clause type
        that satisfies the objectives."""
        log.debug(" Generator is making a first attempt")
        return await self.chat.prompt(f"Produce a {self.clauseType} satisfying the objectives based on the assumptions.")
    
    async def refine(self, critique: str) -> str:
        log.debug(" Generator is refining")
        self.chat.section("CORRECTION")
        self.chat.append(critique)
        return await self.chat.prompt(
            "Reply with a self-contained satisfication of the objectives and nothing more. "
            + "Avoid other changes than suggested by the correction."
        )


class Discriminator(Assessor):
    """Discriminates text for an objective using an LLM"""
    def __init__(self, assumptions: List[str], all_objectives: List[str], objective: str):
        """Create a disriminator for the given objective, with context from the
        given assumptions and all objectives."""
        self.assumptions = format_list(assumptions)
        self.objectives = format_list(all_objectives)
        self.objective = format_list_item(objective)

        self.reset()

    def reset(self):
        """Clear the LLM context and prepare the initial prompt."""
        self.chat = Chat()
        self.chat.append("You are a discriminator. You evaluate text against requirements. ")
        self.chat.append("Validate the included text against the below assumptions and ")
        self.chat.append("objectives. Ensure that complete evidence of the chain of thought is ")
        self.chat.append("provided in the text. You will decide whether the text strictly meets ")
        self.chat.append("these requirements.\n")
        self.chat.section("ASSUMPTIONS")
        self.chat.append(self.assumptions)
        self.chat.section("OBJECTIVES")
        self.chat.append(self.objectives)

    async def assess(self, text: str) -> Assessment:
        """Test the text against the objective, and return a approval or
        critique as appropriate"""
        self.chat.section("TEXT_BEGINS")
        self.chat.append(text)
        self.chat.section("TEXT_ENDS")
        self.chat.append("The assumptions are repeated here for convenience:\n")
        self.chat.section("ASSUMPTIONS")
        self.chat.append(self.assumptions)

        self.chat.section("OBJECTIVE")
        self.chat.append(self.objective)
        await self.chat.pretest("Considering this one objective alone, does the text meet the objective?")

        self.chat.section("OBJECTIVE")
        self.chat.append(self.objective)
        if not await self.chat.test("Considering this one objective, and the reasoning above, does the text meet the objective?"):
            log.debug("Discriminator is suggesting a refinement")
            correction = await self.chat.prompt(
                "What changes do you suggest to make the text meet the objective?"
            )
            return Critique(correction)
        
        return Approval()
    

class FastDiscriminator(Assessor):
    def __init__(self, assumptions: List[str], objectives: List[str]):
        """Return a fresh discriminator."""
        self.assumptions = format_list(assumptions)
        self.objectives = format_list(objectives)

        self.reset()

    async def assess(self, text: str) -> Assessment:
        """Test the text against the objectives, and return a approval or
        critique as appropriate"""
        self.chat.section("TEXT_BEGINS")
        self.chat.append(text)
        self.chat.section("TEXT_ENDS")
        self.chat.append("The assumptions are repeated here for convenience:\n")
        self.chat.section("ASSUMPTIONS")
        self.chat.append(self.assumptions)

        self.chat.section("OBJECTIVES")
        self.chat.append(self.objectives)
        await self.chat.pretest("Considering the objectives, does the text meet the objective?")
        self.chat.section("OBJECTIVES")
        self.chat.append(self.objectives)
        if not await self.chat.test("Considering the objectives and the reasoning above, does the text meet the objective?"):
            log.debug("Discriminator is suggesting a refinement")
            correction = await self.chat.prompt(
                "What changes do you suggest to make the text meet the objective?"
            )
            return Critique(correction)
        
        return Approval()
    
    def reset(self):
        # Prepare the initial prompt
        self.chat = Chat()
        self.chat.append("You are a discriminator. You evaluate text against requirements. ")
        self.chat.append("Validate the included text against the below assumptions and ")
        self.chat.append("objectives. Ensure that complete evidence of the chain of thought is ")
        self.chat.append("provided in the text. You will decide whether the text strictly meets ")
        self.chat.append("these requirements.\n")
        self.chat.section("ASSUMPTIONS")
        self.chat.append(self.assumptions)
        self.chat.section("OBJECTIVES")
        self.chat.append(self.objectives)


async def solve(
    assumptions: List[str],
    objectives: List[str],
    clauseType: str,
    iterations: int = 25,
    assessors: List[Assessor] = [],
    fast: bool = False,
) -> str:
    """Solve a problem by iteratively refining a solution to meet the given assumptions and objectives.
    
    assumptions: a list of assumptions that are assumed to hold true, and any verification of them is erroneous
    objectives: a list of objectives that the text should satisfy
    clauseType: the type of clause that the text should be (e.g. "sentence", "Python function")
    iterations: the number of iterations to perform
    assessors: a list of assessors (in addition to the objectives) that will critique the solution
    
    Return the refined text that satisfies the given assumptions and objectives.
    """

    assert objectives
    assert iterations > 0

    # Add some additional assumptions to help things along
    assumptions = list(assumptions)
    assumptions.append(
        "assumptions are assumed to hold true, and their validity shall not be questioned, nor verified, nor tested"
    )

    # Add some additional objectives to help things along
    objectives = list(objectives)
    objectives.append(f"the text is a {clauseType}")
    objectives.append("assumptions are not questioned, nor verified, nor tested")

    # Choose how stringent to be with the assessors
    assessors = list(assessors)
    if fast:
        assessors.append(FastDiscriminator(assumptions, objectives))
    else:
        for objective in objectives:
            assessors.append(Discriminator(assumptions, objectives, objective))

    # Generate the first attempt
    generator = Generator(assumptions, objectives, clauseType)
    first_attempt = await generator.first_shot()

    # Refine the first attempt until it satisfies the assessors
    return await refine(assessors, iterations, generator, first_attempt)


async def refine(assessors: List[Assessor], iterations: int, generator: Generator, text: str):
    """
    Starting with a first shot at a text, iteratively refine it with the given
    assessors.
    
    assessors: a list of assessors to use for refining the text
    iterations: the number of iterations to perform
    generator: the generator to use for refining the text
    text: the initial text to refine

    Return the refined text that satisfies the given assessors or raise a
    CompletionError if no satisfactory result is found within the iteration
    limit.
    """

    assert iterations > 0

    assessors = list(assessors)
    queue = list(range(len(assessors)))
    run_counts = [0] * len(assessors)

    while iterations > 0 and queue:
        i = queue[0]
        run_counts[i] += 1
        assessor = assessors[i]

        assessment = await assessor.assess(text)

        match assessment:
            case Approval():
                # The assessor approves. Continue with the next assessor.
                queue.pop(0)
                log.debug(f"Refine progress: {len(assessors) - len(queue)}/{len(assessors)}")
            case Critique(feedback):
                # The assessor has feedback for a refinement
                # If no more attempts may be made, fail the solve
                if iterations == 0:
                    raise CompletionError("The generator was unable to produce a satisfactory result.")
                
                # All the assessors get another shot at feedback when the text
                # is refined, so reset the queue
                queue = list(range(len(assessors)))
                # except the current assessor stays at the front of the queue
                del queue[i]
                queue.insert(0, i)
                # Reset (e.g. clear chat context) all the assessors, except
                # the current one
                for j in range(1, len(assessors)):
                    assessors[j].reset()

                # Refine the text
                text = await generator.refine(feedback)
                iterations -= 1
            case Substitution(new_text):
                # The assessor approves, but transformed (formatted) the text.
                # Continue with the assessor's substitution.
                text = new_text
                queue.pop(0)
            case _ as unreachable:
                assert_never(unreachable)

    log.debug("Refine succeeded!")
    return text


