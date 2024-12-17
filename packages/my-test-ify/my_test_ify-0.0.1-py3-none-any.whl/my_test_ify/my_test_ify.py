
from dataclasses import dataclass
from typing import Any, Callable

from .assertive import equals
from .exceptions import TestFunctionError
from .utils import *


@dataclass (init = False)
class Report:
    def __init__(self, summary: Callable[...,str], report: Callable[...,str], failure_stack: Callable[...,list[str]]):
        self.summary = summary
        self.report = report
        self.failure_stack = failure_stack
        

def my_test_ify() -> tuple[Callable[...,Any],Report]:
    _passed_tests_counter = 0
    _failed_tests_counter = 0
    _total_tests_counter = 0
    _failure_message: list[str] = []
    _success_message: list[str] = []
    _stacks: list[str] = []
    
    def summary()-> str:
        return get_summary(_total_tests_counter, _passed_tests_counter, _failed_tests_counter)
    
    def report()-> str:
        _report = ""
        for msg in _failure_message:
            _report = msg + _report
        for msg in _success_message:
            _report = msg + "\n" + _report
        return _report
    
    def failure_stack()-> list[str]:
        return _stacks[:] if len(_stacks) > 0 else [f"{GREEN}No failures{RESET}"]
    
    def run_test[T](
        expected:T, 
        result: T, 
        description:str="",
        test_function: Callable[..., Any] = equals,
        *args: Any,
        **kwargs: Any
    ) -> None:
        if not callable(test_function):
            raise TestFunctionError("The provided test function is not a valid function.")

        nonlocal _total_tests_counter
        nonlocal _passed_tests_counter
        nonlocal _failed_tests_counter
        nonlocal _success_message
        nonlocal _failure_message
        nonlocal _stacks
        
        _total_tests_counter += 1
        
        passed, msg, stack = test_function(expected, result, _total_tests_counter, description, *args, **kwargs)
        
        if stack is not None:
            _stacks.append(stack)
            
        if passed:
            _passed_tests_counter += 1
            _success_message.append(msg)
        else:
            _failed_tests_counter += 1
            _failure_message.append(msg)
    
    def core[T](
        expected:T, 
        result: T, 
        description:str="",
        test_function: Callable[..., Any] = equals,
        *args:list[Any], 
        **kwargs:dict[str,Any]
    ) -> None:

        run_test(expected, result, description, test_function, *args, **kwargs)
    
    return core, Report(summary, report, failure_stack)

