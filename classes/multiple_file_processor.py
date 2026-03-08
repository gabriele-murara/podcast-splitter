from classes.abstracts.has_logger import HasLogger
from classes.by_silence_single_file_processor import BySilenceSingleFileProcessor
from classes.single_file_processor import SingleFileProcessor


class MultipleFileProcessor(HasLogger):

    def __init__(self, **kwargs):
        self.__log_filename = kwargs.get('log_filename', None)
        self.__verbose = kwargs.get('verbose', None)
        self.__audio_files = kwargs.get('audio_files', [])
        self.__seconds = kwargs.get('seconds', None)
        self.__output_directory = kwargs.get('output_directory', None)
        self.__split_by_silence = kwargs.get('split_by_silence', None)

        super().__init__(
            self.__class__.__name__, self.__log_filename, self.__verbose
        )

    def process_files(self):
        for audio_file in self.__audio_files:
            processing_mapping = {
                'track': audio_file,
                'output_directory': self.__output_directory,
                'log_filename': self.__log_filename,
                'verbose': self.__verbose,
                'seconds': self.__seconds
            }
            if self.__split_by_silence:
                processor = BySilenceSingleFileProcessor(**processing_mapping)
                processor.split_track()
            else:
                processor = SingleFileProcessor(**processing_mapping)
                processor.split_track()

    @property
    def log_filename(self):
        return self.__log_filename

    @log_filename.setter
    def log_filename(self, value):
        self.__log_filename = value

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, value):
        self.__verbose = value

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
