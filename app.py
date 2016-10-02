from markovgame.views import top_blueprint
from markovgame.controller import ROUND_GEN

from flask import Flask

searle = {'name': 'John Searle', 'id': 'searle'}
chomsky = {'name': 'Noam Chomsky', 'id': 'chomsky'}
markov = {'name': 'Andrey Markov', 'id': 'markov'}
gen = lambda: (yield '.')
ROUND_GEN.register_author(generator=gen(), **searle)
ROUND_GEN.register_author(generator=gen(), **chomsky)
ROUND_GEN.register_author(generator=gen(), **markov)

app = Flask(__name__)
app.secret_key = b'''\xf9\xd1ct\x02[KkcM KEs\x99\xd3\x9a{2>"\xde\xf3\xcad2\xb6I
\xda\x03\xac\x88\xd3\xeaG\xbe\xff\xb3\xc6%\x98\xdc\xda\xe2\x0fE\x06fgpSgo9\xf0
\x1bp\x7f\x8d"Qc\xa9\xf6'''

app.register_blueprint(top_blueprint)

app.run(debug=True, host='0.0.0.0')
