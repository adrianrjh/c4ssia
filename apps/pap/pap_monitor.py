from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys, os
import random, webbrowser
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common8 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import asyncio
                                                                                       
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
        global refreshDownload, rutaDoc
        data=0
        try:
            data = json.loads(item.decode('utf8'))
            rutaDoc = data['rutaDoc']
            refreshDownload= 1
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="last_session"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="downloadFile"):
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
                        self.pubsub.subscribe(['last_session'],['downloadFile'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['last_session','downloadFile'])
client.start()

async def paso1(q: Q):
    global comboboxProjPaP

    del q.page['btnSave']
    del q.page['checkbox_comanda']
    
    comboboxProjPaP = getAllprojectPaP(r)
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('izq1_12', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,),
        ]
    )

    await q.page.save()

async def paso2(q: Q):
    global data_rows
    del q.page['states1']
    del q.page['checkbox_comanda']
    del q.page['checkbox_comandaNA']
    del q.page['btnSave']

    comboboxProjPaP = getAllprojectPaP(r)
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('izq1_12', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,),
        ]
    )

    q.page['table'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            height = '800px',
            columns=columnsProjectsPaP,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        ),
        ui.button(name='btnModificar',label='Modificar',disabled = False,primary=True,)
    ])

    await q.page.save()

async def paso3(q: Q, flejeF:bool):
    global poste, fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero, potenciaposte
    global flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, remateNA, cableaceroNA
    global data_rows

    del q.page['table']
    del q.page['states1']
    del q.page['btnSave']

    comboboxProjPaP = getAllprojectPaP(r)
    q.page['comboboxBtns'] = ui.section_card(
        box=ui.box('izq1_12', order=1),
        title='',
        subtitle='',
        items=[
                ui.combobox(name='textproyecto', label='Proyectos', value='Seleccionar', choices=comboboxProjPaP,trigger=True),
                ui.button(name='btnSearch',label='Buscar',disabled = False,primary=True,),
        ]
    )

    q.page['checkbox_comanda'] = ui.form_card(
        box = ui.box('izq1_13', order=1),
        items=[
            ui.text('''COMANDA DEL POSTE '''+'''**'''+str(poste)+'''**'''),
            ui.checkbox(name='checkbox_fleje', label='Fleje', value=flejeF, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_herraje', label='Herraje', value=herraje, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_brazo', label='Brazo', value=brazo, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_gaza', label='Gaza', value=gaza, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_raqueta', label='Raqueta', value=raqueta, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cajadistribucion', label='Caja de Distribución', value=cajadistribucion, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cierreempalme', label='Cierre de Empalme', value=cierreempalme, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_remate', label='Remate', value=remate, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cableacero', label='Cable de acero', value=cableacero, disabled=False, trigger = True),
            ui.textbox(name='textpotencia', label='Potencia', value=str(potenciaposte), trigger=True),
        ]
    )

    q.page['checkbox_comandaNA'] = ui.form_card(
        box = ui.box('izq1_13', order=2),
        items=[
            ui.text('''COMANDA DEL POSTE '''+'''**'''+str(poste)+'''**'''+''' NO APLICA'''),
            ui.checkbox(name='checkbox_flejeNA', label='Fleje', value=flejeNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_herrajeNA', label='Herraje', value=herrajeNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_brazoNA', label='Brazo', value=brazoNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_gazaNA', label='Gaza', value=gazaNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_raquetaNA', label='Raqueta', value=raquetaNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cajadistribucionNA', label='Caja de Distribución', value=cajadistribucionNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cierreempalmeNA', label='Cierre de Empalme', value=cierreempalmeNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_remateNA', label='Remate', value=remateNA, disabled=False, trigger = True),
            ui.checkbox(name='checkbox_cableaceroNA', label='Cable de acero', value=cableaceroNA, disabled=False, trigger = True),
            ui.textbox(name='textpotenciaNA', label='Potencia', value=str(potenciaposte), disabled=True, trigger=True),
        ]
    )
    
    q.page['btnSave'] = ui.section_card(box=ui.box('izq1_14', order=1),title='',subtitle='',items=[ui.button(name='btnSave', label='Guardar', disabled = False, primary=True)])
    
    q.page['table'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            height = '800px',
            columns=columnsProjectsPaP,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data_rows],
            #values = ['0'],
            groupable=True,
            downloadable=True,
            resettable=False,
        ),
        ui.button(name='btnModificar',label='Modificar',disabled = False,primary=True,)
    ])

    await q.page.save()

async def refresh(q: Q):
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    try:
        while 1:
            if paso1P == 1 and bandPaso1 == 0:
                bandPaso1 = 1
                await q.run(paso1,q)
                await q.page.save()
            if paso2P == 1 and bandPaso2 == 0:
                bandPaso2 = 1
                await q.run(paso2,q)
                await q.page.save()
            if paso3P == 1 and bandPaso3 == 0:
                bandPaso3 = 1
                await q.run(paso3,q, fleje)
                await q.page.save()
            if paso4P == 1 and bandPaso4 == 0:
                bandPaso4 = 1
                await q.run(paso4,q)
                await q.page.save()
            await q.sleep(0.5)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task
    global bandPaso1, bandPaso2, bandPaso3, bandPaso4
    bandPaso1, bandPaso2, bandPaso3, bandPaso4 = 0, 0, 0, 0
    # Cancela la tarea anterior si existe y aún está corriendo
    if current_refresh_task and not current_refresh_task.done():
        current_refresh_task.cancel()
        try:
            # Espera a que la tarea sea cancelada (opcional)
            await current_refresh_task
        except asyncio.CancelledError:
            # Maneja el caso en que la tarea fue cancelada
            pass
    # Inicia una nueva tarea
    current_refresh_task = asyncio.create_task(refresh(q))

async def pap_monitor(q: Q):
    print(str("starting pap_monitor app..."))
    global ipGlobal,session, r
    global data_rows, data_rows2, proyecto
    global paso1P, paso2P, paso3P, paso4P, bandPaso1, bandPaso2, bandPaso3, bandPaso4
    global poste, poste_completo, fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero, potenciaposte
    global flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, remateNA, cableaceroNA

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

    if q.args.btnAtrasH:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_pap'
        await q.page.save()

    if q.args.textproyecto:
        proyecto = str(q.args.textproyecto)
        await q.page.save()

    if q.args.btnSearch:
        if proyecto != '' and proyecto != 'Seleccionar':
            data_rows = getAllPaP(proyecto)
            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0
        await q.page.save()

    if q.args.btnModificar:
        modificar = q.args.issues
        poste_data = []
        fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero, potenciaposte = False, False, False, False, False, False, False, False, False, 0.0
        flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, cableaceroNA, remateNA = False, False, False, False, False, False, False, False, False
        if modificar == None:
            pass
        if modificar != None:
            if len(modificar)==1:
                data_rows_temp, data_rows_send, found = [], [], 0
                for y in data_rows:
                    for x in modificar:
                        if str(y[0])==str(x):
                            found=1
                            # si quieres quitar los que seleccionaste
                            poste = y[3]
                            proyecto = y[1]
                            potenciaposte = y[11]
                    if found==0:
                        # si quieres quitar los que no seleccionaste
                        data_rows_temp.append(y)
                    found = 0
                poste_data = getPostePaP(r, proyecto, poste)
                if poste_data != 'NO':
                    if poste_data != []:
                        poste = poste_data[0][2]
                        if poste_data[0][3] == 'True':
                            fleje = True
                        if poste_data[0][3] == 'False':
                            fleje = False
                        if poste_data[0][4] == 'True':
                            flejeNA = True
                        if poste_data[0][4] == 'False':
                            flejeNA = False
                        if poste_data[0][5] == 'True':
                            herraje = True
                        if poste_data[0][5] == 'False':
                            herraje = False
                        if poste_data[0][6] == 'True':
                            herrajeNA = True
                        if poste_data[0][6] == 'False':
                            herrajeNA = False
                        if poste_data[0][7] == 'True':
                            brazo = True
                        if poste_data[0][7] == 'False':
                            brazo = False
                        if poste_data[0][8] == 'True':
                            brazoNA = True
                        if poste_data[0][8] == 'False':
                            brazoNA = False
                        if poste_data[0][9] == 'True':
                            gaza = True
                        if poste_data[0][9] == 'False':
                            gaza = False
                        if poste_data[0][10] == 'True':
                            gazaNA = True
                        if poste_data[0][10] == 'False':
                            gazaNA = False
                        if poste_data[0][11] == 'True':
                            raqueta = True
                        if poste_data[0][11] == 'False':
                            raqueta = False
                        if poste_data[0][12] == 'True':
                            raquetaNA = True
                        if poste_data[0][12] == 'False':
                            raquetaNA = False
                        if poste_data[0][13] == 'True':
                            cajadistribucion = True
                        if poste_data[0][13] == 'False':
                            cajadistribucion = False
                        if poste_data[0][14] == 'True':
                            cajadistribucionNA = True
                        if poste_data[0][14] == 'False':
                            cajadistribucionNA = False
                        if poste_data[0][15] == 'True':
                            cierreempalme = True
                        if poste_data[0][15] == 'False':
                            cierreempalme = False
                        if poste_data[0][16] == 'True':
                            cierreempalmeNA = True
                        if poste_data[0][16] == 'False':
                            cierreempalmeNA = False
                        if poste_data[0][17] == 'True':
                            remate = True
                        if poste_data[0][17] == 'False':
                            remate = False
                        if poste_data[0][18] == 'True':
                            remateNA = True
                        if poste_data[0][18] == 'False':
                            remateNA = False
                        if poste_data[0][19] == 'True':
                            cableacero = True
                        if poste_data[0][19] == 'False':
                            cableacero = False
                        if poste_data[0][20] == 'True':
                            cableaceroNA = True
                        if poste_data[0][20] == 'False':
                            cableaceroNA = False
                if poste_data == []:
                    fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero = False, False, False, False, False, False, False, False, False
                    flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, remateNA, cableacerNA = False, False, False, False, False, False, False, False, False

                del q.page['checkbox_comanda']
                del q.page['checkbox_comandaNA']

                q.page['checkbox_comanda'] = ui.form_card(
                    box = ui.box('izq1_13', order=1),
                    items=[
                        ui.text('''COMANDA DEL POSTE '''+'''**'''+str(poste)+'''**'''),
                        ui.checkbox(name='checkbox_fleje', label='Fleje', value=fleje, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_herraje', label='Herraje', value=herraje, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_brazo', label='Brazo', value=brazo, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_gaza', label='Gaza', value=gaza, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_raqueta', label='Raqueta', value=raqueta, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cajadistribucion', label='Caja de Distribución', value=cajadistribucion, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cierreempalme', label='Cierre de Empalme', value=cierreempalme, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_remate', label='Remate', value=remate, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cableacero', label='Cable de acero', value=cableacero, disabled=False, trigger = True),
                        ui.textbox(name='textpotencia', label='Potencia', value=str(potenciaposte), trigger=True),

                    ]
                )

                q.page['checkbox_comandaNA'] = ui.form_card(
                    box = ui.box('izq1_13', order=2),
                    items=[
                        ui.text('''COMANDA DEL POSTE '''+'''**'''+str(poste)+''' NO APLICA'''+'''**'''),
                        ui.checkbox(name='checkbox_flejeNA', label='Fleje', value=flejeNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_herrajeNA', label='Herraje', value=herrajeNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_brazoNA', label='Brazo', value=brazoNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_gazaNA', label='Gaza', value=gazaNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_raquetaNA', label='Raqueta', value=raquetaNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cajadistribucionNA', label='Caja de Distribución', value=cajadistribucionNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cierreempalmeNA', label='Cierre de Empalme', value=cierreempalmeNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_remateNA', label='Remate', value=remateNA, disabled=False, trigger = True),
                        ui.checkbox(name='checkbox_cableaceroNA', label='Cable de acero', value=cableaceroNA, disabled=False, trigger = True),
                        ui.textbox(name='textpotenciaNA', label='Potencia', value=str(potenciaposte), disabled=True, trigger=True),
                    ]
                )
                
                q.page['btnSave'] = ui.section_card(box=ui.box('izq1_14', order=1),title='',subtitle='',items=[ui.button(name='btnSave', label='Guardar', disabled = False, primary=True)])
                
                q.page['table'] = ui.form_card(box=ui.box('der1_11', order=1), items=[
                    ui.table(
                        name='issues',
                        multiple = True,
                        height = '800px',
                        columns=columnsProjectsPaP,
                        rows=[ui.table_row(
                            name=str(dato[0]),
                            cells=dato,
                        )for dato in data_rows],
                        #values = ['0'],
                        groupable=True,
                        downloadable=True,
                        resettable=False,
                    ),
                    ui.button(name='btnModificar',label='Modificar',disabled = False,primary=True,)
                ])
        await q.page.save()

#######     S   I       A   P   L   I   C   A   ########
    if 'checkbox_fleje' in q.args:
        if q.args.checkbox_fleje:
            fleje = q.args.checkbox_fleje
            await q.page.save()
        else:
            fleje = False
            await q.page.save()
    
    if 'checkbox_herraje' in q.args:
        if q.args.checkbox_herraje:
            herraje = q.args.checkbox_herraje
            await q.page.save()
        else:
            herraje = False
            await q.page.save()

    if 'checkbox_brazo' in q.args:
        if q.args.checkbox_brazo:
            brazo = q.args.checkbox_brazo
            await q.page.save()
        else:
            brazo = False
            await q.page.save()
    
    if 'checkbox_gaza' in q.args:
        if q.args.checkbox_gaza:
            gaza = q.args.checkbox_gaza
            await q.page.save()
        else:
            gaza = False
            await q.page.save()
    
    if 'checkbox_raqueta' in q.args:
        if q.args.checkbox_raqueta:
            raqueta = q.args.checkbox_raqueta
            await q.page.save()
        else:
            raqueta = False
            await q.page.save()
    
    if 'checkbox_cajadistribucion' in q.args:
        if q.args.checkbox_cajadistribucion:
            cajadistribucion = q.args.checkbox_cajadistribucion
            await q.page.save()
        else:
            cajadistribucion = False
            await q.page.save()

    if 'checkbox_cierreempalme' in q.args:
        if q.args.checkbox_cierreempalme:
            cierreempalme = q.args.checkbox_cierreempalme
            await q.page.save()
        else:
            cierreempalme = False
            await q.page.save()

    if 'checkbox_remate' in q.args:
        if q.args.checkbox_remate:
            remate = q.args.checkbox_remate
            await q.page.save()
        else:
            remate = False
            await q.page.save()

    if 'checkbox_cableacero' in q.args:
        if q.args.checkbox_cableacero:
            cableacero = q.args.checkbox_cableacero
            await q.page.save()
        else:
            cableacero = False
            await q.page.save()
        
    #######     N   O       A   P   L   I   C   A   ########
    if 'checkbox_flejeNA' in q.args:
        if q.args.checkbox_flejeNA:
            flejeNA = q.args.checkbox_flejeNA
            await q.page.save()
        else:
            flejeNA = False
            await q.page.save()

    if 'checkbox_herrajeNA' in q.args:
        if q.args.checkbox_herrajeNA:
            herrajeNA = q.args.checkbox_herrajeNA
            await q.page.save()
        else:
            herrajeNA = False
            await q.page.save()

    if 'checkbox_brazoNA' in q.args:
        if q.args.checkbox_brazoNA:
            brazoNA = q.args.checkbox_brazoNA
            await q.page.save()
        else:
            brazoNA = False
            await q.page.save()

    if 'checkbox_gazaNA' in q.args:
        if q.args.checkbox_gazaNA:
            gazaNA = q.args.checkbox_gazaNA
            await q.page.save()
        else:
            gazaNA = False
            await q.page.save()

    if 'checkbox_raquetaNA' in q.args:
        if q.args.checkbox_raquetaNA:
            raquetaNA = q.args.checkbox_raquetaNA
            await q.page.save()
        else:
            raquetaNA = False
            await q.page.save()

    if 'checkbox_cajadistribucionNA' in q.args:
        if q.args.checkbox_cajadistribucionNA:
            cajadistribucionNA = q.args.checkbox_cajadistribucionNA
            await q.page.save()
        else:
            cajadistribucionNA = False
            await q.page.save()

    if 'checkbox_cierreempalmeNA' in q.args:
        if q.args.checkbox_cierreempalmeNA:
            cierreempalmeNA = q.args.checkbox_cierreempalmeNA
            await q.page.save()
        else:
            cierreempalmeNA = False
            await q.page.save()

    if 'checkbox_remateNA' in q.args:
        if q.args.checkbox_remateNA:
            remateNA = q.args.checkbox_remateNA
            await q.page.save()
        else:
            remateNA = False
            await q.page.save()

    if 'checkbox_cableaceroNA' in q.args:
        if q.args.checkbox_cableaceroNA:
            cableaceroNA = q.args.checkbox_cableaceroNA
            await q.page.save()
        else:
            cableaceroNA = False
            await q.page.save()

    if 'textpotencia' in q.args:
        if q.args.textpotencia:
            potenciaposte=str(q.args.textpotencia)
            await q.page.save()

    if 'btnSave' in q.args:
        if q.args.btnSave:
            counterStatus = 0
            counterStatusNA = 0
            if fleje == True:
                counterStatus += 1
            if flejeNA ==True:
                counterStatusNA += 1
            if herraje == True:
                counterStatus += 1
            if herrajeNA == True:
                counterStatusNA += 1
            if brazo == True:
                counterStatus += 1
            if brazoNA == True:
                counterStatusNA += 1
            if gaza == True:
                counterStatus += 1
            if gazaNA == True:
                counterStatusNA += 1
            if raqueta == True:
                counterStatus += 1
            if raquetaNA == True:
                counterStatusNA += 1
            if cajadistribucion == True:
                counterStatus += 1
            if cajadistribucionNA == True:
                counterStatusNA += 1
            if cierreempalme == True:
                counterStatus += 1
            if cierreempalmeNA == True:
                counterStatusNA += 1
            if remate == True:
                counterStatus += 1
            if remateNA == True:
                counterStatusNA += 1
            if cableacero == True:
                counterStatus += 1
            if cableaceroNA == True:
                counterStatusNA += 1
            totalchecks = 9-counterStatusNA
            if counterStatus == 0 and totalchecks == 0:
                status = 1
            else:
                status = (counterStatus/totalchecks)
            now = datetime.datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            data_poste={
                "fecha":str(dt_string),
                "proyecto":str(proyecto),
                "poste":str(poste),
                "fleje":str(fleje),"flejeNA":str(flejeNA),
                "herraje":str(herraje),"herrajeNA":str(herrajeNA),
                "brazo":str(brazo),"brazoNA":str(brazoNA),
                "gaza":str(gaza),"gazaNA":str(gazaNA),
                "raqueta":str(raqueta),"raquetaNA":str(raquetaNA),
                "cajadistribucion":str(cajadistribucion),"cajadistribucionNA":str(cajadistribucionNA),
                "cierreempalme":str(cierreempalme),"cierreempalmeNA":str(cierreempalmeNA),
                "remate":str(remate),"remateNA":str(remateNA),
                "cableacero":str(cableacero),"cableaceroNA":str(cableaceroNA),
                "potenciaposte":str(potenciaposte),
            }
            data_status_proyecto ={
                "proyecto":str(proyecto),
                "poste":str(poste),
                "status":str(status),
                "potenciaposte":str(potenciaposte),
            }

            regPostePaP(r, data_poste)
            regDataPaP(r, data_status_proyecto)
            data_rows = getAllPaP(proyecto)

            fleje, herraje, brazo, gaza, raqueta, cajadistribucion, cierreempalme, remate, cableacero, potenciaposte = False, False, False, False, False, False, False, False, False, 0.0
            flejeNA, herrajeNA, brazoNA, gazaNA, raquetaNA, cajadistribucionNA, cierreempalmeNA, remateNA, cableaceroNA = False, False, False, False, False, False, False, False, False

            paso1P = 0
            paso2P = 1
            paso3P = 0
            bandPaso2 = 0

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
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header',size='7%'),
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq',size='25%', zones=[
                                ui.zone('izq1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('izq1_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('izq1_11', size='5%', align='start', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_12', size='15%', align='center', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('izq1_13', size='35%', align='center', direction=ui.ZoneDirection.ROW),
                                        ui.zone('izq1_14', size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                        ui.zone('izq1_15', size='35%', align='start', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
                            ]),
                            ui.zone('der',size='75%', zones=[
                                ui.zone('der1',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der_1', size='100%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', size='100%', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                ]),
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

        q.page['btnAtrasH'] = ui.section_card(box=ui.box('izq1_11', order=1),title='',subtitle='',items=[ui.button(name='btnAtrasH', label='Atrás', disabled = False, primary=True)])

        q.page['states1'] = ui.tall_stats_card(
            box=ui.box('der1_11', order=1),
            items=[
                ui.stat(label='Data not found', value=str("")),
            ]
        )

        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/pap_monitor', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await pap_monitor(q)