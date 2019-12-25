#!/usr/bin/env python

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

def gdef(line):
    if line.startswith('grammar '):
        words = line.split(' ')
        if not words[1].endswith(':'):
            return line
        name = words[1][0:-1]
        return 'def %s():' % name
    return line

def define_grammar(source, to_expr=lambda o: o.s):
    src_lines = [gdef(s) for s in source.split('\n')]
    module = ast.parse('\n'.join(src_lines))
    last_line = 0
    lines = []
    for e in module.body:
        if last_line is not None:
            my_lines = '\n'.join(src_lines[last_line:e.lineno-1])
            lines.append(my_lines)

        if isinstance(e, ast.FunctionDef):
            fname = e.name
            grammar = funct_parser(e, to_expr)
            sline = "%s = %s" % (fname, grammar)
            lines.append(sline)
            last_line = None
        else:
            v = e.lineno
            last_line = e.lineno - 1

    my_lines = '\n'.join(src_lines[last_line:])
    lines.append(my_lines)
    return '\n'.join(lines)

def define_ex_grammars(fn):
    return define_grammar(fn, define_expr)

class Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        return (input.encode('utf8'), len(input))

    def decode(self, input, errors='strict'):
        input_string = codecs.decode(input, 'utf8')
        g = define_ex_grammars(input_string)
        return (g, len(input))

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return Codec().encode(input)

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return Codec().decode(input)[0]

class StreamReader(Codec, codecs.StreamReader):
    pass

class StreamWriter(Codec, codecs.StreamWriter):
    pass

def getregentry():
    return codecs.CodecInfo(
        name='cfg',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )
