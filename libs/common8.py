from h2o_wave import Q, app, main, ui, AsyncSite,site,data
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
import csv, datetime, json
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

session = False
r = ''
selectioned = ''

# Variable global para mantener la referencia de la tarea refresh
current_refresh_task = None
bandRefresh = 0

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)    
except Exception as e:
    print(e)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

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
comboboxGaran = ['NA','1M','3M','6M','9M','1A','3A','5A','8A','10A']
comboboxTrabajadores = ['Jesús Adrián Rojas Hernández', 'Eddy Romero']
comboboxMatDevs = ['Materiales de construccion', 'Equipos de Red']
comboboxMarca = []
comboboxModelo = []
comboboxDescripcion = []
comboboxUnidad = []
marcaPRs, modeloPRs, descripcionPRs, unidadPRs, cantidadPRs, costoPRs, garantiaPRs, linkCompraPRs = 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 1, '', 'Seleccionar', ''

comboboxTipo = []
comboboxMotivos = ['Recolección', 'Dañado Rep', 'Migracion', 'Cancelacion', 'Defecto Fab', 'Dañado Garan', 'Scrap']
comboboxCantidad = ['1', '10', '20', '30', '50', '100', '200', '300', '500', '1000']
comboboxUnidadAdd = ['CAJA', 'PZA', 'm']
comboboxTipoAdd = ['Misc', 'No Misc']
marcaEU, modeloEU, descripcionEU, garantiaEU, noserieEU, motivoEU = 'Seleccionar', 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 'Seleccionar'
marcaEN, modeloEN, descripcionEN, garantiaEN, noserieEN, motivoEN = 'Seleccionar', 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 'Seleccionar'
marcaMC, modeloMC, descripcionMC, garantiaMC, noserieMC, cantidadMC = 'Seleccionar', 'Seleccionar', 'Seleccionar', 'Seleccionar', '', 'Seleccionar'

username, startapp, refreshapp = 'adrianfime', 0, 0
data_rows, data_rows_first, data_rows_keycount = [], [], 0
proyecto, marca, modelo, descripcion, cantidad, costo, garantia, total, linkcompra, encargado, totalPR, recibidos, unidad = '', '', '', '', '', '', '', '', '', '', 0.0, 0, ''
data_rows2 = []
refreshDownload, rutaDoc = 0, ''
data_rows_keycountMat, data_rows_keycountDevs = 0, 0
nameProject=''
paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 1, 0, 0, 0, 0, 0, 0, 0
matsdevs, unidadAddDevs, tipo, tipoderegistro = 'Seleccionar', '', '', ''
data_keycount = 0
poste, fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero, potenciaposte = '', False, False, False, False, False, False, False, False, False , 0.0
flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, remateNA, cableaceroNA = False, False, False, False, False, False, False, False, False 
poste_completo= []
data_to_report = []

columns = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=False, min_width='50'),
    ui.table_column(name='text0', label='Proyecto', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text1', label='Marca', sortable=True, searchable=False, min_width='160'),
    ui.table_column(name='text2', label='Modelo', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text3', label='Descripcion', sortable=True, searchable=False, min_width='310'),
    ui.table_column(name='text4', label='Unidad', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text5', label='Cantidad', sortable=True, searchable=False, min_width='80'),
    ui.table_column(name='text6',  label='Costo', sortable=True, searchable=False, min_width='80'),
    ui.table_column(name='text7',  label='Total', sortable=True, searchable=False, min_width='70'),
    ui.table_column(name='text8',  label='Garantia', sortable=True, searchable=False, min_width='80'),
    ui.table_column(name='text9',  label='Link de compra', sortable=True, searchable=False, min_width='180'),
    ui.table_column(name='text10', label='Recibidos', sortable=True, searchable=False, min_width='80'),
]

columns2 = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=False, min_width='50'),
    ui.table_column(name='text0', label='Proyecto', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text1', label='Marca', sortable=True, searchable=False, min_width='160'),
    ui.table_column(name='text2', label='Modelo', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text3', label='Descripcion', sortable=True, searchable=False, min_width='150'),
    ui.table_column(name='text4', label='Unidad', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text5', label='Cantidad', sortable=True, searchable=False, min_width='90'),
    ui.table_column(name='text6',  label='Costo', sortable=True, searchable=False, min_width='70'),
    ui.table_column(name='text7',  label='Total', sortable=True, searchable=False, min_width='70'),
    ui.table_column(name='text8',  label='Garantia', sortable=True, searchable=False, min_width='70'),
    ui.table_column(name='text9',  label='Link de compra', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text10', label='Recibidos', sortable=True, searchable=False, min_width='70'),
]

columns3 = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=False, min_width='50'),
    ui.table_column(name='text0', label='Marca', sortable=True, searchable=False, min_width='250'),
    ui.table_column(name='text1', label='Modelo', sortable=True, searchable=False, min_width='250'),
    ui.table_column(name='text2', label='Descripcion', sortable=True, searchable=False, min_width='730'),
    ui.table_column(name='text3', label='Unidad', sortable=True, searchable=False, min_width='70'),
]

columns3Devs = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text0', label='Marca', sortable=True, searchable=False, min_width='250'),
    ui.table_column(name='text1', label='Modelo', sortable=True, searchable=False, min_width='250'),
    ui.table_column(name='text2', label='Descripcion', sortable=True, searchable=False, min_width='650'),
    ui.table_column(name='text3', label='Unidad', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text4', label='Tipo', sortable=True, searchable=False, min_width='100'),
]

columnsPRs = [
    ui.table_column(name='text0', label='N° PR', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text2', label='Fecha', sortable=True, searchable=True, min_width='135'),
    ui.table_column(name='text3', label='Encargado', sortable=True, searchable=True, min_width='190'),
    ui.table_column(name='text4', label='Total PR', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text5', label='Status', sortable=True, searchable=True, min_width='100', cell_type=ui.tag_table_cell_type(name='tags2', 
        tags=[        
            ui.tag(label='Active', color='#269c14'), 
            ui.tag(label='Checked', color='#b8bdb7'), 
            ui.tag(label='Authorized', color='#d4c753'), 
            ui.tag(label='Shopping', color='#ed6d66'), 
            ui.tag(label='Purchased', color='#5db4d4'), 
            ui.tag(label='Arrived', color='#f0baf7'),
            ui.tag(label='Check-In', color='#eb7023'),
            ui.tag(label='Done', color='#ffffff')
        ]
    ))
]

columnsProjects = [
    ui.table_column(name='text0', label='Fecha de arranque', sortable=True, searchable=True, min_width='150'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text2', label='Encargado', sortable=True, searchable=True, min_width='190'),
    ui.table_column(name='text3', label='Avance', sortable=True, min_width='70', cell_type=ui.progress_table_cell_type()),
]

columnsDevsOnProject = [
    ui.table_column(name='text0', label='Marca', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text1', label='Modelo', sortable=True, searchable=True, min_width='170'),
    ui.table_column(name='text2', label='Descripcion', sortable=True, searchable=True, min_width='150'),
    ui.table_column(name='text3', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text4', label='N° de Serie', sortable=True, searchable=True, min_width='180'),
    ui.table_column(name='text5', label='Tipo', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6',  label='Status', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text7',  label='Ubicacion', sortable=True, searchable=True, min_width='110'),
]

columnsProjectsPaP = [
    ui.table_column(name='text0', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='120'),
    ui.table_column(name='text2', label='Propietario', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text3', label='ID Poste', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text4',  label='Latitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text5', label='Longitud', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Status', sortable=True, min_width='70', cell_type=ui.progress_table_cell_type()),
    ui.table_column(name='text7', label='ID Caja', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text8', label='N° Ports', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text9', label='ID CE', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text10', label='Clients', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text11', label='To', sortable=True, searchable=True, min_width='70'),
    ui.table_column(name='text12', label='Pot Calculo', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text13', label='Pot Real', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text14', label='Pot Calidad', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text15', label='Tag Pot', sortable=True, searchable=True, min_width='80', cell_type=ui.tag_table_cell_type(name='tags2', 
        tags=[        
            ui.tag(label='Excelente', color='#066d99'),
            ui.tag(label='Muy bueno', color='#099906'), 
            ui.tag(label='Bueno', color='#fae60a'), 
            ui.tag(label='Regular', color='#e35927'), 
            ui.tag(label='Malo', color='#c40a32'),
            ui.tag(label='N/A', color='#172a30'),
        ]
    ))
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

columnsRegEU = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text0', label='N° Serie', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text2', label='Marca', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text3', label='Modelo', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text4', label='Descripcion', sortable=True, searchable=True, min_width='300'),
    ui.table_column(name='text5', label='Garantia', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Motivo', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text7', label='Ubicación', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text8', label='Status', sortable=True, searchable=True, min_width='90'),
]

columnsRegEN = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text0', label='N° Serie', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text2', label='Marca', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text3', label='Modelo', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text4', label='Descripcion', sortable=True, searchable=True, min_width='300'),
    ui.table_column(name='text5', label='Garantia', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Motivo', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text7', label='Ubicación', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text8', label='Status', sortable=True, searchable=True, min_width='90'),
]

columnsRegMC = [
    ui.table_column(name='text', label='N°', sortable=True, searchable=True, min_width='50'),
    ui.table_column(name='text0', label='N° Serie', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text1', label='Proyecto', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text2', label='Marca', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text3', label='Modelo', sortable=True, searchable=False, min_width='200'),
    ui.table_column(name='text4', label='Descripcion', sortable=True, searchable=True, min_width='300'),
    ui.table_column(name='text5', label='Garantia', sortable=True, searchable=True, min_width='80'),
    ui.table_column(name='text6', label='Cantidad', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text7', label='Ubicación', sortable=True, searchable=True, min_width='90'),
    ui.table_column(name='text8', label='Status', sortable=True, searchable=True, min_width='90'),
]

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

def getAll(r,key):
    obj = decode_redis(r.hgetall(key))
    if obj == {}:
        obj = 'NO'
    else:
        pass

    return obj

def materialesYI(r, key, data):
    pp={"materiales":json.dumps(data)}
    r.hmset(key,pp)

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

############## GGGGGGGEEEEEEETTTTT AAAAAALLLLLLLL ############
def getAllMatsDevs(r, materialesdevices):
    all_matsdevs, marca, modelo, descripcion, unidad= [], '', '', '',''
    if materialesdevices == 'Equipos de Red':
        obj = decode_redis(r.get(str('key_equipos_red')))
        if obj == 'NO':
            obj = 'NO'
            return obj
        else:
            for x in range(0, int(obj)+1):
                obj = decode_redis(r.hgetall(str('equipos_red')+str(x)))
                if obj != {}:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
            return all_matsdevs
    if materialesdevices == 'Materiales de construccion':
        obj = decode_redis(r.get(str('key_materiales')))
        if obj == 'NO':
            obj = 'NO'
            return obj
        else:
            for x in range(0, int(obj)+1):
                obj = decode_redis(r.hgetall(str('materiales')+str(x)))
                if obj != {}:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
            return all_matsdevs
############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR MMMMMMAAAAAARRRRRRCCCCCCAAAAA MMMMAAAATTTEEERRRRIIIAAAALLLEEESSS ############
def getAllMatsMarca(r, marcamats):
    all_matsdevs, marca, modelo, descripcion, unidad= [], '', '', '',''
    obj = decode_redis(r.get(str('key_materiales')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('materiales')+str(x)))
            if obj != {}:
                if marcamats == obj['marca']:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
        return all_matsdevs

############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR MMMMMMAAAAAARRRRRRCCCCCCAAAAA DDDDDDDEEEEEEEVVVVVVVSSSSSSS ############
def getAllDevsMarca(r, marcadevs):
    all_matsdevs, marca, modelo, descripcion, unidad= [], '', '', '',''
    obj = decode_redis(r.get(str('key_equipos_red')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('equipos_red')+str(x)))
            if obj != {}:
                if marcadevs == obj['marca']:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
        return all_matsdevs

############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR MMMMMMOOOOODDDDEEEEELLLLLOOOO MMMMAAAATTTEEERRRRIIIAAAALLLEEESSS ############
def getAllMatsModelo(r, modelomats):
    all_matsdevs, marca, modelo, descripcion, unidad= [], '', '', '',''
    obj = decode_redis(r.get(str('key_materiales')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('materiales')+str(x)))
            if obj != {}:
                if modelomats == obj['modelo']:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
        return all_matsdevs

############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR MMMMMMOOOOODDDDEEEEELLLLLOOOO DDDDDDDEEEEEEEVVVVVVVSSSSSSS ############
def getAllDevsModelo(r, modelodevs):
    all_matsdevs, marca, modelo, descripcion, unidad= [], '', '', '',''
    obj = decode_redis(r.get(str('key_equipos_red')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('equipos_red')+str(x)))
            if obj != {}:
                if modelodevs == obj['modelo']:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    unidad = obj['unidad']
                    all_matsdevs.append([marca, modelo, descripcion, unidad])
        return all_matsdevs

############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR DDDDDEEEEESSSSCCCCRRRRIIIIPPPPCCCCIIIOOOONN MMMMAAAATTTEEERRRRIIIAAAALLLEEESSS ############
def getAllMatsDescripcion(r, descripcionmats):
    unidad= ''
    obj = decode_redis(r.get(str('key_materiales')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('materiales')+str(x)))
            if obj != {}:
                if descripcionmats == obj['descripcion']:
                    unidad = obj['unidad']
        return unidad

############## GGGGGGGEEEEEEETTTTT FFFFFFFOOOOOOOORRRRRRR DDDDDEEEEESSSSCCCCRRRRIIIIPPPPCCCCIIIOOOONN DDDDDDDEEEEEEEVVVVVVVSSSSSSS ############
def getAllDevsDescripcion(r, descripciondevs):
    unidad= ''
    obj = decode_redis(r.get(str('key_equipos_red')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('equipos_red')+str(x)))
            if obj != {}:
                if descripciondevs == obj['descripcion']:
                    unidad = obj['unidad']
        return unidad

def devUsedToAlm(r, keycount, fechallegada, nopr, proyecto, marca, modelo, descripcion, garantia, noserie, qr_code, tipo):
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
        "status":'Usado',
        "ubicacion":'Almacen',
        "tipo":str(tipo),
    }
    r.set("key_alm_used",str(keycount))
    r.hmset('alm_used'+str(keycount), device)

def devNewToAlm(r, keycount, fechallegada, nopr, proyecto, marca, modelo, descripcion, garantia, noserie, qr_code, tipo):
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
        "status":'Nuevo',
        "ubicacion":'Almacen',
        "tipo":str(tipo),
    }
    r.set("key_alm_new",str(keycount))
    r.hmset('alm_new'+str(keycount), device)

def getAllMaterialesxMarca(r, mar, mod):
    obj = decode_redis(r.get(str('key_materiales')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        res = ''
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('materiales')+str(x)))
            if obj != {}:
                if res != 'SI':
                    if mar == obj['marca'] and mod == obj['modelo']:
                        res = 'SI'
                    else:
                        res = 'NO'
            else:
                res = 'NO'
        return res

def getAllEquiposRedxMarca(r, mar, mod):
    obj = decode_redis(r.get(str('key_equipos_red')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        res = ''
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('equipos_red')+str(x)))
            if obj != {}:
                if res != 'SI':
                    if mar == obj['marca'] and mod == obj['modelo']:
                        res = 'SI'
                    else:
                        res = 'NO'
            else:
                res = 'NO'
        return res

def getAllDevsxProject(r, proyectoP):
    all_devs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_alm')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('alm')+str(x)))
            if obj != {}:
                if proyectoP == obj['proyecto']:
                    marca = obj['marca']
                    modelo = obj['modelo']
                    descripcion = obj['descripcion']
                    proyecto = obj['proyecto']
                    noserie = obj['noserie']
                    tipo = obj['tipo']
                    status = obj['status']
                    ubicacion = obj['ubicacion']
                    all_devs.append([marca, modelo, descripcion, proyecto, noserie, tipo, status, ubicacion])
        return all_devs

def getSinglePr(r, username, idpr):
    single_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if username == obj['username']:
                    if idpr == obj['noPR']:
                        single_prs = obj
        return single_prs

def getAllPrsxUser(r, username):
    all_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                if username == obj['username']:
                    nopr = obj['noPR']
                    proyecto = obj['proyecto']
                    fecha = obj['fecha']
                    encargado = obj['encargado']
                    totalPR = obj['totalPR']
                    status = obj['status']
                    all_prs.append([nopr, proyecto, fecha, encargado, totalPR, status])
        return all_prs

def getAllPrsxStatus(r, statusPR):
    all_prs, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_prs')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('prs')+str(x)))
            if obj != {}:
                #if statusPR == obj['status']:
                nopr = obj['noPR']
                proyecto = obj['proyecto']
                fecha = obj['fecha']
                encargado = obj['encargado']
                totalPR = obj['totalPR']
                status = obj['status']
                all_prs.append([nopr, proyecto, fecha, encargado, totalPR, status])
        return all_prs

def regList(r, keycount, proyecto, encargado, username, lista, totalPR):
    from numpy.random import seed
    from numpy.random import randint
    seed(1)
    values = randint(0, 100, 1)
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    nopr = (now.strftime("%Y%m%d"))+'-'+str(keycount)
    pp={"proyecto":proyecto,"noPR":str(nopr),"encargado":encargado,"fecha":str(dt_string),"username":username,"lista":json.dumps(lista), "totalPR":totalPR, 'status':'Active'}
    r.set("key_prs",str(keycount))
    r.hmset('prs'+str(keycount), pp)

def updAct(data, option):
    if option == 'checked':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Checked")
    if option == 'authorized':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Authorized")
    if option == 'shopping':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Shopping")
    if option == 'purchased':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Purchased")
    if option == 'arrived':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Arrived")
    if option == 'check-in':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Check-In")
    if option == 'done':
        for i in range(0,len(data)):
            idpr = data[0][0].split("-")
            r.hset("prs"+str(idpr[1]),"status","Done")

def getPostePaP(r, proyectoPaP, postePaP):
    all_poste, nopr, proyecto, fecha, encargado, totalPR, status = [], '', '', '','', '', ''
    obj = decode_redis(r.get(str('key_poste')))
    if obj == 'NO':
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('poste')+str(x)))
            if obj != {}:
                if proyectoPaP == obj['proyecto']:
                    if postePaP == obj['poste']:
                        fecha = obj['fecha']
                        proyecto = obj['proyecto']
                        poste = obj['poste']
                        fleje, flejeNA = obj['fleje'], obj['flejeNA']
                        herraje, herrajeNA = obj['herraje'], obj['herrajeNA']
                        brazo, brazoNA = obj['brazo'], obj['brazoNA']
                        gaza, gazaNA = obj['gaza'], obj['gazaNA']
                        raqueta, raquetaNA = obj['raqueta'], obj['raquetaNA']
                        cajadistribucion, cajadistribucionNA = obj['cajadistribucion'], obj['cajadistribucionNA']
                        cierreempalme, cierreempalmeNA = obj['cierreempalme'], obj['cierreempalmeNA']
                        remate, remateNA = obj['remate'], obj['remateNA']
                        cableacero, cableaceroNA = obj['cableacero'], obj['cableaceroNA']
                        potenciaposte = obj['potenciaposte']
                        all_poste.append([fecha, proyecto, poste, fleje, flejeNA, herraje, herrajeNA, brazo, brazoNA, gaza, gazaNA, raqueta, raquetaNA, cajadistribucion, cajadistribucionNA, cierreempalme, cierreempalmeNA, remate, remateNA, cableacero, cableaceroNA, potenciaposte])
        return all_poste

def regDataPaP(r, data):
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
                if msg[0][1] == data['proyecto']:
                    for y in range(0, len(msg)):
                        if str(msg[y][3]) == str(data['poste']):
                            msg[y][6] = data['status']
                            msg[y][11] = data['potenciaposte']
                            pp={"postes":json.dumps(msg), "proyecto":data['proyecto']}
                            r.hmset("pap"+str(x), pp)

def regPostePaP(r, data):
    key_count = r.get('key_poste')
    if key_count is None:
        key_count = 0
    else:
        key_count = int(key_count.decode("utf-8"))
    poste_existente = False
    for x in range(key_count):
        obj = decode_redis(r.hgetall('poste'+str(x)))
        if obj and obj['proyecto'] == data['proyecto'] and obj['poste'] == data['poste']:
            poste_existente = True
            r.hmset("poste"+str(x), data)
            break
    if not poste_existente:
        # CREAR NUEVO POSTE
        r.hmset("poste" + str(key_count+1), data)
        r.set("key_poste", str(key_count+1))