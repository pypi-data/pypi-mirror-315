from typing import Any

from .utils import GREEN, RED, RESET, YELLOW


class InvalidTypeError(Exception):
    """Exceção lançada quando um tipo incorreto é passado para uma função."""
    def __init__(self, expected_type: Any, received_type: Any, message: str="Tipo de dado incorreto"):
        self.expected_type = expected_type
        self.received_type = received_type
        super().__init__(f"{YELLOW}{message}: expected {GREEN}{expected_type}{YELLOW}, but received {RED}{received_type}{YELLOW}.{RESET}")


class TestFunctionError(Exception):
    """Exceção para problemas na função de teste fornecida."""
    def __init__(self, message: str="Erro com a função de teste fornecida"):
        super().__init__(message)