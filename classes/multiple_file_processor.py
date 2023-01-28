from classes.abstracts.has_logger import HasLogger
from classes.single_file_processor import SingleFileProcessor


class MultipleFileProcessor(HasLogger):

    __audio_files = []
    __seconds = 60
    __output_directory = None
    __log_filename = ""
    __verbose = False

    def __init__(
            self,
            audio_files,
            output_directory,
            seconds=60,
            log_filename="",
            verbose=False
    ):
        super().__init__(self.__class__.__name__, log_filename, verbose)
        self.__log_filename = log_filename
        self.__verbose = verbose
        self.__audio_files = audio_files
        self.__seconds = seconds
        self.__output_directory = output_directory

    def process_files(self):
        for audio_file in self.__audio_files:
            processor = SingleFileProcessor(
                audio_file,
                self.__output_directory,
                self.__seconds,
                self.__log_filename,
                self.__verbose
            )
            processor.split_track()
