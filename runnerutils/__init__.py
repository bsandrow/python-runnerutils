#!/usr/bin/env python

"""
@PACKAGE runnerutils

@TODO Build a multi-args parser and a subsequent runner base class (i.e. MultiArgRunnerBase)

"""

from optparse   import OptionParser
from sys        import argv

##########
## Legacy Code
##
def validate_options(options):
    """ Validates an option definition sctructure (the one used everywhere in runnerutils) """
    good_keys = [
        'type', 'action', 'dest', 'metavar', 'triggers', 'help', 'default',
        'nargs', 'const', 'callback', 'choices', 'callback_args',
        'callback_kwargs',
    ]
    for option in options:
        if 'triggers' not in option.keys():
            raise OptionError("Missing triggers")

        for key in option.keys():
            if key not in good_keys:
                raise OptionError("Bad key value: %s" % key)

def parse_args(options,args=argv):
    """ Use an option definition structure to parse a bunch of args """
    parser = create_parser(options)
    return parser.parse_args(args)

def create_parser(options):
    """ Build an OptionParser auto-magically out of an option definition """
    validate_options(options)
    parser = OptionParser()
    for option in options:
        args = option['triggers']
        del option['triggers']
        parser.add_option(*args,**option)
    return parser

########
## Runner Base Classes
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

        self.__dict__.update(options.__dict__)

    def create_parser(self):
        if getattr(self,'options',None) is None:
            raise RunnerError("Cannot create a parser: self.options() not defined")

        parser_kwargs = {}
        if getattr(self,'parser_opts',None):
            parser_kwargs = self.parser_opts()

        self.parser = OptionParser(**parser_kwargs)
        for option in self.options():
            args = option['triggers']
            del option['triggers']
            self.parser.add_option(*args,**option)

########
## Exception Classes
##
class RunnerError(Exception):
    pass

class OptionError(Exception):
    pass

if __name__ == '__main__':
    print "You should not be here."
