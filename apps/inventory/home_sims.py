from h2o_wave import Q, app, main, ui, AsyncSite,site,data
#from pyzabbix import ZabbixAPI
import threading,json,time,math
from datetime import datetime
import sys
from redis import StrictRedis, ConnectionError
from redistimeseries.client import Client
import random
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from common0 import *
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
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

client = Listener1(r, ['last_session'])
client.start()

async def home_sims(q: Q):
    global session, username
    print("Start aplication home_sims...")

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

    if q.args.btnCotejo:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_cotejo'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnRecepcion:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_recepcion'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAsigOut:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_asignacion'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnDevolución:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_devolucion'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnScrap:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_scrap'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnStocksEN:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_stocksEN'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAltaEU:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_altaEU'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAltaEN:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_altaEN'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnAltaMC:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_altaMC'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnStocksEU:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_stocksEU'
        else:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/login'
        await q.page.save()

    if q.args.btnStocksMC:
        if session == True:
            q.page['meta'].redirect = 'http://'+ipGlobal+':10101/sims_stocksMC'
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
                            ui.zone('izq1_11',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_12',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_13',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_14',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq1_15',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('izq2', size='20%', zones=[
                            ui.zone('izq2_21',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_22',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_23',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_24',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('izq2_25',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('cen1',size='20%', zones=[
                            ui.zone('cen1_11',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_12',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_13',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_14',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('cen1_15',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der1',size='20%', zones=[
                            ui.zone('der1_11',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_12',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_13',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_14',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_15',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                        ]),
                        ui.zone('der2',size='20%', zones=[
                            ui.zone('der1_21',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_22',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_23',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_24',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
                            ui.zone('der1_25',size='20%', align='center',direction=ui.ZoneDirection.COLUMN),
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
        q.page['CassiaImg'] = ui.section_card(box=ui.box('cen1_11', order=1),title='',subtitle='',items=[ui.image(title='', path=content)])
        #####################   1ra LINEA   #################
        #########   a  c  t  i  v  e   #########
        cotejo_logo = 'http://'+ipGlobal+':10101/datasets/cotejo.png'
        q.page['cotejo'] = ui.section_card(box=ui.box(zone='izq2_22', order=1),title='',subtitle='',items=[ui.persona(name="btnCotejo",title='Cotejo', subtitle='', caption='', size='xl', image=cotejo_logo)])
        #########   f  i  b  r  a   #########
        recepcion_logo = 'http://'+ipGlobal+':10101/datasets/recepcion.png'
        q.page['recepcion'] = ui.section_card(box=ui.box(zone='cen1_12', order=1),title='',subtitle='',items=[ui.persona(name="btnRecepcion",title='Recepcion', subtitle='', caption='', size='xl', image=recepcion_logo)])
        #########   w  i  r  e  l  e  s  s   #########
        asignacion_logo = 'http://'+ipGlobal+':10101/datasets/asignacion.png'
        q.page['asignacion'] = ui.section_card(box=ui.box(zone='der1_12', order=1),title='',subtitle='',items=[ui.persona(name="btnAsigOut",title='Asignación y Salida', subtitle='', caption='', size='xl', image=asignacion_logo)])
        #####################   2da LINEA   #################
        #########   p  u  b l  i  c   #########
        devolucion_logo = 'http://'+ipGlobal+':10101/datasets/devolucion.png'
        q.page['devolucion'] = ui.section_card(box=ui.box(zone='izq2_23', order=1),title='',subtitle='',items=[ui.persona(name="btnDevolución",title='Devolución', subtitle='', caption='', size='xl', image=devolucion_logo)])
        #########   d  o  n  e   #########
        scrap_logo = 'http://'+ipGlobal+':10101/datasets/scrap1.png'
        q.page['scrap'] = ui.section_card(box=ui.box(zone='cen1_13', order=1),title='',subtitle='',items=[ui.persona(name="btnScrap",title='Scrap', subtitle='', caption='', size='xl', image=scrap_logo)])
        #########    a l t a   u s a d o s   #########
        altaEU_logo = 'http://'+ipGlobal+':10101/datasets/altaEU.png'
        q.page['altaEU'] = ui.section_card(box=ui.box(zone='der1_13', order=1),title='',subtitle='',items=[ui.persona(name="btnAltaEU",title='Alta Equipos Usados', subtitle='', caption='', size='xl', image=altaEU_logo)])
        #####################   3ra LINEA   #################
        #########    a l t a   n u e v o s   #########
        altaEN_logo = 'http://'+ipGlobal+':10101/datasets/altaEN.png'
        q.page['altaEN'] = ui.section_card(box=ui.box(zone='izq2_24', order=1),title='',subtitle='',items=[ui.persona(name="btnAltaEN",title='Alta Equipos Nuevos', subtitle='', caption='', size='xl', image=altaEN_logo)])
        #########    a l t a   m a t e r i a l  c o n s t r u c c i o n   #########
        altaMC_logo = 'http://'+ipGlobal+':10101/datasets/altaMC.png'
        q.page['altaMC'] = ui.section_card(box=ui.box(zone='cen1_14', order=1),title='',subtitle='',items=[ui.persona(name="btnAltaMC",title='Alta Material Construcción', subtitle='', caption='', size='xl', image=altaMC_logo)])
        #########   s t o c k s  n u e v o s   #########
        stocksEN_logo = 'http://'+ipGlobal+':10101/datasets/stocksEN.png'
        q.page['stocksEN'] = ui.section_card(box=ui.box(zone='der1_14', order=1),title='',subtitle='',items=[ui.persona(name="btnStocksEN",title='Stocks Equipos Nuevos', subtitle='', caption='', size='xl', image=stocksEN_logo)])
        #####################   4ta LINEA   #################
        #########   s t o c k s  u s a d o s   #########
        stocksEU_logo = 'http://'+ipGlobal+':10101/datasets/stocksEU.png'
        q.page['stocksEU'] = ui.section_card(box=ui.box(zone='izq2_25', order=1),title='',subtitle='',items=[ui.persona(name="btnStocksEU",title='Stocks Equipos Usados', subtitle='', caption='', size='xl', image=stocksEU_logo)])
        #########   s t o c k s  c o n s t r u c c i o n   #########
        stocksMC_logo = 'http://'+ipGlobal+':10101/datasets/stocksMC.png'
        q.page['stocksMC'] = ui.section_card(box=ui.box(zone='cen1_15', order=1),title='',subtitle='',items=[ui.persona(name="btnStocksMC",title='Stocks Construcción', subtitle='', caption='', size='xl', image=stocksMC_logo)])

    await q.page.save()

@app('/home_sims', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await home_sims(q)
