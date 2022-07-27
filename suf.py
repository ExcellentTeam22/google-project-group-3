from typing import List

# Taken from geeks for geeks
# https://www.geeksforgeeks.org/auto-complete-feature-using-trie/

# feature using Trie data structure.


# creates a trie node
#from suffix_trie import keys


class TrieNode:
    """ Class TrieNode, creates a trie node.
    :ivar children: Hold nodes for each child inside dictionary.
    :ivar last: Boolean that check if the node is a leaf.
    """
    def __init__(self):
        """Initialising one node for trie"""
        self.children = {}
        self.last = False


def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str


class Trie:
    """ Trie class. Given a prefix it will print all the matching words in the array.
    :ivar root: The root of the prefixes tree.
    """
    def __init__(self):
        """Initialising the trie structure."""
        self.root = TrieNode()

    def form_trie(self, keys: List[str]) -> None:
        """ Forms a trie structure with the given set of strings
        if it does not exists already else it merges the key
        into it by extending the structure as required
        :param keys: List of strings to build branches for each word.
        :return: None.
        """
        for key in keys:
            self.insert(key)  # Inserting one key to the trie.

    def insert(self, key: str) -> None:
        """Inserts a key into trie if it does not exist already.
        And if the key is a prefix of the trie node, just
        marks it as leaf node.
        :param key: A word to put its branch inside the tree.
        :return: None.
        """
        #
        node = self.root

        for a in key:
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]

        node.last = True

    def suggestions_rec(self, node: TrieNode, word: str) -> set[str]:
        """Method to recursively traverse the trie and return a whole word.
        :param node: Node of the last letter at the given prefix.
        :param word: The current word to check.
        :return: Set of the matching word.
        """
        current_words = set()
        if node.last:
            current_words.add(word)

        for a, n in node.children.items():
            temp_result = self.suggestions_rec(n, word + a)
            if temp_result:
                current_words = current_words.union(temp_result)
        return current_words

    def get_all_words_matching_prefix(self, prefix: str) -> set[str]:
        """Returns all the words in the trie whose common prefix is the given key thus listing out all
        the suggestions for autocomplete.
        :param prefix: Wanted prefix to search for it all the matching words.
        :return: Set of all the words that match to the given prefix.
        """
        #
        node = self.root

        for a in prefix:
            # No string in the Trie has this prefix
            if not node.children.get(a):
                return set()
            node = node.children[a]

        # If prefix is present as a word, but
        # there is no subtree below the last
        # matching node.
        if not node.children:
            return set()

        return self.suggestions_rec(node, prefix)


if __name__ == '__main__':
    keys = [reverse("geeks"),
          reverse("geeksforgeeks"),
          reverse("geek"),
          reverse("newgeeks"),
          reverse("friendsongeeks"),
          reverse("toppergeek")]

    # key
    key = "eek"
    status = ["Not found", "Found"]

    # creating trie object
    t = Trie()

    # creating the trie structure
    # with the given set of strings
    t.form_trie(keys)

    # print string having suffix 'P'
    # our trie structure
    words_list = t.get_all_words_matching_prefix(reverse(key))
    if words_list:
        words_list = {reverse(word) for word in words_list}
    print(words_list)

    #comp = t.printStringsWithGivenSuffix(reverse(key))

    #get_all_words_matching_prefix

# Taken from geeks for geeks
# https://www.geeksforgeeks.org/auto-complete-feature-using-trie/