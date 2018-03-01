# coding: utf-8

## os 监控内存
# import time


# def get_total_mem():
#     with open('/proc/meminfo') as f:
#         total = int(f.readline().split()[1])
#         free = int(f.readline().split()[1])
#         available = int(f.readline().split()[1])
#         buffers = int(f.readline().split()[1])
#         cache = int(f.readline().split()[1])
#     mem_use = total - free - buffers - cache
#     localtime = time.asctime( time.localtime(time.time()) )
#     print(localtime)
#     print('MEMORY Total: %.2fGB\tFree: %.2fGB %.1f%%\t \
#         Available: %.2fGB %.1f%%\tMEM_USE: %.2fGB %.1f%%' % 
#            (total/1048576, free/1048576, free/total*100, 
#             available/1048576, available/total, 
#             mem_use/1048576, mem_use/total))

# def main():
#     while True:
#         time.sleep(3)
#         get_total_mem()

## psutil 监控内存
import os
import time
import psutil
import argparse


class MemMonitor():
    '''
    output the information of memory usage
    '''
    def __init__(self, pid=os.getpid(), period=5):
        self.pid = pid
        self.period = period

    def mem_monitor(self):
        p = psutil.Process(self.pid)
        mem = psutil.virtual_memory()
        localtime = time.asctime(time.localtime(time.time()))
        print('------------------------------------------------------')
        print(localtime)
        print('Total: %.2fGB\tFree: %.2fGB %.2f%%\t \
            Available: %.2fGB %.2f%%\tMEM_USE: %.2fGB %.2f%%' % 
               (mem.total/1024**3, mem.free/1024**3, mem.free/mem.total*100, 
                mem.available/1024**3, mem.available/mem.total*100, 
                mem.used/1024**3, mem.used/mem.total*100))
        print("进程名称: %s\t内存占用百分比: %.2f%%" 
            %(p.name(), p.memory_percent()))
        print('------------------------------------------------------')

    def monitor_main(self):
        while os.path.isfile('/proc/%s/stat' %str(self.pid)):
            self.mem_monitor(int(self.pid))
            time.sleep(int(self.period))
        print("--------the process is over--------")

def mem_monitor(pid):
    p = psutil.Process(pid)
    mem = psutil.virtual_memory()
    localtime = time.asctime(time.localtime(time.time()))
    print('------------------------------------------------------')
    print(localtime)
    print('Total: %.2fGB\tFree: %.2fGB %.2f%%\t \
        Available: %.2fGB %.2f%%\tMEM_USE: %.2fGB %.2f%%' % 
           (mem.total/1024**3, mem.free/1024**3, mem.free/mem.total*100, 
            mem.available/1024**3, mem.available/mem.total*100, 
            mem.used/1024**3, mem.used/mem.total*100))
    print("进程名称: %s\t内存占用百分比: %.2f%%" 
        %(p.name(), p.memory_percent()))
    print('------------------------------------------------------')

def monitor_main(**kwargs):
    while os.path.isfile('/proc/%s/stat' %str(kwargs['pid'])):
        mem_monitor(int(kwargs['pid']))
        time.sleep(int(kwargs['period']))
    print("--------the process is over--------")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=\
            'monitor the memory use of programme according to the pid')
    parser.add_argument('-p', '--pid', dest='pid', nargs='?', 
        default=os.getpid(), help='pid of the programme')
    parser.add_argument('-t', '--time', dest='period', nargs='?', 
        default=5, help='输出间隔时间')

    args = parser.parse_args()

    # how to use
    # $ python MemMonitor.py (-p somepid) (-t timespan)

    kwargs = vars(args)
    monitor_main(**kwargs)
