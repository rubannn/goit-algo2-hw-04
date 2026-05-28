from trie import Trie


class Homework(Trie):
    pass


def run_tests(trie) -> None:
    # Перевірка кількості слів, що закінчуються на заданий суфікс.
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса.
    assert trie.has_prefix("app")  # apple, application
    assert not trie.has_prefix("bat")
    assert trie.has_prefix("ban")  # banana
    assert trie.has_prefix("ca")  # cat

    print("All tests passed.")


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    run_tests(trie)
