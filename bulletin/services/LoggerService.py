import logging

class LoggerService():

    @staticmethod
    def console(msg):
        logger = logging.getLogger('console')
        logger.info(msg)

    @staticmethod
    def file(msg):
        logger = logging.getLogger('file')
        logger.info(msg)
