from . import cfg

import sys, codecs
if sys.stdout.encoding != 'cfg':
    sys.stdout = codecs.getwriter('cfg')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'cfg':
    sys.stderr = codecs.getwriter('cfg')(sys.stderr.buffer, 'strict')
