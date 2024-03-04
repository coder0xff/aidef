import asyncio
import hashlib
import inspect
import json
import logging
from typing import Callable, Dict

import nest_asyncio
nest_asyncio.apply()

from cache import cached
from solve import answer
from funcutils import (
    convert_typing_type,
    extract_argument_assumption,
    extract_conditions_from_docstring,
    function_signature,
)
from log import getlogger

log = getlogger(__name__)
log.setLevel(logging.DEBUG)


def _wrap(func: Callable, validators: Dict = {}, ext: str = "txt", fast: bool = False) -> Callable:
    async_eval = inspect.iscoroutinefunction(func)
    func_name = func.__name__
    sig = function_signature(func)
    pre, post = extract_conditions_from_docstring(func.__doc__)
    assert post
    spec = inspect.getfullargspec(func)
    return_type = inspect.getfullargspec(func).annotations.get("return", str)

    async def f_async(*args, **kwargs):
        inputs = extract_argument_assumption(spec, *args, **kwargs)
        inputs_hash = hashlib.sha256(json.dumps(inputs).encode()).hexdigest()
        cache_name = func.__name__ + "_" + str(inputs_hash)
        meta = {"sig": sig, "pre": pre, "post": post, "inputs": inputs}

        with cached("eval", cache_name, ext, meta, "eval") as cache:
            if not cache.has_value:
                log.debug(f"Evaluating {func_name}")
                result = await answer(
                    pre + inputs, post, return_type.__name__, checkers=validators, fast=fast
                )
                log.debug(f"Finished evaluating {func_name}")
                cache.set(result)
            file = cache.file_name

        with open(file, "r") as source_file:
            return convert_typing_type(return_type, source_file.read())

    def f(*args, **kwargs):
        return asyncio.run(f_async(*args, **kwargs))

    if async_eval:
        return f_async
    else:
        return f


def aieval(*args, **kwargs) -> Callable:
    """A decorator that evaluates a functions from its pre and post conditions and the given inputs
    using the OpenAI API."""

    # is it a Critics list?
    if args and isinstance(args[0], list):
        validators = args[0]
    else:
        validators = {}

    if kwargs:
        validators = kwargs.get("validators", validators)
        ext = kwargs.get("ext", "txt")
        fast = kwargs.get("fast", False)

        def f(func):
            return _wrap(func, validators=validators, ext=ext, fast=fast)

        return f

    return _wrap(args[0])
