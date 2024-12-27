from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import csv, time, datetime, json
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError
# adding Folder to the system path
import sys
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import *

session = False
r = ''
selectioned = ''
refreshTable = 0
current_refresh_task = None

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
comboboxHorarios = ['09:00 am - 11:00 am', '11:00 am - 13:00 pm', '13:00 pm - 15:00 pm', '15:00 pm - 17:00 pm', '17:00 pm - 18:00 pm']
comboboxPaquetePlan = ['Comodato', 'Comprado']
comboboxAnchoBanda = ['30MB', '50MB', '100MB', '150MB', '200MB', '250MB']
paso1P, paso2P, paso3P, paso4P, paso5P, paso6P, bandPaso1, bandPaso2, bandPaso3, bandPaso4, paso5P, bandPaso5, bandPaso6 = 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo = '', '', '', '', '', '', ''
tecnologia, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo = '', '', '', '', '', '', ''
proyectoTicket, posteTicket, prioridadTicket, problemaTicket, evidenciaTicket, encoded_string, content, rootEvidencia, comboboxProyecto, comboboxPoste = '', '', '', '', '', '', '', '', [], []
ticketSelectioned, qr_code_iis = '', ''
data_rows_materials, data_rows_materials_keycount = [], 0
data_rows, data_rows_save, data_rows_keycount = [], [], 0
ticketNew_iis = ''
id_client, ip_client, password_client, date_picker_cita, horario_cita, installerWorker = '', '', '', '', '', ''
noticketPaP, tiempoPaP, proyectoPaP, postePaP, asignadoPaP, prioridadPaP, problemaPaP, statusPaP, trabajadorAsignado, textSolucionTicket, solutionTicket = '', '', '', '', '', '', '', '', '', '', ''
####### A   D   D        T  I   C   K   E   T ########
noservicio, telefono, tiposervicio, tipoproblema, problema = '', '', '', '', ''
matsdevsIIS, marcaIIS, modeloIIS, descripcionIIS, unidadIIS, cantidadIIS = '', '', '', '', '', 0.0
comboboxUsers = []
comboboxMatDevs = ['Materiales de construccion', 'Equipos de Red']
comboboxMarca = []
comboboxModelo = []
comboboxDescripcion = []
data_rows_materials1 = []
data_rows_materials_send = []

comboboxTS = ['Fibra Optica', 'Inalámbrico Privado', 'Red de Acceso Publico', 'Otro']
comboboxTP = ['Sin acceso a internet', 'Bajo rendimiento', 'Ampliar paquete', 'Disminuir paquete', 
              'Cambio de contraseña', 'Reubicación de modem', 'Reubicación de servicio', 
              'Ampliar cobertura', 'Intermitencia', 'Otro', 'Liberación de clave','Cambio de equipo']

columnsIIS = [
    ui.table_column(name='text0', label='ID Ticket', sortable=True, searchable=True, min_width='130'),
    ui.table_column(name='text1', label='Nombre del Cliente', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text2', label='Domicilio', sortable=True, searchable=True, min_width='200'),
    ui.table_column(name='text3', label='Localidad', sortable=True, searchable=True, min_width='140'),
    ui.table_column(name='text4', label='Teléfono', sortable=True, searchable=True, min_width='100'),
    ui.table_column(name='text5', label='Paquete Plan', sortable=True, searchable=True, min_width='110'),
    ui.table_column(name='text6', label='Fecha de creación', sortable=True, searchable=True, min_width='150'),
    ui.table_column(name='text7', label='Creador del Ticket', sortable=True, searchable=True, min_width='160'),
    ui.table_column(name='text8', label='Status', sortable=True, searchable=True, max_width='150', cell_type=ui.tag_table_cell_type(name='tags1', 
        tags=[
            ui.tag(label='Active', color='#27964e'),
            ui.tag(label='InfoXAsig', color='#f7f020'),
            ui.tag(label='Date Created', color='#0eb4f0'),
            ui.tag(label='Date Confirmed', color='#7c7e80'),
            ui.tag(label='Ticket Asigned', color='#e6823c'),
            ui.tag(label='Asigned Material', color='#fc039d'),
            ui.tag(label='In Transit', color='#fac9b4'),
            ui.tag(label='In Process', color='#5367fc'),
            ui.tag(label='Installation Finished', color='#cfd4fc'),
            ui.tag(label='Provisioned Client', color='#f55678'),
            ui.tag(label='Attached Evidence', color='#d0e089'),
            ui.tag(label='Payment Received', color='#467a40'),
        ]
    )),
    ui.table_column(name='text9', label='Ultima actualización', sortable=True, searchable=True, min_width='180'),
]

columnsAsig = [
    ui.table_column(name='text', label='N°', sortable=False, searchable=False, max_width='40'),
    ui.table_column(name='text0', label='N° Serie', sortable=False, searchable=False, max_width='100'),
    ui.table_column(name='text1', label='Proyecto', sortable=False, searchable=False, max_width='90'),
    ui.table_column(name='text2', label='Marca', sortable=False, searchable=False, max_width='90'),
    ui.table_column(name='text3', label='Modelo', sortable=False, searchable=False, max_width='100'),
    ui.table_column(name='text4', label='Descripcion', sortable=False, searchable=False, max_width='140'),
    ui.table_column(name='text5', label='Ubicación', sortable=False, searchable=False, max_width='80'),
    ui.table_column(name='text6', label='Status', sortable=False, searchable=False, max_width='60'),
]

columnsAsigIIS1 = [
    ui.table_column(name='text1', label='Marca', sortable=True, searchable=False, min_width='160'),
    ui.table_column(name='text2', label='Modelo', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text3', label='Descripcion', sortable=True, searchable=False, min_width='310'),
    ui.table_column(name='text4', label='Unidad', sortable=True, searchable=False, min_width='100'),
    ui.table_column(name='text5', label='Cantidad', sortable=True, searchable=False, min_width='80'),
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

def getSingleArticle(r, qr_code):
    findDevice = 0
    obj_new = decode_redis(r.get(str('key_alm_new')))
    obj_used = decode_redis(r.get(str('key_alm_used')))
    if obj_new == {} and obj_used == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj_new)+1):
            obj = decode_redis(r.hgetall(str('alm_new')+str(x)))
            if obj != {}:
                if qr_code == obj['qr_code']:
                    if obj['ubicacion'] == "Almacen":
                        findDevice = 1
                        return obj
        for y in range(0, int(obj_used)+1):
            obj = decode_redis(r.hgetall(str('alm_used')+str(y)))
            if obj != {}:
                if qr_code == obj['qr_code']:
                    if obj['ubicacion'] == "Almacen":
                        findDevice = 1
                        return obj
        if findDevice == 0:
            obj = 'NO'
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

def getAllTickets(r, counter, key, findarea):
    all_tickets, noticket, time, proyecto, poste, prioridad, problema, status, asignado = [], '', '', '', '', '', '', '', ''
    obj = decode_redis(r.get(str(counter)))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str(key)+str(x)))
            if obj != {}:
                if obj['area'] == str(findarea):
                    if obj['status'] != 'Validated':
                        noticket = obj['noticket']
                        time = obj['time']
                        proyecto = obj['proyecto']
                        poste = obj['poste']
                        asignado = obj['asignado']
                        prioridad = obj['prioridad']
                        problema = obj['problema']
                        status = obj['status']
                        all_tickets.append([noticket, time, proyecto, poste, asignado, prioridad, problema, status])
        return all_tickets

def getTicketPaP(r, ticketSearch, proyectoSearch, posteSearch):
    all_ticket, noticket, time, proyecto, poste, asignado, prioridad, problema, status, evidencia1, evidencia2, solution = [], '', '', '', '', '', '', '', '', '', '', ''
    obj = decode_redis(r.get(str('key_tickets_obra')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('tickets_obra')+str(x)))
            if obj != {}:
                if obj['noticket'] == str(ticketSearch):
                    if obj['proyecto'] == str(proyectoSearch):
                        if obj['poste'] == str(posteSearch):
                            time = obj['time']
                            noticket = obj['noticket']
                            proyecto = obj['proyecto']
                            poste = obj['poste']
                            asignado = obj['asignado']
                            prioridad = obj['prioridad']
                            problema = obj['problema']
                            status = obj['status']
                            evidencia1 = obj['evidencia1']
                            evidencia2 = obj['evidencia2']
                            solution = obj['solution']
                            all_ticket.append([noticket, time, proyecto, poste, prioridad, problema, status, evidencia1, evidencia2, solution])
        return all_ticket

def regAct(key_count, data):
    r.hmset("tickets_"+str(key_count), data)
    r.set("tickets_key",str(key_count))

def updAct(data, option):
    if option == 0:
        r.hset("tickets_"+str(data['ticket_key']),"area",str(data["area"]))
        r.hset("tickets_"+str(data['ticket_key']),"time",str(data["time"]))
        r.hset("tickets_"+str(data['ticket_key']),"id",str(data["id"]))
        r.hset("tickets_"+str(data['ticket_key']),"cliente",str(data["cliente"]))
        r.hset("tickets_"+str(data['ticket_key']),"contacto",str(data["contacto"]))
        r.hset("tickets_"+str(data['ticket_key']),"servicio",str(data["servicio"]))
        r.hset("tickets_"+str(data['ticket_key']),"problema",str(data["problema"]))
        r.hset("tickets_"+str(data['ticket_key']),"status",str(data["status"]))
        r.hset("tickets_"+str(data['ticket_key']),"asignado",str(data["asignado"]))
        r.hset("tickets_"+str(data['ticket_key']),"descripcion",str(data["descripcion"]))
    if option == 'in process':
        r.hset("tickets_"+str(data[0][0]),"area",str(data[0][1]))
        r.hset("tickets_"+str(data[0][0]),"time",str(data[0][2]))
        r.hset("tickets_"+str(data[0][0]),"id","tickets")
        r.hset("tickets_"+str(data[0][0]),"cliente",str(data[0][3]))
        r.hset("tickets_"+str(data[0][0]),"contacto",str(data[0][4]))
        r.hset("tickets_"+str(data[0][0]),"servicio",str(data[0][5]))
        r.hset("tickets_"+str(data[0][0]),"problema",str(data[0][6]))
        r.hset("tickets_"+str(data[0][0]),"status",'In Process')
        r.hset("tickets_"+str(data[0][0]),"asignado",str(data[0][8]))
        r.hset("tickets_"+str(data[0][0]),"descripcion",str(data[0][9]))
    if option == 'validate':
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        r.hset("tickets_"+str(data[0][0]),"area",str(data[0][1]))
        r.hset("tickets_"+str(data[0][0]),"time",str(data[0][2]))
        r.hset("tickets_"+str(data[0][0]),"id","tickets")
        r.hset("tickets_"+str(data[0][0]),"cliente",str(data[0][3]))
        r.hset("tickets_"+str(data[0][0]),"contacto",str(data[0][4]))
        r.hset("tickets_"+str(data[0][0]),"servicio",str(data[0][5]))
        r.hset("tickets_"+str(data[0][0]),"problema",str(data[0][6]))
        r.hset("tickets_"+str(data[0][0]),"status",'Validated')
        r.hset("tickets_"+str(data[0][0]),"asignado",str(dt_string))
        r.hset("tickets_"+str(data[0][0]),"descripcion",str(data[0][9]))

def updActPaP(r, ticketSearch, proyectoSearch, posteSearch, trabajador, option, descriptionsolution, solution):
    obj = decode_redis(r.get(str('key_tickets_obra')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('tickets_obra')+str(x)))
            if obj != {}:
                if obj['noticket'] == str(ticketSearch):
                    if obj['proyecto'] == str(proyectoSearch):
                        if obj['poste'] == str(posteSearch):
                            if option == 'asigned':
                                r.hset("tickets_obra"+str(x),"status",'Asigned')
                                r.hset("tickets_obra"+str(x),"asignado",trabajador)
                            if option == 'in process':
                                r.hset("tickets_obra"+str(x),"status",'In Process')
                            if option == 'done':
                                r.hset("tickets_obra"+str(x),"status",'Done')
                                r.hset("tickets_obra"+str(x),"evidencia2",solution)
                                r.hset("tickets_obra"+str(x),"solution",descriptionsolution)

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
                msg = json.loads(obj["postes"].replace("'","["))
                for y in range(0,len(msg)):
                    if proyecto != msg[x][1]:
                        proyecto = msg[x][1]
                        all_PaP.append(proyecto)
        return all_PaP

def getAllPostesPaP(project):
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


def getAllTicketsIIS(r, counter, key):
    all_tickets, id_ticket, name_client, address_client, localidad_client, phone_client, paqueteplan, date_ticket, username, status, date_status = [], '', '', '', '', '', '', '', '', '', ''
    obj = decode_redis(r.get(str(counter)))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str(key)+str(x)))
            if obj != {}:
                #if obj['area'] == str(findarea):
                id_ticket = obj['id_ticket']
                name_client = obj['name_client']
                address_client = obj['address_client']
                localidad_client = obj['localidad_client']
                phone_client = obj['phone_client']
                paqueteplan = obj['paqueteplan']
                date_ticket = obj['date_ticket']
                username = obj['username']
                status = obj['status']
                date_status = obj['date_status']
                all_tickets.append([id_ticket, name_client, address_client, localidad_client, phone_client, paqueteplan, date_ticket, username, status, date_status])
        return all_tickets

def getTicketIIS(r, id_ticket):
    obj = decode_redis(r.get(str('tickets_iis_key')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('tickets_iis')+str(x)))
            if obj != {}:
                if id_ticket == obj['id_ticket']:
                    return obj

def updateTicketIIS(r, paso, noticket, data):
    obj = decode_redis(r.get(str('tickets_iis_key')))
    if obj == {}:
        obj = 'NO'
        return obj
    else:
        for x in range(0, int(obj)+1):
            obj = decode_redis(r.hgetall(str('tickets_iis')+str(x)))
            if obj != {}:
                if noticket == obj['id_ticket']:
                    if paso == 'paso1':
                        r.hset("tickets_iis"+str(x),"id_client", str(data[0]))
                        r.hset("tickets_iis"+str(x),"ip_client", str(data[1]))
                        r.hset("tickets_iis"+str(x),"password_client", str(data[2]))
                        r.hset("tickets_iis"+str(x),"status", str('InfoXAsig'))
                    if paso == 'paso2':
                        r.hset("tickets_iis"+str(x),"cita_instalacion", str(data[0]+' '+data[1]))
                        r.hset("tickets_iis"+str(x),"status", str('Date Created'))
                    if paso == 'paso3':
                        r.hset("tickets_iis"+str(x),"instalador", str(data[0]))
                        r.hset("tickets_iis"+str(x),"materiales_instalador",json.dumps(data[1]))
                        r.hset("tickets_iis"+str(x),"status", str('Ticket Asigned'))
                    if paso == 'paso4':
                        r.hset("tickets_iis"+str(x),"materiales_instalador_asignado",json.dumps(data[0]))
                        r.hset("tickets_iis"+str(x),"status", str('Asigned Material'))

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

def changeStateArticle(data, trabajador, action):
    if action == 'asignar':
        obj_new = decode_redis(r.get(str('key_alm_new')))
        obj_used = decode_redis(r.get(str('key_alm_used')))
        if obj_new == {} and obj_used == {}:
            obj = 'NO'
            return obj
        else:
            for y in range(0, len(data)):
                for x in range(0, int(obj_new)+1):
                    obj = decode_redis(r.hgetall(str('alm_new')+str(x)))
                    if obj != {}:
                        if data[y][1] == obj['noserie']:
                            r.hset("alm_new"+str(x),"ubicacion",str(trabajador))
                            r.hset("alm_new"+str(x),"status","Activo")
                for x in range(0, int(obj_used)+1):
                    obj = decode_redis(r.hgetall(str('alm_used')+str(x)))
                    if obj != {}:
                        if data[y][1] == obj['noserie']:
                            r.hset("alm_used"+str(x),"ubicacion",str(trabajador))
                            r.hset("alm_used"+str(x),"status","Activo")
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
                        r.hset("alm"+str(x),"ubicacion",'Scrap')
                        r.hset("alm"+str(x),"status","Scrap")

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