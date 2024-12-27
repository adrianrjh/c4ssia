from h2o_wave import main, app, ui, data, Q, AsyncSite
import time
import random
import redis,datetime
import asyncio
from redis import StrictRedis, ConnectionError
import json, threading
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/wave/libs')
from common2 import *

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
        global niveluht,flujouht,sostenimiento_in,enfriamiento
        global niveluht_rows,flujouht_rows,sostenimiento_in_rows,enfriamiento_rows
        global aguacaliente,salidaproducto,sostenimiento_out, entrada_glicol
        global aguacaliente_rows,salidaproducto_rows,sostenimiento_out_rows, entrada_glicol_rows
        global brixlinea, gas, phEspera, tempEspera
        global tanque1, tanque2, tanque3, tanque4
        global brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows
        global tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows

        try:
            data = json.loads(item.decode('utf8'))
            if data["id"]=='uht_nivel':
                niveluht = data["dato"]
                if len(niveluht_rows)>=1000:
                    niveluht_rows.pop(0)
                niveluht_rows.append([len(niveluht_rows), niveluht])
            if data["id"]=='uht_flujo':
                flujouht = data["dato"]
                if len(flujouht_rows)>=1000:
                    flujouht_rows.pop(0)
                flujouht_rows.append([len(flujouht_rows), flujouht])
            if data["id"]=='uht_tt02':
                sostenimiento_in= data["dato"]
                if len(sostenimiento_in_rows)>=1000:
                    sostenimiento_in_rows.pop(0)
                sostenimiento_in_rows.append([len(sostenimiento_in_rows), sostenimiento_in])
            if data["id"]=='uht_tt03':
                enfriamiento = data["dato"]
                if len(enfriamiento_rows)>=1000:
                    enfriamiento_rows.pop(0)
                enfriamiento_rows.append([len(enfriamiento_rows), enfriamiento])
            if data["id"]=='uht_te04':
                aguacaliente = data["dato"]
                if len(aguacaliente_rows)>=1000:
                    aguacaliente_rows.pop(0)
                aguacaliente_rows.append([len(aguacaliente_rows), aguacaliente])
            if data["id"]=='uht_tt05':
                salidaproducto = data["dato"]
                if len(salidaproducto_rows)>=1000:
                    salidaproducto_rows.pop(0)
                salidaproducto_rows.append([len(salidaproducto_rows), salidaproducto])
            if data["id"]=='uht_te06':
                sostenimiento_out = data["dato"]
                if len(sostenimiento_out_rows)>=1000:
                    sostenimiento_out_rows.pop(0)
                sostenimiento_out_rows.append([len(sostenimiento_out_rows), sostenimiento_out])
            if data["id"]=='uht_te07':
                entrada_glicol = data["dato"]
                if len(entrada_glicol_rows)>=1000:
                    entrada_glicol_rows.pop(0)
                entrada_glicol_rows.append([len(entrada_glicol_rows), entrada_glicol])
            if data["id"]=='BRIX01LINEA':
                brixlinea = data["dato"]
                if len(brixlinea_rows)>=1000:
                    brixlinea_rows.pop(0)
                brixlinea_rows.append([len(brixlinea_rows), brixlinea])
            if data["id"]=='serv_nivelg':
                gas = data["dato"]
                if len(gas_rows)>=1000:
                    gas_rows.pop(0)
                gas_rows.append([len(gas_rows), gas])
            if data["id"]=='uht_ph':
                phEspera = data["dato"]
                if len(phEspera_rows)>=1000:
                    phEspera_rows.pop(0)
                phEspera_rows.append([len(phEspera_rows), phEspera])
            if data["id"]=='uht_temp':
                tempEspera = data["dato"]
                if len(tempEspera_rows)>=1000:
                    tempEspera_rows.pop(0)
                tempEspera_rows.append([len(tempEspera_rows), tempEspera])
            if data["id"]=='LTTK01LT':
                tanque1 = data["dato"]
                if len(tanque1_rows)>=1000:
                    tanque1_rows.pop(0)
                tanque1_rows.append([len(tanque1_rows), tanque1])
            if data["id"]=='LTTK02LT':
                tanque2 = data["dato"]
                if len(tanque2_rows)>=1000:
                    tanque2_rows.pop(0)
                tanque2_rows.append([len(tanque2_rows), tanque2])
            if data["id"]=='LTTK03LT':
                tanque3 = data["dato"]
                if len(tanque3_rows)>=1000:
                    tanque3_rows.pop(0)
                tanque3_rows.append([len(tanque3_rows), tanque3])
            if data["id"]=='LTTK04LT':
                tanque4 = data["dato"]
                if len(tanque4_rows)>=1000:
                    tanque4_rows.pop(0)
                tanque4_rows.append([len(tanque4_rows), tanque4])
        except Exception as e:
            print(e)
    
    def work2(self, item):
        data=0
        global AV080, AV081, AV082, PP001, HW001, FAN001, CW001
        try:
            data = json.loads(item.decode('utf8'))
            ############################################################
            if data["id"]=='AV080':
                if data["onoff"] == False:
                    AV080 = "OFF"
                if data["onoff"] == True:
                    AV080 = "ON"
            if data["id"]== "AV081":
                if data["onoff"] == False:
                    AV081 = "OFF"
                if data["onoff"] == True:
                    AV081 = "ON"
            if data["id"]=='AV082':
                if data["onoff"] == False:
                    AV082 = "OFF"
                if data["onoff"] == True:
                    AV082 = "ON"
            if data["id"]=='PP001':
                if data["onoff"] == False:
                    PP001 = "OFF"
                if data["onoff"] == True:
                    PP001 = "ON"
            if data["id"]== "HW001":
                if data["onoff"] == False:
                    HW001 = "OFF"
                if data["onoff"] == True:
                    HW001 = "ON"
            if data["id"]== "FAN001":
                if data["onoff"] == False:
                    FAN001 = "OFF"
                if data["onoff"] == True:
                    FAN001 = "ON"
            if data["id"]== 'CW001':
                if data["onoff"] == False:
                    CW001 = "OFF"
                if data["onoff"] == True:
                    CW001 = "ON"
        except Exception as e:
            print(e)

    def work3(self, item):
        data=0    
        global Pasteur, Recir
        try:
            data = json.loads(item.decode('utf8'))
            ############################################################
            if data["recircu"] == False:
                Recir = "OFF"
            if data["recircu"] == True:
                Recir = "ON"
            if data["pasteur"] == False:
                Pasteur = "OFF"
            if data["pasteur"] == True:
                Pasteur = "ON"
        except Exception as e:
            print(e)

    def work4(self, item):
        data=0    
        global CALM
        try:
            data = json.loads(item.decode('utf8'))
            ############################################################
            if data["circuitoALM"] == True:
                CALM = "ON"
            if data["circuitoALM"] == False:
                CALM = "OFF"
        except Exception as e:
            print(e)

    def work5(self, item):
        data=0    
        global dataInfo,dataInfoMarca,dataInfoSabor,dataInfoTanque,dataInfoPasteur
        try:
            data = json.loads(item.decode('utf8'))
            if data['on']=="1":
                ############################################################
                dataInfoMarca=data['marca']
                dataInfoSabor=data['sabor']
                dataInfoTanque=data['tanqueDest']
                dataInfo=dataInfoMarca+" "+dataInfoSabor
                print(str(dataInfo))
                dataInfoPasteur=1
            if data['on']=="0":
                ############################################################
                dataInfoMarca=data['marca']
                dataInfoSabor=data['sabor']
                dataInfoTanque=data['tanqueDest']
                dataInfo=dataInfoMarca+" "+dataInfoSabor
                print(str(dataInfo))
                dataInfoPasteur=0


        except Exception as e:
            print(e)


    def run(self):
        while True:
            try:
                message = self.pubsub.get_message()
                if message:
                    if (message['channel'].decode("utf-8")=="uht_flujo" or 
                        message['channel'].decode("utf-8")=="uht_nivel" or 
                        message['channel'].decode("utf-8")=="uht_tt02" or 
                        message['channel'].decode("utf-8")=="uht_tt03" or 
                        message['channel'].decode("utf-8")=="uht_te04" or 
                        message['channel'].decode("utf-8")=="uht_tt05" or 
                        message['channel'].decode("utf-8")=="uht_te06" or 
                        message['channel'].decode("utf-8")=="uht_te07" or 
                        message['channel'].decode("utf-8")=="BRIX01LINEA" or 
                        message['channel'].decode("utf-8")=="LTTK01LT" or 
                        message['channel'].decode("utf-8")=="LTTK02LT" or 
                        message['channel'].decode("utf-8")=="LTTK03LT" or 
                        message['channel'].decode("utf-8")=="LTTK04LT" or 
                        message['channel'].decode("utf-8")=="serv_nivelg"):
                        self.work(message['data'])
                    if (message['channel'].decode("utf-8")=="uht_dig_request" or message['channel'].decode("utf-8")=="uht_ana_request"):
                        self.work2(message['data'])
                    if (message['channel'].decode("utf-8")=="status_UHT"):
                        self.work3(message['data'])
                    if (message['channel'].decode("utf-8")=="status_UHT_2"):
                        self.work4(message['data'])
                    if (message['channel'].decode("utf-8")=="pasteur_onoff"):
                        self.work5(message['data'])

            except ConnectionError:
                print('[lost connection]')
                while True:
                    print('trying to reconnect...')
                    try:
                        self.redis.ping()
                    except ConnectionError:
                        time.sleep(10)
                    else:

                        self.pubsub.subscribe(['status_UHT_2','status_UHT','uht_dig_request','uht_ana_request','uht_flujo','uht_nivel','uht_tt02','uht_tt03','uht_te04','uht_tt05','uht_te06','uht_te07','BRIX01LINEA','LTTK01LT','LTTK02LT','LTTK03LT','LTTK04LT','serv_nivelg','pasteur_onoff'])
                        break
            time.sleep(0.001)  # be nice to the system :)

client = Listener1(r, ['status_UHT_2','status_UHT','uht_dig_request','uht_ana_request','uht_flujo','uht_nivel','uht_tt02','uht_tt03','uht_te04','uht_tt05','uht_te06','uht_te07','BRIX01LINEA','LTTK01LT','LTTK02LT','LTTK03LT','LTTK04LT','serv_nivelg','pasteur_onoff'])
client.start()

async def refresh(q: Q):
    print("refreshing...")
    global inicio_val
    global AV080, AV081, AV082, PP001, HW001, FAN001, CW001, Recir, Pasteur, CALM
    global niveluht,flujouht,sostenimiento_in,enfriamiento
    global niveluht_rows,flujouht_rows,sostenimiento_in_rows,enfriamiento_rows
    global aguacaliente,salidaproducto,sostenimiento_out, entrada_glicol
    global aguacaliente_rows,salidaproducto_rows,sostenimiento_out_rows, entrada_glicol_rows
    global brixlinea, gas, phEspera, tempEspera
    global tanque1, tanque2, tanque3, tanque4
    global brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows
    global tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows
    global temp_min_past, temp_max_past, flujo_min_past, flujo_max_past, tanques_dest
    global recover, dateStart,data_to_run,dataInfo,dataInfoMarca,dataInfoSabor,dataInfoTanque,dataInfoPasteur
    
    recover = getAll(r,"conf_past")
    data_to_run= getAll(r,"pasteur_to_run")

    if data_to_run["pasteur"]=="SI":
        dataInfoMarca=data_to_run['marca']
        dataInfoSabor=data_to_run['sabor']
        dataInfoTanque=data_to_run['tanqueDest']
        dataInfo=dataInfoMarca+" "+dataInfoSabor
        dataInfoPasteur=1
    if data_to_run["pasteur"]=="NO":
        dataInfoPasteur=0

    while True:
        await q.sleep(1)
        q.page['niveluht'].data.qux, q.page['flujouht'].data.qux = niveluht, flujouht 
        q.page['sostenimiento_in'].data.qux,q.page['enfriamiento'].data.qux = sostenimiento_in,enfriamiento
        q.page['aguacaliente'].data.qux, q.page['salidaproducto'].data.qux =  aguacaliente, salidaproducto
        q.page['sostenimiento_out'].data.qux,q.page['entrada_glicol'].data.qux =  sostenimiento_out,entrada_glicol
        q.page['brixlinea'].data.qux, q.page['gas'].data.qux, q.page['phEspera'].data.qux, q.page['tempEspera'].data.qux =  brixlinea, gas, phEspera, tempEspera
        q.page['tanque1'].data.qux, q.page['tanque2'].data.qux, q.page['tanque3'].data.qux, q.page['tanque4'].data.qux = tanque1, tanque2, tanque3, tanque4
        
        q.page['niveluht'].plot_data,q.page['flujouht'].plot_data = niveluht_rows, flujouht_rows
        q.page['sostenimiento_in'].plot_data,q.page['enfriamiento'].plot_data = sostenimiento_in_rows, enfriamiento_rows
        q.page['aguacaliente'].plot_data, q.page['salidaproducto'].plot_data = aguacaliente_rows, salidaproducto_rows
        q.page['sostenimiento_out'].plot_data,q.page['entrada_glicol'].plot_data = sostenimiento_out_rows, entrada_glicol_rows
        q.page['brixlinea'].plot_data, q.page['gas'].plot_data,q.page['phEspera'].plot_data, q.page['tempEspera'].plot_data = brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows
        q.page['tanque1'].plot_data, q.page['tanque2'].plot_data,q.page['tanque3'].plot_data,q.page['tanque4'].plot_data = tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows

        q.page['states'].items[0].value = AV080
        q.page['states2'].items[0].value = AV081
        q.page['states3'].items[0].value = AV082
        q.page['states4'].items[0].value = PP001
        q.page['states5'].items[0].value = HW001
        q.page['states6'].items[0].value = FAN001
        q.page['states7'].items[0].value = CW001
        q.page['states8'].items[0].value = Recir
        q.page['states9'].items[0].value = Pasteur
        q.page['states10'].items[0].value = CALM

        if dataInfoPasteur == 1:
            dataInfoPasteur=2
            if inicio_val==False:
                q.page['titulo'].items[2].button.disabled = False  #iniciar
                dataInfo=dataInfoMarca+" "+dataInfoSabor
                q.page['dataProduct'] = ui.small_stat_card(
                    box=ui.box(zone='header_25', order=1),
                    title='Producto',
                    value=dataInfo,
                )
                q.page['dataTanqueDest'] = ui.small_stat_card(
                    box=ui.box(zone='header_26', order=1),
                    title='Tanque Destino',
                    value=dataInfoTanque,
                )
                await q.page.save()
        
        if dataInfoPasteur == 0:
            q.page['titulo'].items[2].button.disabled = True  #iniciar
            dataInfo="--"
            dataInfoTanque="--"
            q.page['dataProduct'] = ui.small_stat_card(
                box=ui.box(zone='header_25', order=1),
                title='Producto',
                value=dataInfo,
            )
            q.page['dataTanqueDest'] = ui.small_stat_card(
                box=ui.box(zone='header_26', order=1),
                title='Tanque Destino',
                value=dataInfoTanque,
            )
            await q.page.save()


        if inicio_val==False:
            q.page['titulo'].items[0].button.disabled = True  #recovery
            #q.page['titulo'].items[2].button.disabled = True  #iniciar
            q.page['titulo'].items[4].button.disabled = True  #reiniciar
            q.page['titulo'].items[6].button.disabled = True  #finalizar

        if recover == {} and inicio_val == True:
            q.page['titulo'].items[0].button.disabled = True

        if recover['start'] != "--" and inicio_val == False:
            q.page['titulo'].items[0].button.disabled = False

        if inicio_val==True and dateStart != "":
            q.page['confPaste'].items[1].spinbox.disabled = True
            q.page['confPaste'].items[1].spinbox.value = temp_min_past

            q.page['confPaste'].items[2].spinbox.disabled = True
            q.page['confPaste'].items[2].spinbox.value = temp_max_past

            q.page['confPaste1'].items[1].spinbox.disabled = True
            q.page['confPaste1'].items[1].spinbox.value = flujo_min_past

            q.page['confPaste1'].items[2].spinbox.disabled = True
            q.page['confPaste1'].items[2].spinbox.value = flujo_max_past

            #q.page['confPaste2'].items[1].combobox.disabled = True
            #q.page['confPaste2'].items[1].combobox.value = tanques_dest
            
            q.page['titulo'].items[0].button.disabled = True  #recovery
            q.page['titulo'].items[2].button.disabled = True  #iniciar
            q.page['titulo'].items[4].button.disabled = False  #fin
            q.page['titulo'].items[6].button.disabled = False  #finalizar

        await q.page.save()

async def pasteurizacion(q: Q):
    print("starting pasteurizacion")

    global inicio_val, dateStart, dateEnd, r
    global AV080, AV081, AV082, PP001, HW001, FAN001, CW001, Recir, Pasteur, CALM
    global niveluht,flujouht,sostenimiento_in,enfriamiento
    global niveluht_rows,flujouht_rows,sostenimiento_in_rows,enfriamiento_rows
    global aguacaliente,salidaproducto,sostenimiento_out, entrada_glicol
    global aguacaliente_rows,salidaproducto_rows,sostenimiento_out_rows, entrada_glicol_rows
    global brixlinea, gas, phEspera, tempEspera
    global tanque1, tanque2, tanque3, tanque4
    global brixlinea_rows, gas_rows, phEspera_rows, tempEspera_rows
    global tanque1_rows, tanque2_rows, tanque3_rows, tanque4_rows
    global temp_min_past, temp_max_past, flujo_min_past, flujo_max_past, tanques_dest, combotanque, noTanque
    global ipGlobal, comboboxTanques, recover, dateStart,dataInfo,dataInfoTanque,data_to_run,dataInfoPasteur

    recover = getAll(r,"conf_past")

    q.page['meta'] = ui.meta_card(box='')
    inicio_val = q.user.inicio_val or False

    if q.args.textcomment:
        comments=str(q.args.textcomment)

    if q.args.tempmin == 0 or q.args.tempmin == None:
        q.args.tempmin = 0
    if q.args.tempmin >= 1:
        temp_min_past = int(q.args.tempmin)

    if q.args.tempmax == 0 or q.args.tempmax == None:
        q.args.tempmax = 0
    if q.args.tempmax >= 1:
        temp_max_past = int(q.args.tempmax)

    if q.args.flujomin == 0 or q.args.flujomin == None:
        q.args.flujomin = 0
    if q.args.flujomin >= 1:
        flujo_min_past = int(q.args.flujomin)

    if q.args.flujomax == 0 or q.args.flujomax == None:
        q.args.flujomax = 0
    if q.args.flujomax >= 1:
        flujo_max_past = int(q.args.flujomax)

    #if (q.args.tanques == 'Tanque 1') or (q.args.tanques == 'Tanque 2') or (q.args.tanques == 'Tanque 3') or (q.args.tanques == 'Tanque 4'):
        #tanques_dest = q.args.tanques
    if dataInfoTanque == 'tanque1':
        noTanque = 1
    if dataInfoTanque == 'tanque2':
        noTanque = 2
    if dataInfoTanque == 'tanque3':
        noTanque = 3
    if dataInfoTanque == 'tanque4':
        noTanque = 4


    print("n°->"+str(noTanque))


    if q.args.recovery:
        del q.page['confPaste']
        del q.page['confPaste1']
        #del q.page['confPaste2']

        dateStart = str(recover['start'])
        temp_min_past = int(recover['temp_min'])
        temp_max_past = int(recover['temp_max'])
        flujo_min_past = int(recover['flow_min'])
        flujo_max_past = int(recover['flow_max'])
        tanques_dest = str(recover['tank'])
        
        q.page['confPaste'] = ui.form_card(
            box=ui.box(zone='mid1_11_2', order=1),
            items=[
                ui.text_xl('TEMPERATURA'),
                ui.spinbox(name='tempmin', label='Temp Min: ', value = temp_min_past, min = 0, max = 120, disabled = True),
                ui.spinbox(name='tempmax', label='Temp Max: ', value = temp_max_past, min = 0, max = 120, disabled = True),
            ],
        )

        q.page['confPaste1'] = ui.form_card(
            box=ui.box(zone='mid1_12_2', order=1),
            items=[
                ui.text_xl('FLUJO'),
                ui.spinbox(name='flujomin', label='Flujo Min: ', value = flujo_min_past, min = 0, max = 3000, disabled = True),
                ui.spinbox(name='flujomax', label='Flujo Max: ', value = flujo_max_past, min = 0, max = 3000, disabled = True),
            ],
        )

        #q.page['confPaste2'] = ui.form_card(
        #    box=ui.box(zone='mid1_13_2', order=1),
        #    items=[
        #        ui.text_xl('TANQUE DESTINO'),
        #        ui.combobox(name='tanques', label='', value=str(tanques_dest), choices=comboboxTanques, trigger=True, disabled = True),
        #    ],
        #)

        json_datos = json.dumps({"start":1,"tempMin":temp_min_past,"tempMax":temp_max_past,"flujoMin":flujo_min_past,"flujoMax":flujo_max_past,"tanque":noTanque})
        r.publish("start_UR",json_datos)

        q.page['datestart'].value = str(dateStart)
        await q.page.save()
        q.user.inicio_val = inicio_val = True
    
    if q.args.iniciar:
        if temp_min_past > 1:
            if temp_min_past < temp_max_past:
                if flujo_min_past >= 1:
                    if flujo_max_past > flujo_min_past:
                        #if (tanques_dest == 'Tanque 1') or (tanques_dest == 'Tanque 2') or (tanques_dest == 'Tanque 3') or (tanques_dest == 'Tanque 3'):
                            q.page['confPaste'].items[1].spinbox.disabled = True
                            q.page['confPaste'].items[2].spinbox.disabled = True
                            q.page['confPaste1'].items[1].spinbox.disabled = True
                            q.page['confPaste1'].items[2].spinbox.disabled = True
                            #q.page['confPaste2'].items[1].combobox.disabled = True
                            q.user.inicio_val = inicio_val = True
                            now = datetime.datetime.now()
                            dateStart = now.strftime("%Y-%m-%d %H:%M:%S")
                            dateEnd = "--"
                            q.page['dateend'].value = str(dateEnd)
                            q.page['datestart'].value = str(dateStart)
                            regAct(r,"conf_past", str(dateStart), str(temp_min_past), str(temp_max_past), str(flujo_min_past), str(flujo_max_past), str(tanques_dest))
                            
                            json_datos = json.dumps({"start":1,"tempMin":temp_min_past,"tempMax":temp_max_past,"flujoMin":flujo_min_past,"flujoMax":flujo_max_past,"tanque":noTanque})
                            r.publish("start_UR",json_datos)
        await q.page.save()
        
    if q.args.restart:
        #if (Recir == "ON") or (Pasteur == "ON" and CALM == "ON"):
            q.user.inicio_val = inicio_val = False
            q.user.restart = restart = False

            dateStart = "--"
            dateEnd = "--"

            temp_min_past = 90
            temp_max_past = 100
            flujo_min_past = 1500
            flujo_max_past = 2000
            tanques_dest = "Seleccionar"
            json_datos = json.dumps({"start":0,"tempMin":temp_min_past,"tempMax":temp_max_past,"flujoMin":flujo_min_past,"flujoMax":flujo_max_past,"tanque":noTanque})
            r.publish("start_UR",json_datos)
            time.sleep(0.1)
            r.publish("start_UP",json_datos)
            if CALM == "ON":
                json_datos = json.dumps({"start":0,"data":noTanque})
                r.publish("start_UEA",json_datos)
            del q.page['confPaste']
            del q.page['confPaste1']
            #del q.page['confPaste2']

            q.page['confPaste'] = ui.form_card(
                box=ui.box(zone='mid1_11_2', order=1),
                items=[
                    ui.text_xl('TEMPERATURA'),
                    ui.spinbox(name='tempmin', label='Temp Min: ', value = temp_min_past, min = 0, max = 120, disabled = False),
                    ui.spinbox(name='tempmax', label='Temp Max: ', value = temp_max_past, min = 0, max = 120, disabled = False),
                ],
            )

            q.page['confPaste1'] = ui.form_card(
                box=ui.box(zone='mid1_12_2', order=1),
                items=[
                    ui.text_xl('FLUJO'),
                    ui.spinbox(name='flujomin', label='Flujo Min: ', value = flujo_min_past, min = 0, max = 3000, disabled = False),
                    ui.spinbox(name='flujomax', label='Flujo Max: ', value = flujo_max_past, min = 0, max = 3000, disabled = False),
                ],
            )
            q.page['datestart'] = ui.small_stat_card(
                box=ui.box(zone='header_22', order=1),
                title='HORA DE INICIO',
                value=dateStart,
            )
            q.page['dateend'] = ui.small_stat_card(
                box=ui.box(zone='header_23', order=1),
                title='HORA FINAL',
                value=dateEnd,
            )
            data_to_run= getAll(r,"pasteur_to_run")

            if data_to_run["pasteur"]=="SI":
                dataInfoPasteur=1

            if data_to_run["pasteur"]=="NO":
                dataInfoPasteur=0

            #q.page['confPaste2'] = ui.form_card(
            #    box=ui.box(zone='mid1_13_2', order=1),
            #    items=[
            #        ui.text_xl('TANQUE DESTINO'),
            #        ui.combobox(name='tanques', label='', value=str(tanques_dest), choices=comboboxTanques, trigger=True, disabled = False),
            #    ],
            #)

            regAct(r,"conf_past", str("--"), str("--"), str("--"), str("--"), str("--"), str("--"))
            recover = getAll(r,"conf_past")


            await q.page.save()

    if q.args.finalize:
        q.user.inicio_val = inicio_val = False
        q.user.finalizar = finalizar = False
        if dateStart != "--":
            now = datetime.datetime.now()
            dateEnd = now.strftime("%Y-%m-%d %H:%M:%S")
            q.page['dateend'].value = str(dateEnd)

        json_datos = json.dumps({"start":0,"tempMin":temp_min_past,"tempMax":temp_max_past,"flujoMin":flujo_min_past,"flujoMax":flujo_max_past,"tanque":noTanque})
        r.publish("start_UR",json_datos)

        del q.page['confPaste']
        del q.page['confPaste1']
        #del q.page['confPaste2']

        q.page['confPaste'] = ui.form_card(
            box=ui.box(zone='mid1_11_2', order=1),
            items=[
                ui.text_xl('TEMPERATURA'),
                ui.spinbox(name='tempmin', label='Temp Min: ', value = temp_min_past, min = 0, max = 120, disabled = False),
                ui.spinbox(name='tempmax', label='Temp Max: ', value = temp_max_past, min = 0, max = 120, disabled = False),
            ],
        )

        q.page['confPaste1'] = ui.form_card(
            box=ui.box(zone='mid1_12_2', order=1),
            items=[
                ui.text_xl('FLUJO'),
                ui.spinbox(name='flujomin', label='Flujo Min: ', value = flujo_min_past, min = 0, max = 3000, disabled = False),
                ui.spinbox(name='flujomax', label='Flujo Max: ', value = flujo_max_past, min = 0, max = 3000, disabled = False),
            ],
        )



        #q.page['confPaste2'] = ui.form_card(
        #    box=ui.box(zone='mid1_13_2', order=1),
        #    items=[
        #        ui.text_xl('TANQUE DESTINO'),
        #        ui.combobox(name='tanques', label='', value=str(tanques_dest), choices=comboboxTanques, trigger=True, disabled = False),
        #    ],
        #)
        data_to_run= getAll(r,"pasteur_to_run")

        tanqName=" "
        if str(data_to_run["tanqueDest"])=="tanque1":
            tanqName="TANQUE 1"
        if str(data_to_run["tanqueDest"])=="tanque2":
            tanqName="TANQUE 2"
        if str(data_to_run["tanqueDest"])=="tanque3":
            tanqName="TANQUE 3"
        if str(data_to_run["tanqueDest"])=="tanque4":
            tanqName="TANQUE 4"

        fecha1=str(data_to_run["pesado"]).partition(",")[0]

        now = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        json_datos = json.dumps({
            "time":str(dt_string),"id":"PRO","area":"formulacion","operador":str("Prisma Lara"),'key': str(data_to_run["key"]),
            "proceso":str(data_to_run["marca"]),"producto":str(data_to_run["sabor"]),"almacen":str(tanqName),"formu":str(data_to_run["litosFormu"]),
            "timeBrix":data_to_run["datesPromBrix"],"start":str(data_to_run["start"]),"end":str(dateEnd),"fechaPesado":str(fecha1),
            "comments":str(data_to_run["comments"]),                        
        })
        print(str(json_datos))
        try:
            r.publish("PRO_end",json_datos)
        except Exception as e:
            print(e)

        print(str("Creando el registro..."))


        
        temp_min_past = 90
        temp_max_past = 100
        flujo_min_past = 1500
        flujo_max_past = 2000
        tanques_dest = "Seleccionar"
        dataInfoPasteur=0

        regAct(r,"conf_past", str("--"), str("--"), str("--"), str("--"), str("--"), str("--"))
        regRecPasteur(r,'pasteur_to_run',"--","--", "--","--", "--","--")
        recover = getAll(r,"conf_past")


        dateStart = "--"
        dateEnd = "--"

        q.page['datestart'] = ui.small_stat_card(
            box=ui.box(zone='header_22', order=1),
            title='HORA DE INICIO',
            value=dateStart,
        )
        
        q.page['dateend'] = ui.small_stat_card(
            box=ui.box(zone='header_23', order=1),
            title='HORA FINAL',
            value=dateEnd,
        )


        await q.page.save()

    if not q.client.initialized:
        q.client.initialized = True
        bandRef0 = 0
        q.page['meta'] = ui.meta_card(box='', layouts=[
            ui.layout(
                breakpoint='xs',
                #width='768px',
                zones=[
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                        ui.zone('header_2',align='center',size='15%',direction=ui.ZoneDirection.ROW,zones=[
                            ui.zone('header_21',align="center", size='34%', direction=ui.ZoneDirection.ROW),
                            ui.zone('header_22', size='14%'),
                            ui.zone('header_23', size='14%'),
                            ui.zone('header_25', size='14%'),
                            ui.zone('header_26', size='14%'),
                            ui.zone('header_24', align="center", size='10%')
                        ]),
                        ui.zone('body',size='85%',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='10%', zones=[
                                ui.zone('izq1_1_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_2_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_3_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_4_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_5_2', align="center",size='20%', direction=ui.ZoneDirection.ROW)
                            ]),
                            ui.zone('izq2', size='10%', zones=[
                                ui.zone('izq2_1_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq2_2_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq2_3_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq2_4_2', align="center",size='20%', direction=ui.ZoneDirection.ROW),
                                ui.zone('izq2_5_2', align="center",size='20%', direction=ui.ZoneDirection.ROW)
                            ]),
                            ui.zone('mid1',size='80%', zones=[
                                ui.zone('mid1_3',size='100%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid_11',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                                        ui.zone('mid1_1',size='25%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_11_2', align="center", size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_12_2', align="center", size='25%', direction=ui.ZoneDirection.ROW),
                                            #ui.zone('mid1_13_2', align="center", size='16.67%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_14_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_15_2',size='25%', direction=ui.ZoneDirection.ROW)
                                        ]),
                                        ui.zone('mid1_2',size='25%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_21_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_22_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_23_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_24_2',size='25%', direction=ui.ZoneDirection.ROW)
                                        ]),
                                        ui.zone('mid1_3',size='25%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_31_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_32_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_33_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_34_2',size='25%', direction=ui.ZoneDirection.ROW)
                                        ]),
                                        ui.zone('mid1_4',size='25%', direction=ui.ZoneDirection.ROW, zones=[
                                            ui.zone('mid1_41_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_42_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_43_2',size='25%', direction=ui.ZoneDirection.ROW),
                                            ui.zone('mid1_44_2',size='25%', direction=ui.ZoneDirection.ROW)
                                        ]),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')
###############    T   O  P     H  E  A  D  E  R    #################
        q.page['titulo'] = ui.section_card(
            box=ui.box('header_21',order=1),
            title=' ',
            subtitle=' ',
            items=[  
                ui.button(
                    name='recovery',
                    label='Recovery',
                    #caption=' ',
                    #width= '100px',
                    disabled = True,
                    primary=True,
                ),
                ui.separator(label=""),
                ui.button(
                    name='iniciar',
                    label='Start',
                    #caption=' ',
                    #width= '100px',
                    disabled = True,
                    primary=True,
                ),
                ui.separator(label=""),
                ui.button(
                    name='restart',
                    label='Reset',
                    #caption=' Finalizar ',
                    #width= '100px',
                    disabled = True,
                    primary=True,
                ),
                ui.separator(label=""),
                ui.button(
                    name='finalize',
                    label='End',
                    #caption=' Finalizar ',
                    #width= '100px',
                    disabled = True,
                    primary=True,
                ),
            ],
        )

        q.page['datestart'] = ui.small_stat_card(
            box=ui.box(zone='header_22', order=1),
            title='HORA DE INICIO',
            value=dateStart,
        )
        
        q.page['dateend'] = ui.small_stat_card(
            box=ui.box(zone='header_23', order=1),
            title='HORA FINAL',
            value=dateEnd,
        )


        q.page['dataProduct'] = ui.small_stat_card(
            box=ui.box(zone='header_25', order=1),
            title='Producto',
            value=dataInfo,
        )
        q.page['dataTanqueDest'] = ui.small_stat_card(
            box=ui.box(zone='header_26', order=1),
            title='Tanque Destino',
            value=dataInfoTanque,
        )



        content = '![Adrian](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        q.page['shannonImg'] = ui.markdown_card(
            box=ui.box('header_24',order = 1),
            title=' ',
            content= content,
        )

###############   L  E  F  T   S  I  D  E     A    #################
        q.page['states'] = ui.tall_stats_card(
            box=ui.box('izq1_1_2', order=1),
            items=[
                ui.stat(label='RETORNO TANQUE DE ESPERA', value = str(AV080)),
            ]
        )

        q.page['states3'] = ui.tall_stats_card(
            box=ui.box('izq1_2_2', order=1),
            items=[
                ui.stat(label='ENTRADA GLICOL', value=str(AV082)),
            ]
        )

        q.page['states5'] = ui.tall_stats_card(
            box=ui.box('izq1_3_2', order=1),
            items=[
                ui.stat(label='BOMBA DE AGUA CALIENTE', value=str(HW001)),
            ]
        )

        q.page['states7'] = ui.tall_stats_card(
            box=ui.box('izq1_4_2', order=1),
            items=[
                ui.stat(label='BOMBA DE AGUA FRIA', value=str(CW001)),
            ]
        )

        q.page['states9'] = ui.tall_stats_card(
            box=ui.box('izq1_5_2', order=1),
            items=[
                ui.stat(label='PASTEURIZACIÓN', value=str(Pasteur)),
            ]
        )
###############   L  E  F  T   S  I  D  E    B    #################
        q.page['states2'] = ui.tall_stats_card(
            box=ui.box('izq2_1_2', order=1),
            items=[
                ui.stat(label='SALIDA TANQUE DE ESPERA', value=str(AV081)),
            ]
        )

        q.page['states4'] = ui.tall_stats_card(
            box=ui.box('izq2_2_2', order=1),
            items=[
                ui.stat(label='BOMBA DE PRODUCTO', value=str(PP001)),
            ]
        )

        q.page['states6'] = ui.tall_stats_card(
            box=ui.box('izq2_3_2', order=1),
            items=[
                ui.stat(label='TORRE DE ENF.', value=str(FAN001)),
            ]
        )

        q.page['states8'] = ui.tall_stats_card(
            box=ui.box('izq2_4_2', order=1),
            items=[
                ui.stat(label='RECIRCULACIÓN', value=str(Recir)),
            ]
        )

        q.page['states10'] = ui.tall_stats_card(
            box=ui.box('izq2_5_2', order=1),
            items=[
                ui.stat(label='CIRCUITO DE ALM.', value=str(CALM)),
            ]
        )
###############   1ER   E  S  C  A  L  O  N    ################
        q.page['confPaste'] = ui.form_card(
            box=ui.box(zone='mid1_11_2', order=1),
            items=[
                ui.text_xl('TEMPERATURA'),
                ui.spinbox(name='tempmin', label='Temp Min: ', value = temp_min_past, min = 0, max = 120, disabled = False),
                ui.spinbox(name='tempmax', label='Temp Max: ', value = temp_max_past, min = 0, max = 120, disabled = False),
            ],
        )

        q.page['confPaste1'] = ui.form_card(
            box=ui.box(zone='mid1_12_2', order=1),
            items=[
                ui.text_xl('FLUJO'),
                ui.spinbox(name='flujomin', label='Flujo Min: ', value = flujo_min_past, min = 0, max = 3000, disabled = False),
                ui.spinbox(name='flujomax', label='Flujo Max: ', value = flujo_max_past, min = 0, max = 3000, disabled = False),
            ],
        )

        #q.page['confPaste2'] = ui.form_card(
        #    box=ui.box(zone='mid1_13_2', order=1),
        #    items=[
        #        ui.text_xl('TANQUE DESTINO'),
        #        ui.combobox(name='tanques', label='', value=str(tanques_dest), choices=comboboxTanques, trigger=True, disabled = False),
        #    ],
        #)

        q.page['niveluht'] = ui.tall_series_stat_card(
            box=ui.box('mid1_14_2', order=1),
            title='NIVEL UHT (L)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=niveluht),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$cyan',
            plot_data=data('foo qux', 15, rows=niveluht_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['flujouht'] = ui.tall_series_stat_card(
            box=ui.box('mid1_15_2', order=1),
            title='FLUJO (l/h)',
            value='={{intl qux minimum_fraction_digits=2 maximum_fraction_digits=2}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=flujouht),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$red',
            plot_data=data('foo qux', 15, rows=flujouht_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )
###############   2DO   E  S  C  A  L  O  N    #################
        q.page['sostenimiento_in'] = ui.tall_series_stat_card(
            box=ui.box('mid1_21_2', order=1),
            title='ENTRADA SOSTENIMIENTO (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=sostenimiento_in),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$orange',
            plot_data=data('foo qux', 15, rows=sostenimiento_in_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['enfriamiento'] = ui.tall_series_stat_card(
            box=ui.box('mid1_22_2', order=1),
            title='ENFRIAMIENTO 1 (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=enfriamiento),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$blue',
            plot_data=data('foo qux', 15, rows=enfriamiento_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['aguacaliente'] = ui.tall_series_stat_card(
            box=ui.box('mid1_23_2', order=1),
            title='AGUA CALIENTE (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=aguacaliente),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$cyan',
            plot_data=data('foo qux', 15, rows=aguacaliente_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['salidaproducto'] = ui.tall_series_stat_card(
            box=ui.box('mid1_24_2', order=1),
            title='SALIDA PRODUCTO (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=salidaproducto),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$red',
            plot_data=data('foo qux', 15, rows=salidaproducto_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )
###############   3ER   E  S  C  A  L  O  N    #################
        q.page['sostenimiento_out'] = ui.tall_series_stat_card(
            box=ui.box('mid1_31_2', order=1),
            title='SALIDA SOSTENIMIENTO (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=sostenimiento_out),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$orange',
            plot_data=data('foo qux', 15, rows=sostenimiento_out_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['entrada_glicol'] = ui.tall_series_stat_card(
            box=ui.box('mid1_32_2', order=1),
            title='ENTRADA GLICOL (°C)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=1}}',
            data=dict(qux=entrada_glicol),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$blue',
            plot_data=data('foo qux', 15, rows=entrada_glicol_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['brixlinea'] = ui.tall_series_stat_card(
            box=ui.box('mid1_33_2', order=1),
            title='BRIX LINEA (°Brix)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=2}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=2}}',
            data=dict(qux=brixlinea),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$cyan',
            plot_data=data('foo qux', 15, rows=brixlinea_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['gas'] = ui.tall_series_stat_card(
            box=ui.box('mid1_34_2', order=1),
            title='GAS (L)',
            value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            data=dict(qux=gas),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$red',
            plot_data=data('foo qux', 15, rows=gas_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )
###############   4TO   E  S  C  A  L  O  N    #################
        q.page['tanque1'] = ui.tall_series_stat_card(
            box=ui.box('mid1_41_2', order=1),
            title='TANQUE 1 (L)',
            value='={{intl qux minimum_fraction_digits=1 maximum_fraction_digits=2}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=2}}',
            data=dict(qux=brixlinea),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$cyan',
            plot_data=data('foo qux', 15, rows=brixlinea_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['tanque2'] = ui.tall_series_stat_card(
            box=ui.box('mid1_42_2', order=1),
            title='TANQUE 2 (L)',
            value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            data=dict(qux=tanque2),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$red',
            plot_data=data('foo qux', 15, rows=tanque2_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['tanque3'] = ui.tall_series_stat_card(
            box=ui.box('mid1_43_2', order=1),
            title='TANQUE 3 (L)',
            value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            data=dict(qux=tanque3),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$orange',
            plot_data=data('foo qux', 15, rows=tanque3_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        q.page['tanque4'] = ui.tall_series_stat_card(
            box=ui.box('mid1_44_2', order=1),
            title='TANQUE 4 (L)',
            value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            data=dict(qux=tanque4),
            plot_type='area',
            plot_category='foo',
            plot_value='qux',
            plot_color='$blue',
            plot_data=data('foo qux', 15, rows=tanque4_rows),
            plot_zero_value=0,
            plot_curve='linear',
        )

        await q.page.save()
        await q.run(refresh,q)

@app('/pasteur', mode = 'broadcast')
async def serve4(q: Q):
    route = q.args['#']
    await pasteurizacion(q)