from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common4 import *
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis
import csv

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

async def addList(q: Q, reg: int):
    global data_rows

    del q.page['upldCSV']
    del q.page['combotextboxes']
    del q.page['lista-ing-show']
    del q.page['menuBtns']
    
    q.page['table'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
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
    if reg == 0:
        q.page['menuBtns'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnRegis', label='Registro', disabled = False, primary=True),
                ui.button(name='btnCSV', label='CSV File', disabled = False, primary=True)
            ],
        )
    if reg == 1:
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textciudad', label='Ciudad', value='Seleccionar', choices=comboboxEst,trigger=True),
                ui.combobox(name='textmuni', label='Municipio', value='Seleccionar', choices=[],trigger=True),
                ui.textbox(name='textloca', label='Localidad',trigger=True),
                ui.textbox(name='textref', label='Referencia',trigger=True),
                ui.textbox(name='textdepen', label='Dependencia',trigger=True),
                ui.combobox(name='textdispo', label='Dispositivo', value='Seleccionar', choices=comboboxDisp,trigger=True),
                ui.combobox(name='textequipo', label='Equipo', value='Seleccionar', choices=comboboxEquipo,trigger=True),
                ui.combobox(name='texttecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.textbox(name='textip', label='IP',trigger=True),
                ui.textbox(name='textlat', label='Latitud',trigger=True),
                ui.textbox(name='textlong', label='Longitud',trigger=True),
                ui.textbox(name='textid', label='Count',trigger=True),
                ui.combobox(name='textlvl', label='Level', value='Seleccionar', choices=comboboxLvl,trigger=True),
                ui.combobox(name='textconnect', label='Conected To', value='Seleccionar', choices=comboboxMuniCol,trigger=True),
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )

    await q.page.save()

async def showList(q: Q):
    global data_rows, count
    del q.page['table']

    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            multiple = True,
            columns=columns,
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

async def devices(q: Q):
    print(str("starting addDevices..."))
    global ipGlobal,session
    global data_rows, data_rows_keycount
    global comboboxMuniCol, comboboxMuniMich, comboboxMuniJal, comboboxEst, comboboxMuni, comboboxDisp, comboboxEquipo
    global afiliciacion, ciudad, municipio, localidad, referencia, dependencia, equipo, tecnologia
    global dispositivo, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo, host

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

    if q.args.textciudad and ciudad != str(q.args.textciudad):
        val = ' '
        if str(q.args.textciudad) == 'COLIMA':
            comboboxMuni = comboboxMuniCol
            val = 'ARMERÍA'
        if str(q.args.textciudad) == 'MICHOACAN':
            comboboxMuni = comboboxMuniMich
            val = 'ACATIC'
        if str(q.args.textciudad) == 'JALISCO':
            comboboxMuni = comboboxMuniJal
            val = 'ACUITZIO'

        municipio = val
        ciudad = str(q.args.textciudad)
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textciudad', label='Ciudad', value=str(q.args.textciudad), choices=comboboxEst,trigger=True),
                ui.combobox(name='textmuni', label='Municipio', value=str(val), choices=comboboxMuni,trigger=True),
                ui.textbox(name='textloca', label='Localidad', value = '',trigger=True),
                ui.textbox(name='textref', label='Referencia', value = '',trigger=True),
                ui.textbox(name='textdependencia', label='Dependencia', value = '',trigger=True),
                ui.combobox(name='textdispo', label='Dispositivo', value='Seleccionar', choices=comboboxDisp,trigger=True),
                ui.combobox(name='textequipo', label='Equipo', value='Seleccionar', choices=comboboxEquipo,trigger=True),
                ui.combobox(name='texttecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.textbox(name='textip', label='IP', value = '',trigger=True),
                ui.textbox(name='textlat', label='Latitud', value = '',trigger=True),
                ui.textbox(name='textlong', label='Longitud', value = '',trigger=True),
                ui.textbox(name='textid', label='Count',trigger=True),
                ui.combobox(name='textlvl', label='Level', value='Seleccionar', choices=comboboxLvl,trigger=True),
                ui.combobox(name='textconnect', label='Conected To', value='Seleccionar', choices=comboboxMuni,trigger=True),
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )

        await q.page.save()

    if q.args.textmuni:
        if q.args.textmuni != 'Seleccionar':
            municipio = str(q.args.textmuni)
        await q.page.save()

    if q.args.textloca:
        localidad=str(q.args.textloca)
        await q.page.save()

    if q.args.textref:
        referencia=str(q.args.textref)
        await q.page.save()

    if q.args.textdependencia:
        dependencia=str(q.args.textdependencia)
        await q.page.save()

    if q.args.textdispo and dispositivo != str(q.args.textdispo):
        val2 = ' '
        if str(q.args.textdispo) == 'AP':
            comboboxEquipo = comboboxAPTP
            val2 = comboboxAPTP[0]
        if str(q.args.textdispo) == 'PTP':
            comboboxEquipo = comboboxAPTP
            val2 = comboboxAPTP[0]
        if str(q.args.textdispo) == 'SWITCH':
            comboboxEquipo = comboboxSWITCHS
            val2 = comboboxSWITCHS[0]
        if str(q.args.textdispo) == 'ROUTER':
            comboboxEquipo = comboboxROUTERS
            val2 = comboboxROUTERS[0]
        if str(q.args.textdispo) == 'OLT':
            comboboxEquipo = comboboxOLTS
            val2 = comboboxOLTS[0]
        if str(q.args.textdispo) == 'ONU':
            comboboxEquipo = comboboxONU
            val2 = comboboxONU[0]

        equipo = str(val2)
        dispositivo = str(q.args.textdispo)

        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textciudad', label='Ciudad', value=ciudad, choices=comboboxEst,trigger=True),
                ui.combobox(name='textmuni', label='Municipio', value=municipio, choices=comboboxMuni,trigger=True),
                ui.textbox(name='textloca', label='Localidad', value = localidad,trigger=True),
                ui.textbox(name='textref', label='Referencia', value = referencia,trigger=True),
                ui.textbox(name='textdependencia', label='Dependencia', value = dependencia,trigger=True),
                ui.combobox(name='textdispo', label='Dispositivo', value=dispositivo, choices=comboboxDisp,trigger=True),
                ui.combobox(name='textequipo', label='Equipo', value=equipo, choices=comboboxEquipo,trigger=True),
                ui.combobox(name='texttecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.textbox(name='textip', label='IP', value = '',trigger=True),
                ui.textbox(name='textlat', label='Latitud', value = '',trigger=True),
                ui.textbox(name='textlong', label='Longitud', value = '',trigger=True),
                ui.textbox(name='textid', label='Count',trigger=True),
                ui.combobox(name='textlvl', label='Level', value='Seleccionar', choices=comboboxLvl,trigger=True),
                ui.combobox(name='textconnect', label='Conected To', value='Seleccionar', choices=comboboxMuni,trigger=True),
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )

        await q.page.save()

    if q.args.textequipo:
        if q.args.textequipo != 'Seleccionar':
            equipo = str(q.args.textequipo)
        await q.page.save()

    if q.args.texttecno:
        if q.args.texttecno != 'Seleccionar':
            tecnologia = str(q.args.texttecno)
        await q.page.save()

    if q.args.textip:
        ipDevice=str(q.args.textip)
        await q.page.save()

    if q.args.textlat:
        latitud=str(q.args.textlat)
        await q.page.save()

    if q.args.textlong:
        longitud=str(q.args.textlong)
        await q.page.save()

    if q.args.textid:
        ID_Count=str(q.args.textid)
        await q.page.save()

    if q.args.textlvl:
        if q.args.textlvl != 'Seleccionar':
            ID_Lvl = str(q.args.textlvl)
        await q.page.save()

    if q.args.textconnect:
        if q.args.textconnect != 'Seleccionar':
            conectedTo = str(q.args.textconnect)
        await q.page.save()

    if q.args.btnGetDevs:
        devices = []
        devices = getAll(r, 'infraYI')

        if devices != 'NO':
            if devices['data'] != '[]':
                devices = devices['data'].replace("'","[")
                data_rows = json.loads(devices)

                q.page['boton2'].items[0].button.disabled = False
                q.page['boton2'].items[1].button.disabled = False
                q.page['boton2'].items[2].button.disabled = False

        await q.run(showList,q)
        await q.page.save()

    if q.args.addMod:
        if ciudad != "Seleccionar":
            if municipio != "Seleccionar":
                if localidad != '':
                    if referencia != '':
                        if dependencia != '':
                            if equipo != '':
                                if dispositivo != '':
                                    if tecnologia != '':
                                        if ipDevice != '':
                                            if latitud != '':
                                                if longitud != '':
                                                    if ID_Count != '':
                                                        if ID_Count != '':
                                                            if conectedTo != '':
                                                                afiliciacion = ciudad[:4]+"01-"+tecnologia[:4]+'-'+municipio[:4]+'-'+equipo[:4]+str("%03d" % int(ID_Count))
                                                                host = str("%03d" % int(ID_Count))+'-'+ciudad[:4]+'01-'+dependencia+'-'+tecnologia[:4]+'-'+equipo+'-'+referencia+'-'+municipio[:4]+'-'+str("%03d" % int(ID_Count))
                                                                data_rows.append([afiliciacion, ciudad, municipio, localidad, referencia, dependencia, dispositivo, equipo, tecnologia, ipDevice, latitud, longitud, str("%03d" % int(ID_Count)), ID_Lvl,conectedTo, host])
                                                                await q.run(addList, q, 1)
        q.page['boton2'].items[0].button.disabled = False
        q.page['boton2'].items[1].button.disabled = False
        q.page['boton2'].items[2].button.disabled = False
        await q.page.save()

    if q.args.btnRegis:
        del q.page['menuBtns']
        del q.page['upldCSV']
        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textciudad', label='Ciudad', value='Seleccionar', choices=comboboxEst,trigger=True),
                ui.combobox(name='textmuni', label='Municipio', value='Seleccionar', choices=[],trigger=True),
                ui.textbox(name='textloca', label='Localidad',trigger=True),
                ui.textbox(name='textref', label='Referencia',trigger=True),
                ui.textbox(name='textdependencia', label='Dependencia',trigger=True),
                ui.combobox(name='textdispo', label='Dispositivo', value='Seleccionar', choices=comboboxDisp,trigger=True),
                ui.combobox(name='textequipo', label='Equipo', value='Seleccionar', choices=comboboxEquipo,trigger=True),
                ui.combobox(name='texttecno', label='Tecnología', value='Seleccionar', choices=comboboxTecno,trigger=True),
                ui.textbox(name='textip', label='IP',trigger=True),
                ui.textbox(name='textlat', label='Latitud',trigger=True),
                ui.textbox(name='textlong', label='Longitud',trigger=True),
                ui.textbox(name='textid', label='Count',trigger=True),
                ui.combobox(name='textlvl', label='Level', value='Seleccionar', choices=comboboxLvl,trigger=True),
                ui.combobox(name='textconnect', label='Conected To', value='Seleccionar', choices=comboboxMuniCol,trigger=True),
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )

        q.page['btnCSV2'] = ui.section_card(
            box=ui.box('der1_12', order=1),
            title='',
            subtitle='',
            items=[
               ui.button(name='btnCSV', label='CSV File', disabled = False, primary=True,)
            ],
        )
        await q.page.save()

    if q.args.btnCSV:
        del q.page['combotextboxes']
        del q.page['btnCSV2']
        del q.page['menuBtns']
        q.page['upldCSV'] = ui.section_card(
                box=ui.box('der1_11', order=1),
                title='',
                subtitle='',
                items=[
                ui.button(name='btnRegis', label='Registro', disabled = False, primary=True,),
                ui.file_upload(name='file_upload',label='Upload!',multiple=True,file_extensions=['csv'],max_file_size=10,max_size=15)
            ]
        )
        await q.page.save()

    if q.args.file_upload:
        count = 0
        data_rows = []
        # Since multiple file uploads are allowed, the file_upload argument is a list.
        for path in q.args.file_upload:
            # To use the file uploaded from the browser to the wave server, download it into the app.
            local_path = await q.site.download(path, '../../data/')
            with open(local_path) as csvfile:
                reader = csv.reader(csvfile) # change contents to floats
                for row in reader: # each row is a list
                    count += 1
                    if count > 1:
                        afiliciacion = row[0][:4]+"01-"+row[7][:4]+'-'+row[2][:4]+'-'+row[6][:4]+str("%03d" % int(row[11]))
                        host = str("%03d" % int(row[11]))+'-'+row[0][:4]+'01-'+row[4]+'-'+row[7][:4]+'-'+row[6]+'-'+row[3]+'-'+row[1][:4]+'-'+str("%03d" % int(row[11]))
                        data_rows.append([afiliciacion, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], str("%03d" % int(row[11])), row[12], row[13], host])
        q.page['boton2'].items[0].button.disabled = True
        q.page['boton2'].items[1].button.disabled = False
        q.page['boton2'].items[2].button.disabled = False
        await q.run(addList, q, 0)
        await q.page.save()

    if q.args.btnEdit:
        del q.page['menuBtns']
        eliminados = q.args.issues
        if len(eliminados) == 1:
            data_rows_temp, data_rows_send, found = [], [], 0
            for y in data_rows:
                for x in eliminados:
                    if str(y[0])==str(x):
                        found=1
                        # si quieres quitar los que seleccionaste
                        data_rows_send.append(y)
                if found==0:
                    #pass
                    # si quieres quitar los que no seleccionaste
                    data_rows_temp.append(y)
                found=0

        data_rows = data_rows_temp
        afiliciacion = data_rows_send[0][0]
        ciudad = data_rows_send[0][1]
        municipio = data_rows_send[0][2]
        localidad = data_rows_send[0][3]
        referencia = data_rows_send[0][4]
        dependencia = data_rows_send[0][5]
        dispositivo = data_rows_send[0][6]
        equipo = data_rows_send[0][7]
        tecnologia = data_rows_send[0][8]
        ipDevice = data_rows_send[0][9]
        latitud = data_rows_send[0][10]
        longitud = data_rows_send[0][11]
        ID_Count = data_rows_send[0][12]
        ID_Lvl = data_rows_send[0][13]
        conectedTo = data_rows_send[0][14]
        host = data_rows_send[0][15]

        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='textciudad', label='Ciudad', value=ciudad, choices=comboboxEst,trigger=True),
                ui.combobox(name='textmuni', label='Municipio', value=municipio, choices=[],trigger=True),
                ui.textbox(name='textloca', label='Localidad', value=localidad,trigger=True),
                ui.textbox(name='textref', label='Referencia', value=referencia,trigger=True),
                ui.textbox(name='textdependencia', label='Dependencia', value=dependencia,trigger=True),
                ui.combobox(name='textdispo', label='Dispositivo', value=dispositivo, choices=comboboxDisp,trigger=True),
                ui.combobox(name='textequipo', label='Equipo', value=equipo, choices=comboboxEquipo,trigger=True),
                ui.combobox(name='texttecno', label='Tecnología', value=tecnologia, choices=comboboxTecno,trigger=True),
                ui.textbox(name='textip', label='IP', value = ipDevice, trigger=True),
                ui.textbox(name='textlat', label='Latitud', value = latitud,trigger=True),
                ui.textbox(name='textlong', label='Longitud', value = longitud,trigger=True),
                ui.textbox(name='textid', label='Count', value = ID_Count,trigger=True),
                ui.combobox(name='textlvl', label='Level', value=ID_Lvl, choices=comboboxLvl,trigger=True),
                ui.combobox(name='textconnect', label='Conected To', value=conectedTo, choices=comboboxMuniCol,trigger=True),
                ui.button(name='addMod',label='Editar',disabled = False,primary=True,)
            ],
        )

        q.page['btnCSV2'] = ui.section_card(
            box=ui.box('der1_12', order=1),
            title='',
            subtitle='',
            items=[
               ui.button(name='btnCSV', label='CSV File', disabled = False, primary=True,)
            ],
        )
        await q.run(showList,q)
        await q.page.save()

    if q.args.btnSave:
        msg = []
        data_rows_save = []
        devices = getAll(r, 'infraYI')
        if devices != 'NO':
            if devices['data'] != '[]':
                msg = devices['data'].replace("'","[")
                data_rows_save = json.loads(msg)
                guardados = q.args.issues
                data_rows_temp,found=[],0
                for y in data_rows_save:
                    for x in guardados:
                        if str(y[0])==str(x):
                            found=1
                            #data_rows_temp.append(y)
                    if found==0:
                        data_rows_temp.append(y)
                    found=0
                for z in range(0, len(data_rows_temp)):
                    data_rows_save.append([data_rows_temp[z][0], data_rows_temp[z][1], data_rows_temp[z][2], data_rows_temp[z][3], data_rows_temp[z][4], data_rows_temp[z][5], data_rows_temp[z][6], data_rows_temp[z][7], data_rows_temp[z][8], data_rows_temp[z][9], data_rows_temp[z][10], data_rows_temp[z][11], str("%03d" % int(data_rows_temp[z][12])), data_rows_temp[z][13], data_rows_temp[z][14], data_rows_temp[z][15]])
                infraYI(r, 'infraYI', data_rows_save)
                data_rows = []
                ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo, tecnologia, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo = '','','','','','','','','','','','','',''
        if devices['data'] == '[]' or devices == 'NO':
            infraYI(r, 'infraYI', data_rows)
            data_rows = []
            ciudad, municipio, localidad, referencia, dependencia, equipo, dispositivo, tecnologia, ipDevice, latitud, longitud, ID_Count, ID_Lvl, conectedTo = '','','','','','','','','','','','','',''
        await q.run(addList, q, 0)
        await q.page.save()

    if q.args.btnDelete:
        print(str("delete..."))
        eliminados =q.args.issues
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
        infraYI(r, 'infraYI', data_rows)

        await q.run(showList,q)
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
                        ui.zone('body',size='93',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('izq1', size='8%', zones=[
                                ui.zone('izq1_11',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                                ui.zone('izq1_12',size='14%',align='center'),
                                ui.zone('izq1_13',size='14%',align='center'),
                                ui.zone('izq1_14',size= '14%',align='center'),
                                ui.zone('izq1_15',size= '14%',align='center'),
                                ui.zone('izq1_16',size= '14%',align='center'),
                                ui.zone('footer1',size= '15%',align='center')
                            ]),
                            ui.zone('der1',size='92%', zones=[
                                ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                    ui.zone('der1_1', size='40%', direction=ui.ZoneDirection.COLUMN, zones=[
                                            ui.zone('der1_11', size='90%', align='center', direction=ui.ZoneDirection.COLUMN),
                                            ui.zone('der1_12', size='20%', align='center', direction=ui.ZoneDirection.COLUMN),
                                    ]),
                                    ui.zone('der1_2',size='60%', zones=[
                                        ui.zone('der1_21', size='90%', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_22', size='10%', align='center', direction=ui.ZoneDirection.ROW),
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

        #########   Cassia Home   #########
        q.page['boton3'] = ui.section_card(
            box=ui.box('izq1_15', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnGetDevs', label='Get Devices', disabled = False, primary=True,)
            ],
        )

        q.page['menuBtns'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnRegis', label='Registro', disabled = False, primary=True),
                ui.button(name='btnCSV', label='CSV File', disabled = False, primary=True)
            ],
        )

        q.page['boton2'] = ui.section_card(
            box=ui.box('der1_22', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnEdit',label='Edit',disabled = True,primary=True,),
                ui.button(name='btnDelete',label='Delete',disabled = True,primary=True,),
                ui.button(name='btnSave',label='Save',disabled = True,primary=True,)
            ],
        )

        await q.run(showList,q)
        await q.page.save()

@app('/devices', mode = 'unicast')
async def team1(q: Q):
    route = q.args['#']
    await devices(q)