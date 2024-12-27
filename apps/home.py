from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,math
from datetime import datetime
import sys
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

async def renderHome(q: Q):
    global puesto
    if puesto == 'Desarrollador':
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['actmap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnActmap",title='ActMap', subtitle='', caption='', size='xl', image=actmap_logo)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['sitye'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnSitye",title='SIT&E', subtitle='', caption='', size='xl', image=sitye_logo)]
        )
        #########   P   a    P   #########
        pap_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['pap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_12', order=1),
            items=[ui.persona(name="btnPaP",title='PaP', subtitle='', caption='', size='xl', image=pap_logo)]
        )
        #####################   2da LINEA   #################
        #########   S   I   M   S   #########
        sii_logo = 'http://'+ipGlobal+':10101/datasets/sims2.png'
        q.page['sii'] = ui.section_card(
            title='',
            subtitle = '',
            box=ui.box(zone='izq2_23', order=1),
            items=[ui.persona(name="btnSims",title='SIMS', subtitle='', caption='', size='xl', image=sii_logo)]
        )
        #########   U S E R S   #########
        users_logo = 'http://'+ipGlobal+':10101/datasets/users.png'
        q.page['users'] = ui.section_card(
            title='',
            subtitle = '',
            box=ui.box(zone='cen1_13', order=1),
            items=[ui.persona(name="btnUsers",title='Users', subtitle='', caption='', size='xl', image=users_logo)]
        )
        #########   P   R   s   #########
        home_prs_logo = 'http://'+ipGlobal+':10101/datasets/management-pr.png'
        q.page['prs'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_13', order=1),
            items=[ui.persona(name="btnPrs",title='Manage PRs', subtitle='', caption='', size='xl', image=home_prs_logo)]
        )
        #####################   3ra LINEA   #################
        #########   I   I   S   #########
        iis_logo = 'http://'+ipGlobal+':10101/datasets/iis.png'
        q.page['iis'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_24', order=1),
            items=[ui.persona(name="btnIIS",title='I²S', subtitle='', caption='', size='xl', image=iis_logo)]
        )
        #########   a-VSTy   #########
        avsty_logo = 'http://'+ipGlobal+':10101/datasets/a_vsty1.png'
        q.page['avsty'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_14', order=1),
            items=[ui.persona(name="btnAvsty",title='a-VSTy', subtitle='', caption='', size='xl', image=avsty_logo)]
        )
        #########   D   -   S   L   A   #########
        dsla_logo = 'http://'+ipGlobal+':10101/datasets/dsla.png'
        q.page['dsla'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_14', order=1),
            items=[ui.persona(name="btnDsla",title='D-SLA', subtitle='', caption='', size='xl', image=dsla_logo)]
        )
        #####################   4ta LINEA   #################
        #########   S   I   T   o   P   o   #########
        sitopo_logo = 'http://'+ipGlobal+':10101/datasets/sitopo1.png'
        q.page['sitopo'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_25', order=1),
            items=[ui.persona(name="btnSitopo",title='SIToPo', subtitle='', caption='', size='xl', image=sitopo_logo)]
        )
        #########   R   T   M   #########
        monitor_logo = 'http://'+ipGlobal+':10101/datasets/rtm.png'
        q.page['rtm'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_15', order=1),
            items=[ui.persona(name="btnMonitor",title='RTMonitoring', subtitle='', caption='', size='xl', image=monitor_logo)]
        )

    if puesto == 'Administrador':
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['actmap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnActmap",title='ActMap', subtitle='', caption='', size='xl', image=actmap_logo)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['sitye'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnSitye",title='SIT&E', subtitle='', caption='', size='xl', image=sitye_logo)]
        )
    if puesto == 'Soporte Técnico':
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['actmap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnActmap",title='ActMap', subtitle='', caption='', size='xl', image=actmap_logo)]
        )
        #########   S   I   T   &   E   #########
        sitye_logo = 'http://'+ipGlobal+':10101/datasets/sitye.png'
        q.page['sitye'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnSitye",title='SIT&E', subtitle='', caption='', size='xl', image=sitye_logo)]
        )
        #########   R   T   M   #########
        monitor_logo = 'http://'+ipGlobal+':10101/datasets/rtm.png'
        q.page['rtm'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_12', order=1),
            items=[ui.persona(name="btnMonitor",title='RTMonitoring', subtitle='', caption='', size='xl', image=monitor_logo)]
        )
        #####################   2da LINEA   #################
        #########   P   a    P   #########
        pap_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['pap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_23', order=1),
            items=[ui.persona(name="btnPaP",title='PaP', subtitle='', caption='', size='xl', image=pap_logo)]
        )
        #########   I   I   S   #########
        iis_logo = 'http://'+ipGlobal+':10101/datasets/iis.png'
        q.page['iis'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_13', order=1),
            items=[ui.persona(name="btnIIS",title='I²S', subtitle='', caption='', size='xl', image=iis_logo)]
        )

    if puesto == 'Arquitecto':
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        actmap_logo = 'http://'+ipGlobal+':10101/datasets/actmap.png'
        q.page['actmap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnActmap",title='ActMap', subtitle='', caption='', size='xl', image=actmap_logo)]
        )
        #########   P   R   s   #########
        home_prs_logo = 'http://'+ipGlobal+':10101/datasets/management-pr.png'
        q.page['prs'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnPrs",title='Manage PRs', subtitle='', caption='', size='xl', image=home_prs_logo)]
        )
        #####################   2da LINEA   #################
        #########   P   a    P   #########
        pap_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['pap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='der1_12', order=1),
            items=[ui.persona(name="btnPaP",title='PaP', subtitle='', caption='', size='xl', image=pap_logo)]
        )

    if puesto == 'Almacenista':
        #####################   1ra LINEA   #################
        #########   A   c   t   M   a   p   #########
        sims_logo = 'http://'+ipGlobal+':10101/datasets/sims2.png'
        q.page['sims'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnSims",title='SIMS', subtitle='', caption='', size='xl', image=sims_logo)]
        )
        #########   S   I   T   &   E   #########
        iis_logo = 'http://'+ipGlobal+':10101/datasets/iis.png'
        q.page['iis'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='cen1_12', order=1),
            items=[ui.persona(name="btnIIS",title='I²S', subtitle='', caption='', size='xl', image=iis_logo)]
        )

    if puesto == 'Proyectista':
        #####################   1ra LINEA   #################
        #########   P   a    P   #########
        pap_logo = 'http://'+ipGlobal+':10101/datasets/pap.png'
        q.page['pap'] = ui.section_card(
            title='', 
            subtitle = '',
            box=ui.box(zone='izq2_22', order=1),
            items=[ui.persona(name="btnPaP",title='PaP', subtitle='', caption='', size='xl', image=pap_logo)]
        )

    if puesto == '':
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

async def home(q: Q):
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

    if q.args.btnAvsty:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/a_vsty'
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
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_prs'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnProjects:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/projects'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnPaP:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_pap'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnIIS:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_iis'
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

@app('/', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await home(q)