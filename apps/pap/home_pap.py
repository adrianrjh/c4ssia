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
from funcApp import *

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

async def renderHome(q: Q):
    global puesto
    puesto = 'Desarrollador'
    if puesto == 'Desarrollador':
        #####################   1ra LINEA   #################
        #########   P   R   O   J   E   C   T   S   #########
        projects_logo = 'http://'+ipGlobal+':10101/datasets/projects.png'
        q.page['projectsPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnProjectsPaP",title='Projects', subtitle='', caption='', size='xl', image=projects_logo)]
        )
        #########   T   I   C   K   E   T   S   #########
        tickets_logo = 'http://'+ipGlobal+':10101/datasets/tickets-pap.png'
        q.page['ticketsPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnTicketsPaP",title='Tickets', subtitle='', caption='', size='xl', image=tickets_logo)]
        )
        #########   C   R   U   D        P   O   S   T   E   S   #########
        pap_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['crudPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_12', order=1),
            items=[ui.persona(name="btnCrud",title='CRUD Postes', subtitle='', caption='', size='xl', image=pap_logo)]
        )
        #####################   2da LINEA   #################
        #########   O   B   R   A       Y       C   O   N   S   T   R   U   C   C   I   O   N   #########
        obra_logo = 'http://'+ipGlobal+':10101/datasets/obra-pap.png'
        q.page['obraPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_23', order=1),
            items=[ui.persona(name="btnObraPaP",title='Obras y Construcción', subtitle='', caption='', size='xl', image=obra_logo)]
        )
        #########   M   A   N   A   G   E       T   I   C   K   E   T   S   #########
        manage_logo = 'http://'+ipGlobal+':10101/datasets/manage-tickets.png'
        q.page['managePaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_13', order=1),
            items=[ui.persona(name="btnManageTickets",title='Manage Tickets', subtitle='', caption='', size='xl', image=manage_logo)]
        )
        #########   C   O   N   V   E   R   T   E   R        U  T   M   <->   L   A   T   -   L   O   N   G   #########
        converter_logo = 'http://'+ipGlobal+':10101/datasets/converter.png'
        q.page['converterPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_13', order=1),
            items=[ui.persona(name="btnConverter",title='UTMxy <-> Lat Lon Converter', subtitle='', caption='', size='xl', image=converter_logo)]
        )
        #####################   3ra LINEA   #################
        #########   D   E   N   S   I   T   Y   #########
        density_logo = 'http://'+ipGlobal+':10101/datasets/density-pap.png'
        q.page['densityPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_24', order=1),
            items=[ui.persona(name="btnDensityPaP",title='Density', subtitle='', caption='', size='xl', image=density_logo)]
        )
        #########   M   O   N   I   T   O   R   I   N   G       D   E   N   S   I   T   Y   #########
        monitor_density_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['monitorPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_14', order=1),
            items=[ui.persona(name="btnMonitorDensity",title='Monitor Density', subtitle='', caption='', size='xl', image=monitor_density_logo)]
        )
    
    if puesto == 'Proyectista':
        #####################   1ra LINEA   #################
        #########   P   R   O   J   E   C   T   S   #########
        projects_logo = 'http://'+ipGlobal+':10101/datasets/projects.png'
        q.page['projectsPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnProjectsPaP",title='Projects', subtitle='', caption='', size='xl', image=projects_logo)]
        )
        #########   O   B   R   A       Y       C   O   N   S   T   R   U   C   C   I   O   N   #########
        obra_logo = 'http://'+ipGlobal+':10101/datasets/obra-pap.png'
        q.page['obraPaP'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnObraPaP",title='Obras y Construcción', subtitle='', caption='', size='xl', image=obra_logo)]
        )
    if puesto == '':
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

async def home_pap(q: Q):
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
        user = ''
        json_datos = json.dumps({"session":session, "user":user})
        try:
            r.publish("last_session",json_datos)
        except Exception as e:
            print(e)
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnProjectsPaP:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_projects'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnTicketsPaP:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_tickets'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnDensityPaP:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_density'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnObraPaP:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_obra'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnManageTickets:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_manage'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnConverter:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_converter'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnCrud:
        session = True
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/pap_poles'
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
                            ui.zone('izq1_11',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_12',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_13',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_14',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_15',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('izq2', size='20%', zones=[
                            ui.zone('izq2_21',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_22',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_23',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_24',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_25',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('cen1',size='20%', zones=[
                            ui.zone('cen1_11',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_12',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_13',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_14',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_15',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der1',size='20%', zones=[
                            ui.zone('der1_11',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_12',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_13',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_14',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_15',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der2',size='20%', zones=[
                            ui.zone('der1_21',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_22',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_23',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_24',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_25',size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
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
        await q.run(renderHome,q)

    await q.page.save()

@app('/home_pap', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await home_pap(q)