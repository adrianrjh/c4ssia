import json 
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import csv
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
from plotly import graph_objects as go
import requests
import os, qrcode
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

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

convertir = ''

ings, nombings = [], []

comboboxEquipo = []
comboboxDisp = ['AP', 'PTP', 'SWITCH', 'ROUTER', 'OLT', 'ONU']
comboboxOLTS = ['DSP7001_4', 'DSP7001_8', 'DSP7001_16']
comboboxSWITCHS = ['ARISTA 7050S_64_F', 'MIKROTIK RB750R2']
comboboxROUTERS = ['MIKROTIK RB1100', 'MIKROTIK RB450', 'MIKROTIK RB750', 'MIKROTIK RB750 R2', 'MIKROTIK RB760']
comboboxAPTP = ['ROCKET AC', 'ROCKER AC PRISM', 'MIMOSA C5C', 'MIMOSA B11', 'MOTOROLLA C0509A', 'POWERBEAM 5ACGEN2', 'LITEBEAM 5ACGEN2', 'NANO STATION LOCO AC', 'LITEBEAM M5', 'LAP120', 'LAP-GPS']
comboboxONU = ['XC220_G3']
comboboxTecno = ['FIBRA', '5GHz', '2.4GHz']
comboboxLvl = ['L0', 'L1', 'L2', 'L3', 'L4', 'LA', 'LP', 'LSW', 'LR', 'LOL', 'LON']

ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo = '', '', '', '', '', '', ''
tecnologia, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo = '', '', '', '', '', '', ''

data_rows, data_rows_first, data_rows_keycount = [], [], 0
data_rows_density = []
comboboxProjPaP, proyecto = [], ''

subscribersLatR = []
subscribersLonR = []
subscribersIDR = []
subscribersStatusR = []
#######################
subscribersLatO = []
subscribersLonO = []
subscribersIDO = []
subscribersStatusO = []
#######################
subscribersLatY = []
subscribersLonY = []
subscribersIDY = []
subscribersStatusY = []
#######################
subscribersLatG = []
subscribersLonG = []
subscribersIDG = []
subscribersStatusG = []

data_table_0_keycount = 0
data_table_0 = []
data_table_25_keycount = 0
data_table_25 = []
data_table_50_keycount = 0
data_table_50 = []
data_table_75_keycount = 0
data_table_75 = []

subscribers = 0
data = {}
lat_media = 19.1
lon_media = -103.6
zoom_media = 14

paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 1, 0, 0, 0, 0, 0, 0, 0
current_refresh_task = None
current_paso3_task = None

comboboxPropietario, comboboxConectedTo = [], []
propietarioAddPoste, posteAddPoste, latitudAddPoste, longitudAddPoste, idCajaAddPoste, idCEAddPoste, conectedToAddPoste = 'Seleccionar', '', '', '', 'Seleccionar', 'Seleccionar', 'Seleccionar'

notableport, proyecto_density, propietario_density, poste_density, latitud_density, longitud_density, idcaja_density, port_density, potcalculo_density, potreal_density = '', '', '', '', '', '', '', '', '', ''
gponport_density, onuid_density, potclient_density, idclient_density, nameclient_density, paquete_density, tecnico_density, fechainstalacion_density, noserieonu_density = '', '', '', '', '', '', '', '', ''
comboboxPaquetePlan = ['Comodato 30MB', 'Comprado 30MB','Comodato 50MB', 'Comprado 50MB','Comodato 100MB', 'Comprado 100MB','Comodato 150MB', 'Comprado 150MB','Comodato 200MB', 'Comprado 200MB','Comodato 250MB', 'Comprado 250MB']
comboboxGPONOLT = ['1/1/1', '1/1/2','1/1/3', '1/1/4','1/1/5', '1/1/6','1/1/7', '1/1/8','1/1/9', '1/1/10','1/1/11', '1/1/12', '1/1/13', '1/1/14', '1/1/15', '1/1/16']
columns = [
    ui.table_column(name='text', label='Afiliación', sortable=True, searchable=True, max_width='180'),
    ui.table_column(name='text0', label='Ciudad', sortable=True, searchable=True, max_width='70'),
    ui.table_column(name='text1',  label='Municipio', sortable=True, searchable=True, max_width='70'),
    ui.table_column(name='text2', label='Localidad', sortable=True, searchable=True, max_width='70'),
    ui.table_column(name='text3', label='Referencia', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text4', label='Dependencia', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text5', label='Dispositivo', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text6', label='Equipo', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text7', label='Tecnología', sortable=True, searchable=True, max_width='80'),
    ui.table_column(name='text8', label='IP', sortable=True, searchable=True, max_width='70'),
    ui.table_column(name='text9', label='Latitud', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text10', label='Longitud', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text11', label='Count', sortable=True, searchable=True, max_width='40'),
    ui.table_column(name='text12', label='Level', sortable=True, searchable=True, max_width='40'),
    ui.table_column(name='text13', label='Conected To', sortable=True, searchable=True, max_width='40'),
    ui.table_column(name='text14', label='Host', sortable=True, searchable=True, max_width='200')
]

columnsProjects = [
    ui.table_column(name='text0', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='150'),
    ui.table_column(name='text2', label='Propietario', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text3', label='ID Poste', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text4',  label='Latitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text5', label='Longitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Status', sortable=True, min_width='70', cell_type=ui.progress_table_cell_type()),
    ui.table_column(name='text7', label='ID Caja', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text8', label='N° Ports', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text9', label='ID CE', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text10', label='Clients', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text11', label='To', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text12', label='Pot Calculo', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text13', label='Pot Real', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text14', label='Pot Calidad', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text15', label='Tag Pot', sortable=True, searchable=True, min_width='90', cell_type=ui.tag_table_cell_type(name='tags2', 
        tags=[        
            ui.tag(label='Excelente', color='#09b2b8'),
            ui.tag(label='Muy bueno', color='#269c14'), 
            ui.tag(label='Bueno', color='#c2ff3d'), 
            ui.tag(label='Regular', color='#d4c753'), 
            ui.tag(label='Malo', color='#ed6d66'),
            ui.tag(label='No Aplica', color='#b8bdb7'),
        ]
    ))
]

columnsProjectsPaP = [
    ui.table_column(name='text0', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text2', label='Propietario', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text3', label='ID Poste', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text4',  label='Latitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text5', label='Longitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Status', sortable=True, min_width='100', cell_type=ui.progress_table_cell_type()),
    ui.table_column(name='text7', label='ID Caja', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text8', label='ID CE', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text9', label='Active Clients', sortable=True, searchable=True, min_width='120'),
    ui.table_column(name='text10', label='Conected To', sortable=True, searchable=True, min_width='120'),
    ui.table_column(name='text11', label='Potencia', sortable=True, searchable=True, min_width='80'),
]

columnsProjectsDensity = [
    ui.table_column(name='text0', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='150'),
    ui.table_column(name='text2', label='Propietario', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text3', label='ID Poste', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text4',  label='Latitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text5', label='Longitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='ID Caja', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text7', label='Port Caja', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text8', label='Pot Calculo', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text9', label='Pot Real', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text10', label='PON Port', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text11', label='ONU ID', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text12', label='Pot Client', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text13', label='ID Client', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text14', label='Client', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text15', label='Paquete', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text16', label='Tecnico', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text17', label='Fecha Instalación', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text18', label='N° Serie', sortable=True, searchable=True, min_width='90'),
]

def generar_qr(texto, nombre_archivo, nombre_carpeta):
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agrega el texto al objeto QRCode
    qr.add_data(texto)
    qr.make(fit=True)

    # Verificar si la carpeta existe, si no, crearla
    output_dir = '/home/adrian/ws/wave/cassia/data/qrs/'+nombre_carpeta+'/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Genera la imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Guarda la imagen en un archivo
    img.save(output_dir+nombre_archivo)

    return output_dir

def obtener_coordenadas_osm(ciudad):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'adrianfime27@gmail.com'}
    params = {"q": ciudad,"format": "json"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        resultados = response.json()
        if resultados:
            latitud = resultados[0]['lat']
            longitud = resultados[0]['lon']
            return latitud, longitud
        else:
            return "No se encontraron resultados"
    else:
        return "Error en la solicitud: " + str(response.status_code)

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

def getAll(r,key):
    obj = decode_redis(r.hgetall(key))
    if obj == {}:
        obj = 'NO'
    else:
        pass

    return obj

def getAllUsers(r,counter,key):
    all_users, time, user_key, name, lastname, puesto, email, status, username = [], '', '','', '', '', '', '', ''
    obj = decode_redis(r.get(str(counter)))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str(key)+str(x)))
            if obj != {}:
                time = str(obj['time'])
                user_key = str(obj['user_key'])
                name = str(obj['name'])
                lastname = str(obj['lastname'])
                puesto = str(obj['puesto'])
                email = str(obj['email'])
                status = str(obj['status'])
                username = str(obj['username'])
                all_users.append([time, user_key, name, lastname, puesto, email, status, username])
        return all_users

############## GGGGGGGEEEEEEETTTTT AAAAAALLLLLLLL ############
def getAllprojectPaP(r):
    all_PaP, proyecto = [], ''
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                for y in range(0,len(msg)):
                    if proyecto != msg[y][1]:
                        proyecto = msg[y][1]
                        all_PaP.append(proyecto)
        return all_PaP

def getAllPropietPaP(r, proyecto):
    all_propietarios, propietario = [], ''
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                for y in range(0,len(msg)):
                    if propietario != msg[y][2]:
                        propietario = msg[y][2]
                        if propietario in all_propietarios:
                            pass
                        else:
                            all_propietarios.append(propietario)
        if not 'CA' in all_propietarios:
            all_propietarios.append('CA')
        return all_propietarios

def getAllPostesPaP(r, project):
    all_postes, proyecto = [], ''
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                if msg[0][1] == project:
                    for y in range(0,len(msg)):
                        all_postes.append(msg[y][3])
                    return all_postes

def setNewPostePaP(r, project, propietario):
    namePoste, posteNew, propietario_keycount = '', '', 0
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                if msg[0][1] == project:
                    for y in range(0,len(msg)):
                        if msg[y][2] == propietario:
                            propietario_keycount += 1
                    propietario_keycount = int(propietario_keycount)+1
                    if int(propietario_keycount) < 10:
                        propietario_keycount = '00'+str(propietario_keycount)
                    if int(propietario_keycount) > 9 and int(propietario_keycount) < 100:
                        propietario_keycount = '0'+str(propietario_keycount)
                    if propietario == 'YI':
                        namePoste = 'PMN'+str(propietario_keycount)
                    if propietario == 'CFE':
                        namePoste = 'PC'+str(propietario_keycount)
                    if propietario == 'TELMEX':
                        namePoste = 'PME'+str(propietario_keycount)
                    if propietario == 'H. AYUN':
                        namePoste = 'PAE'+str(propietario_keycount)
                    return namePoste

def getAllPaP(project):
    all_postes, proyecto = [], ''
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                if msg[0][1] == project:
                    return msg

def getAllDensityPaP(project):
    all_postes, proyecto = [], ''
    obj = decode_redis(r.get(str('key_pap_density')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap_density')+str(x)))
            if obj != {}:
                msg = obj["puertos"].replace("'","[")
                msg = json.loads(msg)
                if msg[0][1] == project:
                    return msg

def changeFieldTable(r, lista, noPR):
    all_postes, proyecto = [], ''
    obj = decode_redis(r.get(str('key_pap_density')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap_density')+str(x)))
            if obj != {}:
                r.hset("pap_density"+str(x),"puertos",str(json.dumps(lista)))

def regProjPaP(r, data):
    key_count=r.get('key_pap')
    if key_count == {}:
        key_count = 0
    else:
        if key_count == None:
            key_count = 0
            key_count=int(key_count)+1
        else:
            key_count=key_count.decode("utf-8")
            key_count=int(key_count)+1
    pp={"postes":json.dumps(data), "proyecto":data[0][1]}
    r.hmset("pap"+str(key_count), pp)
    r.set("key_pap",str(key_count))

def regProjDensityPaP(r, data):
    key_count=r.get('key_pap_density')
    if key_count == {}:
        key_count = 0
    else:
        if key_count == None:
            key_count = 0
            key_count=int(key_count)+1
        else:
            key_count=key_count.decode("utf-8")
            key_count=int(key_count)+1
    pp={"puertos":json.dumps(data), "proyecto":data[0][1]}
    r.hmset("pap_density"+str(key_count), pp)
    r.set("key_pap_density",str(key_count))

def changePostesPaP(r, project, postes):
    obj = decode_redis(r.get(str('key_pap')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('pap')+str(x)))
            if obj != {}:
                msg = obj["postes"].replace("'","[")
                msg = json.loads(msg)
                for y in range(0,len(msg)):
                    if msg[0][1] == project:
                        res = r.hset("pap"+str(x),"postes",json.dumps(postes))
                        return res

def infraYI(r, key, data):
    #print(json.dumps(data))
    pp={"data":json.dumps(data)}
    r.hmset(key,pp)

def connectionsTraces(proyecto):
    global fig, data_table_0_keycount, data_table_0, data_table_25_keycount, data_table_25, data_table_50_keycount, data_table_50, data_table_75, data_table_75_keycount 
    fig = 0
    data = {}
    ####### from 0 to 24 % #######
    subscribersLatR = []
    subscribersLonR = []
    subscribersIDR = []
    subscribersStatusR = []
    ####### from 25 to 49 % #######
    subscribersLatO = []
    subscribersLonO = []
    subscribersIDO = []
    subscribersStatusO = []
    ####### from 50 to 74 % #######
    subscribersLatY = []
    subscribersLonY = []
    subscribersIDY = []
    subscribersStatusY = []
    ####### from 75 to 100 % #######
    subscribersLatG = []
    subscribersLonG = []
    subscribersIDG = []
    subscribersStatusG = []

    ipsSubs = []
    subscribers = getAllPaP(proyecto)
    ####    T  R  A  C  E  S    ####
    bandFor = 0
    bandSubs = 0
    bandTwrs = 0
    count = 0
    for x in range(len(subscribers)):
        idSecondary = subscribers[x][3]
        latSecondary = subscribers[x][4]
        lonSecondary = subscribers[x][5]
        statusSecondary = subscribers[x][6]
        connSecondary = subscribers[x][11]
        for z in range(len(subscribers)):
            if connSecondary==subscribers[z][3]:
                ####    R   E   D    ####
                if float(subscribers[x][6])*100 >= 0 and float(subscribers[x][6])*100 < 25:
                    subscribersIDR.append([str("subsID"),idSecondary])
                    subscribersLatR.append([float(subscribers[z][4]),float(latSecondary)])
                    subscribersLonR.append([float(subscribers[z][5]),float(lonSecondary)])
                    subscribersStatusR.append([float(subscribers[z][6])])
                    data_table_0_keycount += 1
                    data_table_0.append([str(data_table_0_keycount),str(subscribers[x][0]),str(subscribers[x][1]),str(subscribers[x][2]),str(subscribers[x][3]),
                        str(subscribers[x][4]),str(subscribers[x][5]),str(subscribers[x][6]),str(subscribers[x][7]),str(subscribers[x][8]),str(subscribers[x][9]),str(subscribers[x][10])])
                ####    O   R   A   N   G   E    ####
                if float(subscribers[x][6])*100 >= 25 and float(subscribers[x][6])*100 < 50:
                    subscribersIDO.append([str("subsID"),idSecondary])
                    subscribersLatO.append([float(subscribers[z][4]),float(latSecondary)])
                    subscribersLonO.append([float(subscribers[z][5]),float(lonSecondary)])
                    subscribersStatusO.append([float(subscribers[z][6])])
                    data_table_25_keycount += 1
                    data_table_25.append([str(data_table_25_keycount),str(subscribers[x][0]),str(subscribers[x][1]),str(subscribers[x][2]),str(subscribers[x][3]),
                        str(subscribers[x][4]),str(subscribers[x][5]),str(subscribers[x][6]),str(subscribers[x][7]),str(subscribers[x][8]),str(subscribers[x][9]),str(subscribers[x][10])])
                ####    Y   E   L   L   O   W    ####
                if float(subscribers[x][6])*100 >= 50 and float(subscribers[x][6])*100 < 75:
                    subscribersIDY.append([str("subsID"),idSecondary])
                    subscribersLatY.append([float(subscribers[z][4]),float(latSecondary)])
                    subscribersLonY.append([float(subscribers[z][5]),float(lonSecondary)])
                    subscribersStatusY.append([float(subscribers[z][6])])
                    data_table_50_keycount += 1
                    data_table_50.append([str(data_table_50_keycount),str(subscribers[x][0]),str(subscribers[x][1]),str(subscribers[x][2]),str(subscribers[x][3]),
                        str(subscribers[x][4]),str(subscribers[x][5]),str(subscribers[x][6]),str(subscribers[x][7]),str(subscribers[x][8]),str(subscribers[x][9]),str(subscribers[x][10])])
                ####    G   R   E   E   N   ####
                if float(subscribers[x][6])*100 >= 75 and float(subscribers[x][6])*100 <= 100:
                    subscribersIDG.append([str("subsID"),idSecondary])
                    subscribersLatG.append([float(subscribers[z][4]),float(latSecondary)])
                    subscribersLonG.append([float(subscribers[z][5]),float(lonSecondary)])
                    subscribersStatusG.append([float(subscribers[z][6])])
                    data_table_75_keycount += 1
                    data_table_75.append([str(data_table_75_keycount),str(subscribers[x][0]),str(subscribers[x][1]),str(subscribers[x][2]),str(subscribers[x][3]),
                        str(subscribers[x][4]),str(subscribers[x][5]),str(subscribers[x][6]),str(subscribers[x][7]),str(subscribers[x][8]),str(subscribers[x][9]),str(subscribers[x][10])])
    ######## OFFLINE DEVICES #########
    data['lat0'] = subscribersLatR
    data['lon0'] = subscribersLonR
    data['ID0'] = subscribersIDR
    data['status0'] = subscribersStatusR
    data['color0'] = 'red'
    ######## EMPEZANDO DEVICES #########
    data['lat25'] = subscribersLatO
    data['lon25'] = subscribersLonO
    data['ID25'] = subscribersIDO
    data['status25'] = subscribersStatusO
    data['color25'] = 'orange'
    ######## CONSTRUYENDOSE DEVICES #########
    data['lat50'] = subscribersLatY
    data['lon50'] = subscribersLonY
    data['ID50'] = subscribersIDY
    data['status0'] = subscribersStatusY
    data['color50'] = 'yellow'
    ######## ONLINE DEVICES #########
    data['lat75'] = subscribersLatG
    data['lon75'] = subscribersLonG
    data['ID75'] = subscribersIDG
    data['status75'] = subscribersStatusG
    data['color75'] = 'green'

    coordenadas = obtener_coordenadas_osm(proyecto)
    fig = tracesToMap(data, subscribersStatusG, coordenadas)
    return fig, data_table_0, data_table_25, data_table_50, data_table_75

###############################    R A D I O G R A F I A   T O R R E S - P O S T E S     ###############################
def tracesToMap(data, status, coordenadas):
    global fig, lat_media, lon_media, zoom_media
    try:
        ######## OFFLINE DEVICES #########
        for x in range(len(data["lat0"])):
            if x == 0:
                fig = go.Figure(go.Scattermapbox(
                    name="Completo",
                    mode="markers+lines",
                    lat=[data["lat0"][x][1],data["lat0"][x][0]],
                    lon=[data["lon0"][x][1],data["lon0"][x][0]],
                    marker={'size': 10},
                    text=[data["ID0"][x][1]],
                    marker_color='green')
                )
            if x != 0:
                fig.add_trace(go.Scattermapbox(
                    name="Pendiente",
                    mode="markers+lines",
                    lat=[data["lat0"][x][1],data["lat0"][x][0]],
                    lon=[data["lon0"][x][1],data["lon0"][x][0]],
                    marker={'size': 10},
                    text=[data["ID0"][x][1]],
                    marker_color='red')
                )
        ######## EMPEZANDO DEVICES #########
        for y in range(len(data["lat25"])):
            fig.add_trace(go.Scattermapbox(
                name= "Iniciado",
                mode = "markers+lines",
                lat = [data["lat25"][y][1],data["lat25"][y][0]],
                lon = [data["lon25"][y][1],data["lon25"][y][0]],
                marker = {'size': 10},
                text=[data["ID25"][y][1]],
                marker_color='orange')
            )
        ######## CONSTRUYENDOSE DEVICES #########
        for z in range(len(data["lat50"])):
            fig.add_trace(go.Scattermapbox(
                name= "En Proceso",
                mode = "markers+lines",
                lat = [data["lat50"][z][1],data["lat50"][z][0]],
                lon = [data["lon50"][z][1],data["lon50"][z][0]],
                marker = {'size': 10},
                text=[data["ID50"][z][1]],
                marker_color='#c9c702')
            )
        ######## ONLINE DEVICES #########
        for a in range(len(data["lat75"])):
            fig.add_trace(go.Scattermapbox(
                name= "Completo",
                mode = "markers+lines",
                lat = [data["lat75"][a][1],data["lat75"][a][0]],
                lon = [data["lon75"][a][1],data["lon75"][a][0]],
                marker = {'size': 10},
                text=[data["ID75"][a][1]],
                marker_color='green')
            )
        fig.update_layout(
            hovermode='closest',
            clickmode='event+select',
            mapbox=dict(
                zoom=zoom_media,
                style="open-street-map",
                center=go.layout.mapbox.Center(lat=float(coordenadas[0]),lon=float(coordenadas[1]))
            ),
            #l = left   #t = top   #b = bottom   #r = right
            margin ={'l':0,'t':0,'b':0,'r':0}
        )
        return fig
    except Exception as e:
        print(e)