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

client = Listener1(r, ['last_session','LT01TP0LT'])
client.start()

async def settings(q: Q):
    global session
    print("Start aplication settings...")
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

    if q.args.myprs:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/myprs'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.misequipos:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/mydevices'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.mytickets:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/mytickets'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnDevices:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/devices'
        await q.page.save()

    if q.args.btnConn:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/connections'
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
        q.page['header2_settings'] = ui.header_card(
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
        q.page['CassiaImg'] = ui.section_card(
            box=ui.box('cen1_11', order=1),
            title='',
            subtitle = '',
            items = [
                ui.image(title='', path=content),
            ]
        )
        #########   Add Devices   #########
        devices_logo = 'http://'+ipGlobal+':10101/datasets/add-logo.png'
        q.page['addDev'] = ui.section_card(box=ui.box(zone='izq2_22', order=1),title='',subtitle='',items=[ui.persona(name="btnDevices",title='Manage Device(s)', subtitle='', caption='', size='xl', image=devices_logo)])
        #########   Delete Devices   #########
        makeConn_logo = 'http://'+ipGlobal+':10101/datasets/twrs.png'
        q.page['makeConn'] = ui.section_card(box=ui.box(zone='cen1_12', order=1),title='',subtitle='',items=[ui.persona(name="btnConn",title='Connection(s)', subtitle='', caption='', size='xl', image=makeConn_logo)])
        #########   Delete Devices   #########
        misequipos_logo = 'http://'+ipGlobal+':10101/datasets/misequipos.png'
        q.page['misequipos'] = ui.section_card(box=ui.box(zone='der1_12', order=1),title='',subtitle='',items=[ui.persona(name="misequipos",title='Mis Equipos', subtitle='', caption='', size='xl', image=misequipos_logo)])
        #########   mis pr's   #########
        myprs_logo = 'http://'+ipGlobal+':10101/datasets/myprs.png'
        q.page['myprs'] = ui.section_card(box=ui.box(zone='izq2_23', order=1),title='',subtitle='',items=[ui.persona(name="myprs",title='Mis PRs', subtitle='', caption='', size='xl', image=myprs_logo)])
        #########   mis tickets   #########
        mytickets_logo = 'http://'+ipGlobal+':10101/datasets/tickets.png'
        q.page['mytickets'] = ui.section_card(box=ui.box(zone='cen1_13', order=1),title='',subtitle='',items=[ui.persona(name="mytickets",title='Mis Tickets', subtitle='', caption='', size='xl', image=mytickets_logo)])
    await q.page.save()

@app('/settings', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await settings(q)