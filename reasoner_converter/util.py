"""Utilities."""
import re
from typing import List, Union


def _snake_case(arg: str):
    """Convert string to snake_case.

    Non-alphanumeric characters are replaced with _.
    CamelCase is replaced with snake_case.
    """
    # replace non-alphanumeric characters with _
    tmp = re.sub(r'\W', '_', arg)
    # replace X with _x
    tmp = re.sub(
        r'(?<=[a-z])[A-Z](?=[a-z])',
        lambda c: '_' + c.group(0).lower(),
        tmp
    )
    # lower-case first character
    tmp = re.sub(
        r'^[A-Z](?=[a-z])',
        lambda c: c.group(0).lower(),
        tmp
    )
    return tmp


def _pascal_case(arg: str):
    """Convert string to PascalCase.

    Non-alphanumeric characters are replaced with _.
    "ThisCase" is replaced with "this_case".
    """
    # replace _x with X
    tmp = re.sub(
        r"(?<=[a-zA-Z])_([a-z])",
        lambda c: c.group(1).upper(),
        arg
    )
    # upper-case first character
    tmp = re.sub(
        r"^[a-z]",
        lambda c: c.group(0).upper(),
        tmp
    )
    return tmp


def snake_case(arg: Union[str, List[str]]):
    """Convert each string or set of strings to snake_case."""
    if isinstance(arg, str):
        return _snake_case(arg)
    elif isinstance(arg, list):
        return [_snake_case(arg) for arg in arg]
    else:
        raise ValueError()


def pascal_case(arg: Union[str, List[str]]):
    """Convert each string or set of strings to PascalCase."""
    if isinstance(arg, str):
        return _pascal_case(arg)
    elif isinstance(arg, list):
        return [_pascal_case(arg) for arg in arg]
    else:
        raise ValueError()


def ensure_list(arg: Union[str, List[str]]):
    """Convert scalar arg to a list of one."""
    if isinstance(arg, list):
        return arg
    return [arg]
