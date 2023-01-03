import os.path

import eyed3

from classes.abstracts.has_logger import HasLogger
from classes.multiple_file_processor import MultipleFileProcessor


class Command(HasLogger):

    __track_filename = None
    __tracks_directory = None
    __seconds = 60
    __output_directory = None
    __validation_errors = []
    __files_to_precess = []
    logger = None

    def __init__(self, args):
        super().__init__(self.__class__.__name__)
        self.__files_to_precess = []
        if not self.__validate(args):
            msg = "{} validation errors detected:".format(
                len(self.__validation_errors)
            )
            self.logger.error(msg)
            for msg in self.__validation_errors:
                self.logger.error(msg)

            self.logger.error("exit(1)")
            exit(1)

    def __validate(self, args):
        self.__validation_errors = []
        is_valid = True
        if args.filename is not None:
            self.__track_filename = args.filename
        if args.directory is not None:
            self.__tracks_directory = args.directory
        if args.seconds is not None:
            try:
                self.__seconds = int(args.seconds)
            except ValueError as vex:
                msg = "Passed seconds '{}' is not a valid value. It must be "
                msg += "a positive integer number. Details: {}"
                msg = msg.format(args.seconds, str(vex))
                self.__validation_errors.append(msg)
                is_valid = False
            except Exception as ex:
                msg = "An error occurred during parse seconds '{}'. Details {}"
                msg = msg.format(args.seconds, str(ex))
                self.__validation_errors.append(msg)
                is_valid = False
        else:
            msg = "No seconds passed. Fallback to default {}".format(
                self.__seconds
            )
            self.logger.warn(msg)
        if self.__seconds <= 0:
            msg = "Passed seconds '{}' is not a valid value. It must be "
            msg += "a positive integer number."
            msg = msg.format(args.seconds)
            self.__validation_errors.append(msg)
            is_valid = False
        if args.output is not None:
            self.__output_directory = args.output
        else:
            is_valid = False
            msg = "No 'output' passed. Cannot process."
            self.__validation_errors.append(msg)
        file_path = self.__track_filename
        dir_path = self.__tracks_directory
        if file_path is None and dir_path is None:
            is_valid = False
            msg = "No 'filename' or 'directory' passed. Cannot process."
            self.__validation_errors.append(msg)
        elif file_path is not None and not os.path.isfile(file_path):
            is_valid = False
            msg = "Passed filename '{}' is not a valid file".format(
                file_path
            )
            self.__validation_errors.append(msg)
        elif dir_path is not None and not os.path.isdir(dir_path):
            is_valid = False
            msg = "Passed directory '{}' is not a valid directory".format(
                dir_path
            )
            self.__validation_errors.append(msg)

        if file_path is not None and dir_path is not None:
            msg = "Both 'filename' and 'directory' passed. Merge 'filename' "
            msg += "'{}' with files into directory '{}'"
            self.logger.warn(msg.format(file_path, dir_path))
        return is_valid

    def __collect_files(self):
        msg = "Start to collect audio files..."
        self.logger.info(msg)
        self.__check_single_audio_file(self.__track_filename)
        if self.__tracks_directory is not None:
            for filename in os.listdir(self.__tracks_directory):
                file = os.path.join(self.__tracks_directory, filename)
                if os.path.isfile(file):
                    self.__check_single_audio_file(file)
        msg = "Collected {} files:".format(len(self.__files_to_precess))
        self.logger.info(msg)
        for audio_file in self.__files_to_precess:
            msg = "--> '{}'".format(audio_file.path)
            self.logger.info(msg)

    def __check_single_audio_file(self, audio_file_path):
        if audio_file_path is not None:
            audio_file = eyed3.load(audio_file_path)
            if audio_file is None:
                msg = "'{}' is not an audio file. Skip it.".format(
                    audio_file_path
                )
                self.logger.warning(msg)
            else:
                self.__files_to_precess.append(audio_file)

    def run(self):
        self.__collect_files()
        msg = "Start to process..."
        self.logger.info(msg)
        processor = MultipleFileProcessor(
            self.__files_to_precess, self.__output_directory, self.__seconds
        )
        processor.process_files()
