import asyncio
import hashlib
import inspect
import json
from typing import Callable, Dict

from cache import CacheEntry
from solve import solve
from funcutils import convert_typing_type, extract_argument_assumption, extract_conditions_from_docstring, function_signature


def _wrap(func: Callable, validators: Dict={}, ext: str="txt") -> Callable:
    async_eval=inspect.iscoroutinefunction(func)
    sig = function_signature(func)
    pre, post = extract_conditions_from_docstring(func.__doc__)
    spec = inspect.getfullargspec(func)
    return_type = inspect.getfullargspec(func).annotations.get("return", str)
    
    async def f_async(*args, **kwargs):
        inputs = extract_argument_assumption(spec, *args, **kwargs)
        inputs_hash = hashlib.sha256(json.dumps(inputs).encode()).hexdigest()
        name = func.__name__ + "_" + str(inputs_hash)
        meta = {"sig": sig, "pre": pre, "post": post, "inputs": inputs}

        with CacheEntry("eval", name, ext, meta) as cache:
            if not cache.has_value:
                result = await solve(pre, inputs, post, return_type.__name__, validators=validators)
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

    # is it a validators dictionary?
    if args and isinstance(args[0], dict):
        validators = args[0]
    else:
        validators = {}

    if kwargs:
        validators = kwargs.get("validators", validators)
        ext = kwargs.get("ext", "txt")
        def f(func):
            return _wrap(func, validators=validators, ext=ext)
        return f

    return _wrap(args[0])
