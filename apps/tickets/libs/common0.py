from plotly import graph_objects as go
# from connections import tracesTP, tracesTT
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import os
from ftplib import FTP
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
import csv, datetime, json, time

ipGlobal = '10.0.3.25'
ipRedis = '10.0.3.25'

user = ''

session = False
r = ''
# usernameS = ''
name, lastname, puesto, email, username, password = '','','','','',''
var_ca = 1
data_rows, data_rows_save, data_rows_keycount = [], [], 0
refreshTable = 0
usernameL, passwordL = '', ''
# Variable global para mantener la referencia de la tarea refresh
current_refresh_task = None

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

# def decode_redis(src):
#     if isinstance(src, list):
#         rv = list()
#         for key in src:
#             rv.append(decode_redis(key))
#         return rv
#     elif isinstance(src, dict):
#         rv = dict()
#         for key in src:
#             rv[key.decode()] = decode_redis(src[key])
#         return rv
#     elif isinstance(src, bytes):
#         return src.decode()
#     else:
#         raise Exception("type not handled: " +type(src))

# def getUser(id_key, id1, user, password):
#     obj = decode_redis(r.get(str(id_key)))
#     val = 0
#     if obj == {}:
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str(id1)+str(x)))
#             if obj != {}:
#                 if obj['username'] == str(user):
#                     if obj['password'] == str(password):
#                         if obj['status'] == 'Active':
#                             puesto = obj['puesto']
#                             val = 1
#         if val == 1:
#             return 'Yes', puesto
#         if val == 0:
#             return 'No', ''

# def regAct(key_count,pp):
#     r.hmset("user_"+str(key_count), pp)
#     r.set("user_key",str(key_count))

# columns = [
#     ui.table_column(name='text0', label='Time', sortable=True, searchable=True, max_width='180'),
#     ui.table_column(name='text1', label='User ID', sortable=True, searchable=True, max_width='180'),
#     ui.table_column(name='text2', label='Name', sortable=True, searchable=True, max_width='180'),
#     ui.table_column(name='text3', label='Lastname', sortable=True, searchable=True, max_width='180'),
#     ui.table_column(name='text4', label='Puesto', sortable=True, searchable=True, max_width='180'),
#     ui.table_column(name='text5', label='Email', sortable=True, searchable=True, max_width='200'),
#     ui.table_column(name='text6', label='Status', sortable=True, searchable=True, max_width='180', cell_type=ui.tag_table_cell_type(name='tags1', tags=[ui.tag(label='Waiting', color='#f7f020'),ui.tag(label='Active', color='#27964e')])),
#     ui.table_column(name='text7', label='Username', sortable=True, searchable=True, max_width='180'),
# ]

# def getAllUsers(r,counter,key):
#     all_users, time, user_key, name, lastname, puesto, email, status, username = [], '', '','', '', '', '', '', ''
#     obj = decode_redis(r.get(str(counter)))
#     if obj == {}:
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str(key)+str(x)))
#             if obj != {}:
#                 time = str(obj['time'])
#                 user_key = str(obj['user_key'])
#                 name = str(obj['name'])
#                 lastname = str(obj['lastname'])
#                 puesto = str(obj['puesto'])
#                 email = str(obj['email'])
#                 status = str(obj['status'])
#                 username = str(obj['username'])
#                 all_users.append([time, user_key, name, lastname, puesto, email, status, username])
#         return all_users

# def updAct(data, option):
#     if option == 'validate':
#         now = datetime.datetime.now()
#         dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
#         r.hset("user_"+str(data[0][1]),"time",str(dt_string))
#         r.hset("user_"+str(data[0][1]),"user_key",str(data[0][1]))
#         r.hset("user_"+str(data[0][1]),"name",str(data[0][2]))
#         r.hset("user_"+str(data[0][1]),"lastname",str(data[0][3]))
#         r.hset("user_"+str(data[0][1]),"puesto",str(data[0][4]))
#         r.hset("user_"+str(data[0][1]),"email",str(data[0][5]))
#         r.hset("user_"+str(data[0][1]),"status",'Active')
#         r.hset("user_"+str(data[0][1]),"username",str(data[0][7]))

# def delUser(data):
#     print(data)
#     obj = r.delete("user_"+str(data[0][1]))
#     users = len(getAllUsers(r, 'user_key', 'user_'))
#     if users > 0:
#         return 'Si'
#     else:
#         return 'No'