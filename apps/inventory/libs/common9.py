from h2o_wave import ui
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
import threading, json
import time

rts = 0
r = 0
ipGlobal = '10.0.3.148'
ipRedis = '10.0.3.113'
session = False
i = 0

current_refresh_task = None

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

device0, device1, device2, device3, device4, device5, device6, device7, device8, device9 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
device10, device11, device12, device13, device14, device15, device16, device17, device18, device19 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
device20, device21, device22, device23, device24, device25, device26, device27, device28, device29 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
device30, device31, device32, device33, device34, device35, device36, device37, device38, device39 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
device40, device41, device42, device43, device44, device45, device46, device47, device48, device49 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
device50, device51, device52, device53, device54, device55, device56, device57, device58 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

default_rows = []
for x in range(1000):
  default_rows.append([0, 0])

device0_rows,device1_rows,device2_rows,device3_rows,device4_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device5_rows,device6_rows,device7_rows,device8_rows,device9_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device10_rows,device11_rows,device12_rows,device13_rows,device14_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device15_rows,device16_rows,device17_rows,device18_rows,device19_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device20_rows,device21_rows,device22_rows,device23_rows,device24_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device25_rows,device26_rows,device27_rows,device28_rows,device29_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device30_rows,device31_rows,device32_rows,device33_rows,device34_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device35_rows,device36_rows,device37_rows,device38_rows,device39_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device40_rows,device41_rows,device42_rows,device43_rows,device44_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device45_rows,device46_rows,device47_rows,device48_rows,device49_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device50_rows,device51_rows,device52_rows,device53_rows,device54_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:],default_rows[:]
device55_rows,device56_rows,device57_rows,device58_rows = default_rows[:],default_rows[:],default_rows[:],default_rows[:]

def decode_redis(src):
    try:
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
    except Exception as e:
        return 'NO'

def getAllUsedDevsModels(r, materialesdevices):
    marca, modelo, descripcion = '', '', ''
    modelos_count = {}  # Diccionario para contar los modelos
    try:
        if materialesdevices == 'Equipos de Red':
            obj = decode_redis(r.get(str('key_equipos_red')))
            if obj == 'NO':
                obj = 'NO'
                return obj
            else:
                for x in range(0, int(obj) + 1):
                    obj = decode_redis(r.hgetall(str('equipos_red') + str(x)))
                    if obj != {}:
                        marca = obj['marca']
                        modelo = obj['modelo']
                        descripcion = obj['descripcion']
                        obj_alm = decode_redis(r.get(str('key_alm_used')))
                        for y in range(0, int(obj_alm) + 1):
                            obj = decode_redis(r.hgetall(str('alm_used') + str(y)))
                            if obj != {}:
                                if modelo == obj['modelo']:
                                    # Incrementar el contador del modelo
                                    if modelo in modelos_count:
                                        modelos_count[modelo] += 1
                                    else:
                                        modelos_count[modelo] = 1
            return modelos_count  # Retornar el diccionario con los conteos
    except Exception as e:
        print(e)

def getAllNewDevsModels(r, materialesdevices):
    marca, modelo, descripcion = '', '', ''
    modelos_count = {}  # Diccionario para contar los modelos
    try:
        if materialesdevices == 'Equipos de Red':
            obj = decode_redis(r.get(str('key_equipos_red')))
            if obj == 'NO':
                obj = 'NO'
                return obj
            else:
                for x in range(0, int(obj) + 1):
                    obj = decode_redis(r.hgetall(str('equipos_red') + str(x)))
                    if obj != {}:
                        marca = obj['marca']
                        modelo = obj['modelo']
                        descripcion = obj['descripcion']
                        obj_alm = decode_redis(r.get(str('key_alm_new')))
                        for y in range(0, int(obj_alm) + 1):
                            obj = decode_redis(r.hgetall(str('alm_new') + str(y)))
                            if obj != {}:
                                if modelo == obj['modelo']:
                                    # Incrementar el contador del modelo
                                    if modelo in modelos_count:
                                        modelos_count[modelo] += 1
                                    else:
                                        modelos_count[modelo] = 1
            return modelos_count  # Retornar el diccionario con los conteos
    except Exception as e:
        print(e)