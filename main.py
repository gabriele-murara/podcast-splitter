import argparse

from classes.command import Command
from version import get_app_name, get_version

parser = argparse.ArgumentParser(
    prog='Podcast Splitter',
    description='A program that splits audio tracks and apply metadata',
    epilog='Text at the bottom of help'
)

parser.add_argument(
    '--version',
    help='Shows version number',
    action='version',
    version='{} - v. {}'.format(
        get_app_name(), get_version()
    )
)

parser.add_argument(
    '-f', '--filename', help="The filename of the track to split"
)
parser.add_argument(
    '-d', '--directory', help="The directory of tracks to split"
)
parser.add_argument(
    '-s',
    '--seconds',
    type=int,
    default=60,
    help="The number of seconds of each splitted track"
)

by_silence_help = "Split the track by silence. If this flag is passed, "
by_silence_help += "--seconds is skipped."
parser.add_argument(
    '-b',
    '--by-silence',
    action='store_true',
    help=by_silence_help
)
parser.add_argument(
    '-o',
    '--output',
    help="The destination directory of splitted files",
    required=True
)

parser.add_argument(
    '-v',
    '--verbose',
    help='Shows logs messages to console',
    action='store_true',
    required=False
)

if __name__ == '__main__':
    args = parser.parse_args()
    command = Command(**vars(args))
    command.run()

