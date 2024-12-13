import os
import logging
import datetime
from .. import error_util
import random

## public methods to log
def logLastException(context=''):
    message = f'[{context}] ' + str(error_util.get_last_error_message())
    log.error(message)

def info(message):
    log.info(message)

def debug(message):
    log.debug(message)

def warn(message):
    log.warning(message)

def warning(message):
    log.warning(message)

def error(message):
    log.error(message)

def msg(message, level):
    if level == 'debug':
        debug(message)
    elif level == 'info':
        info(message)
    elif level == 'warn':
        warn(message)
    elif level == 'error':
        error(message)
    else:
        error('Message with out log level: ' + message)

def string_to_loglevel(level):
    if level == 'debug':
        return logging.DEBUG
    elif level == 'info':
        return logging.INFO
    elif level == 'warn':
        return logging.WARN
    elif level == 'error':
        return logging.ERROR
    else:
        error('Message with out log level: ' + level)


def clear_logging(logger_basename: str = 'app'):
    """
    Remove logging configuration.

    log = logging.getLogger(logger_basename)
    log.handlers.clear()

    :return:
    """
    log = logging.getLogger(logger_basename)
    log.handlers.clear()

def init_logging(logger_basename: str = 'app', log_folder: str = './logs', log_level: str = 'debug',
                  log_to_file: bool = False, log_to_console: bool = True, log_in_pergola: bool = None):
    """

    Central init method, can be called repeatedly to update logging configuration.

    Will try to detect whether the application runs in Pergola/Kubernetes to activate specific logging behaviour.

    :param logger_basename: used for config of python logging and as part of the filenames
    :param log_folder: folder to store log files in (log_to_file needs to be True)
    :param log_level: one of debug, info, warn, error, default: debug
    :param log_to_file: True/False (at least one of [log_to_file,log_to_console] must be True)
    :param log_to_console: True/False (at least one of [log_to_file,log_to_console] must be True)
    :param log_in_pergola log_in_pergola: True/False/None - if None is given, logging will try to detect its environment automatically
    :return:
    """
    if not log_to_file and not log_to_console:
        raise Exception('At least one of [log_to_file,log_to_console] must be True')

    log_level_intern = string_to_loglevel(log_level)

    global log
    log = logging.getLogger(logger_basename)
    log.handlers.clear()
    log.setLevel(log_level_intern)

    if log_in_pergola is None:
        # check for Pergola
        if os.getenv("KUBERNETES_PORT") is None:
            log_in_pergola = False
        else:
            log_in_pergola = True

    # create formatter
    if log_in_pergola:
        process_name = compute_pergola_process_name()
        formatter = logging.Formatter('[' + process_name + '] %(levelname)s - %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s [%(processName)s] %(levelname)s - %(message)s')

    # add formatter to handlers
    if log_to_file:
        # create file handler
        prefix = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-').replace('.', '_')
        fh = logging.FileHandler(log_folder + '/' + prefix + '.' + logger_basename + '.log')
        fh.setLevel(log_level_intern)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_to_console:
        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level_intern)
        ch.setFormatter(formatter)
        log.addHandler(ch)

def compute_pergola_process_name():
    """
    Provide a 5-char identifier derived from the Pergola Pod name
    :return: str
    """
    if "HOSTNAME" in os.environ:
        host_name = os.environ["HOSTNAME"]
        host_name = host_name.split("-")[-1][-5:]
    else:
        host_name = str(random.randrange(100)).zfill(5)
    return host_name