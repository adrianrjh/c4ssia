from h2o_wave import Q, app, main, ui, AsyncSite,site,data
#from pyzabbix import ZabbixAPI
import threading,json,time,math
from datetime import datetime
import sys
from redis import StrictRedis, ConnectionError
from redistimeseries.client import Client
import random
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common0 import *
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

client = Listener1(r, ['last_session','LT01TP0LT'])
client.start()

async def home_tickets(q: Q):
    global session
    print("Start aplication home...")

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

    if q.args.btnCreate:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_add'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnActive:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_active'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnFibra:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_fiber'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnWireless:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_wireless'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnPublic:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_public'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnDone:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_done'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnException:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/tickets_exception'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
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
                    ui.zone('body',size='93%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='20%', zones=[
                            ui.zone('izq1_11',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_12',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_13',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_14',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_15',size='20%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('izq2', size='20%', zones=[
                            ui.zone('izq2_21',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_22',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_23',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_24',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_25',size='20%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('cen1',size='20%', zones=[
                            ui.zone('cen1_11',size='20%', align = 'center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_12',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_13',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_14',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_15',size='20%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der1',size='20%', zones=[
                            ui.zone('der1_11',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_12',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_13',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_14',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_15',size='20%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der2',size='20%', zones=[
                            ui.zone('der1_21',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_22',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_23',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_24',size='20%',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_25',size='20%',direction=ui.ZoneDirection.COLUMN),
                        ]),
                    ]),
                ]),
                ],
            ),
        ], theme='winter-is-coming')
        image = 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'
        q.page['header2_home'] = ui.header_card(
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

        ###### Image logo of the company
        content = 'http://'+ipGlobal+':10101/datasets/cassia-logoB.png'
        q.page['CassiaImg'] = ui.section_card(box=ui.box('cen1_11', order=1), title='', subtitle = '', items = [ui.image(title='', path=content)])
        #####################   1ra LINEA   #################
        #########   f  i  b  r  a   #########
        create_logo = 'http://'+ipGlobal+':10101/datasets/add-ticket.png'
        q.page['create'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[
                ui.persona(name="btnCreate",title='Crear Ticket', subtitle='', caption='', size='xl', image=create_logo)
            ]
        )
        #####################   2da LINEA   #################
        #########   a  c  t  i  v  e   #########
        active_logo = 'http://'+ipGlobal+':10101/datasets/greenticket.png'
        q.page['active'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_23', order=1),
            items=[
                ui.persona(name="btnActive",title='Activos', subtitle='', caption='', size='xl', image=active_logo)
            ]
        )
        #########   f  i  b  r  a   #########
        fibra_logo = 'http://'+ipGlobal+':10101/datasets/fibra_ticket.png'
        q.page['fibra'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_13', order=1),
            items=[
                ui.persona(name="btnFibra",title='Fibra Óptica', subtitle='', caption='', size='xl', image=fibra_logo)
            ]
        )
        #########   w  i  r  e  l  e  s  s   #########
        wireless_logo = 'http://'+ipGlobal+':10101/datasets/wireless_ticket.png'
        q.page['wireless'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_13', order=1),
            items=[
                ui.persona(name="btnWireless",title='Inalámbrico Privado', subtitle='', caption='', size='xl', image=wireless_logo)
                ]
            )
        #####################   3ra LINEA   #################
        #########   p  u  b l  i  c   #########
        public_logo = 'http://'+ipGlobal+':10101/datasets/public_ticket.png'
        q.page['public'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_24', order=1),
            items=[
                ui.persona(name="btnPublic",title='Acceso Público', subtitle='', caption='', size='xl', image=public_logo)
            ]
        )
        #########   d  o  n  e   #########
        exception_logo = 'http://'+ipGlobal+':10101/datasets/exception_ticket.png'
        q.page['exception'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_14', order=1),
            items=[
                ui.persona(name="btnException",title='Excepciones', subtitle='', caption='', size='xl', image=exception_logo)
            ]
        )
        #########   e  x  c  e  p  t  i  o  n   #########
        done_logo = 'http://'+ipGlobal+':10101/datasets/done_ticket.png'
        q.page['done'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_14', order=1),
            items=[
                ui.persona(name="btnDone",title='Terminados', subtitle='', caption='', size='xl', image=done_logo)
            ]
        )

    await q.page.save()

@app('/home_tickets', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await home_tickets(q)