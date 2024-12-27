from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import csv, time, datetime, json
from redistimeseries.client import Client
from redis import StrictRedis, ConnectionError

ipGlobal = '10.0.3.25'
ipRedis = '10.0.3.25'

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

# comboboxEquipo = []
# comboboxDisp = ['AP', 'PTP', 'SWITCH', 'ROUTER', 'OLT', 'ONU']
# comboboxOLTS = ['DSP7001_4', 'DSP7001_8', 'DSP7001_16']
# comboboxSWITCHS = ['ARISTA 7050S_64_F', 'MIKROTIK RB750R2']
# comboboxROUTERS = ['MIKROTIK RB1100', 'MIKROTIK RB450', 'MIKROTIK RB750', 'MIKROTIK RB750 R2', 'MIKROTIK RB760']
# comboboxAPTP = ['ROCKET AC', 'ROCKER AC PRISM', 'MIMOSA C5C', 'MIMOSA B11', 'MOTOROLLA C0509A', 'POWERBEAM 5ACGEN2', 'LITEBEAM 5ACGEN2', 'NANO STATION LOCO AC', 'LITEBEAM M5', 'LAP120', 'LAP-GPS']
# comboboxONU = ['XC220_G3']
# comboboxTecno = ['FIBRA', '5GHz', '2.4GHz']
# comboboxLvl = ['L0', 'L1', 'L2', 'L3', 'L4', 'LA', 'LP', 'LSW', 'LR', 'LOL', 'LON']
# paso1P, paso2P, paso3P, paso4P, paso5P, paso6P, bandPaso1, bandPaso2, bandPaso3, bandPaso4, paso5P, bandPaso5, bandPaso6 = 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
# ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo = '', '', '', '', '', '', ''
# tecnologia, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo = '', '', '', '', '', '', ''
# proyectoTicket, posteTicket, prioridadTicket, problemaTicket, evidenciaTicket, encoded_string, content, rootEvidencia, comboboxProyecto, comboboxPoste = '', '', '', '', '', '', '', '', [], []
data_rows = []

# noticketPaP, tiempoPaP, proyectoPaP, postePaP, asignadoPaP, prioridadPaP, problemaPaP, statusPaP, trabajadorAsignado, textSolucionTicket, solutionTicket = '', '', '', '', '', '', '', '', '', '', ''
# comboboxUsers = []
####### A   D   D        T  I   C   K   E   T ########
# noservicio, telefono, tiposervicio, tipoproblema, problema = '', '', '', '', ''
# comboboxTS = ['Fibra Optica', 'Inalámbrico Privado', 'Red de Acceso Publico', 'Otro']
# comboboxTP = ['Sin acceso a internet', 'Bajo rendimiento', 'Ampliar paquete', 'Disminuir paquete', 
#               'Cambio de contraseña', 'Reubicación de modem', 'Reubicación de servicio', 
#               'Ampliar cobertura', 'Intermitencia', 'Otro', 'Liberación de clave','Cambio de equipo']

columns = [
    ui.table_column(name='text0', label='N°Ticket', sortable=True, searchable=True, max_width='70'),
    ui.table_column(name='text1', label='Área', sortable=True, searchable=True, max_width='90'),
    ui.table_column(name='text2', label='Fecha', sortable=True, searchable=True, max_width='150'),
    ui.table_column(name='text3', label='Cliente', sortable=True, searchable=True, max_width='80'),
    ui.table_column(name='text4', label='Contacto', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text5', label='Servicio', sortable=True, searchable=True, max_width='170'),
    ui.table_column(name='text6', label='Problema', sortable=True, searchable=True, max_width='170'),
    ui.table_column(name='text7', label='Status', sortable=True, searchable=True, max_width='90', cell_type=ui.tag_table_cell_type(name='tags1', tags=[ui.tag(label='Waiting', color='#f7f020'),ui.tag(label='Active', color='#27964e'), ui.tag(label='In Process', color='#0eb4f0'), ui.tag(label='Done', color='#7c7e80'), ui.tag(label='Validated', color='#e6823c')])),
    ui.table_column(name='text8', label='Asignado', sortable=True, searchable=True, max_width='150'),
    ui.table_column(name='text9', label='Descripción', sortable=True, searchable=True, max_width='300'),
]

# columnsDone = [
#     ui.table_column(name='text0', label='N°Ticket', sortable=True, searchable=True, max_width='70'),
#     ui.table_column(name='text1', label='Área', sortable=True, searchable=True, max_width='90'),
#     ui.table_column(name='text2', label='Fecha', sortable=True, searchable=True, max_width='150'),
#     ui.table_column(name='text3', label='Cliente', sortable=True, searchable=True, max_width='80'),
#     ui.table_column(name='text4', label='Contacto', sortable=True, searchable=True, max_width='120'),
#     ui.table_column(name='text5', label='Servicio', sortable=True, searchable=True, max_width='170'),
#     ui.table_column(name='text6', label='Problema', sortable=True, searchable=True, max_width='170'),
#     ui.table_column(name='text7', label='Status', sortable=True, searchable=True, max_width='90', cell_type=ui.tag_table_cell_type(name='tags2', tags=[ui.tag(label='Waiting', color='#f7f020'),ui.tag(label='Active', color='#27964e'), ui.tag(label='In Process', color='#0eb4f0'), ui.tag(label='Done', color='#7c7e80'), ui.tag(label='Validated', color='#e6823c')])),
#     ui.table_column(name='text8', label='Terminado', sortable=True, searchable=True, max_width='150'),
#     ui.table_column(name='text9', label='Descripción', sortable=True, searchable=True, max_width='300'),
# ]

# columnsTicketsPaP = [
#     ui.table_column(name='text0', label='N°Ticket', sortable=True, searchable=True, min_width='140'),
#     ui.table_column(name='text1', label='Creado', sortable=True, searchable=True, min_width='140'),
#     ui.table_column(name='text2', label='Proyecto', sortable=True, searchable=True, min_width='200'),
#     ui.table_column(name='text3', label='Poste', sortable=True, searchable=True, min_width='80'),
#     ui.table_column(name='text4', label='Asignado A', sortable=True, searchable=True, min_width='150'),
#     ui.table_column(name='text5', label='Prioridad', sortable=True, searchable=True, min_width='100', cell_type=ui.tag_table_cell_type(name='tags2', tags=[ui.tag(label='Baja', color='#2096f7'),ui.tag(label='Media', color='#a820f7'), ui.tag(label='Alta', color='#f72081'), ui.tag(label='Muy Alta', color='#f72020')])),
#     ui.table_column(name='text6', label='Problema', sortable=True, searchable=True, min_width='300', cell_overflow='wrap'),
#     ui.table_column(name='text7', label='Status', sortable=True, searchable=True, min_width='150', cell_type=ui.tag_table_cell_type(name='tags', tags=[ui.tag(label='Active', color='#27964e'), ui.tag(label='Asigned', color='#fc701e'), ui.tag(label='In Process', color='#0eb4f0'), ui.tag(label='Done', color='#7c7e80'), ui.tag(label='Validated', color='#cc05f0')])),
# ]

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

# def getAllTickets(r, counter, key, findarea):
#     all_tickets, noticket, time, proyecto, poste, prioridad, problema, status, asignado = [], '', '', '', '', '', '', '', ''
#     obj = decode_redis(r.get(str(counter)))
#     if obj == {}:
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str(key)+str(x)))
#             if obj != {}:
#                 if obj['area'] == str(findarea):
#                     if obj['status'] != 'Validated':
#                         noticket = obj['noticket']
#                         time = obj['time']
#                         proyecto = obj['proyecto']
#                         poste = obj['poste']
#                         asignado = obj['asignado']
#                         prioridad = obj['prioridad']
#                         problema = obj['problema']
#                         status = obj['status']
#                         all_tickets.append([noticket, time, proyecto, poste, asignado, prioridad, problema, status])
#         return all_tickets

# def getTicketPaP(r, ticketSearch, proyectoSearch, posteSearch):
#     all_ticket, noticket, time, proyecto, poste, asignado, prioridad, problema, status, evidencia1, evidencia2, solution = [], '', '', '', '', '', '', '', '', '', '', ''
#     obj = decode_redis(r.get(str('key_tickets_obra')))
#     if obj == {}:
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str('tickets_obra')+str(x)))
#             if obj != {}:
#                 if obj['noticket'] == str(ticketSearch):
#                     if obj['proyecto'] == str(proyectoSearch):
#                         if obj['poste'] == str(posteSearch):
#                             time = obj['time']
#                             noticket = obj['noticket']
#                             proyecto = obj['proyecto']
#                             poste = obj['poste']
#                             asignado = obj['asignado']
#                             prioridad = obj['prioridad']
#                             problema = obj['problema']
#                             status = obj['status']
#                             evidencia1 = obj['evidencia1']
#                             evidencia2 = obj['evidencia2']
#                             solution = obj['solution']
#                             all_ticket.append([noticket, time, proyecto, poste, prioridad, problema, status, evidencia1, evidencia2, solution])
#         return all_ticket

# def regAct(key_count, data):
#     r.hmset("tickets_"+str(key_count), data)
#     r.set("tickets_key",str(key_count))

# def updAct(data, option):
#     if option == 0:
#         r.hset("tickets_"+str(data['ticket_key']),"area",str(data["area"]))
#         r.hset("tickets_"+str(data['ticket_key']),"time",str(data["time"]))
#         r.hset("tickets_"+str(data['ticket_key']),"id",str(data["id"]))
#         r.hset("tickets_"+str(data['ticket_key']),"cliente",str(data["cliente"]))
#         r.hset("tickets_"+str(data['ticket_key']),"contacto",str(data["contacto"]))
#         r.hset("tickets_"+str(data['ticket_key']),"servicio",str(data["servicio"]))
#         r.hset("tickets_"+str(data['ticket_key']),"problema",str(data["problema"]))
#         r.hset("tickets_"+str(data['ticket_key']),"status",str(data["status"]))
#         r.hset("tickets_"+str(data['ticket_key']),"asignado",str(data["asignado"]))
#         r.hset("tickets_"+str(data['ticket_key']),"descripcion",str(data["descripcion"]))
#     if option == 'in process':
#         r.hset("tickets_"+str(data[0][0]),"area",str(data[0][1]))
#         r.hset("tickets_"+str(data[0][0]),"time",str(data[0][2]))
#         r.hset("tickets_"+str(data[0][0]),"id","tickets")
#         r.hset("tickets_"+str(data[0][0]),"cliente",str(data[0][3]))
#         r.hset("tickets_"+str(data[0][0]),"contacto",str(data[0][4]))
#         r.hset("tickets_"+str(data[0][0]),"servicio",str(data[0][5]))
#         r.hset("tickets_"+str(data[0][0]),"problema",str(data[0][6]))
#         r.hset("tickets_"+str(data[0][0]),"status",'In Process')
#         r.hset("tickets_"+str(data[0][0]),"asignado",str(data[0][8]))
#         r.hset("tickets_"+str(data[0][0]),"descripcion",str(data[0][9]))
#     if option == 'validate':
#         now = datetime.datetime.now()
#         dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
#         r.hset("tickets_"+str(data[0][0]),"area",str(data[0][1]))
#         r.hset("tickets_"+str(data[0][0]),"time",str(data[0][2]))
#         r.hset("tickets_"+str(data[0][0]),"id","tickets")
#         r.hset("tickets_"+str(data[0][0]),"cliente",str(data[0][3]))
#         r.hset("tickets_"+str(data[0][0]),"contacto",str(data[0][4]))
#         r.hset("tickets_"+str(data[0][0]),"servicio",str(data[0][5]))
#         r.hset("tickets_"+str(data[0][0]),"problema",str(data[0][6]))
#         r.hset("tickets_"+str(data[0][0]),"status",'Validated')
#         r.hset("tickets_"+str(data[0][0]),"asignado",str(dt_string))
#         r.hset("tickets_"+str(data[0][0]),"descripcion",str(data[0][9]))

# def updActPaP(r, ticketSearch, proyectoSearch, posteSearch, trabajador, option, descriptionsolution, solution):
#     obj = decode_redis(r.get(str('key_tickets_obra')))
#     if obj == {}:
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str('tickets_obra')+str(x)))
#             if obj != {}:
#                 if obj['noticket'] == str(ticketSearch):
#                     if obj['proyecto'] == str(proyectoSearch):
#                         if obj['poste'] == str(posteSearch):
#                             if option == 'asigned':
#                                 r.hset("tickets_obra"+str(x),"status",'Asigned')
#                                 r.hset("tickets_obra"+str(x),"asignado",trabajador)
#                             if option == 'in process':
#                                 r.hset("tickets_obra"+str(x),"status",'In Process')
#                             if option == 'done':
#                                 r.hset("tickets_obra"+str(x),"status",'Done')
#                                 r.hset("tickets_obra"+str(x),"evidencia2",solution)
#                                 r.hset("tickets_obra"+str(x),"solution",descriptionsolution)

# def getAllprojectPaP(r):
#     all_PaP, proyecto = [], ''
#     obj = decode_redis(r.get(str('key_pap')))
#     if obj == 'NO':
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str('pap')+str(x)))
#             if obj != {}:
#                 msg = obj["postes"].replace("'","[")
#                 msg = json.loads(msg)
#                 for y in range(0,len(msg)):
#                     if proyecto != msg[x][1]:
#                         proyecto = msg[x][1]
#                         all_PaP.append(proyecto)
#         return all_PaP

# def getAllPostesPaP(project):
#     all_postes, proyecto = [], ''
#     obj = decode_redis(r.get(str('key_pap')))
#     if obj == 'NO':
#         obj = 'NO'
#         return obj
#     else:
#         for x in range(0, int(obj)+1):
#             obj = decode_redis(r.hgetall(str('pap')+str(x)))
#             if obj != {}:
#                 msg = obj["postes"].replace("'","[")
#                 msg = json.loads(msg)
#                 if msg[0][1] == project:
#                     for y in range(0,len(msg)):
#                         all_postes.append(msg[y][3])
#                     return all_postes