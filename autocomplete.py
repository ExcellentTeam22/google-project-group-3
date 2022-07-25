from dataclasses import dataclass
import re
from typing import List


@dataclass
class AutoCompleteData:
    """
    Save inside a data structure the details about each match.

    """
    def __init__(self, completed_sentence: str, source_text: str, offset: int, score: int):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score


if __name__ == '__main__':
    pass

