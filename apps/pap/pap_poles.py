from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common4 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import asyncio

#class Listener1(threading.Thread):
#    def __init__(self, r, channels):
#        threading.Thread.__init__(self)
#
#        self.redis,self.init = r,0
#        self.pubsub = self.redis.pubsub()
#        print('Listener1...')
#
#        try:
#            self.pubsub.subscribe(channels)
#        except Exception as e:
#            print(e)
#
#    def work(self, item):
#        global session, puesto, username
#        data=0
#        try:
#            data = json.loads(item.decode('utf8'))
#            session = data['session']
#            puesto = data['puesto']
#            username = data['username']
#        except Exception as e:
#            print(e)
#
#    def run(self):
#        while True:
#            try:
#                message = self.pubsub.get_message()
#                if message:
#                    if (message['channel'].decode("utf-8")=="last_session"):
#                        self.work(message['data'])
#                    else:
#                        pass
#                        #self.work(message['data'])
#            except ConnectionError:
#                print('[lost connection]')
#                while True:
#                    print('trying to reconnect...')
#                    try:
#                        self.redis.ping()
#                    except ConnectionError:
#                        time.sleep(10)
#                    else:
#                        self.pubsub.subscribe(['last_session'])
#                        break
#            time.sleep(0.001)  # be nice to the system :)
#
#client = Listener1(r, ['last_session','LT01TP0LT'])
#client.start()

async def paso1(q: Q):
    global comboboxProjPaP, proyecto
    del q.page['table']
    del q.page['upldCSV']
    del q.page['plot']
    del q.page['combotextboxes']
    del q.page['btnHomePaso1']
    del q.page['table']

    proyecto = ''
    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    comboboxProjPaP = getAllprojectPaP(r)
    if comboboxProjPaP == 'NO':
        comboboxProjPaP = []
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnDelPole',label='Quitar',disabled = False,primary=False,),
                ui.button(name='btnAddPole',label='Agregar',disabled = False,primary=False,),
        ]
    )

    await q.page.save()

async def paso2(q: Q):
    global data_rows
    del q.page['comboboxBtns']
    del q.page['plot']

    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    comboboxProjPaP = getAllprojectPaP(r)
    if comboboxProjPaP == 'NO':
        comboboxProjPaP = []
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnDelPole',label='Quitar',disabled = False,primary=False,),
                ui.button(name='btnAddPole',label='Agregar',disabled = False,primary=False,),
        ]
    )
    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            height = '800px',
            columns=columnsProjectsPaP,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        ),
        ui.button(name='btnDelPoleAction',label='Eliminar Poste',disabled = False,primary=True,)
    ])

    await q.page.save()

async def paso3(q: Q):
    global comboboxPropietario, comboboxConectedTo, data_rows, proyecto
    global propietarioAddPoste, posteAddPoste, latitudAddPoste, longitudAddPoste, idCajaAddPoste, idCEAddPoste, conectedToAddPoste

    del q.page['table']
    del q.page['comboboxBtns']

    comboboxPropietario = getAllPropietPaP(r, proyecto)
    comboboxConectedTo = getAllPostesPaP(r, proyecto)
    q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
    q.page['combotextboxes'] = ui.section_card(
        box=ui.box('der1_11', order=1),
        title='',
        subtitle='',
        items=[
            ui.combobox(name='combopropietario', label='Propietario', value=str(propietarioAddPoste), choices=comboboxPropietario,trigger=True, disabled=False),
            ui.textbox(name='textboxPoste', label='Poste', value=str(posteAddPoste), disabled=True),
            ui.textbox(name='textboxLatitud', label='Latitud', value=str(latitudAddPoste), disabled=False, required=True, trigger=True),
            ui.textbox(name='textboxLongitud', label='Longitud', value=str(longitudAddPoste), disabled=False, required=True, trigger=True),
            ui.combobox(name='comboIDCaja', label='ID Caja', value=str(idCajaAddPoste), choices=['N/A'], trigger=True, disabled=False),
            ui.combobox(name='comboIDCE', label='ID CE', value=str(idCEAddPoste), choices=['N/A'], trigger=True, disabled=False),
            ui.combobox(name='comboconnectedto', label='Conected To', value=str(conectedToAddPoste), choices=comboboxConectedTo, trigger=True, disabled=False),
            ui.button(name='btnSig1', label='Siguiente', disabled = False, primary=True,)
        ],
    )

    q.page['btnHomePaso1'] = ui.section_card(box=ui.box('der1_12', order=1),title='',subtitle='',items=[ui.button(name='btnHomePaso1', label='Inicio', disabled = False, primary=True)])
    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columnsProjectsPaP,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            # Add pagination attribute to make your table paginated.
            # Register events to listen, all of these have to be handled by developer.
            #values = ['0'],
            groupable=False,
            downloadable=True,
            resettable=False,
        )
    ])

    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
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
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(paso3,q)
                await q.page.save()
            if paso4P == 1 and bandPaso4 == 0:
                bandPaso4 = 1
                await q.run(paso4,q)
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global paso1P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    paso1P, bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 1, 0, 0, 0, 0
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

async def pap_poles(q: Q):
    print(str("starting pap_poles..."))
    global ipGlobal,session
    global data_rows, data_rows_keycount
    global comboboxPropietario, comboboxConectedTo, proyecto
    global propietarioAddPoste, posteAddPoste, latitudAddPoste, longitudAddPoste, idCajaAddPoste, idCEAddPoste, conectedToAddPoste
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
        if q.args.textproyecto != 'Seleccionar':
            proyecto = str(q.args.textproyecto)
        await q.page.save()

    if q.args.btnDelPole:
        if proyecto != '' and proyecto != 'Seleccionar':
            data_rows = getAllPaP(proyecto)
            paso1P = 0
            paso2P = 1
            paso3P = 0
            paso4P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.btnAddPole:
        if proyecto != '' and proyecto != 'Seleccionar':
            data_rows = getAllPaP(proyecto)
            paso1P = 0
            paso2P = 0
            paso3P = 1
            paso4P = 0
            bandPaso3 = 0
        await q.page.save()

    if q.args.combopropietario and propietarioAddPoste!=str(q.args.combopropietario):
        propietarioAddPoste = str(q.args.combopropietario)
        posteAddPoste = setNewPostePaP(r, proyecto, propietarioAddPoste)
        if propietarioAddPoste == 'CA' and posteAddPoste == '':
            posteAddPoste = 'CA001'
        paso1P = 0
        paso2P = 0
        paso3P = 1
        paso4P = 0
        bandPaso3 = 0
        await q.page.save()

    if q.args.textboxLatitud:
        latitudAddPoste=str(q.args.textboxLatitud)
        await q.page.save()

    if q.args.textboxLongitud:
        longitudAddPoste=str(q.args.textboxLongitud)
        await q.page.save()

    if q.args.comboIDCaja and idCajaAddPoste!=str(q.args.comboIDCaja):
        idCajaAddPoste=str(q.args.comboIDCaja)
        await q.page.save()

    if q.args.comboIDCE and idCEAddPoste!=str(q.args.comboIDCE):
        idCEAddPoste=str(q.args.comboIDCE)
        await q.page.save()

    if q.args.comboconnectedto:
        if q.args.comboconnectedto != 'Seleccionar':
            conectedToAddPoste = str(q.args.comboconnectedto)
        await q.page.save()

    if q.args.btnHomePaso1:
        data_rows = []
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        bandPaso1 = 0
        await q.page.save()

    if q.args.btnSig1:
        data_rows.append([str(len(data_rows)), str(proyecto), str(propietarioAddPoste), str(posteAddPoste), str(latitudAddPoste), str(longitudAddPoste), '0.0', str(idCajaAddPoste), str(idCEAddPoste), '0', str(conectedToAddPoste)])
        propietarioAddPoste, posteAddPoste, latitudAddPoste, longitudAddPoste, idCajaAddPoste, idCEAddPoste, conectedToAddPoste = 'Seleccionar', '', '', '', 'Seleccionar', 'Seleccionar', 'Seleccionar'
        changePostesPaP(r, proyecto, data_rows)
        data_rows = getAllPaP(proyecto)
        paso1P = 0
        paso2P = 0
        paso3P = 1
        paso4P = 0
        bandPaso3 = 0        
        await q.page.save()

    if q.args.btnDelPoleAction:
        selectioned = q.args.issues
        if selectioned == None:
            q.page["meta"].side_panel = ui.side_panel(
                title="",
                items=[ui.text("Selecciona un poste para eliminarlo.")],
                name="side_panel",
                events=["dismissed"],
                closable=True,
                width = '400px',
            )
        if selectioned and selectioned != None:
            if len(selectioned) == 1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in selectioned:
                        if str(y[0])==str(x):
                            # si quieres quitar los que seleccionaste
                            found=1
                            data_rows_send.append(y)
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found=0
                data_rows = data_rows_temp
                changePostesPaP(r, proyecto, data_rows)
                paso1P = 0
                paso2P = 1
                paso3P = 0
                paso4P = 0
                bandPaso2 = 0
            else:
                q.page["meta"].side_panel = ui.side_panel(
                    title="",
                    items=[ui.text("Solo puedes eliminar un poste a la vez.")],
                    name="side_panel",
                    events=["dismissed"],
                    closable=True,
                    width = '400px',
                )
                paso1P = 0
                paso2P = 1
                paso3P = 0
                paso4P = 0
                bandPaso2 = 0
        await q.page.save()

    if q.events.side_panel:
        if q.events.side_panel.dismissed:
            q.page["meta"].side_panel = None
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
                            ui.zone('izq1', size='15%', zones=[
                                ui.zone('izq1_11', size= '15%', align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12', size= '14%', align='center'),
                                ui.zone('izq1_13', size= '14%', align='center'),
                                ui.zone('izq1_14', size= '14%', align='center'),
                                ui.zone('izq1_15', size= '14%', align='center'),
                                ui.zone('izq1_16', size= '14%', align='center'),
                                ui.zone('footer1', size= '15%', align='center')
                            ]),
                            ui.zone('der1',size='85%',direction=ui.ZoneDirection.ROW, zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='30%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='80%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='60%', direction=ui.ZoneDirection.COLUMN, zones=[
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
        q.page['header2_pap_poles'] = ui.header_card(
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
        await q.run(start_or_restart_refresh,q)
        await q.page.save()

@app('/pap_poles', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_poles(q)