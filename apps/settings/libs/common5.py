import json 
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import csv
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError

ipGlobal = '10.0.3.25'
ipRedis = '10.0.3.25'

session = False
r = ''
selectioned = ''

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

# ings, nombings = [], []

# Create columns for our issue table.
columns = [
    ui.table_column(name='text', label='Connection', sortable=True, searchable=True, max_width='200'),
    ui.table_column(name='text0', label='Device 1', sortable=True, searchable=True, max_width='250'),
    ui.table_column(name='text1', label='Device 2', sortable=True, searchable=True, max_width='250'),
]

devices = []
comboboxDev1 = []
comboboxDev2 = []

ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo, tecnologia, ipDevice, latitud, longitud, ID_Count, conectedTo = '','','','','','','','','','','','',''
device1, device2 = '', ''
data_rows, data_rows_get = [], []

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

def getAll(r,key):
    obj = decode_redis(r.hgetall(key))
    if obj == {}:
        obj = 'NO'
    else:
        pass
    return obj

# def regAct(r, key, admin, password):
#     pp={"admin": str(admin), 'password':str(password)}
#     r.hmset(key, pp)

def infraYI(r, key, data):
    #print(json.dumps(data))
    pp={"data":json.dumps(data)}
    r.hmset(key,pp)

def connsYI(r, key, data):
    #print(json.dumps(data))
    pp={"data":json.dumps(data)}
    r.hmset(key,pp)

# def truncate(num, decimal):
#     my_digits = 10**decimal  #raise 10 to the number of decimal places
#     #shifting the decimal part and converting to integer
#     int_val = int(num* my_digits)
#     #return the truncated value
#     return int_val/my_digits