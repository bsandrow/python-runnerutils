#!/usr/bin/env python

"""
@PACKAGE runnerutils

@TODO Build a multi-args parser and a subsequent runner base class (i.e. MultiArgRunnerBase)

"""

from optparse   import OptionParser
from sys        import argv,exit

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

    def __init__(self,args=argv):
        """
        A default __init__() which allows the user to forego defining their own
        __init__() in the subclass
        """
        self.parse_args(args)

    def parse_args(self,args=argv):
        """
        Parse the args and jam the result into the attribute namespace. BEWARE!
        This *will* clobber existing values.
        """
        if self._parser is None:
            self._parser_init()

        if args is None:
            raise RunnerError("No args defined")

        (opts,leftovers) = self._parser.parse_args(args)
        self._args       = leftovers
        self.__dict__.update(options.__dict__)

    def _parser_init(self):
        """
        Setup a 'base-state' for parser(s)
        """
        if getattr(self,'options',None) is None:
            raise RunnerError("self.options() not defined")
        opts          = self.options()
        kwargs        = self.parser_opts() if getattr(self,'parser_opts',None) else {}
        self._parser  = self._create_parser(self,kwargs,opts)
        if self._parser is None:
            raise RunnerError("Could not create parser")

    def _create_parser(self,kwargs,options):
        """
        Create a parser from a set of kwargs to pass to the OptionParser()
        constructor, and a list of kwargs to pass to add_option()
        """
        if getattr(self,'options',None) is None:
            raise RunnerError("self.options() not defined")

            parser = OptionParser(**kwargs)
            for option in options:
                args = option['triggers']
                del option['triggers']
                parser.add_option(*args,**option)

class MultiCommandRunnerBase(RunnerBase):

    def parse_args(self,args=argv):
        """
        Process the multi-command arglist. args before the command go to a
        global parser, and args after the command go to the command-specific
        parser.
        """
        if self._parser is None or self._cmdparsers is None:
            self._parser_init()
        if args is None:
            raise RunnerError("No args defined")

        # Parse base options
        (opts,leftovers) = self._parser.parse_args(args)
        self.__dict__.update(opts.__dict__)

        # We need at least one arg to process a command
        if len(leftovers) < 1:
            print "Bad command: "
            self._parser.print_help()
            exit(1)

        # Grab the command and validate it
        self._command = leftovers.pop(0)
        if self._command not in self._cmdparsers.keys():
            print "Bad command: %s" % cmd
            self._parser.print_help()
            exit(1)

        # Process args for command
        (opts,leftovers2) = self._cmdparsers[cmd].parser_args(leftovers)
        self.__dict__.update(opts.__dict__)
        self._args = leftovers2

    def _parser_init(self):
        """
        Setup a base state for the initial parser and each of the command parsers
        """
        if getattr(self,'options',None) is None:
            raise RunnerError('self.options() not defined')
        if getattr(self,'cmd_options',None) is None:
            raise RunnerError('self.cmd_options() not defined')

        # Setup the main parser
        opts         = self.options()
        kwargs       = self.parser_opts() if getattr(self,'parser_opts',None) else {}
        self._parser = self._create_parser(self,kwargs,opts)
        self._parser.disable_interspersed_args()

        # Setup the individual cmd parsers
        cmdopts          = self.cmd_options()
        kwargs           = self.parser_opts() if getattr(self,'parser_opts',None) else {}
        self._cmdparsers = dict()
        for cmd in cmdopts.keys():
            self._cmdparsers[cmd] = self._create_parser(self,kwargs,cmdopts[cmd])
            if self.cmdparsers[cmd] is None:
                raise RunnerError("Could not create parser for command: %s" % cmd)


########
## Exception Classes
##
class RunnerError(Exception):
    pass

class OptionError(Exception):
    pass

if __name__ == '__main__':
    print "You should not be here."
