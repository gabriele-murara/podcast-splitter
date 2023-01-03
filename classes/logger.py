import logging


class Logger:
    logger = None

    def __init__(self, name):
        if self.logger is None:
            self.logger = logging.getLogger(name)
            self.logger.setLevel(logging.DEBUG)

            fh = logging.FileHandler("/tmp/tap.log")
            fh.setLevel(logging.DEBUG)

            format_tpl = '%(asctime)s %(process)d: %(levelname)s [%(module)s:'
            format_tpl += '%(name)s:%(funcName)s:%(lineno)d] - %(message)s'
            formatter = logging.Formatter(format_tpl)
            fh.setFormatter(formatter)

            self.logger.handlers = []
            self.logger.addHandler(fh)
