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

async def a_vsty(q: Q):
    global session
    print("Start aplication a_vsty...")

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
        user = ''
        json_datos = json.dumps({"session":session, "user":user})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnActmap:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/maps'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnMonitor:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/rtm'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnSitye:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_tickets'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnSims:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_sims'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnUsers:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/users'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()
    
    if q.args.btnPrs:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/prs'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
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
                            ui.zone('izq1_11', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_12', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_13', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_15', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('izq2', size='20%', zones=[
                            ui.zone('izq2_11', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_12', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_13', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_15', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('cen1',size='20%', zones=[
                            ui.zone('cen1_11', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_12', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_13', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_15', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der1',size='20%', zones=[
                            ui.zone('der1_11', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_12', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_13', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_14', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_15', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der2',size='20%', zones=[
                            ui.zone('der1_21', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_22', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_23', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_24', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_25', size='20%', align='start', direction=ui.ZoneDirection.COLUMN),
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

        checkRight = 'http://'+ipGlobal+':10101/datasets/checkRight.png'
        checkWrong = 'http://'+ipGlobal+':10101/datasets/checkWrong.png'
        checkWarning = 'http://'+ipGlobal+':10101/datasets/image.png'
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['0'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq1_11', order=1),
            items=[ui.persona(name="btnDsla",title='Oficina Central', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkRight)]
        )
        #########   D   -   S   L   A   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['1'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_11', order=1),
            items=[ui.persona(name="btnActmap",title='Las Torres', subtitle='', caption='', size='xl', image=actmap_logo),ui.image(title='', path=checkWarning)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['2'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_11', order=1),
            items=[ui.persona(name="btnSitye",title='Francisco Hernandez', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkRight)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['3'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_11', order=1),
            items=[ui.persona(name="btnDsla",title='Tepames', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWrong)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['4'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_21', order=1),
            items=[ui.persona(name="btnSitye",title='Piscila', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWarning)]
        )
        #####################   2da LINEA   #################
        #########   A   c   t   M   a   p   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['5'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq1_12', order=1),
            items=[ui.persona(name="btnDsla",title='Reporteros', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWrong)]
        )
        #########   D   -   S   L   A   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['6'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_12', order=1),
            items=[ui.persona(name="btnActmap",title='Coalcoman', subtitle='', caption='', size='xl', image=actmap_logo),ui.image(title='', path=checkRight)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['7'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnSitye",title='La Placita', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWrong)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['8'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_12', order=1),
            items=[ui.persona(name="btnDsla",title='Tecoman', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkRight)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['9'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_22', order=1),
            items=[ui.persona(name="btnSitye",title='Ixtlahuacan', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkRight)]
        )
        #####################   3ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['10'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq1_13', order=1),
            items=[ui.persona(name="btnDsla",title='Campo 4', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWarning)]
        )
        #########   D   -   S   L   A   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['11'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_13', order=1),
            items=[ui.persona(name="btnActmap",title='Sitio 12', subtitle='', caption='', size='xl', image=actmap_logo),ui.image(title='', path=checkRight)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['12'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_13', order=1),
            items=[ui.persona(name="btnSitye",title='Sitio 13', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWrong)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['13'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_13', order=1),
            items=[ui.persona(name="btnDsla",title='Sitio 14', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWarning)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['14'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_23', order=1),
            items=[ui.persona(name="btnSitye",title='Sitio 15', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWrong)]
        )
        #####################   4ta LINEA   #################
        #########   A   c   t   M   a   p   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['15'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq1_14', order=1),
            items=[ui.persona(name="btnDsla",title='Sitio 16', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkRight)]
        )
        #########   D   -   S   L   A   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['16'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_14', order=1),
            items=[ui.persona(name="btnActmap", title='Sitio 17', subtitle='', caption='', size='xl', image=actmap_logo),ui.image(title='', path=checkWarning)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['17'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_14', order=1),
            items=[ui.persona(name="btnSitye", title='Sitio 18', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWrong)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['18'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_14', order=1),
            items=[ui.persona(name="btnDsla", title='Sitio 19', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkRight)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['19'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_24', order=1),
            items=[ui.persona(name="btnSitye", title='Sitio 20', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkWrong)]
        )
        #####################   5ta LINEA   #################
        #########   A   c   t   M   a   p   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['20'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq1_15', order=1),
            items=[ui.persona(name="btnDsla", title='Sitio 16', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWarning)]
        )
        #########   D   -   S   L   A   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['21'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_15', order=1),
            items=[ui.persona(name="btnActmap", title='Sitio 17', subtitle='', caption='', size='xl', image=actmap_logo),ui.image(title='', path=checkWrong)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['22'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_15', order=1),
            items=[ui.persona(name="btnSitye", title='Sitio 18', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkRight)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['23'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_15', order=1),
            items=[ui.persona(name="btnDsla", title='Sitio 19', subtitle='', caption='', size='xl', image=dsla_logo),ui.image(title='', path=checkWarning)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['24'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_25', order=1),
            items=[
                ui.persona(name="btnSitye", title='Picachos', subtitle='', caption='', size='xl', image=sitye_logo),ui.image(title='', path=checkRight)]
        )

        q.page['0'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['0'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['1'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['1'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['2'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['2'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['3'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['3'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['4'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['4'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['5'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['5'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['6'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['6'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['7'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['7'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['8'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['8'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['9'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['9'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['10'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['10'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['11'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['11'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['12'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['12'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['13'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['13'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['14'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['14'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['15'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['15'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['16'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['16'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['17'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['17'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['18'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['18'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['19'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['19'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['20'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['20'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['21'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['21'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['22'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['22'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['23'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['23'].items[0].persona.caption = '227V AC - 46.4V DC'
        q.page['24'].items[0].persona.subtitle = '27°C - 54HR'
        q.page['24'].items[0].persona.caption = '227V AC - 46.4V DC'

    await q.page.save()

@app('/a_vsty', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await a_vsty(q)