from random import randint


class Generator(object):
    def __init__(self, total_sentences, sentence_start_picker, counts_pickers):
        self._total_sentences = total_sentences
        self._sentence_start_picker = sentence_start_picker
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
