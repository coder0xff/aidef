import asyncio
import logging
from typing import List, assert_never

from chat import Chat
from critic import Critic, Critique, Ready, Refine, Substitute
from format import format_list, format_list_item
from log import getlogger

log = getlogger(__name__)
log.setLevel(logging.DEBUG)


class CompletionError(Exception):
    pass


class Generator:
    def __init__(self, assumptions: List[str], objectives: List[str], clauseType: str):
        """Return a fresh generator."""
        self.chat = Chat()
        self.clauseType = clauseType

        # Prepare the initial prompt
        self.append("You are a generator. You will produce a text that satisfies the following ")
        self.append("objectives and assumptions. Don't produce any other text such as metadata ")
        self.append("or commentary. Ensure that the output is exactly as requested, avoiding ")
        self.append("abstractions and stearing clear of distractions.\n")
        self.chat.section("ASSUMPTIONS")
        self.append(format_list(assumptions))
        self.chat.section("OBJECTIVES")
        self.append(format_list(objectives))

    async def first_attempt(self) -> str:
        log.debug(" Generator is making a first attempt")
        return await self.chat.prompt(f"Produce a {self.clauseType} satisfying the objectives based on the assumptions.")
    
    async def correction(self, critique: str) -> str:
        log.debug(" Generator is refining")
        self.chat.section("CORRECTION")
        self.append(critique)
        return await self.chat.prompt(
            "Reply with a self-contained satisfication of the objectives and nothing more. "
            + "Avoid other changes than suggested by the correction."
        )

    def append(self, txt):
        self.chat.append(txt)

    def spoof(self, txt: str):
        self.chat.spoof_prompt(f"Produce a {self.clauseType} satisfying the objectives based on the assumptions.", txt)


class Discriminator(Critic):
    def __init__(self, assumptions: List[str], all_objectives: List[str], objective: str):
        """Return a fresh discriminator."""
        self.assumptions = format_list(assumptions)
        self.objectives = format_list(all_objectives)
        self.objective = format_list_item(objective)

        self.reset()

    async def test(self, text: str) -> Critique:
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
            return Refine(correction)
        
        return Ready()
    
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


class FastDiscriminator(Critic):
    def __init__(self, assumptions: List[str], objectives: List[str]):
        """Return a fresh discriminator."""
        self.assumptions = format_list(assumptions)
        self.objectives = format_list(objectives)

        self.reset()

    async def test(self, text: str) -> Critique:
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
            return Refine(correction)
        
        return Ready()
    
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

# def objective_critic(assumptions: List[str], objectives: List[str]) -> Critic:
#     assumptions = list(assumptions)
#     objectives = list(objectives)
#     objective_index = None
#     next_objective_index = 0  # a.k.a progress
#     objective = objectives[next_objective_index]
#     correction = None
#     last_refinement_objective_index = None
#     discriminator = Discriminator(assumptions, objectives, next_objective_index)

#     async def f(text: str):
#         nonlocal assumptions
#         nonlocal objectives
#         nonlocal objective_index
#         nonlocal next_objective_index
#         nonlocal objective
#         nonlocal correction
#         nonlocal last_refinement_objective_index
#         nonlocal discriminator

#         # Ask the discriminator if the text met the objective
#         if (correction := await discriminator.test(text)):
#             # It did not
#             next_objective_index = 0

#             # Remember the objective that caused a correction
#             last_refinement_objective_index = objective_index
            
#             return Refine(correction)
           
#         # The text meets the objective!
#         log.debug(f"{next_objective_index}/{len(objectives)} objectives met")

#         # Check if all objectives are met
#         if next_objective_index == len(objectives):
#             # Success
#             log.debug("Objective refinement succeeded!")
#             return Ready()

#         # Prepare the next objective
#         objective_index = next_objective_index
#         objective = objectives[objective_index]
#         discriminator = Discriminator(assumptions, objectives, objective_index)

#         next_objective_index += 1

#         # The last objective that caused a refinement is remembered.
#         # It already agreed with the present text, so not taksies backsies.
#         if next_objective_index == last_refinement_objective_index:
#             next_objective_index += 1

#         # setup for the next iteration with the next objective

#         return Inconclusive()

#     return f


async def refine(critics: List[Critic], iterations: int, generator: Generator, text: str):
    assert iterations > 0

    critics = list(critics)
    queue = list(range(len(critics)))
    run_counts = [0] * len(critics)

    while iterations > 0 and queue:
        i = queue[0]
        run_counts[i] += 1
        critic = critics[i]

        critique = await critic.test(text)

        match critique:
            case Substitute(new_text):
                text = new_text
                queue.pop(0)
            case Refine(correction):
                # The critic has a suggestion for a refinement
                # If no more attempts may be made, fail the solve
                if iterations == 0:
                    raise CompletionError("The generator was unable to produce a satisfactory result.")
                
                # Add all critics back to the queue
                queue = list(range(len(critics)))
                # Except the current critic stays at the front of the queue
                del queue[i]
                queue.insert(0, i)

                for j in range(1, len(critics)):
                    # Reset all critics except the current one
                    critics[j].reset()

                # The refinement says what to do, but additional negative prompt helps the generator
                text = await generator.correction(correction)
                iterations -= 1
            case Ready():
                queue.pop(0)
                log.debug(f"Refine progress: {len(critics) - len(queue)}/{len(critics)}")
            case _ as unreachable:
                assert_never(unreachable)

    log.debug("Refine succeeded!")
    return text


async def answer(
    assumptions: List[str],
    objectives: List[str],
    clauseType: str,
    iterations: int = 25,
    checkers: List[Critic] = [],
    fast: bool = False,
) -> str:
    """Solve a problem by iteratively refining a text to meet the given assumptions and objectives.
    
    assumptions: a list of assumptions that are assumed to hold true, and any verification of them is erroneous
    objectives: a list of objectives that the text should satisfy
    clauseType: the type of clause that the text should be
    iterations: the number of iterations to perform
    checkers: errors to feed to the generator
    
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

    critics = list(checkers)
    if fast:
        critics.append(FastDiscriminator(assumptions, objectives))
    else:
        for objective in objectives:
            critics.append(Discriminator(assumptions, objectives, objective))

    generator = Generator(assumptions, objectives, clauseType)
    first_attempt = await generator.first_attempt()

    return await refine(critics, iterations, generator, first_attempt)
