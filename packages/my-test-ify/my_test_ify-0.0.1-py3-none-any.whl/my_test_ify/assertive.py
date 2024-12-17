from typing import Any, Callable, Type

from .exceptions import InvalidTypeError
from .utils import *


def equals[T](tested: T, expected: T, id_test: int, description: str="") -> tuple[bool, str, str|None]:
    if type(expected) != type(tested):
        raise InvalidTypeError(type(expected), type(tested), "Type Error: 'expected' and 'tested' values ​​must be the same type")
    
    if expected == tested:
        msg = f"{GREEN}✓ {description} -> Passed!{RESET}"
        return True, msg, None
    else:
        path, str_stack = error_location()
        msg = f"{RED}\n--------------------------------------------------"
        msg += f"\n{path}"
        msg += f"\n{RED}Test {id_test} failed: {description}"
        msg += f"\n{YELLOW}Expected: {expected}"
        msg += f"\n{RED   }Tested:   {tested}"
        msg += f"\n--------------------------------------------------{RESET}\n"
        return False, msg, str_stack
    
def not_equals[T](tested: T, expected: T, id_test: int, description: str="") -> tuple[bool, str, str|None]:
    if type(expected) != type(tested):
        raise InvalidTypeError(type(expected), type(tested), "Type Error: 'expected' and 'tested' values ​​must be the same type")
    
    if expected != tested:
        msg = f"{GREEN}✓ {description} -> Passed!{RESET}"
        return True, msg, None
    else:
        path, str_stack = error_location()
        msg = f"{RED}\n--------------------------------------------------"
        msg += f"\n{path}"
        msg += f"\n{RED}Test {id_test} failed: {description}"
        msg += f"\n{YELLOW}Expected value not equal to: {expected}"
        msg += f"\n{RED   }But the tested was equal to: {tested}"
        msg += f"\n--------------------------------------------------{RESET}\n"
        return False, msg, str_stack
    

def greater_than(tested: int|float, expected: int|float, id_test: int, description: str="") -> tuple[bool, str, str|None]:
    if not isinstance(tested, (int, float)):
        raise InvalidTypeError(type(expected), type(tested), f"Type Error: the 'tested' value must be int or float, but it is of{type(tested)}")
    if not isinstance(expected, (int, float)):
        raise InvalidTypeError(type(expected), type(tested), f"Type Error: the 'expected' value must be int or float, but it is of{type(expected)}")
    
    if type(expected) != type(tested):
        raise InvalidTypeError(type(expected), type(tested), "Type Error: 'expected' and 'tested' values ​​must be the same type")
    
    if tested > expected:
        msg = f"{GREEN}✓ {description} -> Passed!{RESET}"
        return True, msg, None
    else:
        path, str_stack = error_location()
        msg = f"{RED}\n--------------------------------------------------"
        msg += f"\n{path}"
        msg += f"\n{RED   }Test {id_test} failed: {description}"
        msg += f"\n{YELLOW}The tested value ({RED}{tested}{YELLOW}) must be greater than the expected value ({RED}{expected}{YELLOW})!"
        msg += f"\n{RED}--------------------------------------------------{RESET}\n"
        return False, msg, str_stack


def less_than(tested: int|float, expected: int|float, id_test: int, description: str="") -> tuple[bool, str, str|None]:
    if not isinstance(tested, (int, float)):
        raise InvalidTypeError(type(expected), type(tested), f"Type Error: the 'tested' value must be int or float, but it is of{type(tested)}")
    if not isinstance(expected, (int, float)):
        raise InvalidTypeError(type(expected), type(tested), f"Type Error: the 'expected' value must be int or float, but it is of{type(expected)}")
    
    if type(expected) != type(tested):
        raise InvalidTypeError(type(expected), type(tested), "Type Error: 'expected' and 'tested' values ​​must be the same type")
    
    if tested < expected:
        msg = f"{GREEN}✓ {description} -> Passed!{RESET}"
        return True, msg, None
    else:
        path, str_stack = error_location()
        msg = f"{RED}\n--------------------------------------------------"
        msg += f"\n{path}"
        msg += f"\n{RED   }Test {id_test} failed: {description}"
        msg += f"\n{YELLOW}The tested value ({RED}{tested}{YELLOW}) must be less than the expected value ({RED}{expected}{YELLOW})!"
        msg += f"\n{RED}--------------------------------------------------{RESET}\n"
        return False, msg, str_stack


def raises_exception(
    expected_exception:  Type[Exception], 
    func: Callable[...,Any], 
    id_test: int, 
    description: str="",
    *args:list[Any], 
    **kwargs:dict[str,Any]
) -> tuple[bool, str, str|None]:
    try:
        func(*args, **kwargs)
    except expected_exception as e:
        return True, f"{GREEN}✓ {description} -> Passed!{RESET}", None
    except Exception as e:
        path, str_stack = error_location()
        
        msg = f"{RED}\n--------------------------------------------------"
        msg += f"\n{path}"
        msg += f"\n{RED}Test {id_test} failed: {description}"
        msg += f"\n{YELLOW}Unexpected exception {RED}{e}{YELLOW} raised!"
        msg += f"\n{RED}--------------------------------------------------{RESET}\n"
        
        return False, msg, str_stack
    path, str_stack = error_location()
    msg = f"{RED}\n--------------------------------------------------"
    msg += f"\n{path}"
    msg += f"\n{RED}Test {id_test} failed: {description}"
    msg += f"\n{YELLOW}No exception raised, but expected {RED}{expected_exception.__name__}{YELLOW} raised!"
    msg += f"\n{RED}--------------------------------------------------{RESET}\n"
    return False, msg, str_stack
