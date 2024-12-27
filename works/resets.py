from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import sys
import random
import pandas as pd
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from common3 import *
import csv

async def addList(q: Q, list: ings, array: nombings):
    global nombings, columns3
    
    del q.page['lista-ing-show']

    columns3 = []
    await q.page.save()
    #for x in range(0,int(len(nombings))):
    #    columns3.append(ui.table_column(name='text'+str(x), label=str(nombings[x]), sortable=True, searchable=True, max_width='120'))

    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            columns=columns,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in ings],
            #values = ['0'],
            groupable=True,
            downloadable=True
        )
    ])

    await q.page.save()

async def showList(q: Q):
    global data_rows, count

    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
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

async def resets(q: Q):
    print(str("starting pesado..."))
    global ipGlobal
    global data_rows, data_rows_keycount
    global resetMuni, resetTipo, resetAfi, resetID, resetIMEI, resetTel, resetSIM, resetSerie

    q.page['meta'] = ui.meta_card(box='')

    if q.args.textcomment1:
        resetAfi=str(q.args.textcomment1)

        await q.page.save()

    if q.args.textcomment2:
        resetID=str(q.args.textcomment2)

        await q.page.save()

    if q.args.textcomment3:
        resetIMEI=str(q.args.textcomment3)

        await q.page.save()

    if q.args.textcomment4:
        resetTel=str(q.args.textcomment4)

        await q.page.save()

    if q.args.textcomment5:
        resetSIM=str(q.args.textcomment5)

        await q.page.save()

    if q.args.textcomment6:
        resetSerie=str(q.args.textcomment6)
        
        await q.page.save()

    if q.args.comboboxmuni:
        resetMuni = str(q.args.comboboxmuni)

        await q.page.save()

    if q.args.comboboxtipo:
        resetTipo = str(q.args.comboboxtipo)

        await q.page.save()

    if q.args.btnActualizar:
        if len(data_rows) == 0:
            count = 0
            with open("/home/seguritech/ws/Documents/resets-colima.csv") as csvfile:
                reader = csv.reader(csvfile) # change contents to floats
                for row in reader: # each row is a list
                    count += 1
                    if count > 1:
                        data_rows.append(row)

        await q.run(showList,q)

    if q.args.addMod:
        if resetMuni != "Seleccionar":
            if resetTipo != "Seleccionar":
                if resetAfi != '':
                    if resetID != '':
                        if resetIMEI != '':
                            if resetTel != '':
                                if resetSIM != '':
                                    if resetSerie != '':
                                        data_rows.append([resetMuni,resetTipo,resetAfi,resetID,resetIMEI,resetTel,resetSIM,resetSerie])
        await q.run(addList,q)
        await q.page.save()

    if q.args.btnEnviar:
        selectioned = q.args.issues
        found = 0
        for y in data_rows:
            for x in selectioned:
                if str(y[0])==str(x):
                    found=1
                    selectioned = y
            if found==0:    
                pass
            found=0

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
                    ui.zone('header',size='0%'),
                    ui.zone('body',size='100%',direction=ui.ZoneDirection.ROW, zones=[
                        ui.zone('izq1', size='14%', zones=[
                            ui.zone('izq1_1',size='15%',align='center',direction=ui.ZoneDirection.ROW),
                            ui.zone('izq1_2',size='14%'),
                            ui.zone('izq1_3',size='14%'),
                            ui.zone('izq1_4',size= '14%'),
                            ui.zone('izq1_5',size= '14%'),
                            ui.zone('izq1_6',size= '14%'),
                            ui.zone('footer1',size= '15%')
                        ]),
                        ui.zone('der1',size='86%', zones=[
                            ui.zone('right_11',size='100%',direction=ui.ZoneDirection.COLUMN, zones=[
                                ui.zone('der1_1', size='20%', direction=ui.ZoneDirection.COLUMN, zones=[
                                        ui.zone('der1_11', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_12', direction=ui.ZoneDirection.COLUMN),
                                        ui.zone('der1_13', direction=ui.ZoneDirection.COLUMN)
                                ]),
                                ui.zone('der1_2',size='60%', zones=[
                                    ui.zone('der1_21', size='100%', direction=ui.ZoneDirection.ROW),
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
        ], theme='one-dark-prosolarized')

        q.page['combotextboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmuni', label='Municipio', value='Seleccionar', choices=comboboxMuni,trigger=True),
                ui.combobox(name='comboboxtipo', label='Tipo', value='Seleccionar', choices=comboboxTipo,trigger=True),
                ui.textbox(name='textcomment1', label='Afiliciación',trigger=True),
                ui.textbox(name='textcomment2', label='ID-reset',trigger=True),
                ui.textbox(name='textcomment3', label='IMEI',trigger=True),
                ui.textbox(name='textcomment4', label='Teléfono',trigger=True),
                ui.textbox(name='textcomment5', label='SIM',trigger=True),
                ui.textbox(name='textcomment6', label='No. Serie',trigger=True),
            ],
        )

        q.page['boton1'] = ui.section_card(
            box=ui.box('der1_11', order=2),
            title='',
            subtitle='',
            items=[
                ui.button(name='addMod',label='Agregar',disabled = False,primary=True,)
            ],
        )

        q.page['boton2'] = ui.section_card(
            box=ui.box('der1_31', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnEnviar',label='Enviar',disabled = False,primary=True,)
            ],
        )

        q.page['boton3'] = ui.section_card(
            box=ui.box('izq1_2', order=1),
            title='',
            subtitle='',
            items=[
                ui.button(name='btnActualizar',label='Actualizar',disabled = False,primary=True,)
            ],
        )

        content = '![Adrian](http://'+ipGlobal+':10101/datasets/SeguriTech.png)'
        q.page['shannonImg'] = ui.markdown_card(
            box='izq1_1',
            title='Version 1.0 (c) 2022 Development by ',
            content= content,
        )
        await q.run(showList,q)
        await q.page.save()

@app('/reset', mode = 'broadcast')
async def team1(q: Q):
    route = q.args['#']
    await resets(q)