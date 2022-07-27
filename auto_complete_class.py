
from dataclasses import dataclass
import re
from typing import List
from words_details_class import WordDetails


@dataclass
class AutoCompleteData:
    """
    Save inside a data structure the details about each match.
    """
    def __init__(self, word_detail: WordDetails, substring_list: List[str], score: int):

        self.completed_sentence = word_detail.full_row
        pattern = "("
        for index, word in enumerate(substring_list):
            pattern += r"[^\w']*" + word
        pattern += ")"
        match = re.search(pattern, self.completed_sentence.lower())
        if match:
            self.offset = self.completed_sentence.lower().index(match.group(1))
        self.source_text = word_detail.file_path
        self.score = score

    def __str__(self):
        return f"Sentence = {self.completed_sentence}\nOffset = {self.offset}\n " \
               f"Source = {self.source_text}\nScore = {self.score}\n\n"
