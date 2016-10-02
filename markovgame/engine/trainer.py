from nltk.tokenize import word_tokenize
from string import punctuation

punctuation_strip_mapper = dict(
    [(ord(c), None) for c in punctuation + "“‘’”–"])
del punctuation_strip_mapper[ord('.')]


class Trainer(object):
    def __init__(self, training_text):
        self._training_text = training_text
        self._trained = False

    def _tokenize(self):
        ugly_print = self._training_text.translate(dict(
            [(ord(i), o) for (i, o) in zip("“‘’”–", "\"''\"-")]
        ))
        self._words = word_tokenize(ugly_print)

    def _count_words(self):
        counts = {}
        sentence_start_frequencies = {}
        total_sentences = 0
        for (first, second) in double_iterate(self._words):
            if first not in counts:
                counts[first] = {'total': 1, 'words': {second: 1}}
            elif second not in counts[first]['words']:
                counts[first]['words'][second] = 1
                counts[first]['total'] += 1
            else:
                counts[first]['words'][second] += 1
                counts[first]['total'] += 1

            if first == '.':
                if second not in sentence_start_frequencies:
                    sentence_start_frequencies[second] = 1
                else:
                    sentence_start_frequencies[second] += 1
                total_sentences += 1
        self._counts = counts
        self._sentence_start_frequencies = sentence_start_frequencies
        self._total_sentences = total_sentences

    def _process_table(self):
        self._sentence_start_picker = make_random_picker(
            self._sentence_start_frequencies)
        counts_pickers = {}
        for (word, word_data) in self._counts.items():
            picker = make_random_picker(word_data['words'])
            counts_pickers[word] = {'total': word_data['total'],
                                    'picker': picker}
        self._counts_pickers = counts_pickers

    def train(self):
        self._tokenize()
        self._count_words()
        self._process_table()
        self._trained = False

    @property
    def compiled(self):
        if not self._trained:
            self.train()
        return {'total_sentences': self._total_sentences,
                'sentence_start_picker': self._sentence_start_picker,
                'counts_pickers': self._counts_pickers}


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
