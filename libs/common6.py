from h2o_wave import ui
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
import threading, json
import time
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

session = False
rts = 0

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

niveluht, flujouht, sostenimiento_in, enfriamiento = 0.0,0.0,0.0,0.0
aguacaliente, salidaproducto, sostenimiento_out, entrada_glicol = 0.0,0.0,0.0,0.0
brixlinea, gas, phEspera, tempEspera = 0.0,0.0,0.0,0.0
tanque1, tanque2, tanque3, tanque4 = 0.0,0.0,0.0,0.0

default_rows = []
for x in range(1000):
  default_rows.append([0, 0])

niveluht_rows,flujouht_rows=default_rows[:],default_rows[:]
sostenimiento_in_rows,enfriamiento_rows = default_rows[:],default_rows[:]
aguacaliente_rows, salidaproducto_rows = default_rows[:],default_rows[:]
sostenimiento_out_rows, entrada_glicol_rows = default_rows[:], default_rows[:]
brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows = default_rows[:], default_rows[:], default_rows[:], default_rows[:]
tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows = default_rows[:], default_rows[:], default_rows[:], default_rows[:]

##### V A R I A B L E S  I N I C I A L E S ########
temp_min_past, temp_max_past, flujo_min_past, flujo_max_past, tanques_dest, noTanque = 90, 100, 1500, 2000, "Seleccionar", 0

i = 0
intoOne = 0
dateStart = "--"
dateEnd = "--"
dataInfo,dataInfoMarca,dataInfoSabor,dataInfoTanque,dataInfoPasteur="--","--","--","--",0

AV080, AV081, AV082, PP001, HW001, FAN001, CW001, Pasteur, Recir, CALM = "-","-","-","-","-","-","-","-","-","-"
recover,data_to_run = [],[]
comboboxTanques = ['Tanque 1','Tanque 2','Tanque 3','Tanque 4']
inicio_val=True
comboboxDisp = ['AP', 'OLT', 'ONU', 'PTP', 'ROUTER', 'SWITCH']
data_rows = [['2', 'ENABLED', '0159', '3.654', '0.1245', '49.313']]
data_rows2 = [['0159', 'OFFLINE', 'INACTIVE', 'MISSMATCHED']]
equipo, device = '', ''
columnsT = []
columnsT2 = []
columnsDev = []
columnsDev2 = []
columnsOLT = ['PORT ID','STATUS','ONLINE ONU N°','OPTIC VCC (V)','OPTIC BIAS (mA)','OPTIC PWR (dBm)']
columnsOLT2 = ['ONU DESCRIPTION','ONLINE STATUS','CONFIG STATUS','MATCH STATUS']

table_cells = []
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
    return obj

def regAct(r,key,dateStart,temp_min,temp_max,flow_min,flow_max,tank):
    conf={
    "start": str(dateStart),
    "temp_min": str(temp_min),
    "temp_max": str(temp_max),
    "flow_min": str(flow_min),
    "flow_max": str(flow_max),
    "tank": str(tank)}
    r.hmset(key, conf)


def regRecPasteur(r,key,datestart,pesado,marca,sabor,tanqueDest,pasteur):
    register={
    "start": str(datestart),
    "pesado": str(pesado),
    "marca": str(marca),
    "sabor": str(sabor),
    "tanqueDest": str(tanqueDest),
    "pasteur": str(pasteur),
    "litosFormu": str("--"),
    "datesPromBrix": str("--"),
    "comments": str("--"),
    "key": str("--")
    }
    r.hmset(key, register)



def truncate(num, decimal):
    my_digits = 10**decimal  #raise 10 to the number of decimal places
    #shifting the decimal part and converting to integer
    int_val = int(num* my_digits)
    #return the truncated value
    return int_val/my_digits
