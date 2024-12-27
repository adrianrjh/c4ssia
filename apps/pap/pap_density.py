from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common4 import *
sys.path.insert(0, '/home/adrian/ws/wave/cassia/data')
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import asyncio

class Listener1(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)

        self.redis,self.init = r,0
        self.pubsub = self.redis.pubsub()
        print('Listener1...')

        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)

    def work(self, item):
        global session, puesto, username
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            session = data['session']
            puesto = data['puesto']
            username = data['username']
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    else:
                        pass
                        #self.work(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['last_session'])
                        break
            time.sleep(0.001)  # be nice to the system :)

#client = Listener1(r, ['last_session','LT01TP0LT'])
#client.start()

async def paso1(q: Q):
    global comboboxProjPaP, proyecto, data_rows
    
    del q.page['table']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']

    proyecto = ''
    comboboxProjPaP = getAllprojectPaP(r)
    if comboboxProjPaP == 'NO':
        comboboxProjPaP = []
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,)        ]
    )

    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            height = '600px',
            columns=columnsProjectsDensity,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=True,
        ),
        ui.button(name = 'btnEdit', label = 'Editar', disabled = False, primary = True)
    ])

    await q.page.save()

async def paso2(q: Q):
    global comboboxProjPaP, proyecto, data_rows
    global notableport, proyecto_density, propietario_density, poste_density, latitud_density, longitud_density, idcaja_density, port_density, potcalculo_density, potreal_density
    global potclient_density, idclient_density, nameclient_density, paquete_density, tecnico_density, fechainstalacion_density, noserieonu_density, gponport_density, onuid_density, proyecto

    del q.page['table']
    del q.page['comboboxBtns']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']

    now = datetime.datetime.now()
    dateStart = now.strftime("%Y-%m-%d %H:%M:%S")

    comboboxUsers = []
    users = getAllUsers(r, 'user_key', 'user_')
    for x in range(0,len(users)):
        comboboxUsers.append(users[x][2]+' '+users[x][3]+'/'+users[x][7])

    q.page['combotextboxes1'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.textbox(name='textnoposte', label='N°', value=str(notableport),trigger=True, disabled=True),
            ui.textbox(name='textproyecto', label='Proyecto', value=str(proyecto_density), disabled=True),
            ui.textbox(name='textpropietario', label='Propietario', value=str(propietario_density), disabled=True, trigger=True),
            ui.textbox(name='textidposte', label='ID Poste', value=str(poste_density), disabled=True, trigger=True),
            ui.textbox(name='textlatitud', label='Latitud', value=str(latitud_density), trigger=True, disabled=True),
            ui.textbox(name='textlongitud', label='Longitud', value=str(longitud_density), trigger=True, disabled=True),
            ui.textbox(name='textidcaja', label='ID Caja', value=str(idcaja_density),  trigger=True, disabled=True),
            ui.textbox(name='textportcaja', label='Port', value=str(port_density), trigger=True, disabled=True),
            ui.textbox(name='textpotcalculo', label='Pot Calculo', value=str(potcalculo_density), trigger=True, disabled=True),
            ui.textbox(name='textpotreal', label='Pot Real', value=str(potreal_density), trigger=True, disabled=True),
        ],
    )

    q.page['combotextboxes2'] = ui.section_card(
        box=ui.box('der1_12', order=1),
        title='',
        subtitle='',
        items=[
            ui.combobox(name='combogponport', label='PON Port', value=str(gponport_density), choices=comboboxGPONOLT,trigger=True, disabled=False),
            ui.textbox(name='textonuid', label='ONU ID', value=str(onuid_density),trigger=True, disabled=False),
            ui.textbox(name='textpotclient', label='Pot Client', value=str(potclient_density),trigger=True, disabled=False),
            ui.textbox(name='textidcliente', label='ID Client', value=str(idclient_density), disabled=False),
            ui.textbox(name='textnameclient', label='Client', value=str(nameclient_density), disabled=False, trigger=True),
            ui.combobox(name='combopaquete', label='Paquete', value=str(paquete_density), choices=comboboxPaquetePlan,trigger=True, disabled=False),
            ui.combobox(name='combotecnico', label='Tecnico', value=str(tecnico_density), choices=comboboxUsers, trigger=True, disabled=False),
            ui.date_picker(name='date_picker_instalacion', label='Fecha de Instalación', value=dateStart, disabled=True),
            ui.textbox(name='textnoserie', label='N° Serie', value=str(noserieonu_density), disabled=False, trigger=True),
            ui.button(name='btnSig1', label='Guardar Info', disabled = False, primary=True,)
        ],
    )

    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            height = '600px',
            columns=columnsProjectsDensity,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=True,
        ),
        ui.button(name = 'btnEdit', label = 'Editar', disabled = False, primary = True)
    ])


    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, bandPaso1, bandPaso2
    try:
        while 1:
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                await q.run(paso1,q)
                await q.page.save()
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                await q.run(paso2,q)
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global paso1P, paso2P, bandPaso1, bandPaso2
    paso1P, paso2P, bandPaso1, bandPaso2 = 1, 0, 0, 0
    # Cancela la tarea anterior si existe y aún está corriendo
    if current_refresh_task and not current_refresh_task.done():
        current_refresh_task.cancel()
        try:
            # Espera a que la tarea sea cancelada (opcional)
            await current_refresh_task
        except asyncio.CancelledError:
            # Maneja el caso en que la tarea fue cancelada
            pass
    # Inicia una nueva tarea
    current_refresh_task = asyncio.create_task(refresh(q))

async def pap_density(q: Q):
    print(str("starting pap_density..."))
    global ipGlobal,session
    global data_rows, data_rows_keycount, data_rows_density
    global notableport, proyecto_density, propietario_density, poste_density, latitud_density, longitud_density, idcaja_density, port_density, potcalculo_density, potreal_density
    global potclient_density, idclient_density, nameclient_density, paquete_density, tecnico_density, fechainstalacion_density, noserieonu_density, gponport_density, onuid_density, proyecto
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4

    q.page['meta'] = ui.meta_card(box='')

    if q.args.home:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.settings:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/settings'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.logout:
        session = False
        puesto = ''
        json_datos = json.dumps({"session":session, "puesto":puesto})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_pap'
        await q.page.save()

    if q.args.textproyecto:
        proyecto = str(q.args.textproyecto)
        await q.page.save()

    if q.args.combogponport and gponport_density != q.args.combogponport:
        gponport_density = str(q.args.combogponport)
        await q.page.save()

    if q.args.textonuid:
        onuid_density = str(q.args.textonuid)
        await q.page.save()

    if q.args.textpotclient:
        potclient_density = str(q.args.textpotclient)
        await q.page.save()

    if q.args.textidcliente:
        idclient_density = str(q.args.textidcliente)
        await q.page.save()

    if q.args.textnameclient:
        nameclient_density = str(q.args.textnameclient)
        await q.page.save()

    if q.args.combopaquete and paquete_density != q.args.combopaquete:
        paquete_density = str(q.args.combopaquete)
        await q.page.save()

    if q.args.combotecnico and tecnico_density != q.args.combotecnico:
        tecnico_density = str(q.args.combotecnico)
        await q.page.save()

    if q.args.date_picker_instalacion:
        fechainstalacion_density = str(q.args.date_picker_instalacion)
        await q.page.save()

    if q.args.textnoserie:
        noserieonu_density = str(q.args.textnoserie)
        await q.page.save()

    if q.args.btnConsultar:
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnSearch:
        if proyecto != '' and proyecto != 'Seleccionar':
            data_rows = getAllDensityPaP(proyecto)
            paso1P = 1
            paso2P = 0
            paso3P = 0
            paso4P = 0
            bandPaso1 = 0
        await q.page.save()

    if q.args.btnEdit:
        modificar = q.args.issues
        notableport, proyecto_density, propietario_density, poste_density, latitud_density, longitud_density, idcaja_density, port_density, potcalculo_density, potreal_density = '', '', '', '', '', '', '', '', '', ''
        gponport_density, onuid_density, potclient_density, idclient_density, nameclient_density, paquete_density, tecnico_density, fechainstalacion_density, noserieonu_density = '', '', '', '', '', '', '', '', ''
        if modificar == None:
            pass
        if modificar != None:
            if len(modificar)==1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in modificar:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            notableport = y[0]
                            proyecto_density = y[1]
                            propietario_density = y[2]
                            poste_density = y[3]
                            latitud_density = y[4]
                            longitud_density = y[5]
                            idcaja_density = y[6]
                            port_density = y[7]
                            potcalculo_density = y[8]
                            potreal_density = y[9]
                            gponport_density = y[10]
                            onuid_density = y[11]
                            potclient_density = y[12]
                            idclient_density = y[13]
                            nameclient_density = y[14]
                            paquete_density = y[15]
                            tecnico_density = y[16]
                            fechainstalacion_density = y[17]
                            noserieonu_density = y[18]
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found = 0
        paso1P = 0
        paso2P = 1
        paso3P = 0
        paso4P = 0
        bandPaso2 = 0
        await q.page.save()

    if q.args.btnSig1:
        data_rowsPRFor = getAllDensityPaP(proyecto)
        data_rows_density, found = [], 0
        for y in data_rowsPRFor:
            if str(y[0])==str(notableport):
                # si quieres quitar los que seleccionaste
                found=1
                y[10] = gponport_density
                y[11] = onuid_density
                y[12] = potclient_density
                y[13] = idclient_density
                y[14] = nameclient_density
                y[15] = paquete_density
                y[16] = tecnico_density
                y[17] = fechainstalacion_density
                y[18] = noserieonu_density
                data_rows_density.append(y)
            if found==0:
                # si quieres quitar los que no seleccionaste
                data_rows_density.append(y)
            found=0
        changeFieldTable(r, data_rows_density, proyecto)
        data_rows = getAllDensityPaP(proyecto)
        notableport, proyecto_density, propietario_density, poste_density, latitud_density, longitud_density, idcaja_density, port_density, potcalculo_density, potreal_density = '', '', '', '', '', '', '', '', '', ''
        gponport_density, onuid_density, potclient_density, idclient_density, nameclient_density, paquete_density, tecnico_density, fechainstalacion_density, noserieonu_density = '', '', '', '', '', '', '', '', ''
        paso1P = 0
        paso2P = 1
        paso3P = 0
        paso4P = 0
        bandPaso2 = 0
        await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        #if session != True:
        #    q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        #    await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='4%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('der1',size='96%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='20%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='50%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='50%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='80%', zones=[
                                        ui.zone('der1_21', size='100%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_pap_density'] = ui.header_card(
            box='header',
            title='C 4 S S I A',
            subtitle='YAA Internet',
            items=[
                ui.menu(
                    image=image,
                    items=[
                        ui.command(name='home', label='Home', icon='Home'),
                        ui.command(name='settings', label='Settings', icon='Settings'),
                        ui.command(name='logout', label='Logout', icon='SignOut'),
                    ]
                )
            ],
        )
        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='', disabled = False, primary=True, icon='Back')])
        await q.run(start_or_restart_refresh,q)
        await q.page.save()

@app('/pap_density', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_density(q)