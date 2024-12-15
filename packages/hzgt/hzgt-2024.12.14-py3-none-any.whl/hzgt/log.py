import logging
import re
import sys
import time

try:
    import curses
except:
    curses = None


PY3 = sys.version_info[0] >= 3

if PY3:
    unicode = str
else:
    unicode = unicode


def _stderr_supports_color():
    color = False
    if curses is not None and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:  # noqa
            pass
    return color


# 保持这些可配置选项为全局变量，但可根据需要在实例中修改
LEVEL = logging.INFO
PREFIX = '[%(name)s %(asctime)s] -- %(levelname)s: '
PREFIX_MPROC = '[%(levelname)1.1s %(asctime)s %(process)s]'
COLOURED = _stderr_supports_color()
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class LogFormatter(logging.Formatter):
    def __init__(self, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._coloured = COLOURED and _stderr_supports_color()
        self.PREFIX = prefix
        if self._coloured:
            curses.setupterm()
            if not PY3:
                fg_color = unicode(curses.tigetstr("setaf") or curses.tigetstr("setf") or "", "ascii")
            else:
                fg_color = curses.tigetstr("setaf") or curses.tigetstr("setf") or b""
                fg_color = fg_color.decode('ascii')
            self._colors = {
                logging.DEBUG: curses.tparm(fg_color, 4).decode('ascii'),
                logging.INFO: curses.tparm(fg_color, 2).decode('ascii'),
                logging.WARNING: curses.tparm(fg_color, 3).decode('ascii'),
                logging.ERROR: curses.tparm(fg_color, 1).decode('ascii')
            }
            self._normal = curses.tigetstr("sgr0").decode('ascii')

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as err:
            record.message = "Bad message (%r): %r" % (err, record.__dict__)

        record.asctime = time.strftime(TIME_FORMAT, self.converter(record.created))
        prefix = self.PREFIX % record.__dict__
        if self._coloured:
            prefix = self._colors.get(record.levelno, self._normal) + prefix + self._normal

        try:
            message = unicode(record.message)
        except UnicodeDecodeError:
            message = repr(record.message)

        formatted = prefix + " " + message
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + "\n" + record.exc_text
        return formatted.replace("\n", "\n    ")

def set_log(name: str, logfilename: str, level: int = logging.INFO, encoding="utf-8"):
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
    :param level: 日志级别，默认2    logging.INFO
    :param encoding: 编码，默认utf-8
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

    formatter = LogFormatter(PREFIX)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    log_file = logging.FileHandler(filename=logfilename, encoding=encoding)
    log_file.setFormatter(formatter)

    logger.addHandler(stream)
    logger.addHandler(log_file)

    return logger
