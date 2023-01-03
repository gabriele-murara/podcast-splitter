from classes.abstracts.has_logger import HasLogger
from classes.single_file_processor import SingleFileProcessor


class MultipleFileProcessor(HasLogger):

    __audio_files = []
    __seconds = 60
    __output_directory = None

    def __init__(self, audio_files, output_directory, seconds=60):
        super().__init__(self.__class__.__name__)
        self.__audio_files = audio_files
        self.__seconds = seconds
        self.__output_directory = output_directory

    def process_files(self):
        self.logger.info("Ho {} files".format(len(self.__audio_files)))
        for audio_file in self.__audio_files:
            processor = SingleFileProcessor(
                audio_file, self.__output_directory, self.__seconds
            )
            processor.split_track()
