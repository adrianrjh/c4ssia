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
import csv

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

async def formu_ticket(q: Q):
    global comboboxTS, comboboxTP
    global noservicio, telefono, tiposervicio, tipoproblema, problema
    
    del q.page['combotextboxes0']
    del q.page['combotextboxes1']
    del q.page['combotextboxes2']
    del q.page['combotextboxes3']
    del q.page['combotextboxes4']
    del q.page['combotextboxes5']
    
    q.page['combotextboxes0'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_10', order=1),
        items=[ui.textbox(name='textnoserv', label='N° de Servicio', trigger=True)]
    )
    q.page['combotextboxes1'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_11', order=1),
        items=[ui.textbox(name='texttel', label='Telefono de contacto', trigger=True)]
    )
    q.page['combotextboxes2'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_12', order=1),
        items=[ui.combobox(name='comboboxtipoServ', label='Tipo de servicio', value='Seleccionar', choices=comboboxTS, trigger=True)]
    )
    q.page['combotextboxes3'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_13', order=1),
        items=[ui.combobox(name='comboboxtipoProb', label='Tipo de problema', value='Seleccionar', choices=comboboxTP, trigger=True)]
    )
    q.page['combotextboxes4'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_14', order=1),
        items=[ui.textbox(name='descripcion', label='Descripción del problema', trigger=True, multiline=True, width='400px')]
    )
    q.page['combotextboxes5'] = ui.section_card(
        title = '',
        subtitle = '',
        box=ui.box('der1_15', order=1),
        items=[ui.button(name='btnAdd', label='Add Ticket', disabled = False, primary=True)]
    )
    await q.page.save()

async def tickets_add(q: Q):
    print(str("starting tickets_add..."))
    global ipGlobal,session
    global comboboxTS, comboboxTP
    global noservicio, telefono, tiposervicio, tipoproblema, problema

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

    if q.args.textnoserv:
        noservicio=str(q.args.textnoserv)
        await q.page.save()

    if q.args.texttel:
        telefono=str(q.args.texttel)
        await q.page.save()

    if q.args.comboboxtipoServ:
        if q.args.comboboxtipoServ != 'Seleccionar':
            tiposervicio = str(q.args.comboboxtipoServ)
        await q.page.save()

    if q.args.comboboxtipoProb:
        if q.args.comboboxtipoProb != 'Seleccionar':
            tipoproblema = str(q.args.comboboxtipoProb)
        await q.page.save()

    if q.args.descripcion:
        problema=str(q.args.descripcion)
        await q.page.save()

    if q.args.btnAdd:
        if noservicio != '':
            if telefono != '':
                if tiposervicio != "Seleccionar":
                    if tipoproblema != "Seleccionar":
                        if problema != '':
                            now = datetime.datetime.now()
                            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                            json_datos = json.dumps({
                                "time":str(dt_string),
                                "id":"tickets",
                                "status":"Waiting",
                                "area":"activos",
                                "cliente":str(noservicio),
                                "contacto":str(telefono),
                                "servicio":str(tiposervicio),
                                "problema":str(tipoproblema),
                                "asignado":str(dt_string),
                                "descripcion":str(problema),
                            })
                            try:
                                r.publish("tickets",json_datos)
                                time.sleep(0.3)
                            except Exception as e:
                                print(e)
                                pass
                            await q.run(formu_ticket,q)
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
                            ui.zone('der1_1', size='100%', align='center', direction=ui.ZoneDirection.COLUMN, zones=[
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

        await q.run(formu_ticket,q)
        await q.page.save()

@app('/tickets_add', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await tickets_add(q)