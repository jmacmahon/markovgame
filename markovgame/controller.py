from itertools import permutations, combinations
from random import choice
from .engine.generator import format


class RoundGenerator(object):
    def __init__(self):
        self._authors = {}
        self._generators = {}

    def register_author(self, name, id, generator):
        self._authors[id] = {'name': name, 'id': id}
        self._generators[id] = generator

    def get_permutation(self, n):
        combs = list(combinations(self._authors.values(), n))
        combination = choice(combs)
        perms = list(permutations(combination))
        perm = choice(perms)
        return perm

    def generate_sentence(self, perm):
        answer = choice(perm)
        sentence = format(self._generators[answer['id']])
        return (answer, sentence)

ROUND_GEN = RoundGenerator()


def new_state():
    state = {
        'current_round': 0,
        'sentence': '',
        'authors': [],
        'points': 0,
        'answer': ''
    }
    generate_round(state)
    return state


def generate_round(state):
    perm = ROUND_GEN.get_permutation(3)
    answer, sentence = ROUND_GEN.generate_sentence(perm)

    state['answer'] = answer
    state['sentence'] = sentence
    state['authors'] = perm
    state['current_round'] += 1


def make_guess(guess, state):
    old_answer = state['answer']
    if guess == old_answer['id']:
        state['points'] += 1
        generate_round(state)
        return (True, old_answer)
    else:
        state['points'] -= 1
        generate_round(state)
        return (False, old_answer)
