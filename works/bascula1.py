from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import redis
from redis import StrictRedis, ConnectionError
import sys
import random
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
        data=0
        global nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,intoData,itera,startendP,autoMan,ingreso,cantidad,cantidadIng
        try:
            data = json.loads(item.decode('utf8'))
            if data != 0 and startendP==True:
                if data["id"] == "pesadoL":
                    print(str(data))
                    if nombre!=data["nombre"]:
                        itera,pesoAct,pesoTotal=0,0,0
                    nombre = data['nombre']
                    lote = data['lote']
                    proveedor = data['proveedor']
                    if proveedor=="Productos selectos de Agave SPR de RL de CV":
                        proveedor="PSA"
                    if proveedor=="Deerland probiotics and enzymes":
                        proveedor="Deerland"
                    ingreso = data['fechaingreso']
                    codigo = data['codigo']
                    caducidad = data['caducidad']
                    status = data['status'] 
                    cantidad  = data['peso']
                    cantidadIng = data['pesoIng']
                    if nombre=="Pineapple Tepache Culture":
                        autoMan=False
                    else:
                        autoMan=True
                    intoData=1

                if data["id"] == "bascula3":
                    if nombre!="--":
                        pesoAct = truncate(data['dato'],3)

        except Exception as e:
            print(e)

    def work2(self, item):
        data=0
        global dateStart,dateEnd,data_rows,dateStartBD,r,data_rowsPub
        global nombre,lote,proveedor,codigo,caducidad,status,pesoTotal,itera,rescombomarca,rescombosabor,comments
        try:
            data = json.loads(item.decode('utf8'))
            print(str(data))
            if len(data_rowsPub)>0 or len(data["data"])>0:
                json_datos = json.dumps(
                    {"timestart":str(dateStart),
                    "timeend":str(dateEnd),
                    "marca":str(rescombomarca),
                    "sabor":str(rescombosabor),
                    "bascula1":data_rowsPub,
                    "bascula2":data["data"],
                    "comments":comments}
                )
                r.publish("finishedPesado",json_datos)
            else:
                print("No published...")
            data_rowsPub=[]
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if message['channel'].decode("utf-8")=="pesado": 
                        self.work(message['data'])
                    if message['channel'].decode("utf-8")=="endPesado": 
                        self.work2(message['data'])
            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:
                        self.pubsub.subscribe(['pesado','endPesado'])
                        break
            time.sleep(0.001)  # be nice to the system :)

try:
    r = StrictRedis(host=ipRedis,port=6379,db=0,health_check_interval=30,socket_keepalive=True)
except Exception as e:
    print(e)

client = Listener1(r, ['pesado','endPesado'])
client.start()

async def refresh(q: Q):
    global nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,intoData,itera,autoMan,intoOne,cantidad,cantidadIng
    global msg2,recover2,recover,msg1,combomarca,combosabor,comboboxMarcas,comboboxSabor

    card1 = q.page['nombreIng']
    card2 = q.page['loteIng']
    card3 = q.page['provIng']
    card4 = q.page['codIng']
    card5 = q.page['cadIng']
    card6 = q.page['statIng']
    card7 = q.page['pesoBasc']
    card8 = q.page['itePeso']
    card9 = q.page['pesoSum']
    card10 = q.page['totalAlmacen']
    card11 = q.page['totalAlmacenIng']
    
    while 1:
        print("while..")
        recover2 = getAll(r,"pesado-act2")
        #msg2 = recover2["lista"].replace("'","[")
        recover = getAll(r,"pesado-act")
        #msg1 = recover["lista"].replace("'","[")

        if startendP==True and intoOne==0:

            if autoMan==False:
                q.page['pesoMan'] = ui.form_card(
                    box=ui.box('der1_21', order=3), items=[
                    ui.textbox(name='manualPeso',label='Ingresar Peso Manualmente'),
                ])
            q.page['titulo'].items[0].button.disabled = True  #recover
            q.page['titulo'].items[1].button.disabled = True  #start
            q.page['titulo'].items[3].button.disabled = False #finalize
            q.page['comboboxes'] = ui.section_card(
                box='izq1_6',
                title='',
                subtitle='',
                items=[
                    ui.combobox(name='comboboxmarca', label='Marca', value=str(combomarca), choices=comboboxMarcas,trigger=True),
                    ui.combobox(name='comboboxsabor', label='Sabor', value=str(combosabor), choices=comboboxSabor,trigger=True)
                ],
            )
            q.page['comboboxes'].items[0].combobox.disabled = True
            q.page['comboboxes'].items[1].combobox.disabled = True

            await q.run(showList,q)
            intoOne=1
        if startendP==False and intoOne==1:
            q.page['titulo'].items[0].button.disabled = True
            q.page['titulo'].items[1].button.disabled = False
            q.page['titulo'].items[3].button.disabled = True
            await q.run(showList,q)
            intoOne=0

        #if (recover["lista"] != "[]") or (recover['nombre']!="--"):
        #    q.page['titulo'].items[0].button.disabled = False
        #    print("1")

        if recover != {} and startendP:
            q.page['titulo'].items[0].button.disabled = True
            print("2")

        if recover == {}:
            q.page['titulo'].items[0].button.disabled = True
            print("3")

        if  len(data_rows)>0:
            q.page['titulo'].items[2].button.disabled = False
            print("4")
        else:
            q.page['titulo'].items[2].button.disabled = True

        if startendP==True:
            if intoData==1:
                card1.value = nombre
                card2.value = lote
                card3.value = proveedor
                card4.value = codigo
                card5.value = caducidad
                card6.value = status
                card10.value =str(cantidad)+" kg"
                card10.title = nombre
                card11.value =str(cantidadIng)+" kg"
                card11.title = nombre
                if autoMan==False:
                    del q.page['pesoSum']
                    q.page['pesoMan'] = ui.form_card(
                        box=ui.box('der1_21', order=3), items=[
                        ui.textbox(name='manualPeso',label='Ingresar Peso Manualmente'),
                    ])
                intoData=0
            if nombre!="--" and nombre!="Tepache Pina Culture":
                card7.value = str(pesoAct)+" kg"
                card8.value=itera
                card9.value=str(pesoTotal)+" kg"
        
        #if dateStart != "--" and dateEnd == "--":
        #    q.page['titulo'].items[1].button.disabled = True
        #    q.page['titulo'].items[3].button.disabled = False

        await q.page.save()
        await q.sleep(1)

async def addList(q: Q):
    global data_rows,data_rows_keycount 
    global nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,itera,cantidad,cantidadIng,combomarca,combosabor
    data_rows_keycount += 1 
    data_rows.append([str(data_rows_keycount),str(ingreso),str(nombre), str(codigo),str(proveedor),str(lote), str(caducidad), str(status),str(itera),str(pesoTotal)])
    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_31', order=1), items=[
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
            resettable=True,
        )
    ])

    nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,itera,cantidad,cantidadIng="--","--","--","--","--","--",0,0,0,0.0,0.0
    regAct(r,"pesado-act",data_rows_keycount,dateStart,nombre,lote,proveedor,codigo,caducidad,status,itera,pesoTotal,combomarca,combosabor,data_rows)
    card1 = q.page['nombreIng'].value = nombre
    card2 = q.page['loteIng'].value = lote
    card3 = q.page['provIng'].value = proveedor
    card4 = q.page['codIng'].value = codigo
    card5 = q.page['cadIng'].value = caducidad
    card6 = q.page['statIng'].value = status
    card7 = q.page['pesoBasc'].value = "0 kg"
    card8 = q.page['itePeso'].value = itera
    card9 = q.page['pesoSum'].value = "0 kg"
    card10 = q.page['totalAlmacen'].value = str(cantidad)+" kg"
    card10 = q.page['totalAlmacen'].title = "--"
    card11 = q.page['totalAlmacenIng'].value = str(cantidadIng)+" kg"
    card11 = q.page['totalAlmacenIng'].title = "--"

    await q.page.save()

async def showList(q: Q):
    global data_rows 
    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_31', order=1), items=[
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
            resettable=True,
        )
    ])

    await q.page.save()

async def bascula1(q: Q):
    print(str("starting bascula1..."))
    global recover,data_rows,r,msg2,data_rowsPub,ipGlobal,intoOne,comments
    global dateStart,dateEnd,startendP,data_rows_keycount,nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,itera,autoMan
    global recover2,msg1,comboboxMarcas,comboboxSabor_OCA,comboboxSabor_TEPACHE,comboboxSabor_SALUTARIS,comboboxSabor_PUNTA,combomarca,combosabor,comboboxSabor,rescombomarca,rescombosabor

    recover2 = getAll(r,"pesado-act2")
    #msg2 = recover2["lista"].replace("'","[")
    recover = getAll(r,"pesado-act")
    #msg1 = recover["lista"].replace("'","[")
    
    intoOne = 0
    ite_count = q.user.ite_count or 0
    pesoBasc = q.user.pesoBasc or 0
    sumaPeso = q.user.sumaPeso or 0

    q.page['meta'] = ui.meta_card(box='')

    if q.args.comboboxsabor:
        combosabor=str(q.args.comboboxsabor)

    if q.args.textcomment:
        comments=str(q.args.textcomment)
        #print(str(comments))

    if q.args.comboboxmarca and combomarca!=str(q.args.comboboxmarca):
        val=" "
        if str(q.args.comboboxmarca)=="OCA":
            comboboxSabor=comboboxSabor_OCA
            val="BERRY ACAI"
        if str(q.args.comboboxmarca)=="TEPACHE":
            comboboxSabor=comboboxSabor_TEPACHE
            val="STRAWBERRY HIBISCUS"
        if str(q.args.comboboxmarca)=="SALUTARIS":
            comboboxSabor=comboboxSabor_SALUTARIS
            val="TORONJA"
        if str(q.args.comboboxmarca)=="PUNTA DELICIA":
            comboboxSabor=comboboxSabor_PUNTA
            val="MUSANITA BANANO"
        if str(q.args.comboboxmarca)=="BAJA INGRE":
            comboboxSabor=comboboxSabor_BAJA
            val="BAJA INGRE"


        combosabor=val
        combomarca=str(q.args.comboboxmarca)

        q.page['comboboxes'] = ui.section_card(
            box='izq1_6',
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value=str(q.args.comboboxmarca), choices=comboboxMarcas,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value=str(val), choices=comboboxSabor,trigger=True)

            ],
        )
        await q.page.save()
    if q.args.recovery:
        msg = []
        startendP = True
        print("Recuperando información...")
        msg = recover["lista"].replace("'","[")
        data_rows = json.loads(msg)

        data_rows_keycount = int(recover["keys"])
        dateStart = recover["start"]
        nombre = recover["nombre"]
        lote = recover["lote"]
        proveedor = recover["proveedor"]
        codigo = recover["codigo"]
        caducidad = recover["caducidad"]
        status = recover["status"]
        itera = int(recover["ite"])
        pesoTotal = float(recover["peso"])
        combomarca=str(recover["marca"])
        combosabor=str(recover["sabor"])

        q.page['comboboxes'] = ui.section_card(
            box='izq1_6',
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value=str(combomarca), choices=comboboxMarcas,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value=str(combosabor), choices=comboboxSabor,trigger=True)

            ],
        )
        q.page['datestart'].value = str(dateStart)
        q.page['nombreIng'].value = str(nombre)
        q.page['loteIng'].value = str(lote)
        q.page['provIng'].value = str(proveedor)
        q.page['codIng'].value = str(codigo)
        q.page['cadIng'].value = str(caducidad)
        q.page['statIng'].value = str(status)
        q.page['itePeso'].value = str(itera)
        q.page['pesoSum'].value = str(pesoTotal)+" kg"
        q.page['titulo'].items[0].button.disabled = True
        q.page['titulo'].items[1].button.disabled = True
        q.page['titulo'].items[3].button.disabled = False
        q.page['comboboxes'].items[0].combobox.disabled = True
        q.page['comboboxes'].items[1].combobox.disabled = True

        json_datos = json.dumps({"timestart":str(dateStart),"timeend":str(dateEnd),"id":"bascula-lab-recovery","dato":startendP})
        r.publish("startPesado",json_datos)

        await q.run(showList,q)
        await q.page.save()

    if q.args.start:
        print(str(combomarca))
        if combomarca=="OCA" or combomarca=="TEPACHE" or combomarca=="SALUTARIS" or combomarca=="PUNTA DELICIA" or combomarca=="BAJA INGRE":
            print(str("start..."))
            print(str(combomarca))
            print(str(combosabor))
            data_rows_keycount = 0
            data_rows=[]
            startendP = True
            q.page['titulo'].items[0].button.disabled = True
            q.page['titulo'].items[1].button.disabled = True
            q.page['titulo'].items[3].button.disabled = False
            now = datetime.datetime.now()
            dateStart = now.strftime("%Y-%m-%d %H:%M:%S %p")
            dateEnd = "--"
            q.page['paso0Fin'].value = str(dateEnd)
            print(str(dateStart))
            q.user.ite_count = ite_count = 0
            q.user.pesoBasc = pesoBasc = 0
            q.user.sumaPeso = sumaPeso = 0
            q.page['datestart'].value = str(dateStart)
            q.page['itePeso'].value = str(ite_count)
            q.page['pesoBasc'].value = str(pesoBasc)+" kg"
            q.page['pesoSum'].value = str(sumaPeso)+" kg"

            json_datos = json.dumps({"timestart":str(dateStart),"timeend":str(dateEnd),"id":"bascula-lab","dato":startendP})
            r.publish("startPesado",json_datos)

            regAct(r,"pesado-act",data_rows_keycount,dateStart,nombre,lote,proveedor,codigo,caducidad,status,itera,pesoTotal,combomarca,combosabor,data_rows)

            q.page['comboboxes'].items[0].combobox.disabled = True
            q.page['comboboxes'].items[1].combobox.disabled = True

            await q.run(showList,q)
            await q.page.save()

    if q.args.delete:
        print(str("delete..."))
        eliminados =q.args.issues
        print(str(eliminados))
        data_rows_temp,found=[],0
        for y in data_rows:
            for x in eliminados:
                if str(y[0])==str(x):
                    found=1
            if found==0:
                data_rows_temp.append(y)
            found=0

        data_rows=data_rows_temp
        if len(data_rows) == 0:
            data_rows_keycount = 0
        #regList(r,"pesado-act",data_rows)

        await q.run(showList,q)
        await q.page.save()
        
    if q.args.finalize:
        print(str("finalize..."))
        startendP = False
        data_rows_keycount=0
        q.page['titulo'].items[0].button.disabled = True
        q.page['titulo'].items[1].button.disabled = False
        q.page['titulo'].items[3].button.disabled = True
        q.page['comboboxes'].items[0].combobox.disabled = False
        q.page['comboboxes'].items[1].combobox.disabled = False

        if dateStart != "--":
            now = datetime.datetime.now()
            dateEnd = now.strftime("%Y-%m-%d %H:%M:%S %p")
            q.page['paso0Fin'].value = str(dateEnd)
        else:
            q.page['meta'].notification = '[ERROR] TOMAR HORA DE INICIO'

        json_datos = json.dumps({"timestart":str(dateStart),"timeend":str(dateEnd),"id":"bascula-lab","dato":startendP})
        payload = json.dumps({"key":"PES_reporte","data":data_rows,"start":dateStart,"end":dateEnd})
        data_rowsPub = data_rows

        rescombomarca,rescombosabor=combomarca,combosabor
        nombre,lote,proveedor,codigo,caducidad,status,pesoAct,pesoTotal,itera="--","--","--","--","--","--",0,0,0
        dateStartBD,combomarca,combosabor = "--","seleccionar"," "
        data_rows,comboboxSabor=[],[]
        regAct(r,"pesado-act",data_rows_keycount,dateStartBD,nombre,lote,proveedor,codigo,caducidad,status,itera,pesoTotal,combomarca,combosabor,data_rows)
        
        q.user.ite_count = ite_count = 0
        q.user.pesoBasc = pesoBasc = 0
        q.user.sumaPeso = sumaPeso = 0

        q.page['nombreIng'].value = nombre
        q.page['loteIng'].value = lote
        q.page['provIng'].value = proveedor
        q.page['codIng'].value = codigo
        q.page['cadIng'].value = caducidad
        q.page['statIng'].value = status
        q.page['itePeso'].value = str(ite_count)
        q.page['pesoBasc'].value = str(pesoAct)+ " kg"
        q.page['pesoSum'].value = str(sumaPeso)+ " kg"
        
        #r.publish("PES_reporte",payload)
        r.publish("startPesado",json_datos)

        q.page['comboboxes'] = ui.section_card(
            box='izq1_6',
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value='seleccionar', choices=comboboxMarcas,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value='seleccionar', choices=comboboxSabor,trigger=True)
            ],
        )
        
        q.page['comentarios'] = ui.section_card(
            box=ui.box('izq1_7',order = 2),
            title='',
            subtitle='',
            items=[
                ui.textbox(name='textcomment', label='Observaciones',trigger=True),
            ],
        )

        await q.run(showList,q)
        await q.page.save()           

    if q.args.sumaIte:
        if startendP == True and nombre!="--" and autoMan==True:
            pesoTotal=truncate(pesoTotal+pesoAct,3)
            itera=itera+1
            regAct(r,"pesado-act",data_rows_keycount,dateStart,nombre,lote,proveedor,codigo,caducidad,status,itera,pesoTotal,combomarca,combosabor,data_rows)
        await q.page.save()

    if q.args.addIng:
        if startendP == True and nombre!="--":
            if autoMan==False:
                print(q.args.manualPeso)
                if str(q.args.manualPeso).isdigit():
                    pesoMan = float(f'{q.args.manualPeso}')
                    print(str("OK digit...")+str(pesoMan))
                    pesoTotal=truncate(pesoTotal+int(pesoMan),3)
                    del q.page['pesoMan']
                    q.page['pesoSum'] = ui.small_stat_card(
                        box=ui.box('der1_21', order=3),
                        title='TOTAL',
                        value=f'{sumaPeso} kg',
                    )
                    autoMan=True
                    itera=1
                    await q.run(addList,q)

                else:
                    print("No es un numero...")
            else:
                if pesoTotal>0:
                    await q.run(addList,q)

        await q.page.save()

    if not q.client.initialized:
        q.client.initialized = True
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                    ui.zone('header',size='8%'),
                    #ui.zone('top', direction=ui.ZoneDirection.ROW, size='90px'),
                    #ui.zone('top1', direction=ui.ZoneDirection.ROW, size='90px'),
                    ui.zone('body',size='92%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='18%', zones=[
                            ui.zone('izq1_1',align='center',size='12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_2',align='center',size='14%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_3',align='center',size='14%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_4',align='center',size= '14%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_5',align='center',size= '14%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_6',align='center',size= '12%',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_7',size= '12%',align='center'),
                            ui.zone('footer1',size= '8%')
                        ]),
                        ui.zone('der1',size='82%', zones=[
                            ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                                ui.zone('der1_1',size='15%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('der1_11', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_12', direction=ui.ZoneDirection.ROW),
                                    ui.zone('der1_13', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('der1_2',size='15%', zones=[
                                    ui.zone('der1_21', direction=ui.ZoneDirection.ROW),
                                ]),
                                ui.zone('der1_3',size='70%', zones=[
                                    ui.zone('der1_31',size='100%', direction=ui.ZoneDirection.ROW),
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
            title='Bascula Laboratorio',
            subtitle=' ',
            items=[
                ui.button(
                    name='recovery',
                    label='Recovery',
                    disabled = True,
                    primary=True,
                ),
                ui.button(
                    name='start',
                    label='Start',
                    disabled = False,
                    primary=True,
                ),
                ui.button(
                    name='delete',
                    label='Delete',
                    disabled = True,
                    primary=True,
                ),
                ui.button(
                    name='finalize',
                    label='End',
                    disabled = True,
                    primary=True,
                ),
            ],
        )

        content = '![Adrian](http://'+ipGlobal+':10101/datasets/ShannonWeaver.png)'
        #content = '![Joel](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        q.page['shannonImg'] = ui.markdown_card(
            box=ui.box('izq1_1',order = 1),
            title=' ',
            content= content,
        )

        q.page['datestart'] = ui.small_stat_card(
            box=ui.box(zone='izq1_2', order=1),
            title='Hora de Inicio',
            value=dateStart,
        )
        
        q.page['paso0Fin'] = ui.small_stat_card(
            box=ui.box(zone='izq1_3', order=1),
            title='Hora Final',
            value=dateEnd,
        )

        q.page['nombreIng'] = ui.small_stat_card(
            box=ui.box('der1_11', order=1),
            title='NOMBRE',
            value=f'{nombre}',
        )
        
        q.page['loteIng'] = ui.small_stat_card(
            box=ui.box('der1_11', order=2),
            title='LOTE',
            value=f'{lote}',
        )
        
        q.page['provIng'] = ui.small_stat_card(
            box=ui.box('der1_12', order=1),
            title='PROVEEDOR',
            value=f'{proveedor}',
        )
        
        q.page['codIng'] = ui.small_stat_card(
            box=ui.box('der1_12', order=2),
            title='CODIGO',
            value=f'{codigo}',
        )
        
        q.page['cadIng'] = ui.small_stat_card(
            box=ui.box('der1_13', order=1),
            title='CADUCIDAD',
            value=f'{caducidad}',
        )
        
        q.page['statIng'] = ui.small_stat_card(
            box=ui.box('der1_13', order=2),
            title='STATUS',
            value=f'{status}',
        )

        q.page['itePeso'] = ui.small_stat_card(
            box=ui.box('der1_21', order=1),
            title='CANTIDAD',
            value=f'{itera}',
        )

        q.page['pesoBasc'] = ui.small_stat_card(
            box=ui.box('der1_21', order=2),
            title='PESO BASCULA',
            value=f'{pesoAct} kg',
        )

        q.page['pesoSum'] = ui.small_stat_card(
            box=ui.box('der1_21', order=3),
            title='TOTAL',
            value=f'{sumaPeso} kg',
        )

        q.page['bascula'] = ui.section_card(
            box='der1_21',
            title='Suma de pesos',
            subtitle='(Solo sumar si el valor es correcto)',
            items=[
                ui.button(
                    name='sumaIte',
                    label='+',
                    #caption=' ',
                    #width= '80px',
                    disabled = False,
                    primary=True,
                ),
                ui.button(
                    name='addIng',
                    label='Agregar a la Lista',
                    #caption=' ',
                    #width= '100px',
                    disabled = False,
                    primary=True,
                ),
            ],
        )

        q.page['totalAlmacen'] = ui.small_stat_card(
            box=ui.box('izq1_4', order=1),
            title=nombre+" x Lote",
            value=f'{cantidad} kg',
        )

        q.page['totalAlmacenIng'] = ui.small_stat_card(
            box=ui.box('izq1_5', order=1),
            title=nombre+" x Ing",
            value=f'{cantidadIng} kg',
        )

        q.page['comboboxes'] = ui.section_card(
            box='izq1_6',
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value='seleccionar', choices=comboboxMarcas,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value='seleccionar', choices=comboboxSabor,trigger=True)
            ],
        )

        q.page['comentarios'] = ui.section_card(
            box=ui.box('izq1_7',order = 2),
            title='',
            subtitle='',
            items=[
                ui.textbox(name='textcomment', label='Observaciones',trigger=True),
            ],
        )

        #if msg2!="[]":
        #    q.page['titulo'].items[0].button.disabled = False
        #    print("1.1")

        if msg1!="[]":
            q.page['titulo'].items[0].button.disabled = False
            print("1.1.1")

        q.page['footer'] = ui.footer_card(box=ui.box('footer1', order=1), caption='Version 1.0 by Shannon Weaver.')

        await q.page.save()
        await q.run(showList,q)
        await q.run(refresh,q)


@app('/bascula1', mode = 'broadcast')
async def team1(q: Q):
    route = q.args['#']
    await bascula1(q)