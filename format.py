import json

from funcutils import create_callable_from_str, dump_last_exception, extract_conditions_from_docstring, function_signature, is_valid_function_definition


NO_LANGUAGE_FORMATTING_BLOCK = {
    "The text contains undesirable metadata in the form of a language formatting block": lambda x: (
        None
        if not (x.startswith("```") and x.endswith("```"))
        else x.split("\n")[1:-1]
    ),
}


def _is_quoted_string(x):
    try:
        value = eval(x)
    except Exception as e:
        return False        
    return isinstance(value, str)


NO_QUOTES = {
    "The text is surrounded by quotes": lambda x: 'remove the quotes' if _is_quoted_string(x) else None,
}

PYTHON = {
    **NO_LANGUAGE_FORMATTING_BLOCK,
    "The text does not begin with 'def ' and a function name": lambda x: (
        x.split("\n")[0] if not x.startswith("def ") else None
    ),
    "The text is not a single python function definition": lambda x: (
        x if not is_valid_function_definition(x) else None
    ),
}

def _is_json(x):
    try:
        json.loads(x)
    except json.JSONDecodeError as e:
        dump_last_exception(e)
        return False
    else:
        return True
    
JSON = {
    **NO_LANGUAGE_FORMATTING_BLOCK,
    **NO_QUOTES,
    "The text is not valid JSON": lambda x: None if _is_json(x) else x,
}
