from nltk.tokenize import word_tokenize
from string import punctuation


punctuation_strip_mapper = dict([(ord(c), None) for c in punctuation + "“‘’”"])
del punctuation_strip_mapper[ord('.')]


class Trainer(object):
    def __init__(self, training_text):
        self._training_text = training_text

    def _tokenize(self):
        stripped = self._training_text.translate(punctuation_strip_mapper)
        self._words = word_tokenize(stripped)

    def _count_words(self):
        counts = {}
        base_frequencies = {}
        total_words = 0
        for (first, second) in double_iterate(self._words):
            if not first in counts:
                counts[first] = {'total': 1, 'words': {second: 1}}
            elif not second in counts[first]['words']:
                counts[first]['words'][second] = 1
                counts[first]['total'] += 1
            else:
                counts[first]['words'][second] += 1
                counts[first]['total'] += 1

            if not first in base_frequencies:
                base_frequencies[first] = 1
            else:
                base_frequencies[first] += 1
            total_words += 1
        self._counts = counts
        self._base_frequencies = base_frequencies
        self._total_words = total_words

    def _process_table(self):
        pass

    def train(self):
        self._tokenize()
        self._count_words()
        self._process_table()


def make_random_picker(frequencies):
    picker = {}
    i = 0
    for (item, count) in frequencies.items():
        picker[i] = item
        i += count
    return picker


def double_iterate(iterable_):
    iterator = iter(iterable_)
    first, second = next(iterator), next(iterator)
    yield first, second
    while True:
        first, second = second, next(iterator)
        yield first, second
