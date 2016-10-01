from . import controller

from flask import Blueprint, render_template, session, request, redirect
import flask
import pprint

top_blueprint = Blueprint('top_blueprint', __name__,
                          template_folder='../templates')


@top_blueprint.route('/')
def game():
    if 'state' not in session:
        session['state'] = controller.new_state()
    return render_template('game.html',
                           current_round=session['state']['current_round'],
                           sentence=session['state']['sentence'],
                           authors=session['state']['authors'],
                           points=session['state']['points'])


@top_blueprint.route('/answer', methods=['POST'])
def answer():
    if 'state' not in session:
        return redirect('/')
    if 'guess' not in request.form:
        return redirect('/')

    guess = request.form['guess']

    # Hack around session.__getitem__ not being updateable
    state = session['state']
    (correct, answer) = controller.make_guess(guess, state)
    session['state'] = state

    if correct:
        return render_template('correct.html',
                               currentRound=session['state']['current_round'],
                               points=session['state']['points'],
                               answer=answer
                               )
    else:
        return render_template('incorrect.html',
                               currentRound=session['state']['current_round'],
                               points=session['state']['points'],
                               answer=answer
                               )


@top_blueprint.route('/reset')
def reset():
    session.clear()
    return redirect('/')
