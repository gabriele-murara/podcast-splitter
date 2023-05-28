import argparse

from classes.command import Command


parser = argparse.ArgumentParser(
    prog='Tracce a Pezzi',
    description='A program that splits auto tracks and apply metadata',
    epilog='Text at the bottom of help'
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
    command = Command(args)
    command.run()

