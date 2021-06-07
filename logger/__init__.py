#!/usr/bin/python3
from inspect import currentframe
import traceback 

LOG_FILE= "error.log"
LOG_RED = "line {}: \033[91m{}\033[00m"
LOG_YEL = "line {}\t: \033[96m{}\033[00m"

def error_log(s):
    cf = currentframe()
    s=str(s)
    trace = traceback.format_exc()
    if 'None' not in trace: print(trace)
    print(LOG_RED.format(str(cf.f_back.f_lineno).zfill(4), s))
    file = open(LOG_FILE, "a+")
    file.write("\n"+s)
    file.close()
    return True

def log(s):
    cf = currentframe()
    s=str(s)
    print(LOG_YEL.format(cf.f_back.f_lineno,s))
