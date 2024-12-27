from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common7 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv, asyncio, base64

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

client = Listener1(r, ['last_session'])
client.start()

async def paso1(q: Q):
    global proyectoTicket, comboboxProyecto

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    comboboxProyecto = []
    comboboxProyecto = getAllprojectPaP(r)

    q.page['combotextboxes0'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.combobox(name='comboboxProyecto', label='Proyecto', value='Seleccionar', choices=comboboxProyecto,trigger=True), ui.button(name='btnSiguiente1',label='Siguiente',disabled = False,primary=True,)]
    )

    await q.page.save()

async def paso2(q: Q):
    global proyectoTicket, posteTicket

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    q.page['form_ticket'] = ui.form_card(
        box=ui.box('izq1_11', order=1),
        items=[
            ui.text_xl('Proyecto:'),
            ui.textbox(name='textboxProyTicket', label='', value=str(proyectoTicket), disabled=True)
        ]
    )
    comboboxPoste = getAllPostesPaP(proyectoTicket)
    q.page['combotextboxes1'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.combobox(name='comboboxPoste', label='Poste', value='Seleccionar', choices=comboboxPoste,trigger=True), ui.button(name='btnSiguiente2',label='Siguiente',disabled = False,primary=True,)]
    )
    await q.page.save()

async def paso3(q: Q):
    global proyectoTicket, posteTicket

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    q.page['form_ticket'] = ui.form_card(
        box=ui.box('izq1_11', order=1),
        items=[
            ui.text_xl('Proyecto:'),
            ui.textbox(name='textboxProyTicket', label='', value=str(proyectoTicket), disabled=True),
            ui.text_xl('Poste:'),
            ui.textbox(name='textboxPosteTicket', label='', value=str(posteTicket), disabled=True)
        ]
    )
    comboboxPrioridad = ['Baja', 'Media', 'Alta', 'Muy Alta']
    q.page['combotextboxes2'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.combobox(name='comboboxPrioridad', label='Nivel de Prioridad', value='Seleccionar', choices=comboboxPrioridad,trigger=True), ui.button(name='btnSiguiente3',label='Siguiente',disabled = False,primary=True,)]
    )
    await q.page.save()

async def paso4(q: Q):
    global proyectoTicket, posteTicket, prioridadTicket

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    q.page['form_ticket'] = ui.form_card(
        box=ui.box('izq1_11', order=1),
        items=[
            ui.text_xl('Proyecto:'),
            ui.textbox(name='textboxProyTicket', label='', value=str(proyectoTicket), disabled=True),
            ui.text_xl('Poste:'),
            ui.textbox(name='textboxPosteTicket', label='', value=str(posteTicket), disabled=True),
            ui.text_xl('Prioridad:'),
            ui.textbox(name='textboxPrioriTicket', label='', value=str(prioridadTicket), disabled=True),
        ]
    )
    q.page['combotextboxes3'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.textbox(name='textDescriTicket', label='Descripción del problema', trigger=True, multiline=True, width='400px'), ui.button(name='btnSiguiente4',label='Siguiente',disabled = False,primary=True,)]
    )
    await q.page.save()

async def paso5(q: Q):
    global proyectoTicket, posteTicket, prioridadTicket, problemaTicket

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    q.page['form_ticket'] = ui.form_card(
        box=ui.box('izq1_11', order=1),
        items=[
            ui.text_xl('Proyecto:'),
            ui.textbox(name='textboxProyTicket', label='', value=str(proyectoTicket), disabled=True),
            ui.text_xl('Poste:'),
            ui.textbox(name='textboxPosteTicket', label='', value=str(posteTicket), disabled=True),
            ui.text_xl('Prioridad:'),
            ui.textbox(name='textboxPrioriTicket', label='', value=str(prioridadTicket), disabled=True),
            ui.text_xl('Descripción del problema:'),
            ui.text_l(str(problemaTicket)),
        ]
    )
    q.page['combotextboxes4'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.file_upload(name='uploadEvidTicket', label='Subir Evidencia', multiple=False, compact=True,file_extensions=['png', 'jpg', 'jpeg'],), ui.button(name='btnSiguiente5',label='Siguiente',disabled = False,primary=True,)]
    )
    await q.page.save()

async def paso6(q: Q):
    global proyectoTicket, posteTicket, prioridadTicket, problemaTicket, evidenciaTicket, content

    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    del q.page['form_ticket']
    del q.page['Img']

    q.page['form_ticket'] = ui.form_card(
        box=ui.box('izq1_11', order=1),
        items=[
            ui.text_xl('Proyecto:'),
            ui.textbox(name='textboxProyTicket', label='', value=str(proyectoTicket), disabled=True),
            ui.text_xl('Poste:'),
            ui.textbox(name='textboxPosteTicket', label='', value=str(posteTicket), disabled=True),
            ui.text_xl('Prioridad:'),
            ui.textbox(name='textboxPrioriTicket', label='', value=str(prioridadTicket), disabled=True),
            ui.text_xl('Descripción del problema:'),
            ui.text_l(str(problemaTicket)),
        ]
    )

    evidenciaTicket = evidenciaTicket.split('/')
    content = '![Adrian](http://'+ipGlobal+':10101/datasets/'+evidenciaTicket[7]+')'

    q.page['Img'] = ui.markdown_card(
        box=ui.box('izq1_11',order = 1),
        title='Evidencia:',
        content= content,
    )

    q.page['combotextboxes5'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.button(name='btnSiguiente6',label='Crear Ticket', disabled = False, primary = False)]
    )
    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, paso4P, paso5P, paso5P, bandPaso1, bandPaso2, bandPaso3, bandPaso4, bandPaso5, bandPaso6
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
            if paso5P == 1 and bandPaso5 == 0:
                bandPaso5 = 1
                await q.run(paso5,q)
                await q.page.save()
            if paso6P == 1 and bandPaso6 == 0:
                bandPaso6 = 1
                await q.run(paso6,q)
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global bandPaso1, bandPaso2, bandPaso3, bandPaso4, bandPaso5, bandPaso6
    bandPaso1, bandPaso2, bandPaso3, bandPaso4, bandPaso5, bandPaso6 = 0, 0, 0, 0, 0, 0
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

async def pap_tickets(q: Q):
    print(str("starting pap_tickets..."))
    global ipGlobal,session
    global proyectoTicket, posteTicket, prioridadTicket, problemaTicket, evidenciaTicket, encoded_string, content, rootEvidencia
    global paso1P, paso2P, paso3P, paso4P, paso5P, paso6P, bandPaso1, bandPaso2, bandPaso3, bandPaso4, bandPaso5, bandPaso6

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

    if q.args.comboboxProyecto:
        if q.args.comboboxProyecto != 'Seleccionar':
            proyectoTicket = str(q.args.comboboxProyecto)
        await q.page.save()

    if q.args.btnSiguiente1:
        if proyectoTicket != 'Seleccionar' and proyectoTicket != '':
            paso1P = 0
            paso2P = 1
            paso3P = 0
            paso4P = 0
            paso5P = 0
            paso6P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.comboboxPoste:
        if q.args.comboboxPoste != 'Seleccionar':
            posteTicket = str(q.args.comboboxPoste)
        await q.page.save()

    if q.args.btnSiguiente2:
        if posteTicket != 'Seleccionar' and posteTicket != '':
            paso1P = 0
            paso2P = 0
            paso3P = 1
            paso4P = 0
            paso5P = 0
            paso6P = 0
            bandPaso3 = 0
        await q.page.save()

    if q.args.comboboxPrioridad:
        if q.args.comboboxPrioridad != 'Seleccionar':
            prioridadTicket = str(q.args.comboboxPrioridad)
        await q.page.save()

    if q.args.btnSiguiente3:
        if prioridadTicket != 'Seleccionar' and prioridadTicket != '':
            paso1P = 0
            paso2P = 0
            paso3P = 0
            paso4P = 1
            paso5P = 0
            paso6P = 0
            bandPaso4 = 0
        await q.page.save()

    if q.args.textDescriTicket:
        problemaTicket=str(q.args.textDescriTicket)
        await q.page.save()

    if q.args.btnSiguiente4:
        if problemaTicket != 'Seleccionar' and problemaTicket != '':
            paso1P = 0
            paso2P = 0
            paso3P = 0
            paso4P = 0
            paso5P = 1
            paso6P = 0
            bandPaso5 = 0
        await q.page.save()

    if q.args.uploadEvidTicket:
        for path in q.args.uploadEvidTicket:
            evidenciaTicket = await q.site.download(path, '../../data/')
            rootEvidencia = str(evidenciaTicket)
        await q.page.save()

    if q.args.btnSiguiente5:
        if evidenciaTicket != '':
            paso1P = 0
            paso2P = 0
            paso3P = 0
            paso4P = 0
            paso5P = 0
            paso6P = 1
            bandPaso6 = 0
        await q.page.save()

    if q.args.btnSiguiente6:
        try:
            with open(rootEvidencia, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(e)
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        noticket = str(now.strftime("%Y%m%d"))+str(proyectoTicket[:4])+str(posteTicket)
        json_datos = json.dumps({
            "time":str(dt_string),
            "id":"tickets_obra",
            "noticket":str(noticket),
            "status":"Active",
            "area":"yi_obra",
            "proyecto":str(proyectoTicket),
            "poste":str(posteTicket),
            "prioridad":str(prioridadTicket),
            "problema":str(problemaTicket),
            "creado":str(dt_string),
            "asignado":'Eduardo Espíndola',
        })
        datos_ticket={
            "time":str(dt_string),
            "id":"tickets_obra",
            "noticket":str(noticket),
            "status":"Active",
            "area":"yi_obra",
            "proyecto":str(proyectoTicket),
            "poste":str(posteTicket),
            "prioridad":str(prioridadTicket),
            "problema":str(problemaTicket),
            "creado":str(dt_string),
            "asignado":'Eduardo Espíndola',
            "evidencia1":encoded_string,
            "evidencia2":'',
            "solution":'',
        }
        #try:
        #    key_count=r.get('key_tickets_obra')
        #    if key_count == {} or key_count == None:
        #        key_count = 0
        #    else:
        #        key_count=key_count.decode("utf-8")
        #except Exception as e:
        #    print(e)
        r.set("key_tickets_obra",str(1))#str(int(key_count)+1))
        r.hmset('tickets_obra'+str(1), datos_ticket)
        try:
            r.publish("pap_tickets",json_datos)
            time.sleep(0.3)
        except Exception as e:
            print(e)
            pass
        paso1P = 1
        paso2P = 0
        paso3P = 0
        paso4P = 0
        paso5P = 0
        paso6P = 0
        bandPaso1 = 0
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
                            ui.zone('izq1_1', size='50%', align='start', direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('izq1_10', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_11', size='50%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_12', size='40%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_13', size='00%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_14', size='00%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_15', size='00%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('izq1_16', size='00%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ]),
                            ui.zone('der1_1', size='50%', align='start', direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_10', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_11', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_12', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_13', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_14', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_15', size='14%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_16', size='16%', align='center', direction=ui.ZoneDirection.ROW),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_devices'] = ui.header_card(
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
        
        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])
        
        await q.run(start_or_restart_refresh,q)
        await q.page.save()

@app('/pap_tickets', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_tickets(q)