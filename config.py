# Import libraries needed to display files and operate time.

from pathlib import Path
from IPython.display import FileLink
from IPython.display import IFrame
from os.path import splitext
from datetime import timedelta
from datetime import datetime
import subprocess

# Configure and simplify the Natural Language Toolkit (NTLK) Portuguese treebank.

import nltk
from nltk import tokenize
from nltk.corpus import floresta
def simplify_tag(t):
    if "+" in t:
        return t[t.index("+")+1:]
    else:
        return t
twords = nltk.corpus.floresta.tagged_words()
twords = [(w.lower(),simplify_tag(t)) for (w,t) in twords]

# Insert some missing tagged prepositions.

twords.insert(0,('da','prp'))
twords.insert(0,('de','prp'))
twords.insert(0,('di','prp'))
twords.insert(0,('do','prp'))
twords.insert(0,('du','prp'))

# Define ```title_pos_tag``` function that is similar to ```title``` built-in function but doesn't capitalize ```text``` input string conjunctions and prepositions. It is useful when titling proper names.

def title_pos_tag(text):
    def pos_tag_portuguese(tokens):
        for index in range(len(tokens)):
            for word in twords:
                token = tokens[index].lower()
                if word[0] == token:
                    tag = word[1]
                    tokens[index] = (token, tag)
                    break
        return tokens
    tokens = tokenize.word_tokenize(text, language='portuguese')
    tagged = pos_tag_portuguese(tokens)
    new_text = ''
    for index in range(len(tagged)):
        token = tagged[index]
        if isinstance(token, tuple):
            word = token[0]
            tag  = token[1]
            # n:         substantivo
            # prop:      nome próprio
            # art:       artigo
            # pron:      pronome
            # pron-pers: pronome pessoal
            # pron-det:  pronome determinativo
            # pron-indp: substantivo/pron-indp
            # adj:       adjetivo
            # n-adj:     substantivo/adjetivo
            # v:         verbo
            # v-fin:     verbo finitivo
            # v-inf:     verbo infinitivo
            # v-pcp:     verbo particípio
            # v-ger:     verbo gerúndio
            # num:       numeral
            # prp:       preposição
            # adj:       adjetivo
            # conj:      conjunção
            # conj-s:    conjunção subordinativa
            # conj-c:    conjunção coordenativa
            # intj:      interjeição
            # adv:       advérbio
            # xxx:       outro
            if 'conj' in tag or \
               'prp'  in tag:
                new_text = new_text + ' ' + word.lower()
            else:
                new_text = new_text + ' ' + word.capitalize()
        else:
            new_text = new_text + ' ' + token.capitalize()
    new_text = new_text.strip()
#     return (new_text, tagged) # uncomment this line if is desired to retriev the tags as well
    return new_text

# Create ```showJSON``` object that shows an expandable JSON file ```json_data``` content (*credits to [David Caldwell](https://github.com/caldwell/renderjson)*)

import uuid, json
from IPython.display import HTML, display

class showJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        htmlstr = """
        <html>
            <head>
                <style>
                    .renderjson a              {{ text-decoration: none; }}
                    .renderjson .disclosure    {{ color: crimson;
                                                  font-size: 150%; }}
                    .renderjson .syntax        {{ color: grey; }}
                    .renderjson .string        {{ color: red; }}
                    .renderjson .number        {{ color: blue; }}
                    .renderjson .boolean       {{ color: plum; }}
                    .renderjson .key           {{ color: blue; }}
                    .renderjson .keyword       {{ color: goldenrodyellow; }}
                    .renderjson .object.syntax {{ color: seagreen; }}
                    .renderjson .array.syntax  {{ color: salmon; }}
                </style>
            </head>
            <body>
                <div id="{0}" style="height: 600px; width:100%;"></div>
                <script>
                    require(["renderjson.js"], function() {{
                        renderjson.set_show_to_level('all');
                        document.getElementById('{0}').appendChild(renderjson({1}))
                    }});
                </script>
            </body>
        </html>
        """.format(self.uuid, self.json_str)
        display(HTML(htmlstr))

# Define the week names list.

week_names = ('segunda','terça','quarta','quinta','sexta','sábado','domingo')