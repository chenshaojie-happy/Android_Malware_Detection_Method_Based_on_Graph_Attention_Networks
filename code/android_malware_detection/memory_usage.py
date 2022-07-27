# coding=utf-8
import os
# import time
import psutil

def memory_usage():
    mem_available = psutil.virtual_memory().available
    mem_process = psutil.Process(os.getpid()).memory_info().rss
    usage = 'memory used: ' + str(round(mem_process / 1024 / 1024 / 1024, 2)) + 'GB, memory available: ' + str(round(mem_available / 1024 / 1024 / 1024, 2)) + 'GB'
    # return round(mem_process / 1024 / 1024 / 1024, 2), round(mem_available / 1024 / 1024 / 1024, 2)
    return usage