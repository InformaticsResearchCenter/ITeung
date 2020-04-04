import psutil
from lib import reply

def auth(data):
    if reply.getNumberGroup(data[0]) == 1:
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    msgreply=cpu_usage()+disk_usage()+memory_usage()
    return msgreply

def cpu_usage():
    cpu='====CPU USAGE====\n'
    cpu_percentage='CPU Usage: '+str(int(psutil.cpu_percent(interval=1)))+'%\n'
    message_cpu=cpu+cpu_percentage
    return message_cpu

def disk_usage():
    path = r'C:'
    disk='\n====DISK USAGE====\n'
    status_disk= psutil.disk_usage(path=path)
    total_disk='Total Space: '+str(int(status_disk.total/(1024*1024*1024)))+'GB\n'
    used_disk='Used Space: '+str(int(status_disk.used/(1024*1024*1024)))+'GB\n'
    free_disk='Free Space: '+str(int(status_disk.free/(1024*1024*1024)))+'GB\n'
    message_disk=disk+total_disk+used_disk+free_disk
    return message_disk

def memory_usage():
    memory='\n====MEMORY USAGE====\n'
    status_memory=psutil.virtual_memory()
    total_memory='Total Memory: '+str(int(status_memory.total/(1024*1024*1024)))+'GB\n'
    used_memory='Used Memory: '+str(int(status_memory.used/(1024*1024*1024)))+'GB\n'
    free_memory='Free Memory: '+str(int(status_memory.free/(1024*1024*1024)))+'GB\n'
    message_memory=memory+total_memory+used_memory+free_memory
    return message_memory