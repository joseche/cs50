import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
PP -> P NP
NP -> N | Det NP | NP PP | Adj NP | Det Adj NP | P NP | NP Adv
VP -> V | V NP | VP PP | Adv V | V Adv | Adv V NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    from nltk.tokenize import word_tokenize

    filtered_words = []
    all_words = word_tokenize(sentence)
    filtered_words.extend(word.lower() for word in all_words if any(c.isalpha() for c in word))
    return filtered_words


def has_np_child(tree):
    for child in tree:
        if type(child) is str:
            continue
        if child._label == "NP" or has_np_child(child):
            return True
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    pt = nltk.tree.ParentedTree.convert(tree)
    queue = []
    visited = []
    np_chunks = []
    for child in pt:
        queue.append(child)
    while queue:
        node = queue.pop()
        if node in visited:
            continue
        visited.append(node)
        for child in node:
            if child not in visited and type(child) is not str:
                queue.append(child)
        if node._label == "NP" and not has_np_child(node):
            np_chunks.append(node)
    return np_chunks


if __name__ == "__main__":
    main()
