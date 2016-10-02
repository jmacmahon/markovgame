from random import randint


class Generator(object):
    def __init__(self, total_sentences, sentence_start_frequencies, counts):
        self._total_sentences = total_sentences
        self._sentence_start_frequencies = sentence_start_frequencies
        self._counts = counts

        self._process_table()

    def _process_table(self):
        self._sentence_start_picker = make_random_picker(
            self._sentence_start_frequencies)
        counts_pickers = {}
        for (word, word_data) in self._counts.items():
            picker = make_random_picker(word_data['words'])
            counts_pickers[word] = {'total': word_data['total'],
                                    'picker': picker}
        self._counts_pickers = counts_pickers

    def start_word(self):
        return pick(self._sentence_start_picker, self._total_sentences)

    def next_word(self, prev_word):
        try:
            picker = self._counts_pickers[prev_word]['picker']
            total = self._counts_pickers[prev_word]['total']
            return pick(picker, total)
        except KeyError:
            return '.'

    def __iter__(self):
        prev = self.start_word()
        yield prev
        while not prev == '.':
            prev = self.next_word(prev)
            yield prev


def make_random_picker(frequencies):
    picker = {}
    i = 0
    for (item, count) in frequencies.items():
        picker[i] = item
        i += count
    return picker


def pick(picker, total):
    number = randint(0, total - 1)
    found = False
    while number >= 0:
        try:
            return picker[number]
        except KeyError:
            number -= 1
    raise ValueError('Number not found in picker')


NO_SPACE_BEFORE_WORDS = ["''", "'", ',', '.', ':', ';', ')', "'s", "n't", "'m",
                         "'re", '!', '%', '?']
NO_SPACE_AFTER_WORDS = ['``', '`', '(']
REPLACEMENTS = {'``': '“', "''": '”', '`': '‘', "'": '’'}


def replace(word):
    try:
        return REPLACEMENTS[word]
    except KeyError:
        return word


def format(generator):
    sentence = ""
    no_space = False
    for word in generator:
        if word in NO_SPACE_BEFORE_WORDS:
            sentence += replace(word)
        else:
            if not no_space:
                sentence += ' '
            no_space = False
            if word in NO_SPACE_AFTER_WORDS:
                no_space = True
                sentence += replace(word)
            else:
                sentence += replace(word)
    return sentence.strip()
