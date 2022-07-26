# Python3 code for the above program
class TrieNode():
    def __init__(self):
        # Initialize one node for trie
        self.children = {}
        self.last = False


def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str


class Trie():
    def __init__(self):

        # Initialize the trie structure
        self.root = TrieNode()
        self.word_list = []

    def formTrie(self, keys):

        # Forms a trie structure
        # with the given set of
        # strings if it does not
        # exists already else it
        # merges the key into it
        # by extending the
        # structure as required
        for key in keys:
            # inserting one key
            # to the trie.
            self.insert(key)

    def insert(self, key):

        # Inserts a key into
        # trie if it does not
        # exist already. And if
        # the key is a suffix
        # of the trie node, just
        # marks it as leaf node.
        node = self.root

        for a in list(key):
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]

        node.last = True

    def search(self, key):

        # Searches the given key
        # in trie for a full match
        # and returns True on
        # success else returns False
        node = self.root
        found = True

        for a in list(key):
            if not node.children.get(a):
                found = False
                break

            node = node.children[a]

        return node and node.last and found

    def printStrings(self, node, word):

        # Method to recursively
        # traverse the trie
        # and return a whole word
        if node.last:
            self.word_list.append(word)

        for a, n in node.children.items():
            self.printStrings(n, word + a)

    def printStringsWithGivenSuffix(self, key):

        # Returns all the words in
        # the trie whose common
        # suffix is the given key
        # thus listing out all
        # the strings
        node = self.root
        not_found = False
        temp_word = ''

        for a in list(key):
            if not node.children.get(a):
                not_found = True
                break

            temp_word += a
            node = node.children[a]

        if not_found:
            return 0
        elif node.last and not node.children:
            return -1

        self.printStrings(node, temp_word)

        for s in self.word_list:
            print(reverse(s))
        return 1


# Driver Code

# keys to form the trie structure
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
t.formTrie(keys)

# print string having suffix 'P'
# our trie structure
comp = t.printStringsWithGivenSuffix(reverse(key))
#https://www.geeksforgeeks.org/find-strings-that-end-with-a-given-suffix/
