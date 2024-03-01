import asyncio
import functools
import io
import inspect
import json
import sys
from typing import Any, Callable, List, Optional

from aieval import aieval
from cache import CacheEntry
from format import JSON, PYTHON
from funcutils import create_callable_from_str, dump_last_exception, extract_conditions_from_docstring, function_signature
from solve import solve


@functools.lru_cache(maxsize=1000)
def cached_is_callable(symbol: Any) -> bool:
    return callable(symbol)


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
def generate_test_cases(signature: str, preconditions: List[str], postconditions: List[str]) -> List[str]:
    """
    @pre "signature" is a string representing the function signature
    @pre "preconditions" is a list of strings representing the preconditions of the function
    @pre "postconditions" is a list of strings representing the postconditions of the function
    @post the return value is a json list of test case descriptions that explore the space of the preconditions as inputs, including edge cases, and the expected results.
    """
    pass


@aieval(JSON, ext="json")
def generate_test_case_names(signature: str, preconditions: List[str], postconditions: List[str], test_cases: List[str]) -> List[str]:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_cases" is a list of test case descriptions
    @post the return value is a json list of test case names suitable for use as Python function names
    @post the test case names each include the name of the function under test
    """
    pass


@aieval(PYTHON, ext="py")
async def generate_test(signature: str, preconditions: List[str], postconditions: List[str], test_name: str, test_description: str) -> str:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_name" is the name of the Python test to implement for the function under test
    @pre "test_description" is the test case description of the Python test to implement for the function under test
    @post the return value is a Python function that exercises the function under test with the described inputs and verifies the described outputs
    @post the Python function first prints "TEST CASE BEGINS"
    @post the Python function prints its name and the test case description to stdout
    @post the Python function calls the function under test within a try block and print the exception to stdout if the function under test raises an exception
    @post the Python function does not put any code in a try block other than the call of the function under test
    @post the Python function prints PASS or FAIL to stdout to communicate the results
    @post the Python function prints the cause of the failure to stdout if the test fails, including the actual result of the function under test
    @post the Python function finally prints "TEST CASE ENDS"
    """
    pass


@aieval(PYTHON, ext="py")
async def refine_test(signature: str, preconditions: List[str], postconditions: List[str], test_name: str, test_description: str, test_function: str, refinement_data: str) -> str:
    """
    @pre "signature" is signature of the function under test
    @pre "preconditions" is a list of preconditions of the function under test
    @pre "postconditions" is a list of postconditions of the function under test
    @pre "test_name" is the name of the Python test to implement for the function under test
    @pre "test_description" is the test case description of the Python test to implement for the function under test
    @pre "test_function" is the Python function that exercises the function under test with the described inputs and verifies the described outputs
    @pre "refinement_data" is the data from the previous test run
    @post the return value is a refined Python function that exercises the function under test with the described inputs and verifies the described outputs
    @post the Python function first prints "TEST CASE BEGINS"
    @post the Python function prints its name and the test case description to stdout
    @post the Python function prints a line with PASS or FAIL on its own line to stdout to communicate the results
    @post the Python function prints the cause of the failure to stdout if the test fails
    @post the Python function finally prints "TEST CASE ENDS"
    """
    pass


class TestError(Exception):
    pass


@aieval
async def accuse_test_failure(signature: str, preconditions: List[str], postconditions: List[str], function_implementation: str, test_name: str, test_description: str, test_implementation: str, test_failure: str):
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
    pass


def generate_python(name, sig, pre, post):
    """Generate the body of a Python function from its pre and post conditions."""
    post = list(post)
    post.append("The function has a docstring")
    py_file = None

    with CacheEntry("func", name, "py", {"sig": sig, "pre": pre, "post": post}) as cache:
        if not cache.has_value:
            test_cases = generate_test_cases(sig, pre, post)
            test_names = generate_test_case_names(sig, pre, post, test_cases)

            async def generate_tests():
                return await asyncio.gather(*[generate_test(sig, pre, post, test_name, test_case) for test_name, test_case in zip(test_names, test_cases)])
            test_funcs = asyncio.run(generate_tests())

            async def tester(text) -> int:
                for i in range(len(test_funcs)):
                    for _ in range(3):
                        try:
                            test_failure = run_function_test(text, test_funcs[i])
                        except Exception:
                            test_funcs[i] = await refine_test(sig, pre, post, test_names[i], test_cases[i], test_funcs[i], dump_last_exception())
                            continue
                        if test_failure:
                            for _ in range(3):
                                accusation = await accuse_test_failure(sig, pre, post, text, test_names[i], test_cases[i], test_funcs[i], test_failure)
                                if "CULPRIT: test_implementation" in accusation:
                                    test_funcs[i] = await refine_test(sig, pre, post, test_names[i], test_cases[i], test_funcs[i], accusation)
                                    break
                                if "CULPRIT: function_implementation" in accusation:
                                    return accusation
                            else:
                                raise Exception("Analysis of the test failure did not yield a clear culprit.")
                        else:
                            break

            python_validators2 = dict(PYTHON)
            python_validators2["The function does not pass the test cases"] = tester

            global_functions = "The following functions are available.\n"            
            for value in globals().values():
                if cached_is_callable(value):
                    if value.__name__ == name:
                        continue
                    docstring_lines = [f'\t{line}' for line in value.__doc__.splitlines()]
                    global_functions + "\n"
                    global_functions += f"def {value.__name__}{inspect.signature(value)}:\n\t{docstring_lines}\n"


            func_def = asyncio.run(solve(pre, [global_functions], post, f"Python function with signature `{sig}`", validators=python_validators2))
                
            cache.set(func_def)

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
    func_def = generate_python(name, sig, pre, post)

    result = create_callable_from_str(func_def)
    result.__doc__ = result.__doc__ + "\n" + func.__doc__
    globals()[name] = result
    return result
