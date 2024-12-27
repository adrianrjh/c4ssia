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

    def work2(self, item):
        global data_rows, refreshTable, data_rows_save, r
        global noticket, area, tiempo, cliente, contacto, servicio, problema, status, asignado, descripcion
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            noticket = str(data['ticket_key'])
            area = str(data['area'])
            tiempo = str(data['time'])
            cliente = str(data['cliente'])
            contacto = str(data['contacto'])
            servicio = str(data['servicio'])
            problema = str(data['problema'])
            status = str(data['status'])
            asignado = str(data['asignado'])
            descripcion = str(data['descripcion'])
            data_rows.append([noticket, area, tiempo, cliente, contacto, servicio, problema, status, asignado, descripcion])
            updAct(data, 0)
            refreshTable = 1
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="tickets_exception"):
                        self.work2(message['data'])
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
                        self.pubsub.subscribe(['last_session'],['tickets_exception'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['last_session','tickets_exception'])
client.start()

async def showList(q: Q):
    global data_rows, columns
    
    q.page['table'] = ui.form_card(box=ui.box('mid1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    await q.page.save()

async def refresh(q: Q):
    global fig, refreshTable, data_rows
    while 1:
        if refreshTable == 1:
            refreshTable = 0
            await q.run(showList,q)
        await q.sleep(1)

async def tickets_exception(q: Q):
    print(str("starting tickets_exception app..."))
    global ipGlobal,session, r
    global data_rows, noticket, area, tiempo, cliente, contacto, servicio, problema, status, asignado, descripcion

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
#########   U   P   D   A   T   E     T   A   B   L   E   ############
    if q.args.btnUpd:
        data_rows = getAllTickets(r, 'tickets_key', 'tickets_', 'exceptions')

        if data_rows == 'NO':
            data_rows = []
        elif len(data_rows) > 0:
            q.page['boton2'].items[0].button.disabled = False
            q.page['boton2'].items[1].button.disabled = False
            q.page['boton2'].items[2].button.disabled = False
            q.page['boton2'].items[3].button.disabled = False

        await q.run(showList, q)
        await q.page.save()
#########  R  E  T  U  R  N     T  O     T  I  C  K  E  T  S     A  C  T  I  V  E  ############
    if q.args.btnReturn:
        eliminados = q.args.issues
        data_rows_temp, data_rows_send, found = [], [], 0
        for y in data_rows:
            for x in eliminados:
                if str(y[0])==str(x):
                    found=1
                    # si quieres quitar los que seleccionaste
                    data_rows_send.append(y)
            if found==0:
                # si quieres quitar los que no seleccionaste
                data_rows_temp.append(y)
            found=0
        for i in range(0,len(data_rows_send)):
            if data_rows_send[i][7] != 'Validated':
                data_rows = data_rows_temp
                now = datetime.datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                json_datos = json.dumps({
                    "ticket_key":str(data_rows_send[i][0]),
                    "area":"activos",
                    "time":str(data_rows_send[i][2]),
                    "id":"tickets",
                    "cliente":str(data_rows_send[i][3]),
                    "contacto":str(data_rows_send[i][4]),
                    "servicio":str(data_rows_send[i][5]),
                    "problema":str(data_rows_send[i][6]),
                    "status":"Waiting",
                    "asignado":str(dt_string),
                    "descripcion":str(data_rows_send[i][9]),             
                })
                try:
                    r.publish("tickets_return",json_datos)
                    time.sleep(0.3)
                except Exception as e:
                    print(e)
                await q.run(showList,q)
        await q.page.save()
######### V  A  L  I  D  A  T  E ############
    if q.args.btnValidate:
        eliminados = q.args.issues
        if len(eliminados) == 1:
            data_rows_temp, data_rows_send, found = [], [], 0
            for y in data_rows:
                for x in eliminados:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                if found==0:
                    #pass
                    # si quieres quitar los que no seleccionaste
                    data_rows_temp.append(y)
                found=0
            for i in range(0,len(data_rows_send)):
                if data_rows_send[i][7] != 'Validated':
                    print(data_rows_send)
                    updAct(data_rows_send, 'validate')
                    data_rows = getAllTickets(r, 'tickets_key', 'tickets_', 'exceptions')
            await q.run(showList, q)
        await q.page.save()

    q.page['meta'] = ui.meta_card(box='', icon='http://'+ipGlobal+':10101/datasets/cassia-logo1.png')
    if not q.client.initialized:
        q.client.initialized = True
        if session != True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
            await q.page.save()
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('left', size='0%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('mid',size='90%', zones=[
                                ui.zone('mid1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('mid1_1', size='90%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('mid1_11', size='90%', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('mid1_12', size='10%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('mid1_2',size='10%', zones=[
                                        ui.zone('mid1_21', size='90%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('mid1_22', size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der1', size='10%', zones=[
                                ui.zone('der1_11',size='16%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('der1_12',size='16%',align='center'),
                                ui.zone('der1_13',size='16%',align='center'),
                                ui.zone('der1_14',size= '16%',align='center'),
                                ui.zone('der1_15',size= '16%',align='center'),
                                ui.zone('der1_16',size= '16%',align='center'),
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
                        ui.command(name='tickets', label='Tickets', icon='Ticket'),
                        ui.command(name='misequipos', label='Mis Equipos', icon='ProductVariant'),
                        ui.command(name='myprs', label='Mis PRs', icon='SurveyQuestions'),
                        ui.command(name='settings', label='Settings', icon='Settings'),
                        ui.command(name='logout', label='Logout', icon='SignOut'),
                    ]
                )
            ],
        )
        #########   BTNS   #########
        q.page['btns1'] = ui.section_card(
            box=ui.box('der1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnUpd', label='Update Table', disabled = False, primary=True,),
            ],
        )
        #########   Cassia Home   #########
        q.page['boton2'] = ui.section_card(
            box=ui.box('mid1_12', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnReturn', label='Return to Tickets Active', disabled = False, primary=False),
                ui.button(name='btnValidate', label='Validate', disabled = False, primary=False),
            ],
        )

        await q.page.save()
        await q.run(showList,q)
        await q.run(refresh,q)

@app('/tickets_exception', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await tickets_exception(q)