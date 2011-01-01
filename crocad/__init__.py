#!python
# -*- coding: utf-8 -*-


import logging
import sys

from crocad import donut


__all__ = ['main']


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
    
    op = optparse.OptionParser("""
%prog [-v] donut --inner-radius=STITCHES --row-count=ROWS
""")
    op.disable_interspersed_args()
    
    op.add_option('-v', '--verbose', action='count', default=0)
    global_options, args = op.parse_args(argv)
    
    if global_options.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif global_options.verbose > 2:
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