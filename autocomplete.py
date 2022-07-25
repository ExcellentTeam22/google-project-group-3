from os.path import exists
import pickle
import re
from typing import Any, List
from words_details_class import WordDetails

DICTIONARY_DATA_FILE_PATH = r"..\words_dict.pk"


def create_data_dictionary(files_list: List[str]) -> dict[str, List[WordDetails]]:
    """ Receive a list of files and return a dictionary.
    The dictionary's keys are all the words inside the files, and the value is a list that includes details about
    the word (an object named WordDetails that gives us information about the place that the word found).

    :param files_list: A list includes paths to files.
    :return: Dictionary with words as keys and List[WordDetails] as value.
    """
    words_dict = {}
    for file_path in files_list:
        try:
            with open(file_path, encoding='UTF8') as file:
                pos = 0
                for row_number, row in enumerate(file.readlines()):
                    words_list = [word.lower() for word in re.findall(r"\W*(\w+)\W*", row)]
                    for word_place, word in enumerate(words_list):
                        new_word = WordDetails(word, row_number, word_place, pos, file_path)
                        if word in words_dict.keys():
                            words_dict[word].append(new_word)
                        else:
                            words_dict[word] = [new_word, ]
                    pos = file.tell()
        except OSError as err:
            print(f"File: {file_path}, Error: {err}")
    return words_dict


def save_dictionary_data(my_dict: dict, file_path: str) -> None:
    """ Save a dictionary in the file_path as a pk file.
    :param my_dict: A dictionary.
    :param file_path: Wanted file's path.
    :return: None.
    """
    with open(file_path, "wb") as file:
        pickle.dump(my_dict, file)


def load_data(file_path: str) -> Any:
    """ Loading a pk file and return it as and object.
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as file:
        return pickle.load(file)


def initialize_data(files_list: List[str]) -> dict[str, List[WordDetails]]:
    """ Initialize data and return data structure.

    :param files_list: List of files' paths.
    :return: Dictionary as a data structure for all the files.
    """
    if exists(DICTIONARY_DATA_FILE_PATH):
        return load_data(DICTIONARY_DATA_FILE_PATH)
    words_dict = create_data_dictionary(files_list)
    save_dictionary_data(words_dict, DICTIONARY_DATA_FILE_PATH)
    return words_dict


if __name__ == '__main__':
    my_data = initialize_data([r"../abs-guide.txt", r"../Concepts.txt"])



