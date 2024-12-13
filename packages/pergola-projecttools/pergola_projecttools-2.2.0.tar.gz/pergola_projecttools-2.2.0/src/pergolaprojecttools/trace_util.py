import psutil
import os

def get_mem():
    mem_in_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    mem_formatted = '%.1f MB' % mem_in_mb
    return mem_formatted