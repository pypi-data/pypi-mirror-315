import logging
from logging.handlers import RotatingFileHandler


def set_log(name: str, logfilename: str, level: int = 2,
            prefix: str = '[%(name)s %(asctime)s] -- %(levelname)s: %(message)s',
            datefmt: str = "%Y-%m-%d %H:%M:%S",
            maxBytes: int = 2 * 1024 * 1024, backupCount: int = 3, encoding = "utf-8"):
    """
    创建一个具有指定名称、时间、级别、日志的日志记录器

    level
        - 0 -- logging.NOTSET
        - 1 -- logging.DEBUG
        - 2 -- logging.INFO
        - 3 -- logging.WARNING
        - 4 -- logging.ERROR
        - 5 -- logging.CRITICAL
    :param logfilename: 日志文件路径
    :param level: 日志级别，默认2 -- logging.INFO
    :param encoding: 编码，默认utf-8
    :param maxBytes: 日志文件最大字节数，默认2 * 1024 * 1024（2MB）
    :param backupCount: 备份文件数量，默认3
    :return:
    """
    LOG_LEVEL_LIST = {
        0: logging.NOTSET,
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL,

        logging.NOTSET: logging.NOTSET,
        logging.DEBUG: logging.DEBUG,
        logging.INFO: logging.INFO,
        logging.WARNING: logging.WARNING,
        logging.ERROR: logging.ERROR,
        logging.CRITICAL: logging.CRITICAL
    }

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL_LIST[level])

    formatter = logging.Formatter(prefix, datefmt=datefmt)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    log_file = RotatingFileHandler(filename=logfilename, encoding=encoding, maxBytes=maxBytes, backupCount=backupCount)
    log_file.setFormatter(formatter)

    logger.addHandler(stream)
    logger.addHandler(log_file)

    return logger

