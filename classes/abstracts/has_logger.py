from classes.logger import Logger


class HasLogger:

    logger = None

    def __init__(self, name):
        if self.logger is None:
            self.logger = Logger(name).logger
