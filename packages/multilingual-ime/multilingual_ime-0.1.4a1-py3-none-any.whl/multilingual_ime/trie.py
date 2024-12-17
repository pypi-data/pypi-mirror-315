import heapq
import json

from .core.custom_decorators import lru_cache_with_doc


class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None


def modified_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the modified Levenshtein distance between two strings.
    The modified Levenshtein distance is the minimum number of single-character edits (insertions, deletions, substitutions, or swaps) required to change one word into the other.
    The difference between the modified Levenshtein distance and the original Levenshtein distance is that the modified Levenshtein distance allows for swapping two adjacent characters.
    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The modified Levenshtein distance between the two strings.

    Examples:
        >>> modified_levenshtein_distance("abc", "abcc")  # 1
        >>> modified_levenshtein_distance("abc", "acb")  # 1
        >>> modified_levenshtein_distance("flaw", "lawn")  # 2
        >>> modified_levenshtein_distance("kitten", "sitting")  # 3
    """

    if len(s1) < len(s2):
        return modified_levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))

    for i, char1 in enumerate(s1):
        current_row = [i + 1]

        for j, char2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            # substitutions = previous_row[j] + (char1 != char2)
            if char1 != char2:
                if i > 0 and j > 0 and s1[i - 1] == char2 and s1[i] == char1:
                    substitutions = previous_row[j - 1]
                else:
                    substitutions = previous_row[j] + 1
            else:
                substitutions = previous_row[j]

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.keyStrokeCatch = {}

    def insert(self, key: str, input_value: any) -> None:
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if node.value is None:
            node.value = [input_value]
        else:
            node.value.extend([input_value])

    def search(self, query_key: str) -> list:
        node = self.root
        for char in query_key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.value

    def _dfs_traverse(self, node: TrieNode, query: str, keySoFar: str) -> list:
        min_heap = []
        if node.children == {}:
            current_distance = modified_levenshtein_distance(query, keySoFar)
            heapq.heappush(min_heap, (current_distance, keySoFar))
            return min_heap
        else:
            for char, child_node in node.children.items():
                min_heap = list(
                    heapq.merge(
                        min_heap, self._dfs_traverse(child_node, query, keySoFar + char)
                    )
                )
                if len(min_heap) > 5:
                    min_heap = min_heap[:5]
                if len(min_heap) > 0 and min_heap[0][0] == 0:  # found exact match
                    return min_heap
            if node.value is not None:
                current_distance = modified_levenshtein_distance(query, keySoFar)
                heapq.heappush(min_heap, (current_distance, keySoFar))
            return min_heap

    @lru_cache_with_doc(maxsize=128, typed=False)
    def find_closest_match(self, query: str) -> list[dict]:
        """
        Find the closest match to the query string in the trie.
        Args:
            query (str): The query string.

        Returns:
            [dict]: A list of dictionaries containing the distance, keySoFar, and value of the closest match to the query string.

        """
        quick_search = self.search(query)
        if quick_search is not None:
            return [
                {
                    "distance": 0,
                    "keySoFar": query,
                    "value": quick_search,
                }
            ]

        minHeap = self._dfs_traverse(self.root, query, "")
        min_distance_candidate = minHeap[0]
        return [
            {
                "distance": candidate[0],
                "keySoFar": candidate[1],
                "value": self.search(candidate[1]),
            }
            for candidate in minHeap
            if candidate[0] <= min_distance_candidate[0]
        ]


from .candidate import CandidateWord

if __name__ == "__main__":
    data_dict_path = ".\\multilingual_ime\\src\\keystroke_mapping_dictionary\\english_dict_with_frequency.json"
    keystroke_mapping_dict = json.load(open(data_dict_path, "r", encoding="utf-8"))
    trie = Trie()
    if keystroke_mapping_dict is not None:
        for key, value in keystroke_mapping_dict.items():
            Candidate_words = [
                CandidateWord(
                    word=element[0], keystrokes=key, word_frequency=element[1]
                )
                for element in value
            ]
            for candidate in Candidate_words:
                trie.insert(key, candidate)
    result = trie.find_closest_match("apple")
    print(result)
