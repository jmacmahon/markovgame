from flask import Flask, render_template, session, request, redirect
import flask
import pprint

app = Flask(__name__)
app.secret_key = b'\xf9\xd1ct\x02[KkcM KEs\x99\xd3\x9a{2>"\xde\xf3\xcad2\xb6I\xda\x03\xac\x88\xd3\xeaG\xbe\xff\xb3\xc6%\x98\xdc\xda\xe2\x0fE\x06fgpSgo9\xf0\x1bp\x7f\x8d"Qc\xa9\xf6'

@app.route('/')
def game():
    if 'init' not in session:
        session['init'] = True
        session['currentRound'] = 1
        session['answers'] = {}
        session['points'] = 0
        session['lastAnsweredRound'] = 0
    elif session['lastAnsweredRound'] == session['currentRound']:
        session['currentRound'] += 1
    
    currentRound = session['currentRound']

    searle = {'name': 'John Searle', 'id': 'searle'}
    chomsky = {'name': 'Noam Chomsky', 'id': 'chomsky'}
    markov = {'name': 'Andrey Markov', 'id': 'markov'}

    answer = chomsky
    sentence = 'Colourless green ideas sleep furiously.'
    
    session['answers'][str(currentRound)] = answer
    
    return render_template('game.html',
                           currentRound = session['currentRound'],
                           sentence = sentence,
                           authors = [searle, chomsky, markov],
                           points = session['points']
                           )

@app.route('/answer', methods = ['POST'])
def answer():
    if 'init' not in session:
        return redirect('/')
    if 'guess' not in request.form:
        return redirect('/')
    
    currentRound = session['currentRound']
    answer = session['answers'][str(currentRound)]
    guess = request.form['guess']
    correct = guess == answer['id']

    if not (session['lastAnsweredRound'] == session['currentRound']):
        session['lastAnsweredRound'] = session['currentRound']
        if correct:
            session['points'] += 1
        else:
            session['points'] -= 1

    if correct:
        return render_template('correct.html',
                               currentRound = currentRound,
                               points = session['points'],
                               answer = answer
                               )
    else:
        return render_template('incorrect.html',
                               currentRound = currentRound,
                               points = session['points'],
                               answer = answer
                               )

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
