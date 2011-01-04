#!python
# -*- coding: utf-8 -*-


import logging
import sys

class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logging.getLogger('crocad').addHandler(NullHandler())

from crocad import donut, ball


__all__ = ['main']


log = logging.getLogger('crocad')


COMMAND_ALIASES = {
    'torus': 'donut',
    'sphere': 'ball',
}


def find_command(command):
    """
    Attempts to find an imported module with the name `command`, and then
    obtains and returns that moule's `main` function.
    """
    command = COMMAND_ALIASES.get(command, command)
    
    command_module = globals().get(command)
    if hasattr(command_module, 'main'):
        return getattr(command_module, 'main')
    else:
        raise Exception('Unknown command: %s' % command)


def main(argv=sys.argv[1:]):
    """
    Crochet CAD's command-line entry-point.
    """
    import optparse
    
    op = optparse.OptionParser("""%prog [-va] COMMAND [COMMAND-OPTIONS]
  
Help:
  %prog --help
  %prog COMMAND --help""",
description="""
Generate a crochet pattern for a geometric primitive, specified as COMMAND.
Supported commands are 'ball' and 'donut'. For details of options for a
specific command, run '%prog COMMAND --help' with the name of the command.
""".strip()
)
    op.disable_interspersed_args()
    
    og = optparse.OptionGroup(op, 'Global Options',
    'Global options must be provided before the name of the crochet-cad'
    ' command. They can be used for any crochet-cad command.')
    og.add_option('-v', '--verbose', action='count', default=0,
        help='print out extra information - only really used for debugging.')
    og.add_option('-a', '--accurate', action='store_true', default=False,
        help='generate an exact pattern'
        ' which may not produce such an even end-product.')
    op.add_option_group(og)
    
    global_options, args = op.parse_args(argv)
    
    logging.basicConfig()
    logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
    if global_options.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif global_options.verbose > 1:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if args:
        command = args.pop(0)
        find_command(command)(args, global_options)
    else:
        op.error('No command was provided.')


if __name__ == '__main__':
    main()