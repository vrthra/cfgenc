import codecs
import re
import ast

def define_name(o):
    return o.id if isinstance(o, ast.Name) else o.s

def get_alternatives(op, to_expr=lambda o: o.s):
    if isinstance(op, ast.BinOp) and isinstance(op.op, ast.BitOr):
        return get_alternatives(op.left, to_expr) + [to_expr(op.right)]
    return [to_expr(op)]

def funct_parser(tree, to_expr=lambda o: o.s):
    return {assign.targets[0].id: get_alternatives(assign.value, to_expr) for assign in tree.body}

def define_expr(op):
    if isinstance(op, ast.BinOp) and isinstance(op.op, ast.Add):
        return (*define_expr(op.left), define_name(op.right))
    return (define_name(op),)

def define_grammar(source, to_expr=lambda o: o.s):
    module = ast.parse(source)
    my_grammars = []
    for e in module.body:
        if isinstance(e, ast.FunctionDef):
        # we only want to look at function definitions.
            fname = e.name
            grammar = funct_parser(e, to_expr)
            my_grammars.append("%s = %s" % (fname, grammar))
    return my_grammars

def define_ex_grammars(fn):
    return "\n".join(define_grammar(fn, define_expr))

class CFGCodec(codecs.Codec):
    def encode(self, input, errors='strict'):
        return (input.encode('utf8'), len(input))

    def decode(self, input, errors='strict'):
        input_string = codecs.decode(input, 'utf8')
        g = define_ex_grammars(input_string)
        return (g, len(input))

class CFGIncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return CFGCodec().encode(input)

class CFGIncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return CFGCodec().decode(input)

class CFGStreamReader(CFGCodec, codecs.StreamReader):
    pass

class CFGStreamWriter(CFGCodec, codecs.StreamWriter):
    pass

def search(encoding):
    if encoding == "cfg":
        return codecs.CodecInfo(
            name='cfg',
            encode=CFGCodec().encode,
            decode=CFGCodec().decode,
            incrementalencoder=CFGIncrementalEncoder,
            incrementaldecoder=CFGIncrementalDecoder,
            streamreader=CFGStreamReader,
            streamwriter=CFGStreamWriter,
        )
    return None

codecs.register(search)
