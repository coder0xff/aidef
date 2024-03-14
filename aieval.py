import asyncio
import hashlib
import inspect
import json
import logging
from typing import Callable, Dict

import nest_asyncio
nest_asyncio.apply()

from cache import cached
from solve import solve
from funcutils import (
    convert_typing_type,
    extract_argument_assumption,
    extract_conditions_from_docstring,
    function_signature,
)
from log import getlogger

log = getlogger(__name__)
log.setLevel(logging.DEBUG)


def _generate_callable(func: Callable, validators: Dict = {}, ext: str = "txt", fast: bool = False) -> Callable:
    """Generate the function that will be returned by the aieval decorator."""

    # Get basic information about the function and its signature.
    func_name = func.__name__
    sig = function_signature(func)
    spec = inspect.getfullargspec(func)
    return_type = inspect.getfullargspec(func).annotations.get("return", str)

    # Extract the pre and post conditions from the docstring
    pre, post = extract_conditions_from_docstring(func.__doc__)
    assert post

    # This is the function that runs when the decorated user function is called
    async def f_async(*args, **kwargs):
        # Convert the passed in arguments into assumption strings
        inputs = extract_argument_assumption(spec, *args, **kwargs)

        # Produce a key for the cache
        inputs_hash = hashlib.sha256(json.dumps(inputs).encode()).hexdigest()
        cache_name = func.__name__ + "_" + str(inputs_hash)
        meta = {"sig": sig, "pre": pre, "post": post, "inputs": inputs}

        # Evaluate the function with caching
        with cached("eval", cache_name, ext, meta, "eval") as cache:
            if not cache.has_value:
                # There's no cached result, so we need to evaluate the function
                log.debug(f"Evaluating {func_name}")

                # Evaluate the function using the LLM solve
                result = await solve(
                    pre + inputs, post, return_type.__name__, assessors=validators, fast=fast
                )

                log.debug(f"Finished evaluating {func_name}")

                # Cache the result
                cache.set(result)
            
            # The cache file to read the result from
            file = cache.file_name

        with open(file, "r") as source_file:
            result = source_file.read()
            # If the return type isn't a string, try to convert
            result = convert_typing_type(return_type, result)
            return result

    if inspect.iscoroutinefunction(func):
        # if the user function is async, return the async handler directly
        return f_async
    else:
        # If the user function isn't async, wrap f_async in a blocking func
        def f(*args, **kwargs):
            return asyncio.run(f_async(*args, **kwargs))
        return f


def aieval(*args, **kwargs) -> Callable:
    """A decorator that generates a functions output using an LLM."""

    # is the input an Assessor list?
    if args and isinstance(args[0], list):
        validators = args[0]
    else:
        validators = {}

    # if aieval was passed configuration and not a function (yet)
    if kwargs or validators:
        # Prepare the configuration and return a new decorator that
        # will wrap the function its passed
        validators = kwargs.get("validators", validators)
        ext = kwargs.get("ext", "txt")
        fast = kwargs.get("fast", False)

        def f(func):
            return _generate_callable(func, validators=validators, ext=ext, fast=fast)

        return f

    # if aieval was passed a function
    return _generate_callable(args[0])
