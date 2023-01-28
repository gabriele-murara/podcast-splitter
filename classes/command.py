import os.path

import eyed3

from classes.abstracts.has_logger import HasLogger
from classes.multiple_file_processor import MultipleFileProcessor
import os
from dotenv import load_dotenv
import tempfile


class Command(HasLogger):

    __track_filename = None
    __tracks_directory = None
    __seconds = 60
    __output_directory = None
    __validation_errors = []
    __files_to_process = []
    __log_filename = ""
    __verbose = False
    logger = None

    def __init__(self, args):
        load_dotenv()

        log_file_path = os.getenv('LOG_FILE_PATH')
        if not log_file_path:
            tmp_path = tempfile.gettempdir()
            log_file_path = os.path.join(tmp_path, "tracce_a_pezzi.log")
        self.__log_filename = log_file_path
        self.__verbose = False
        if args.verbose:
            self.__verbose = args.verbose
        super().__init__(
            self.__class__.__name__, self.__log_filename, self.__verbose
        )
        if not self.verbose:
            msg = "Log messages are written to '{}'. Use --verbose for display "
            msg += "log messages in the standard output"
            print(msg.format(self.__log_filename))

        self.__files_to_process = []
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
        msg = "Collected {} files:".format(len(self.__files_to_process))
        self.logger.info(msg)
        # for audio_file in self.__files_to_process:
        #     msg = "--> '{}'".format(audio_file.path)
        #     self.logger.info(msg)

    def __check_single_audio_file(self, audio_file_path):
        if audio_file_path is not None:
            audio_file = eyed3.load(audio_file_path)
            if audio_file is None:
                msg = "'{}' is not an audio file. Skip it.".format(
                    audio_file_path
                )
                self.logger.warning(msg)
            else:
                self.__files_to_process.append(audio_file)

    def run(self):
        self.__collect_files()
        msg = "Start to process..."
        self.logger.info(msg)
        processor = MultipleFileProcessor(
            self.__files_to_process,
            self.__output_directory,
            self.__seconds,
            self.__log_filename,
            self.__verbose,
        )
        processor.process_files()
