import argparse
import os

from boolifyer.booleans import Booleans

from podcast_splitter.classes.command import Command
from podcast_splitter.classes.print_envs_action import PrintEnvs
from podcast_splitter.version import get_app_name, get_version
from dotenv import load_dotenv

def main():

    load_dotenv()

    parser = argparse.ArgumentParser(
        prog='Podcast Splitter',
        description='A program that splits audio tracks and applies metadata.'
    )

    parser.add_argument(
        '--version',
        help='Show the version number',
        action='version',
        version='{} - v. {}'.format(
            get_app_name(), get_version()
        )
    )

    parser.add_argument(
        '-f',
        '--filename',
        required=True,
        help="The filename of the track to split."
    )
    parser.add_argument(
        '-d',
        '--directory',
        help="The directory containing tracks to split.",
        required=False
    )

    parser.add_argument(
        '-s',
        '--seconds',
        type=int,
        required=False,
        default=60,
        help="The duration in seconds of each split track."
    )

    by_silence_help = "Split the track by detected silence. If this flag is "
    by_silence_help += "used, --seconds is ignored."
    parser.add_argument(
        '-b',
        '--by-silence',
        action='store_true',
        required=False,
        default=Booleans.to_boolean(
            os.getenv('SPLIT_BY_SILENCE', default=False)),
        help=by_silence_help
    )
    parser.add_argument(
        '-o',
        '--output_directory',
        help="The destination directory for split files.",
        required=False,
        default=(os.getenv('OUTPUT_DIRECTORY', default=None))
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help='Show log messages in the console.',
        action='store_true',
        required=False,
        default=Booleans.to_boolean(os.getenv(
            'NANO_LOGGER_WRITE_TO_CONSOLE', default=False
        ))
    )

    parser.add_argument(
        '--envs',
        help='Print environment variables.',
        action=PrintEnvs,
        nargs=0,
        required=False
    )

    args = parser.parse_args()
    var_args = vars(args)
    command = Command(**var_args)
    command.run()

