from dataclasses import dataclass
from os.path import exists
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


# def find_all_matches(words_list: List[str], ) -> List[AutoCompleteData]:
#     matches = []
#     start_position = 0
#     for word in words_list:
#         path = "../" + word
#         if len(word) <= 2:
#             continue
#         if len(word) >= 3 and not exists(path):
#             return []
#
#
#
#
# def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
#     words_list = re.findall(r"\W*\w+\W*", prefix)
#     matches_found = find_all_matches(words_list)
#     if len(matches_found):
#         return matches_found
#     return list_after_change_letters()

if __name__ == '__main__':
    pass

