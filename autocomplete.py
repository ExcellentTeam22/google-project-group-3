from dataclasses import dataclass
from os import walk
import re
from string import ascii_lowercase
from typing import List
from words_details_class import WordDetails


DATA = {}

#taken from geeks for geeks
#https://www.geeksforgeeks.org/auto-complete-feature-using-trie/

# feature using Trie data structure.

#creates a trie node
class TrieNode():
	def __init__(self):
		# Initialising one node for trie
		self.children = {}
		self.last = False

#Given a prefix it will print all the matching words in the array
class Trie():

	def __init__(self):

		# Initialising the trie structure.
		self.root = TrieNode()

	def formTrie(self, keys):

		# Forms a trie structure with the given set of strings
		# if it does not exists already else it merges the key
		# into it by extending the structure as required
		for key in keys:
			self.insert(key) # inserting one key to the trie.

	def insert(self, key):

		# Inserts a key into trie if it does not exist already.
		# And if the key is a prefix of the trie node, just
		# marks it as leaf node.
		node = self.root

		for a in key:
			if not node.children.get(a):
				node.children[a] = TrieNode()

			node = node.children[a]

		node.last = True

	def suggestionsRec(self, node, word):

		# Method to recursively traverse the trie
		# and return a whole word.
		if node.last:
			print(word)

		for a, n in node.children.items():
			self.suggestionsRec(n, word + a)

	def printAutoSuggestions(self, key):

		# Returns all the words in the trie whose common
		# prefix is the given key thus listing out all
		# the suggestions for autocomplete.
		node = self.root

		for a in key:
			# no string in the Trie has this prefix
			if not node.children.get(a):
				return 0
			node = node.children[a]

		# If prefix is present as a word, but
		# there is no subtree below the last
		# matching node.
		if not node.children:
			return -1

		self.suggestionsRec(node, key)
		return 1


# Driver Code
keys = ["hello world", "dog", "hell", "cat", "a", "hel", "help", "helps", "helping"]
# keys to form the trie structure.
key = "he"
# key for autocomplete suggestions.

# creating trie object
t = Trie()

# creating the trie structure with the
# given set of strings.
t.formTrie(keys)

# autocompleting the given key using
# our trie structure.
comp = t.printAutoSuggestions(key)

if comp == -1:
	print("No other strings found with this prefix\n")
elif comp == 0:
	print("No string found with this prefix\n")


#taken from geeks for geeks
#https://www.geeksforgeeks.org/auto-complete-feature-using-trie/



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
                    words_list = [word.lower() for word in re.findall(r"\W*([\w']+)\W*", row)]
                    p2prev_word = None
                    for word_place, word in enumerate(words_list):
                        new_word = WordDetails(word, row_number, word_place, pos, file_path)
                        if word in words_dict.keys():
                            words_dict[word].append(new_word)
                        else:
                            words_dict[word] = [new_word, ]
                        if p2prev_word:
                            p2prev_word.set_next(new_word)
                        p2prev_word = new_word
                    pos = file.tell()
        except OSError as err:
            print(f"File: {file_path}, Error: {err}")
    return words_dict


def initialize_data(files_list: List[str]) -> dict[str, List[WordDetails]]:
    """ Initialize data and return data structure.

    :param files_list: List of files' paths.
    :return: Dictionary as a data structure for all the files.
    """
    words_dict = create_data_dictionary(files_list)
    return words_dict


def make_list_of_files() -> List[str]:
    """

    :return:
    """
    dir_path = r"..\archive"
    # dir_path = r"..\t"
    res = []
    for (dir_path, dir_names, files_names) in walk(dir_path):
        res.extend([dir_path + "\\" + file_name for file_name in files_names])
    return res


def check_user_words(words_list: List[str], score_if_found: int) -> List[AutoCompleteData]:
    """ Receive a list of words and check if there is a sentence inside the data structure that
     matches the received list. Return maximum five results.

    :param words_list:
    :param score_if_found:
    :return:
    """
    word_result = []
    all_exists_words = DATA.get(words_list[0])
    if not all_exists_words:
        return []
    for obj in all_exists_words:
        current_word = obj
        if len(words_list) >= 2:
            current_word = obj.next
            for word in words_list[1:]:
                if not current_word or current_word.word != word:
                    break
                current_word = current_word.next
            else:
                word_result.append(obj) # Need to change to the wanted object.
                print(obj.file_path, obj.row_num, score_if_found)
                if len(word_result) == 5:
                    break
        else:
            word_result.append(current_word)
        if len(word_result) == 5:
            break

    # Temporary output.
    return word_result


def calculate_optional_results(substring: str, score: int) -> List[AutoCompleteData]:
    words_list = [word.lower() for word in re.findall(r"\W*([\w']+)\W*", substring)]
    word_result = []

    word_result += check_user_words(words_list, score)

    """
    for fixed_prefix in find_word_suffix(words_list[0]):
        for fixed_suffix in find_word_prefix(words_list[-1]):
            if len(word_result) > 5:
                break
            word_result += check_user_words([fixed_prefix] + words_list[1:-1] + [fixed_suffix], len(prefix) * 2)
    """
    return word_result


def get_best_k_completions(prefix: str) -> List[AutoCompleteData]:
    """ Receive the user's string and return the top 5 rows at the texts that could complete the sentence.
    The string could be with one mistake, and it should be a substring of a sentence.
    :param prefix: Part of a sentence that the user insert.
    :return: Best 5 results.
    """
    prefix_length = len(prefix)
    score = prefix_length * 2
    word_result = calculate_optional_results(prefix, score)

    # switch
    minus_score = 5
    for i in range(0, prefix_length):
        current_letter = prefix[i]
        if current_letter == ' ':
            continue
        for letter in ascii_lowercase:
            if letter == current_letter:
                continue
            if len(word_result) >= 5:
                return word_result[:5]
            current_string = (prefix[:i] if i != 0 else "") + letter + (prefix[i+1:] if i != prefix_length-1 else "")
            word_result += calculate_optional_results(current_string, score - minus_score)
            minus_score = minus_score - 1 if minus_score != 1 else minus_score

    # add
    minus_score = 10
    for i in range(0, prefix_length + 1):
        for letter in ascii_lowercase:
            if len(word_result) >= 5:
                return word_result[:5]
            current_string = (prefix[:i] if i != 0 else "") + letter + (prefix[i:] if i != prefix_length else "")
            word_result += calculate_optional_results(current_string, score - minus_score)
            minus_score = minus_score - 2 if minus_score != 2 else minus_score

    # sub
    minus_score = 10
    for i in range(prefix_length):
        if len(word_result) >= 5:
            return word_result[:5]
        current_string = (prefix[:i] if i != 0 else "") + (prefix[i + 1:] if i != prefix_length-1 else "")
        word_result += calculate_optional_results(current_string, score - minus_score)
        minus_score = minus_score - 2 if minus_score != 2 else minus_score

    return word_result[:5]


if __name__ == '__main__':
    DATA = initialize_data(make_list_of_files())

    while True:
        prefix = input("Please enter a prefix: ")
        get_best_k_completions(prefix)
        # print(get_best_k_completions(prefix))

