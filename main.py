import argparse
import os

from boolifyer.booleans import Booleans

from classes.command import Command
from classes.print_envs_action import PrintEnvs
from version import get_app_name, get_version
from dotenv import load_dotenv

load_dotenv()

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
    '-f',
    '--filename',
    required=True,
    help="The filename of the track to split"
)
parser.add_argument(

    '-d',
    '--directory',
    help="The directory of tracks to split",
    required=False
)
parser.add_argument(
    '-s',
    '--seconds',
    type=int,
    required=False,
    default=60,
    help="The number of seconds of each splitted track"
)

by_silence_help = "Split the track by silence. If this flag is passed, "
by_silence_help += "--seconds is skipped."
parser.add_argument(
    '-b',
    '--by-silence',
    action='store_true',
    required=False,
    default=Booleans.to_boolean(os.getenv('SPLIT_BY_SILENCE', default=False)),
    help=by_silence_help
)
parser.add_argument(
    '-o',
    '--output',
    help="The destination directory of splitted files",
    required=False,
    default=(os.getenv('OUTPUT_DIRECTORY', default=None))
)

parser.add_argument(
    '-v',
    '--verbose',
    help='Shows logs messages to console',
    action='store_true',
    required=False,
    default=Booleans.to_boolean(os.getenv('VERBOSE', default=False))
)

parser.add_argument(
    '--envs',
    help='Print environments',
    action=PrintEnvs,
    nargs=0,
    required=False
)


if __name__ == '__main__':

    args = parser.parse_args()
    var_args = vars(args)
    command = Command(**var_args)
    command.run()

