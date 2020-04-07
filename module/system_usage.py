import psutil, pyspeedtest, speedtest
from lib import reply

def auth(data):
    if reply.getNumberGroup(data[0]) == 1:
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    msgreply=cpu_usage()+disk_usage()+memory_usage()+network_usage()+network_ping()
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

def network_usage():
    network = '\n====NETWORK SPEEDTEST====\n'
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    res = speed.results.dict()
    download = str(round(float(res['download'] / 1000000), 3)) + ' Mbit/s'
    upload = str(round(float(res['upload'] / 1000000), 3)) + ' Mbit/s'
    message_network=network+download+upload
    return message_network

def network_ping():
    ping='\n====NETWORK PING====\n'
    whatsapp='WhatsApp: '+str(int(pyspeedtest.SpeedTest('web.whatsapp.com').ping()))+'ms\n'
    siap='System Akademik SIAP: '+str(int(pyspeedtest.SpeedTest('siap.poltekpos.ac.id').ping()))+'ms\n'
    message_ping=ping+whatsapp+siap
    return message_ping