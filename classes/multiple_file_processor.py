import os

from boolifyer.booleans import Booleans

from classes.by_silence_single_file_processor import BySilenceSingleFileProcessor
from classes.single_file_processor import SingleFileProcessor


class MultipleFileProcessor:

    def __init__(self, **kwargs):
        self.__audio_files = kwargs.get('audio_files', [])
        self.__seconds = kwargs.get('seconds', None)
        self.__output_directory = kwargs.get('output_directory', None)
        self.__split_by_silence = kwargs.get('split_by_silence', None)
        self.__verbose = kwargs.get(
            'verbose',
            Booleans.to_boolean(os.getenv(
                'NANO_LOGGER_WRITE_TO_CONSOLE', default=False
            ))
        )

    def process_files(self):
        for audio_file in self.__audio_files:
            processing_mapping = {
                'track': audio_file,
                'output_directory': self.__output_directory,
                'seconds': self.__seconds,
                'verbose': self.__verbose
            }
            if self.__split_by_silence:
                processor = BySilenceSingleFileProcessor(**processing_mapping)
                processor.split_track()
            else:
                processor = SingleFileProcessor(**processing_mapping)
                processor.split_track()

    @property
    def audio_files(self):
        return self.__audio_files

    @audio_files.setter
    def audio_files(self, value):
        self.__audio_files = value

    @property
    def seconds(self):
        return self.__seconds

    @seconds.setter
    def seconds(self, value):
        self.__seconds = value

    @property
    def output_directory(self):
        return self.__output_directory

    @output_directory.setter
    def output_directory(self, value):
        self.__output_directory = value

    @property
    def split_by_silence(self):
        return self.__split_by_silence

    @split_by_silence.setter
    def split_by_silence(self, value):
        self.__split_by_silence = value
