import argparse
import os


class PrintEnvs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        self.print_envs()
        parser.exit()

    def print_envs(self):
        envs = [
            'LOG_FILE_PATH',
            'OUTPUT_DIRECTORY',
            'SPLIT_SECONDS',
            'SPLIT_BY_SILENCE',
            'VERBOSE'
        ]

        for e in envs:
            print("'{}' = {}".format(e, os.getenv(e)))

