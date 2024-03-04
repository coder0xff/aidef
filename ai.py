import asyncio
import io
import inspect
import json
import re
import sys
from typing import Any, Callable, Dict, List, Optional

from aieval import aieval
from cache import cached
from critic import Critic, Critique, JSON, PYTHON, Ready, Refine
from funcutils import (
    create_callable_from_str,
    dump_last_exception,
    extract_conditions_from_docstring,
    function_signature,
)
from log import getlogger
from solve import Critic, answer


log = getlogger(__name__)
log.setLevel("DEBUG")


IGNORED_GLOBALS = [
    ("def f(*args, **kwargs):", None),
    ("def f_async(*args, **kwargs):", None),
]


callable_cache = {}
def cached_is_callable(symbol: Any) -> bool:
    try:
        if symbol in callable_cache:
            return callable_cache[symbol]
    except TypeError:
        return False
    result = callable(symbol)
    callable_cache[symbol] = result
    return result


def global_functions_text(excluded_names: List[str]) -> str:
    global_functions = ""
    for value in globals().values():
        if cached_is_callable(value):                    
            if value.__name__ in excluded_names:
                continue
            if value.__module__ in {"typing", "builtins"}:
                continue
            try:
                signature = f"def {value.__name__}{inspect.signature(value)}:"
            except ValueError:
                continue
            if (signature, value.__doc__) in IGNORED_GLOBALS:
                continue
            global_functions + "\n"
            global_functions += f'{signature}\n    """{value.__doc__}"""\n'


def run_function_test(function_under_test: str, test_function: str) -> Optional[str]:
    namespace = {}
    create_callable_from_str(function_under_test, namespace)
    test = create_callable_from_str(test_function, namespace)
    # redirect stdout to a string
    redirected = sys.stdout = io.StringIO()
    try:
        test()
    finally:
        # restore stdout
        sys.stdout = sys.__stdout__
    output = redirected.getvalue()
    if "PASS\n" in output:
        return None
    if "FAIL\n" not in output:
        raise Exception("The test did not print 'PASS\\n' or 'FAIL\\n'.")
    return output


@aieval(JSON, ext="json")
def generate_test_cases(
    signature: str, preconditions: List[str], postconditions: List[str]
) -> List[Dict[str, str]]:
    """
    @pre "signature" is a string representing the function signature
    @pre "preconditions" is a list of strings representing the preconditions of the function
    @pre "postconditions" is a list of strings representing the postconditions of the function
    @post the return value is a JSON list of test case descriptions that collectively explore the full space (and not more) of the preconditions as inputs, including edge cases, and the expected results based on the postconditions
    @post the return value is a JSON list of test case descriptions that make no additional assumptions beyond the preconditions, and performs no validation of given assumptions
    @post the return value is a JSON list of test case descriptions that test no additional objectives than those given, and test the given objectives completely
    @post the return value is a JSON list of dictionaries containing the key 'description' explaining what the test verifies, and the key 'inputs' which are literals to pass to the function under test
    """


@aieval(JSON, ext="json")
def generate_test_case_names(
    signature: str,
    preconditions: List[str],
    postconditions: List[str],
    test_cases: List[str],
) -> List[str]:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_cases" is a list of test case descriptions
    @post the return value is a JSON list of test case names suitable for use as Python function names, each containing the name of the function under test
    """


@aieval(PYTHON, ext="py")
async def generate_test(
    signature: str,
    preconditions: List[str],
    postconditions: List[str],
    test_name: str,
    test_description: str,
) -> str:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_name" is the name of the Python test to implement for the function under test
    @pre "test_description" is the test case description of the Python test to implement for the function under test
    @post the return value is a Python function that calls the function under test within a try block using the described inputs
    @post the return value is a Python function that does not put any code in a try block other than the call to the function under test
    @post the return value is a Python function that prints 1) the expected output of the function under test, 2) the actual output of the function under test, and 3) "PASS" or "FAIL" to stdout to communicate the results
    """


@aieval(PYTHON, ext="py")
async def refine_test(
    signature: str,
    preconditions: List[str],
    postconditions: List[str],
    test_name: str,
    test_description: str,
    test_function: str,
    test_result: str,
) -> str:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_name" is the name of the Python test to implement for the function under test
    @pre "test_description" is the test case description of the Python test to implement for the function under test
    @pre "test_function" is the Python function that executed the test
    @pre "test_result" is the text that was printed by the test function
    @post the return value is a refined "test_function"
    @post the return value is a Python function that calls the function under test within a try block using the described inputs
    @post the return value is a Python function that does not put any code in a try block other than the call to the function under test
    @post the return value is a Python function that prints 1) the expected output of the function under test, 2) the actual output of the function under test, and 3) "PASS" or "FAIL" to stdout to communicate the results
    """


@aieval
async def accuse_test_failure(
    signature: str,
    preconditions: List[str],
    postconditions: List[str],
    function_implementation: str,
    test_name: str,
    test_description: str,
    test_implementation: str,
    test_failure: str,
):
    """
    @pre "signature" is the signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "function_implementation" is the Python function that exercises the function under test with the described inputs and verifies the described outputs
    @pre "test_name" is the name of the Python test to implement for the function under test
    @pre "test_description" is the test case description of the Python test to implement for the function under test
    @pre "test_implementation" is the Python function that exercises the function under test with the described inputs and verifies the described outputs
    @pre "test_failure" is the output of the test function when it failed
    @pre the "preconditions" and "postconditions" superscede the "test_description", and only the preconditions may be assumed, and only the postconditions must be satisfied and satisfied completely
    @pre a "test_description" that does not assume the "preconditions" is erroneous
    @pre a "test_description" that exceeds the "postconditions" is erroneous
    @post the return value is a string that elaborates on why the test failed, examines the "test_implementation" for bugs or incorrect assumptions beyond those specified, and examines the "function_implementation" for bugs or incorrect assumptions beyond those specified.
    @post if the "test_description" is erroneous, it is assumed that the "function_implementation" is correct and the "test_implementation" is incorrect
    @post the return value ends with either the text "CULPRIT: test_implementation" or "CULPRIT: function_implementation"
    """


async def generate_python(name: str, sig: str, pre: List[str], post: List[str]) -> str:
    """Generate the body of a Python function and its tests from its pre and post conditions."""
    post = list(post)
    py_file = None

    with cached(
        "func", name, "py", {"sig": sig, "pre": pre, "post": post}
    ) as cache:
        if not cache.has_value:
            log.debug(f"Generating Python function for {name}.")

            test_cases = generate_test_cases(sig, pre, post)
            # Sometimes the test cases include extra information that we don't want
            test_cases = [{"description": v["description"], "inputs": v["inputs"]} for v in test_cases]            
            log.debug(f"Generated test cases for Python function {name}.")

            test_names = generate_test_case_names(sig, pre, post, test_cases)
            log.debug(f"Generated names for the test cases for Python function {name}.")

            async def generate_tests():
                coroutines = []
                for test_name, test_case in zip(test_names, test_cases):
                    log.debug(f"Generating test {test_name}")
                    coroutines.append(
                        generate_test(sig, pre, post, test_name, test_case)
                    )
                return await asyncio.gather(*coroutines)
                # return [await coroutine for coroutine in coroutines]  # for debugging

            log.debug(f"Generating tests for Python function {name}.")
            test_funcs = await generate_tests()
            log.debug(f"Generated tests for Python function {name}.")
            class Tester(Critic):
                def __init__(self, i: int):
                    self.i = i

                async def test(self, text: str) -> Critique:
                    i = self.i
                    ALLOWED_ATTEMPTS = 5
                    attempt = 0
                    while True:
                        try:
                            log.debug(f"Running {test_names[i]} ({attempt + 1}/{ALLOWED_ATTEMPTS} attempts).")
                            test_failure = run_function_test(text, test_funcs[i])
                        except Exception:
                            log.debug(f"{test_names[i]} raised an exception.")
                            test_funcs[i] = await refine_test(
                                sig,
                                pre,
                                post,
                                test_names[i],
                                test_cases[i],
                                test_funcs[i],
                                dump_last_exception(),
                            )
                            continue
                        if test_failure:
                            for _ in range(3):
                                accusation = await accuse_test_failure(
                                    sig,
                                    pre,
                                    post,
                                    text,
                                    test_names[i],
                                    test_cases[i],
                                    test_funcs[i],
                                    test_failure,
                                )
                                if "CULPRIT: test_implementation" in accusation:
                                    attempt += 1
                                    if attempt >= ALLOWED_ATTEMPTS:
                                        raise Exception(f"{test_names[i]} was incorrect after {ALLOWED_ATTEMPTS} attempts to refine it.")
                                    log.debug(f"Refining {test_names[i]}.")
                                    test_funcs[i] = await refine_test(
                                        sig,
                                        pre,
                                        post,
                                        test_names[i],
                                        test_cases[i],
                                        test_funcs[i],
                                        accusation,
                                    )
                                    break
                                if "CULPRIT: function_implementation" in accusation:
                                    log.debug(f"Refining {name}.")
                                    return Refine(accusation)
                            else:
                                raise Exception(
                                    "Analysis of the test failure did not yield a clear culprit."
                                )
                        else:
                            log.debug(f"Test {test_names[i]} passed.")
                            return Ready()
                    else:
                        raise Exception("Test failed to pass after refinement.")

            checkers = list(PYTHON)
            checkers.extend([Tester(i) for i in range(len(test_funcs))])

            global_functions = global_functions_text([name])

            if global_functions:
                global_functions = "The following functions are available.\n" + global_functions
                log.debug(global_functions)
                inputs = [global_functions]
            else:
                inputs = []

            post = list(post)
            post.append("The function has a docstring")
            
            func_def = await answer(
                pre + inputs,
                post,
                f"Python function with signature `{sig}`",
                checkers=checkers,
            )

            func_and_tests = func_def + "\n\n" + "\n\n".join(test_funcs)
            cache.set(func_and_tests)

        py_file = cache.file_name

    with open(py_file, "r") as source_file:
        func_def = source_file.read()

    return func_def


@aieval(JSON, ext="json")
def conditions_from_description(desc: str, signature: str) -> str:
    """
    @pre "desc" is a plain-language description of a Python function
    @pre "signature" is a Python function signature
    @post the return value is JSON
    @post the return value contains a key "preconditions" containing a list of strings, each containing plain-language, of the preconditions of the described function
    @post the return value contains a key "postconditions" containing a list of strings, each containing plain-language, of the postconditions of the described function
    @post the preconditions do not make any assumptions other than about the input arguments, or the preconditions are empty if there are no arguments
    @post the postconditions do not make any assumptions other than about the return value
    """


@aieval(JSON, ext="json")
def conditions_from_signature(signature: str) -> str:
    """
    @pre "signature" is a Python function signature
    @post the return value is JSON
    @post the return value contains a key "preconditions" containing a list of strings, each containing plain-language, of the preconditions of the described function
    @post the return value contains a key "postconditions" containing a list of strings, each containing plain-language, of the postconditions of the described function
    @post the preconditions do not make any assumptions other than about the input arguments, or the preconditions are empty if there are no arguments
    @post the postconditions do not make any assumptions other than about the return value
    """


def ai(func: Callable) -> Callable:
    """A decorator that generates the body of a function from its pre and post conditions using the
    OpenAI API. Functions will be cached in the wordking directory."""
    # Use introspection to get the pre and post conditions from the docstring
    name = func.__name__
    sig = function_signature(func)
    pre, post = extract_conditions_from_docstring(func.__doc__)
    if not pre and not post:
        conditions = json.loads(conditions_from_description(func.__doc__, sig))
        pre, post = conditions["preconditions"], conditions["postconditions"]

    # Do the work of generating the function implementation
    func_and_tests = asyncio.run(generate_python(name, sig, pre, post))

    r = re.compile(r"^def ", re.MULTILINE)
    split_indices = [m.start() for m in r.finditer(func_and_tests)]
    func_def, *tests = [f for i, j in zip(split_indices, split_indices[1:] + [-1]) if (f:=func_and_tests[i:j]).strip()]
    result = create_callable_from_str(func_def)
    if func.__doc__ is not None:
        result.__doc__ = result.__doc__ + "\n" + func.__doc__
    globals()[name] = result
    return result
