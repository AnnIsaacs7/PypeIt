#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-
"""
This script runs PypeIt
"""
import argparse

from pypeit import msgs

def parser(options=None):
    """
    Parse the command-line arguments.
    """
    args = argparse.ArgumentParser(description=msgs.usage(),
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
    args.add_argument('pypeit_file', type=str,
                      help='PypeIt reduction file (must have .pypeit extension)')
    args.add_argument('-d', '--detector', metavar='D', type=int, nargs='+', default=None,
                      help='One or more detectors to reduce (1-indexed).  If not provided, all '
                           'detectors are reduced.  If the output files exist and -o is used, '
                           'the outputs for the input detector will be replaced.')
    args.add_argument('-p', '--redux_path', type=str,
                      help='Path for output reductions.  Default is the current working '
                           'directory.')
    args.add_argument('-q', '--noqa', dest='qa', default=True, action='store_false',
                      help='Do not produce any qa plots.  Can also set qadir=none (the little n '
                           'is important) in the pypeit file.')
    args.add_argument('-l', '--nolog', dest='log', default=True, action='store_false',
                      help='By default, a log of the printed messages are written to a file '
                           'with the same name as your pypeit file but with a \'.log\' '
                           'extension.  This suppresses output to the log file.  You can also '
                           'change the name of the log file using the \'logfile\' keyword in '
                           'the pypeit file.')
    args.add_argument('-i', '--bad_headers', default=False, action='store_true',
                      help='Ignore headers that do not have the required metadata.  WARNING: '
                           'Use at your own risk.')
    args.add_argument('-m', '--use_masters', default=False, action='store_true',
                      help='Load previously generated MasterFrames')
    args.add_argument('-v', '--verbosity', type=int, default=1,
                      help='Verbosity level between 0 [none] and 2 [all]')
    args.add_argument('-o', '--overwrite', default=False, action='store_true',
                      help='Overwrite any existing files/directories')
    args.add_argument('-s', '--show', default=False, action='store_true',
                      help='Show reduction steps via plots (which will block further execution '
                           'until clicked on) and outputs to ginga. Requires remote control '
                           'ginga session via "ginga --modules=RC &"')
    args.add_argument('-b', '--debug', default=False, action='store_true',
                      help='Show many more reduction steps via matplotlib plots (which will '
                           'block further execution until clicked on).')
    return args.parse_args() if options is None else args.parse_args(options)


def main(args):

    import os
    from IPython import embed

    from pypeit import pypeit
    from pypeit.par.pypeitpar import ExecutionPar

    # Check the input pypeit file name.
    # TODO: Would be better to have some code that makes sure we can
    # actually parse the file they provide as a pypeit file.
    if os.path.splitext(args.pypeit_file)[1] != '.pypeit':
        msgs.error('Bad extension for PypeIt reduction file.  File must end in .pypeit.')

    # Initiate logging for bugs and command line help
    # These messages will not be saved to a log file
    # Set the default variables
#    qck = False
#    cpu = 1
    #vrb = 2

    # JFH I don't see why this is an optional argument here. We could
    # allow the user to modify an infinite number of parameters from
    # the command line? Why do we have the PypeIt file then? This
    # detector can be set in the pypeit file. Detector?

    # KBW: It's useful to have the main control-flow parameters be
    # changed on the command-line instead of having to edit the pypeit
    # file.

    # TODO: Allow spectrograph to be provided as a command-line argument?
    execpar = ExecutionPar(detnum=args.detector, redux_path=args.redux_path,
                           ignore_bad_headers=args.bad_headers, reuse_masters=args.use_masters,
                           verbosity=args.verbosity, overwrite=args.overwrite, show=args.show,
                           debug=args.debug)

    # Report and finalize some parameters
    if args.detector is not None:
        msgs.info("Restricting reductions to detector(s)={}".format(args.detector))

    if not args.qa:
        msgs.info('No QA plots will be produced.')
        execpar['qadir'] = None

    if args.log:
        execpar['logfile'] = pypeit.PypeIt.default_log_file(args.pypeit_file)
    else:
        msgs.info('No logfile will be written.')
        execpar['logfile'] = None

    # Instantiate the main pipeline reduction object
    pypeIt = pypeit.PypeIt(args.pypeit_file, par=execpar)
    # Reduce the data
    pypeIt.reduce_all()
    # Wrap the QA (only done if QA was written)
    pypeIt.build_qa()

    return 0

