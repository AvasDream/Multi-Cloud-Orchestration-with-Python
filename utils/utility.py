import logging

def init_logging(name, filemode="w"):
    logging.basicConfig(filename="automation.log",
                        filemode=filemode,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger = logging.getLogger(name)
    return logger
