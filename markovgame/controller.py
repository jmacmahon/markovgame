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
    searle = {'name': 'John Searle', 'id': 'searle'}
    chomsky = {'name': 'Noam Chomsky', 'id': 'chomsky'}
    markov = {'name': 'Andrey Markov', 'id': 'markov'}

    answer = chomsky
    sentence = 'Colourless green ideas sleep furiously.'
    authors = [searle, chomsky, markov]

    state['answer'] = answer
    state['sentence'] = sentence
    state['authors'] = authors
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
