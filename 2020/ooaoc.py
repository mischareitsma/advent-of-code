import time
from dataclasses import dataclass
from typing import Any


@dataclass
class Part:
    part: int
    fn: function

    start_time: float = 0
    end_time: float = 0

    is_test: bool = False

    # Answers normally are ints, but sometimes strings, just store as
    # an string, as we print it anyways.
    answer: str = ''
    

class Day:

    def __init__(self):
        start_time: float
        end_time: float
