# cfgenc
An encoding that translates context free grammars

Essentially, copy over the `cfg.pth` and cfgencoding to your
`lib/python_xx/site-packages/` directory. Once you do that, you will
be able to use the encoder to translate files.

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

Unfortunately, this only works if you import it in another file.

```python
import g
print(g.expression_grammar)
```
