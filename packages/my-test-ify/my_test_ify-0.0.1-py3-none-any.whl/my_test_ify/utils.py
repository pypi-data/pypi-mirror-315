import inspect
import os
import re

WHITE = "\033[97m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_summary(_total_tests_counter: int, _passed_tests_counter: int, _failed_tests_counter: int) -> str:
    msg = f"{RESET}\n\n--------------------------------------------------"
    msg += f"\n{BLUE}SUMMARY OF TESTS"
    msg += f"\n{YELLOW} Total: {_total_tests_counter}"
    msg += f"\n{GREEN }Passed: {_passed_tests_counter}"
    msg += f"\n{RED   }Failed: {_failed_tests_counter}"
    msg += f"\n{RESET}--------------------------------------------------\n\n"
    return msg
    

def error_location() -> tuple[str, str]:
    stack = inspect.stack()
    frame = stack[-1]
    list_path: list[str] = re.split(r"[\\/]", frame.filename)
    code_context = frame.code_context[0].strip() if frame.code_context else ""
    file: str = list_path.pop()
    if os.name == 'nt':
        path: str = "\\".join(list_path) + "\\"
    elif os.name == 'posix':
        path: str = "/".join(path) + "/"


    path = f"{YELLOW}Method '{code_context}' was called {RED}on line {frame.lineno}{YELLOW} in file '{path}{RED}{file}'."
    return path, get_str_stack(stack)


def get_str_stack(stack: list[inspect.FrameInfo]) -> str:
    str_stack = f"{RED}\nSTACK:"

    for frame in stack:
            
        str_stack += f"\n{YELLOW}filename:     {WHITE}{frame.filename}"
        str_stack += f"\n{YELLOW}lineno:       {WHITE}{frame.lineno}"
        str_stack += f"\n{YELLOW}Code Context: {WHITE}{frame.code_context[0].strip() if frame.code_context else ''}"
        str_stack += f"\n{YELLOW}function:     {WHITE}{frame.function}"
        str_stack += "\n=============================================================================================="
    str_stack += f"\n{RED}END STACK!{RESET}\n"
    
    return str_stack
    
    
    
