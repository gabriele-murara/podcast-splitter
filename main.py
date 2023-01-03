import argparse

from classes.command import Command
from classes.single_file_processor import SingleFileProcessor


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
parser.add_argument(
    '-o',
    '--output',
    help="The destination directory of splitted files",
    required=True
)


if __name__ == '__main__':
    args = parser.parse_args()
    command = Command(args)
    command.run()
    # print(args)
    # path = "/media/gabriele/DOCUMENTI/Development/TracceAPezziWorkspace/20221116215626_radio_bomboclat_16112022.mp3"
    # processor = SingleFileProcessor(path)
    # processor.split_tracks()

