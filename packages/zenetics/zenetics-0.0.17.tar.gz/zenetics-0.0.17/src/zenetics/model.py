from dataclasses import dataclass
from typing import Union


@dataclass
class TestCase:
    id: int
    name: str
    input: str
    description: Union[str, None] = None
    expected_output: Union[str, None] = None
