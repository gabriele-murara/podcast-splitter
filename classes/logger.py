import os
import logging
import tempfile


class Logger:
    logger = None
    verbose = False

    def __init__(self, name, log_filename="", verbose=False):
        if self.logger is None:
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)

            if log_filename == '':
                tmp_path = tempfile.gettempdir()
                log_filename = os.path.join(tmp_path, "tracce_a_pezzi.log")

            is_file_writable = False
            try:
                file = open(log_filename, "a")
                is_file_writable = file.writable()
            except FileNotFoundError as fe:
                is_file_writable = False
                msg = "A {} error occurred. Details: {}".format(
                    fe.__class__.__name__, str(fe)
                )
                print(msg)
            except Exception as e:
                is_file_writable = False
                msg = "A {} error occurred. Details: {}".format(
                    e.__class__.__name__, str(e)
                )
                print(msg)

            self.logger.handlers = []

            if not is_file_writable:
                msg = "Log file {} is not writable. Check your .env file or "
                msg += "set the environment variable LOG_FILE_PATH. Log "
                msg += "messages will be written to the standard output"
                print(msg.format(log_filename))
                verbose = True
            else:
                fh = logging.FileHandler(log_filename)
                fh.setLevel(logging.DEBUG)

                format_tpl = '%(asctime)s %(process)d: %(levelname)s [%(module)s:'
                format_tpl += '%(name)s:%(funcName)s:%(lineno)d] - %(message)s'
                formatter = logging.Formatter(format_tpl)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

            if verbose:
                console = logging.StreamHandler()
                console_format_tpl = '%(asctime)s [%(levelname)s] - %(message)s'
                console_formatter = logging.Formatter(console_format_tpl)
                console.setFormatter(console_formatter)
                self.logger.addHandler(console)

            self.verbose = verbose

    def is_verbose(self):
        return self.verbose
