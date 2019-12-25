# cfgenc
An encoding that translates context free grammars

Essentially, copy over the `cfg.py` to your
`lib/python_xx/encodings/` directory. If you want to know where that is, use

```
>>> import encodings, os
>>> print(os.path.dirname(encodings.__file__))
```

Once you do that, you will be able to use the encoder to translate files.

E.g.

```python
# coding: cfg

def expression_grammar():
    start   = expr
    expr    = (term + '+' + expr
            |  term + '-' + expr)
    term    = (factor + '*' + term
            |  factor + '/' + term
            |  factor)
    factor  = ('+' + factor
            |  '-' + factor
            |  '(' + expr + ')'
            |  integer + '.' + integer
            |  integer)
    integer = (digit + integer
            |  digit)
    digit   = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
```

Usage:

```python
import g
print(g.expression_grammar)
```

```shell
$ python3 g1.py            
{'start': [('expr',)], 
 'expr': [('term', '+', 'expr'), ('term', '-', 'expr')],
 'term': [('factor', '*', 'term'), ('factor', '/', 'term'), ('factor',)],
 'factor': [('+', 'factor'), ('-', 'factor'), ('(', 'expr', ')'), 
    ('integer', '.', 'integer'), ('integer',)], 
 'integer': [('digit', 'integer'), ('digit',)], 
 'digit': [('0',), ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)]}
```

Or directly: put it in `g.py`

```python
# coding: cfg

def expression_grammar():
    start   = expr
    expr    = (term + '+' + expr
            |  term + '-' + expr)
    term    = (factor + '*' + term
            |  factor + '/' + term
            |  factor)
    factor  = ('+' + factor
            |  '-' + factor
            |  '(' + expr + ')'
            |  integer + '.' + integer
            |  integer)
    integer = (digit + integer
            |  digit)
    digit   = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    
print(expression_grammar)
```

Usage:

```shell
$ python3 g.py
{'start': [('expr',)], 'expr': [('term', '+', 'expr'), ('term', '-', 'expr')], 'term': [('factor', '*', 'term'), ('factor', '/', 'term'), ('factor',)], 'factor': [('+', 'factor'), ('-', 'factor'), ('(', 'expr', ')'), ('integer', '.', 'integer'), ('integer',)], 'integer': [('digit', 'integer'), ('digit',)], 'digit': [('0',), ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)]}
```
