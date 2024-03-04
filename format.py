from typing import List


def indent(text: str, amount: int = 4) -> str:
    return "\n".join(" " * amount + line for line in text.splitlines())


def format_list_item(item: str) -> str:
    """Format a list item with indentation and a bullet point."""
    head, *tail = item.splitlines()
    result = f"    * {head}\n" + indent("\n".join(tail))
    if not result.endswith("\n"):
        result += "\n"
    return result


def format_list(items: List[str]) -> str:
    """Given a list of assumptions, return a string where each assumption is formatted as a list item."""
    return "".join(format_list_item(assumption) for assumption in items)


