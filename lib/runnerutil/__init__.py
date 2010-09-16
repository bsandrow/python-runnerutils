from optparse   import OptionParser
from sys        import argv

"""
@PACKAGE runnerutil
"""

########
## Validates an optspec structure
##
def validate(optspec):
    good_keys = [
        'type', 'action', 'dest', 'metavar', 'trigger', 'help', 'default',
        'nargs', 'const', 'callback', 'choices', 'callback_args',
        'callback_kwargs',
    ]
    for optdef in optspec:
        if 'triggers' not in optdef.keys():
            raise OptSpecError("Missing triggers")
        for key in optdef.keys():
            if key not in good_keys:
                raise OptSpecError("Bad key value: %s" % key)

########
## Push a set of args through an optspec-built OptionParser and return the
## result.
##
def parse_args(optspec,args=argv):
    parser = create_parser_from_optspec(optspec)
    return parser.parse_args(args)

########
## Build a OptionParser out of an optspec
##
def create_parser(optspec):
    parser = OptionParser()
    for optdef in optspec:
        args = optdef['triggers']
        del optdef['triggers']
        parser.add_option(*args,**optdef)
    return parser


########
## Base Class for Runners
##
class RunnerBase(object):
    parse_ns = dict()       # a namespace for arg processing vars (useful for allowing subclasses to change behavior)
    parser   = None         # parser

    def __init__(self,args=argv):
        self.parse_args(args)

    def parse_args(self,args):
        if args is not None:
            self.parse_ns['unparsed_args'] = args

        if self.parser is None:
            self.create_parser()

        if self.parser is None:
            raise RunnerError("No parser defined")

        if self.parse_ns['unparsed_args'] is None:
            raise RunnerError("No args defined")

        (options,args_left) = self.parser.parse_args(args)
        self.parse_ns['parsed_options'] = options
        self.parse_ns['leftover_args']  = args_left

    def create_parser(self):
        if getattr(self,'optspec',None) is None:
            raise RunnerError("Cannot create a parser: self.optspec() not defined")

        parser_kwargs = {}
        if getattr(self,'parser_opts',None):
            parser_kwargs = self.parser_opts()

        self.parser = OptionParser(**parser_kwargs)
        for optdef in self.optspec():
            args = optdef['triggers']
            del optdef['triggers']
            self.parser.add_option(*args,**kwargs)


class RunnerError(Exception):
    pass

class OptSpecError(Exception):
    pass
