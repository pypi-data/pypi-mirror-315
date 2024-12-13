import sys
import os
import traceback

def get_last_error_message():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if exc_tb is not None:
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        message = str(exc_type) + ', '+ str(fname) + ': Line '+ str(exc_tb.tb_lineno) + '' + '\n'
        message = message + traceback.format_exc()
    else:
        message = None
    return message
