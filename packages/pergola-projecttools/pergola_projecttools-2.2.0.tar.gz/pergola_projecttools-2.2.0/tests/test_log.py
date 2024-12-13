import pytest
from src.pergolaprojecttools import log

def test_log():
    log.init_logging()

    log.info('Log it')
    log.logLastException('A context')

    from src.pergolaprojecttools.trace_util import get_mem
    log.info('Important info ' + get_mem())

    log.clear_logging()