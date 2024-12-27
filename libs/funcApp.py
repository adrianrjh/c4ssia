from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import json
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError

ipGlobal = '10.0.3.25'
ipRedis = '10.0.3.25'

session = False
r = ''
errno = ''
try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

data_rows, data_rowsPR, comboboxUsers, deviceRecep = [], [], [], []
comboboxGaran = ['NA','1M','3M','6M','9M','1A','3A','5A','8A','10A']
comboboxMisc = ['Misc','No Misc']
# Variable global para mantener la referencia de la tarea refresh
current_refresh_task = None
current_showlist_task = None
# Create columns for our issue table.
paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 1, 0, 0, 0, 0, 0, 0, 0
garantia, noserie, miscellaniuos = '', '', ''
sumaIteDevs = 0
data_rows_keycount = 0
single_article, noserie, marcaDev, modeloDev, descripcion, garantia, motivo, ubicacion, status = [], '', '', '', '', '', '', '', ''
qr_code = ''
trabajador = ''
dataaaa = []
data_to_report = []
counter = 0
marcaEU, modeloEU, descripcionEU, garantiaEU, noserieEU, motivoEU = 'Seleccionar', 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 'Seleccionar'
comboboxMotivos = ['Dañado Rep', 'Migracion', 'Cancelacion', 'Defecto Fab', 'Dañado Garan', 'Scrap']
columns = [
    ui.table_column(name='text', label='N° Equipo', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text0', label='Proyecto', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text1', label='Marca', sortable=True, searchable=False, max_width='140'),
    ui.table_column(name='text2', label='Modelo', sortable=True, searchable=False, max_width='140'),
    ui.table_column(name='text3', label='Descripcion', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text4', label='Cantidad', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text5', label='Garantia', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text6', label='Recibidos', sortable=True, searchable=True, max_width='140'),
]

columnsAsig = [
    ui.table_column(name='text', label='N° Equipo', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text0', label='N° Serie', sortable=True, searchable=True, max_width='200'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text2', label='Marca', sortable=True, searchable=False, max_width='100'),
    ui.table_column(name='text3', label='Modelo', sortable=True, searchable=False, max_width='140'),
    ui.table_column(name='text4', label='Descripcion', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text5', label='Garantia', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text6', label='Motivo', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text7', label='Ubicación', sortable=True, searchable=True, max_width='110'),
    ui.table_column(name='text8', label='Status', sortable=True, searchable=True, max_width='110'),
]

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

def getUser(id_key, id1, user):
    obj = decode_redis(r.get(str(id_key)))
    val = 0
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str(id1)+str(x)))
            if obj != {}:
                if obj['username'] == str(user):
                    fullname = str(obj['name'])+' '+str(obj['lastname'])
                    puesto = obj['puesto']
                    return fullname, puesto

def changeFieldTable(r, lista, noPR):
    r.hset("prs"+str(noPR),"lista",str(json.dumps(lista)))

def getSingleArticle(r, qr_code):
    obj = decode_redis(r.get(str('key_alm')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('alm')+str(x)))
            if obj != {}:
                if qr_code == obj['qr_code']:
                    return obj

def getSinglePr(r, idpr):
    single_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if idpr == obj['noPR']:
                    msg = json.loads(obj['lista'].replace("'","["))
                    for x in range(0,len(msg)):
                        noDev = msg[x][0]
                        proyecto = msg[x][1]
                        marcaDev = msg[x][2]
                        modeloDev = msg[x][3]
                        descripcion = msg[x][4]
                        cantidad = msg[x][5]
                        garantia = msg[x][7]
                        recibidos = msg[x][9]
                        single_prs.append([noDev, proyecto, marcaDev, modeloDev, descripcion, cantidad, garantia, recibidos])
        return single_prs

def getSinglePrAll(r, idpr):
    single_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if idpr == obj['noPR']:
                    msg = json.loads(obj['lista'].replace("'","["))
                    return msg

def getSinglePrAll2(r, idpr):
    single_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if idpr == obj['noPR']:
                    return obj

def getAllPrsxStatus(r, statusPR):
    all_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if statusPR == obj['status']:
                    nopr = obj['noPR']
                    proyecto = obj['proyecto']
                    fecha = obj['fecha']
                    encargado = obj['encargado']
                    totalPR = obj['totalPR']
                    status = obj['status']
                    all_prs.append([nopr, proyecto, fecha, encargado, totalPR, status])
        return all_prs

def devToAlm(r, keycount, fechallegada, nopr, proyecto, marca, modelo, descripcion, garantia, noserie, qr_code, tipo):
    device={
        "fechallegada":str(fechallegada),
        "nopr":str(nopr),
        "proyecto":str(proyecto),
        "marca":str(marca),
        "modelo":str(modelo),
        "descripcion":str(descripcion),
        "garantia":str(garantia),
        "noserie":str(noserie),
        "qr_code":str(qr_code),
        "status":'Almacenado',
        "ubicacion":'Almacen',
        "tipo":str(tipo),
    }
    r.set("key_alm",str(keycount))
    r.hmset('alm'+str(keycount), device)

def updAct(data, option):
    if option == 'arrived':
        idpr = data['noPR'].split("-")
        r.hset("prs"+str(idpr[1]),"status","Check-In")

def changeStateArticle(data, trabajador, action):
    if action == 'asignar':
        obj = decode_redis(r.get(str('key_alm')))
        if obj == {}:
            obj = 'NO'
            return obj
        else:
            for x in range(0, int(obj)+1):
                obj = decode_redis(r.hgetall(str('alm')+str(x)))
                if obj != {}:
                    if data[0][1] == obj['noserie']:
                        idpr = obj['nopr'].split("-")
                        trabajador = trabajador.split("/")
                        r.hset("alm"+str(x),"ubicacion",str(trabajador[0]))
                        r.hset("alm"+str(x),"status","Activo")
    if action == 'devolver':
        obj = decode_redis(r.get(str('key_alm')))
        if obj == {}:
            obj = 'NO'
            return obj
        else:
            for x in range(0, int(obj)+1):
                obj = decode_redis(r.hgetall(str('alm')+str(x)))
                if obj != {}:
                    if data[0][1] == obj['noserie']:
                        idpr = obj['nopr'].split("-")
                        trabajador = trabajador.split("/")
                        r.hset("alm"+str(x),"ubicacion",'Almacen')
                        r.hset("alm"+str(x),"status","Almacenado")
    if action == 'scrap':
        obj = decode_redis(r.get(str('key_alm')))
        if obj == {}:
            obj = 'NO'
            return obj
        else:
            for x in range(0, int(obj)+1):
                obj = decode_redis(r.hgetall(str('alm')+str(x)))
                if obj != {}:
                    if data[0][1] == obj['noserie']:
                        idpr = obj['nopr'].split("-")
                        trabajador = trabajador.split("/")
                        r.hset("alm"+str(x),"ubicacion",'Scrap')
                        r.hset("alm"+str(x),"status","Scrap")