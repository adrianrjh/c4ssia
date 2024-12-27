from pythonping import ping
import threading
import time
import json
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))

def doQuerySUBS():
    global r
    subs = []
    json_datos = {}
    band = 0
    print("Get data subscribers...")
    data = decode_redis(r.hgetall('infraYI'))
    if data == {}:
        data = 'NO'
    else:
        data = json.loads(data['data'])
        pass
    for sub in range(len(data)):
        if data[sub][0] != '' and data[sub][9] != '' and data[sub][10] != '' and data[sub][11] != '':
            subs.append((data[sub][0], data[sub][1], data[sub][2], data[sub][3], 
                         data[sub][4], data[sub][5], data[sub][6], data[sub][7], 
                         data[sub][8], data[sub][9], data[sub][10], data[sub][11], 
                         data[sub][12], data[sub][13], data[sub][14], data[sub][15]))
        else:
            pass
    return subs

ips = []
ipSubs = doQuerySUBS()
for x in range(0,len(ipSubs)):
  if ipSubs[x][3] != 'PISCILA':
    ips.append(ipSubs[x][9])

def ping_host(ip):
    while True:
      try:
        response = ping(ip, size=1, count=1)
        if response.rtt_avg_ms < 2000:
          rts.add(str(ip), int(time.time()), float(response.rtt_avg_ms))
          #print(f"{ip}: {response.rtt_avg_ms} ms")
        else:
          rts.add(str(ip), int(time.time()), float(0.0))
          #print(f"Unreachable {ip}")
      except Exception as e:
        print(e)
      time.sleep(10)  # Espera 10 segundos antes del próximo ping

# Crear y empezar un hilo para cada host
for host in ips:
    thread = threading.Thread(target=ping_host, args=(host,))
    thread.start()