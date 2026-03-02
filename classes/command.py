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
    __split_by_silence = False
    __output_directory = None
    __validation_errors = []
    __files_to_process = []
    logger = None

    def __init__(self, **kwargs):
        load_dotenv()

        #####################################################################
        # FIXME attributes to manage
        self.__track_filename = kwargs.get('track_filename', None)
        self.__tracks_directory = kwargs.get('tracks_directory', None)
        self.__seconds = kwargs.get('seconds', 60)
        self.__split_by_silence = kwargs.get('split_by_silence', False)
        self.__output_directory = kwargs.get('output_directory', None)
        self.__validation_errors = kwargs.get('validation_errors', [])
        self.__files_to_process = kwargs.get('files_to_process', [])
        #####################################################################

        log_file_path = os.getenv('LOG_FILE_PATH')
        if not log_file_path:
            tmp_path = tempfile.gettempdir()
            log_file_path = os.path.join(tmp_path, "tracce_a_pezzi.log")

        self.__log_filename = kwargs.get('log_filename', log_file_path)
        self.__verbose = kwargs.get('verbose', False)

        # FIXME fix this constructor
        super().__init__(
            self.__class__.__name__, self.__log_filename, self.__verbose
        )

        if not self.is_verbose():
            msg = "Log messages are written to '{}'. Use --verbose for display "
            msg += "log messages in the standard output"
            print(msg.format(self.__log_filename))

        # FIXME validation doesnt work
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
        if args.by_silence and args.by_silence is True:
            self.__split_by_silence = True
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
        elif not self.__split_by_silence:
            msg = "No seconds passed. Fallback to default {}".format(
                self.__seconds
            )
            self.logger.warn(msg)
        if not self.__split_by_silence and self.__seconds <= 0:
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
            self.__split_by_silence,
        )
        processor.process_files()

    @property
    def track_filename(self):
        return self.__track_filename

    @track_filename.setter
    def track_filename(self, value):
        self.__track_filename = value

    @property
    def tracks_directory(self):
        return self.__tracks_directory

    @tracks_directory.setter
    def tracks_directory(self, value):
        self.__tracks_directory = value

    @property
    def seconds(self):
        return self.__seconds

    @seconds.setter
    def seconds(self, value):
        self.__seconds = value

    @property
    def split_by_silence(self):
        return self.__split_by_silence

    @split_by_silence.setter
    def split_by_silence(self, value):
        self.__split_by_silence = value

    @property
    def output_directory(self):
        return self.__output_directory

    @output_directory.setter
    def output_directory(self, value):
        self.__output_directory = value

    @property
    def validation_errors(self):
        return self.__validation_errors

    @validation_errors.setter
    def validation_errors(self, value):
        self.__validation_errors = value

    @property
    def files_to_process(self):
        return self.__files_to_process

    @files_to_process.setter
    def files_to_process(self, value):
        self.__files_to_process = value

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