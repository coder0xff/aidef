import ast
from dataclasses import dataclass
import inspect
import json
import re
import sys
import traceback
from typing import Callable, Dict, List, Optional, Tuple, TypeAlias


def extract_conditions_from_docstring(docstring: str) -> Tuple[List[str], List[str]]:
    """Parse preconditions and postconditions from a docstring. When a line
    begins with \s+@pre or \s+@post, the following text including newlines is
    a precondition or postcondition in the returned pair of lists,
    respectively. @pre or @post inside 3x double quotes are ignored. Newlines
    are converted to Posix line endings."""

    if docstring is None:
        return [], []
    
    pres: List[str] = []
    posts: List[str] = []
    current: Optional[List[str]] = None
    State: TypeAlias = Optional[Callable[[str], "State"]] 
    state: State = None
    buffer = ""
    pre_token = "@pre "
    post_token = "@post "

    def carriage_return(char: str) -> State:
        nonlocal buffer
        buffer += "\n"
        if char == "\n":
            return start_of_line_or_whitespace
        return start_of_line_or_whitespace(char)

    def start_of_line_or_whitespace(char: str) -> State:
        nonlocal current
        nonlocal buffer
        if char == "\r":
            return carriage_return
        if char == "@":
            if current is not None:
                current[-1] += buffer
            buffer = char
            return at_symbol
            
        buffer += char
        if char == "\"":
            return quote
        if char.isspace():
            return start_of_line_or_whitespace
        return content

    def content(char: str) -> State:
        nonlocal current
        nonlocal buffer
        if char == "\r":
            return carriage_return
        
        buffer += char
        if char == "\"":
            return quote
        if char == "\n":
            return start_of_line_or_whitespace
        return content

    def at_symbol(char: str) -> State:
        nonlocal current
        nonlocal buffer
        if char == "\r":
            return carriage_return
        
        buffer += char
        if char == "\"":
            return quote
        if buffer == pre_token:
            buffer = ""
            pres.append("")
            current = pres
            return content
        if buffer == post_token:
            buffer = ""
            posts.append("")
            current = posts
            return content
        if char != pre_token[len(buffer) - 1] and char != post_token[len(buffer) - 1]:
            return content
        return at_symbol

    def quote(char: str) -> State:
        nonlocal buffer
        if char == "\r":
            return carriage_return
        
        buffer += char
        if buffer[-3:] == "\"\"\"":
            return quoted
        if char == "\"":
            return quote
        return content

    def quoted_carriage_return(char: str) -> State:
        nonlocal buffer
        buffer += "\n"
        if char == "\n":
            return quoted
        return quoted(char)

    def quoted(char: str) -> State:
        nonlocal buffer
        if char == "\r":
            return quoted_carriage_return
        
        buffer += char
        if buffer[-3:] == "\"\"\"":
            return content
        return quoted

    state = start_of_line_or_whitespace
    for char in docstring:
        if state is None:
            if current is not None:
                current[-1] += buffer
            break
        state = state(char)

    if state is not None and current is not None:
        current[-1] += buffer

    pres = [stripped_pre for pre in pres if (stripped_pre := pre.strip())]
    posts = [stripped_post for post in posts if (stripped_post := post.strip())]
    return pres, posts


def function_signature(func: Callable) -> str:
    """Return the function signature of a function, including annotations."""
    spec = inspect.getfullargspec(func)
    return f"{func.__name__}{inspect.signature(func)}"


def is_valid_function_definition(func_str: str) -> bool:
    """
    Checks if the given string is a valid Python function definition
    and contains nothing more than a single function definition.

    Args:
    func_str (str): The string containing the function definition.

    Returns:
    bool: True if the string is a valid single function definition, False otherwise.
    """

    # assert there are no lines after the def that have less indentation, as a security measure
    lines = func_str.split("\n")
    first_line_indent = lines[0][: len(lines[0]) - len(lines[0].lstrip())]
    for i, line in enumerate(lines):
        if i == 0:
            continue
        if line.strip() == "":
            continue
        if not line.startswith(first_line_indent):
            raise ValueError(
                "The provided string contains lines after the function definition that have less indentation than the function definition itself. This is not allowed as a security measure."
            )

    try:
        # Parse the function string into an AST node
        parsed_ast = ast.parse(func_str)

        # Check if the AST only contains a single FunctionDef node at the top level
        return len(parsed_ast.body) == 1 and isinstance(
            parsed_ast.body[0], ast.FunctionDef
        )
    except SyntaxError:
        # If parsing the string raises a SyntaxError, it's not valid Python code
        return False


def create_callable_from_str(
    func_str: str, namespace: Optional[Dict] = None
) -> Callable:
    """Create a callable from a string containing a function definition."""

    if not is_valid_function_definition(func_str):
        raise ValueError(
            "The provided string does not contain a valid single function definition."
        )

    # Define a unique namespace (dict) to execute the function definition in isolation
    if namespace is None:
        # Make a new namespace like the globals but separate
        namespace = dict(globals())

    # Extract the function name from the provided string
    if not (m := re.match(r"def\s+(\w+)\s*\(", func_str)):
        raise ValueError(
            "The provided string does not seem to contain a function definition."
        )
    func_name = m.group(1)

    # Execute the function definition in the provided namespace
    exec(func_str, namespace, namespace)

    # Find the function object in the local namespace
    if func_name not in namespace:
        raise ValueError(
            f"The provided string does not seem to contain a function definition named '{func_name}'."
        )

    func = namespace[func_name]
    return func


def extract_function_name(signature):
    """
    Extracts the function name from its signature string.

    Parameters:
    - signature (str): The signature string of the function.

    Returns:
    - str: The extracted name of the function, or an empty string if not found.
    """
    # Regular expression pattern to match the function name
    pattern = r"^\s*def\s+(\w+)"

    # Searching for the pattern in the signature string
    match = re.search(pattern, signature)

    # Returning the matched group (function name) if found, else an empty string
    return match.group(1)


def convert_typing_type(input_type, input_str):
    """
    Converts an input string to the specified typing type.

    Parameters:
    - input_type: A typing type like List[str], Dict[str, int], etc.
    - input_str: A string representation of the value to be converted.

    Returns:
    - The converted value in the specified typing type.
    """

    if input_type == str:
        return input_str

    # Parse the input string using json.loads for basic JSON structures
    parsed_input = json.loads(input_str)

    # Match the input_type and return the appropriately parsed input
    if hasattr(input_type, "__origin__"):
        # Handle List[T]
        if input_type.__origin__ == list:
            return [item for item in parsed_input]
        # Handle Dict[K, V]
        elif input_type.__origin__ == dict:
            return {k: v for k, v in parsed_input.items()}
        # Handle Set[T]
        elif input_type.__origin__ == set:
            return {item for item in parsed_input}
        # Handle Tuple[T, ...]
        elif input_type.__origin__ == tuple:
            return tuple(parsed_input)

    return input_type(parsed_input)


def dump_last_exception():
    # Catch the exception and print its traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return traceback.format_exception(exc_type, exc_value, exc_traceback)


def extract_argument_assumption(
    spec: inspect.FullArgSpec, *args, **kwargs
) -> List[str]:
    """Given a function signature and its arguments, return a list of assumptions about the arguments."""
    return [f"{arg} is \"{value}\"" for arg, value in zip(spec.args, args)] + [
        f"The argument {arg} is {value}" for arg, value in kwargs.items()
    ]
