from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import redis
from redis import StrictRedis, ConnectionError
from redistimeseries.client import Client
import sys
import random
# adding Folder to the system path
sys.path.insert(0, '/home/wave/libs')
from common import *

class Listener1(threading.Thread):
    def __init__(self, r, rts, channels):
        threading.Thread.__init__(self)
        self.redis,self.init,self.redists = r,0,rts
        self.pubsub = self.redis.pubsub()
        print('Listener1...')
        try:
            self.pubsub.subscribe(channels)
        except Exception as e:
            print(e)

    def work(self, item):
        data =0
        try:
            data = json.loads(item.decode('utf8'))
        except:
            pass
        if data != 0:
            if data["id"]=="bascula1":
                global bascReja
                bascReja = round(data["dato"],2)
                self.sumCV(data)
                try:
                    rts.add(data["id"], int(time.time() * 1000), data["dato"])
                except:
                    print("[ERROR bascula1]####################################### rts.create "+str(data))
            if data["id"]=="bascula2":
                global bascFruta
                bascFruta = round(data["dato"],2)
                self.sumCB(data)
                try:
                    rts.add(data["id"], int(time.time() * 1000), data["dato"])
                except:
                    print("[ERROR bascula2]####################################### rts.create "+str(data))

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message['channel'].decode("utf-8")=="basculas_request": 
                        self.work(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['basculas_request'])
                        break
            time.sleep(0.001)  # be nice to the system :)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

try:
    rts = Client(host=ipRedis,port=6379,socket_keepalive=True,retry_on_timeout=True)
except Exception as e:
    print(e)

client = Listener1(r, rts, ['basculas_request'])
client.start()


async def addList(q: Q):
    del q.page['lista-ing-show']
    global data_rows,data_rows_keycount, dateStart, lote
    global combomodelo,combonumero, cantidadOrmas, comments, cantidadOrmasTotal

    data_rows_keycount += 1
    data_rows.append([str(data_rows_keycount), str(combomodelo), str(combonumero), str(cantidadOrmas), str(comments)])
    q.page['btnDel'].items[0].button.disabled = False
    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            columns=columns1,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    regAct(r,"pedido-act",dateStart,lote, cantidadOrmasTotal, data_rows)

    await q.page.save()

async def showList(q: Q):
    global data_rows, columns1
    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            columns=columns1,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        )
    ])

    await q.page.save()
async def create_pedido(q: Q):
    print(str("starting pesado..."))
    global r, ipGlobal, dateStart, dateEnd, dateLote
    global listIngs, lote, data_rows, data_rows_keycount, recover,msg, msg1
    global comboboxMarcas, combomodelo, combonumero, comboboxNumero, cantidadOrmas, comments, cantidadOrmasTotal, cantidadOrmasTotalNew

    recover = getAll(r,"pedido-act")
    try:
        msg1 = recover["lista"].replace("'","[")
    except Exception:
        msg1 = []

    q.page['meta'] = ui.meta_card(box='')

    if q.args.recovery:
        msg = []
        startendP = True
        print("Recuperando información...")
        dateStart = recover["start"]
        lote = recover["lote"]
        cantidadOrmasTotal = int(recover["totalormas"])
        msg = recover["lista"].replace("'","[")
        data_rows = json.loads(msg)
        data_rows_keycount = len(data_rows)

        q.page['datestart'].value = str(dateStart)
        q.page['pedidoLote'].valuaee = str(lote)
        q.page['ormasTotal'].value = str(cantidadOrmasTotal)
        q.page['titulo'].items[0].button.disabled = True
        q.page['titulo'].items[1].button.disabled = True
        q.page['titulo'].items[2].button.disabled = False
        q.page['btnDel'].items[0].button.disabled = False
        await q.run(showList,q)
        await q.page.save()

    if q.args.start:
        data_rows = []
        q.page['titulo'].items[0].button.disabled = True
        q.page['titulo'].items[1].button.disabled = True
        q.page['titulo'].items[2].button.disabled = False
        now = datetime.datetime.now()
        dateLote = now.strftime("%Y%m%d")
        num_rand = random.randint(10,100)
        lote='L'+str(dateLote)+'-'+str(num_rand)
        dateStart = now.strftime("%Y-%m-%d %H:%M:%S %p")
        dateEnd = "--"
        q.page['datestart'].value = str(dateStart)
        q.page['dateend'].value = str(dateEnd)
        q.page['pedidoLote'].value = str(lote)

        regAct(r,"pedido-act",dateStart, lote, cantidadOrmasTotal, data_rows)

        await q.page.save()

    if q.args.finalize:
        q.page['titulo'].items[0].button.disabled = True
        q.page['titulo'].items[1].button.disabled = False
        q.page['titulo'].items[2].button.disabled = True

        if cantidadOrmasTotal > 0:
            print('publish...')
            json_datos = json.dumps({"start":str(dateStart),"end":str(dateEnd),"lote":lote, "ormasTotal":cantidadOrmasTotal,"lista":data_rows})
            rts.add("hola",int(int(time.time() * 1000)), cantidadOrmasTotal)
            r.publish("create-pedido",json_datos)
        else:
            pass

        if dateStart != "--":
            now = datetime.datetime.now()
            dateEnd = now.strftime("%Y-%m-%d %H:%M:%S %p")
            q.page['dateend'].value = str(dateEnd)
        else:
            q.page['meta'].notification = '[ERROR] TOMAR HORA DE INICIO'

        data_rows_keycount = 0
        lote = '--'
        q.page['pedidoLote'].value = lote
        cantidadOrmasTotal = 0
        cantidadOrmas = 0
        q.page['ormasTotal'].value = cantidadOrmasTotal
        q.page['btnDel'].items[0].button.disabled = True
        data_rows = []
        dateStart = '--'

        regAct(r,"pedido-act",dateStart, lote, cantidadOrmasTotal, data_rows)
        await q.run(showList,q)
        await q.page.save()

    if q.args.comboboxmodelo:
        combomodelo = str(q.args.comboboxmodelo)
        await q.page.save()

    if q.args.comboboxnumero:
        combonumero = str(q.args.comboboxnumero)
        await q.page.save()

    if q.args.spincantidad == 0 or q.args.spincantidad == None:
        q.args.spincantidad = 0
        await q.page.save()
    elif q.args.spincantidad >= 1:
        cantidadOrmas = int(q.args.spincantidad)
        await q.page.save()

    if q.args.textcomment:
        comments=str(q.args.textcomment)
        await q.page.save()

    if q.args.add:
        if lote != '--':
            if combomodelo != "Seleccionar" and combonumero != "Seleccionar":
                if cantidadOrmas > 0:
                    if comments != '--':
                        cantidadOrmasTotal = cantidadOrmasTotal+cantidadOrmas
                        q.page['comboboxes'] = ui.section_card(
                            box=ui.box('der1_12', order=1),
                            title='Agregar un modelo por registro',
                            subtitle='Agregar hasta terminar pedido',
                            items=[
                                ui.combobox(name='comboboxmodelo', label='Modelo', value='Seleccionar', choices=comboboxModelo,trigger=True),
                                ui.combobox(name='comboboxnumero', label='Número', value='Seleccionar', choices=comboboxNumero,trigger=True),
                                ui.spinbox(name='spincantidad', label='Cantidad: ', value=100, disabled = False, max=10000, min=0,trigger=True),
                            ],
                        )
                        q.page['comentarios'] = ui.section_card(
                            box=ui.box('der1_13',order = 1),
                            title='',
                            subtitle='',
                            items=[
                                ui.textbox(name='textcomment', label='Observaciones',trigger=True),
                            ],
                        )
                        q.page['ormasTotal'].value = cantidadOrmasTotal
                        await q.run(addList,q)
        await q.page.save()

    if q.args.delete:
        eliminados =q.args.issues
        data_rows_temp,found=[],0
        for y in data_rows:
            for x in eliminados:
                if str(y[0])==str(x):
                    found=1
            if found==0:    
                data_rows_temp.append(y)
            ormasRes = int(y[3])
            cantidadOrmasTotalNew = cantidadOrmasTotal-ormasRes
            found=0

        data_rows=data_rows_temp
        if len(data_rows) == 0:
            data_rows_keycount = 0
        
        regList(r,"pedido-act",data_rows)
        data_rows_keycount = len(data_rows)

        q.page['ormasTotal'].value = cantidadOrmasTotalNew
        cantidadOrmasTotal = cantidadOrmasTotalNew
        await q.run(showList,q)
        await q.page.save()

    if not q.client.initialized:
        q.client.initialized = True
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                    ui.zone('header',size='10%'),
                    ui.zone('body',size='90%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='15%', zones=[
                            ui.zone('izq1_1',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_2',size='14%'),
                            ui.zone('izq1_3',size='14%'),
                            ui.zone('izq1_4',size= '14%'),
                            ui.zone('izq1_5',size= '14%'),
                            ui.zone('izq1_6',size= '14%'),
                            ui.zone('footer1',size= '15%')
                        ]),
                        ui.zone('cen1',size='85%', zones=[
                            ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_1', size='15%', direction=ui.ZoneDirection.ROW, zones=[
                                        ui.zone('der1_11', size='12.5%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_12', size='50%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_13', size='15%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_14', size='10%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_15', size='12.5%', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('der1_2',size='65%', zones=[
                                    ui.zone('der1_21', size='80%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_22', size='20%', direction=ui.ZoneDirection.ROW),
                                ]),
                                ui.zone('der1_3',size='20%', zones=[
                                    ui.zone('der1_31',size='33%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_32',size='33%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_32',size='33%', direction=ui.ZoneDirection.ROW),
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
                ],
            ),
        ], theme='winter-is-coming')

        q.page['titulo'] = ui.section_card(
            # Place card in the header zone, regardless of viewport size.
            box='header',
            title='Entrada de pedido',
            subtitle='',
            items=[
                ui.button(
                    name='recovery',
                    label='Recovery',
                    disabled = True,
                    primary=True,
                ),
                ui.button(
                    name='start',
                    label='Crear pedido',
                    disabled = False,
                    primary=True,
                ),
                ui.button(
                    name='finalize',
                    label='Enviar Pedido',
                    disabled = True,
                    primary=True,
                ),
            ],
        )

        q.page['datestart'] = ui.small_stat_card(
            box=ui.box(zone='izq1_2', order=1),
            title='Hora de Inicio',
            value=dateStart,
        )
        
        q.page['dateend'] = ui.small_stat_card(
            box=ui.box(zone='izq1_3', order=1),
            title='Hora Final',
            value=dateEnd,
        )

        q.page['pedidoLote'] = ui.small_stat_card(
            box=ui.box('der1_11', order=1),
            title='LOTE PEDIDO',
            value=f'{lote}',
        )

        q.page['comboboxes'] = ui.section_card(
            box=ui.box('der1_12', order=1),
            title='Agregar un modelo por registro',
            subtitle='Agregar hasta terminar pedido',
            items=[
                ui.combobox(name='comboboxmodelo', label='Modelo', value='Seleccionar', choices=comboboxModelo,trigger=True),
                ui.combobox(name='comboboxnumero', label='Número', value='Seleccionar', choices=comboboxNumero,trigger=True),
                ui.spinbox(name='spincantidad', label='Cantidad: ', value=100, disabled = False, max=10000, min=0,trigger=True),
            ],
        )

        q.page['comentarios'] = ui.section_card(
            box=ui.box('der1_13',order = 1),
            title='',
            subtitle='',
            items=[
                ui.textbox(name='textcomment', label='Observaciones',trigger=True),
            ],
        )

        q.page['ormasTotal'] = ui.small_stat_card(
            box=ui.box('der1_14', order=1),
            title='NO. DE ORMAS A USAR',
            value=f'{cantidadOrmasTotal}',
        )
        
        q.page['btnAdd'] = ui.section_card(
            box=ui.box('der1_15', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(
                    name='add',
                    label='Agregar',
                    #caption=' ',
                    width= '120px',
                    disabled = False,
                    primary=True,
                ),
            ],
        )

        q.page['btnDel'] = ui.section_card(
            box=ui.box('der1_22', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(
                    name='delete',
                    label='Delete',
                    #caption=' ',
                    #width= '120px',
                    disabled = True,
                    primary=True,
                ),
            ],
        )

        if msg1!='[]':
            q.page['titulo'].items[0].button.disabled = False

        #content = '![Adrian](http://'+ipGlobal+':10101/datasets/cuadra.png)'
        #content = '![Joel](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        #q.page['shannonImg'] = ui.markdown_card(
        #    box='izq1_1',
        #    title='Version 1.0 (c) 2023 Development by ',
        #    content= content,
        #)

        await q.page.save()
        await q.run(showList,q)

@app('/create_pedido', mode = 'broadcast')
async def team1(q: Q):
    route = q.args['#']
    await create_pedido(q)