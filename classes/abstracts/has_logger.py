from classes.logger import Logger


class HasLogger:

    logger = None
    verbose = False

    def __init__(self, name, log_filename, verbose=False):
        if self.logger is None:
            log = Logger(name, log_filename, verbose)
            self.logger = log.logger
            self.verbose = log.is_verbose()
