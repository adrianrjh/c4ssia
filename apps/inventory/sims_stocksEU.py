from h2o_wave import main, app, ui, data, Q, AsyncSite
import time
import random
import redis,datetime
import asyncio
from redis import StrictRedis, ConnectionError
import json, threading
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from common9 import *
# adding Folder to the system path
sys.path.insert(0, '/home/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

async def refresh(q: Q):
    global device0, device1, device2, device3, device4, device5, device6, device7, device8, device9
    global device10, device11, device12, device13, device14, device15, device16, device17, device18, device19
    global device20, device21, device22, device23, device24, device25, device26, device27, device28, device29
    global device30, device31, device32, device33, device34, device35, device36, device37, device38, device39
    global device40, device41, device42, device43, device44, device45, device46, device47, device48, device49
    global device50, device51, device52, device53, device54, device55, device56, device57, device58
    
    try:
        while 1:
            #counter_article = rts.get('DSP7001-16')
            #device0 = counter_article[1]
            #if len(device0_rows)>=1000:
            #    device0_rows.pop(0)
            #device0_rows.append([len(device0_rows), device0])
            #q.page['device0'].data.qux = device0 
            await q.page.save()
            await q.sleep(1)
    except asyncio.CancelledError:
        print("La tarea 'refresh' fue cancelada")
        return

async def start_or_restart_refresh(q: Q):
    global current_refresh_task

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

async def sims_stocksEU(q: Q):
    print("starting sims_stocksEU")

    global inicio_val, dateStart, dateEnd, r, session, ipGlobal
    global device0, device1, device2, device3, device4, device5, device6, device7, device8, device9
    global device10, device11, device12, device13, device14, device15, device16, device17, device18, device19
    global device20, device21, device22, device23, device24, device25, device26, device27, device28, device29
    global device30, device31, device32, device33, device34, device35, device36, device37, device38, device39
    global device40, device41, device42, device43, device44, device45, device46, device47, device48, device49
    global device50, device51, device52, device53, device54, device55, device56, device57, device58

    if q.args.btnAtras:
        q.page['meta'].redirect = 'http://'+ipGlobal+':10101/home_sims'
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
                    ui.zone('left1_11',size='100%',direction=ui.ZoneDirection.ROW,zones=[
                        ui.zone('body',size='100%',direction=ui.ZoneDirection.ROW, zones=[
                            ui.zone('mid_1',size='100%',direction=ui.ZoneDirection.COLUMN,zones=[
                                ui.zone('mid1_1',size='10%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_10',size='10%', align='start', direction=ui.ZoneDirection.COLUMN),
                                    ui.zone('mid1_11',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_12',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_13',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_14',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_15',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_16',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_17',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_18',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_19',size='10%', align='center', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('mid1_2',size='20%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_20',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_21',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_22',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_23',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_24',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_25',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_26',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_27',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_28',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_29',size='10%', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('mid1_3',size='20%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_30',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_31',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_32',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_33',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_34',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_35',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_36',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_37',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_38',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_39',size='10%', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('mid1_4',size='20%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_40',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_41',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_42',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_43',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_44',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_45',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_46',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_47',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_48',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_49',size='10%', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('mid1_5',size='20%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_50',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_51',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_52',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_53',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_54',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_55',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_56',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_57',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_58',size='10%', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_59',size='10%', direction=ui.ZoneDirection.ROW),
                                ]),
                                ui.zone('mid1_6',size='10%', direction=ui.ZoneDirection.ROW, zones=[
                                    ui.zone('mid1_60',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_61',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_62',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_63',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_64',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_65',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_66',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_67',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_68',size='10%', align='center', direction=ui.ZoneDirection.ROW),
                                    ui.zone('mid1_69',size='10%', align='center', direction=ui.ZoneDirection.ROW)
                                ]),
                            ]),
                        ]),
                    ]),
                ],
            ),
        ], theme='winter-is-coming')

###############   1ER   E  S  C  A  L  O  N    ################
        q.page['btnAtras'] = ui.section_card(box=ui.box('mid1_10', order=1),title='',subtitle='',items=[ui.button(name='btnAtras', label='Atrás', disabled = False, primary=True)])  

        q.page['device0'] = ui.tall_series_stat_card(
            box=ui.box('mid1_11', order=1),title='device0',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device0),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device0_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device1'] = ui.tall_series_stat_card(
            box=ui.box('mid1_12', order=1),title='device1',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device1),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device1_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device2'] = ui.tall_series_stat_card(
            box=ui.box('mid1_13', order=1),title='device2',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device2),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device2_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device3'] = ui.tall_series_stat_card(
            box=ui.box('mid1_14', order=1),title='device3',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device3),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device3_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device4'] = ui.tall_series_stat_card(
            box=ui.box('mid1_15', order=1),title='device4',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device4),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device4_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device5'] = ui.tall_series_stat_card(
            box=ui.box('mid1_16', order=1),title='device5',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device5),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device5_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device6'] = ui.tall_series_stat_card(
            box=ui.box('mid1_17', order=1),title='device6',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device6),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device6_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device7'] = ui.tall_series_stat_card(
            box=ui.box('mid1_18', order=1),title='device7',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device7),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device7_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device8'] = ui.tall_series_stat_card(
            box=ui.box('mid1_19', order=1),title='device8',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device8),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$cyan',plot_data=data('foo qux', 15, rows=device8_rows),
            plot_zero_value=0,plot_curve='linear')
###############   2DO   E  S  C  A  L  O  N    #################
        q.page['device9'] = ui.tall_series_stat_card(
            box=ui.box('mid1_20', order=1),title='device9',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device9),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device9_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device10'] = ui.tall_series_stat_card(
            box=ui.box('mid1_21', order=1),title='device10',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device10),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device10_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device11'] = ui.tall_series_stat_card(
            box=ui.box('mid1_22', order=1),title='device11',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device11),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device11_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device12'] = ui.tall_series_stat_card(
            box=ui.box('mid1_23', order=1),title='device12',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device12),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device12_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device13'] = ui.tall_series_stat_card(
            box=ui.box('mid1_24', order=1),title='device13',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device13),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device13_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device14'] = ui.tall_series_stat_card(
            box=ui.box('mid1_25', order=1),title='device14',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device14),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device14_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device15'] = ui.tall_series_stat_card(
            box=ui.box('mid1_26', order=1),title='device15',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device15),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device15_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device16'] = ui.tall_series_stat_card(
            box=ui.box('mid1_27', order=1),title='device16',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device16),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device16_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device17'] = ui.tall_series_stat_card(
            box=ui.box('mid1_28', order=1),title='device17',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device17),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device17_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device18'] = ui.tall_series_stat_card(
            box=ui.box('mid1_29', order=1),title='device18',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device18),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$orange',plot_data=data('foo qux', 15, rows=device18_rows),
            plot_zero_value=0,plot_curve='linear')
###############   3ER   E  S  C  A  L  O  N    #################
        q.page['device19'] = ui.tall_series_stat_card(
            box=ui.box('mid1_30', order=1),title='device19',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device19),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device19_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device20'] = ui.tall_series_stat_card(
            box=ui.box('mid1_31', order=1),title='device20',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device20),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device20_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device21'] = ui.tall_series_stat_card(
            box=ui.box('mid1_32', order=1),title='device21',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device21),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device21_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device22'] = ui.tall_series_stat_card(
            box=ui.box('mid1_33', order=1),title='device22',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device22),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device22_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device23'] = ui.tall_series_stat_card(
            box=ui.box('mid1_34', order=1),title='device23',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device23),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device23_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device24'] = ui.tall_series_stat_card(
            box=ui.box('mid1_35', order=1),title='device24',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device24),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device24_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device25'] = ui.tall_series_stat_card(
            box=ui.box('mid1_36', order=1),title='device25',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device25),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device25_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device26'] = ui.tall_series_stat_card(
            box=ui.box('mid1_37', order=1),title='device26',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device26),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device26_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device27'] = ui.tall_series_stat_card(
            box=ui.box('mid1_38', order=1),title='device27',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device27),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device27_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device28'] = ui.tall_series_stat_card(
            box=ui.box('mid1_39', order=1),title='device28',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device28),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$red',plot_data=data('foo qux', 15, rows=device28_rows),
            plot_zero_value=0,plot_curve='linear')
###############   4TO   E  S  C  A  L  O  N    #################
        q.page['device29'] = ui.tall_series_stat_card(
            box=ui.box('mid1_40', order=1),title='device29',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device29),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device29_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device30'] = ui.tall_series_stat_card(
            box=ui.box('mid1_41', order=1),title='device30',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device30),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device30_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device31'] = ui.tall_series_stat_card(
            box=ui.box('mid1_42', order=1),title='device31',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device31),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device31_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device32'] = ui.tall_series_stat_card(
            box=ui.box('mid1_43', order=1),title='device32',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device32),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device32_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device33'] = ui.tall_series_stat_card(
            box=ui.box('mid1_44', order=1),title='device33',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device33),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device33_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device34'] = ui.tall_series_stat_card(
            box=ui.box('mid1_45', order=1),title='device34',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device34),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device34_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device35'] = ui.tall_series_stat_card(
            box=ui.box('mid1_46', order=1),title='device35',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device35),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device35_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device36'] = ui.tall_series_stat_card(
            box=ui.box('mid1_47', order=1),title='device36',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device36),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device36_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device37'] = ui.tall_series_stat_card(
            box=ui.box('mid1_48', order=1),title='device37',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device37),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device37_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device38'] = ui.tall_series_stat_card(
            box=ui.box('mid1_49', order=1),title='device38',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device38),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$blue',plot_data=data('foo qux', 15, rows=device38_rows),
            plot_zero_value=0,plot_curve='linear')

###############   5TO   E  S  C  A  L  O  N    #################
        q.page['device39'] = ui.tall_series_stat_card(
            box=ui.box('mid1_50', order=1),title='device39',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device39),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device39_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device40'] = ui.tall_series_stat_card(
            box=ui.box('mid1_51', order=1),title='device40',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device40),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device40_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device41'] = ui.tall_series_stat_card(
            box=ui.box('mid1_52', order=1),title='device41',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device41),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device41_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device42'] = ui.tall_series_stat_card(
            box=ui.box('mid1_53', order=1),title='device42',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device42),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device42_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device43'] = ui.tall_series_stat_card(
            box=ui.box('mid1_54', order=1),title='device43',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device43),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device43_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device44'] = ui.tall_series_stat_card(
            box=ui.box('mid1_55', order=1),title='device44',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device44),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device44_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device45'] = ui.tall_series_stat_card(
            box=ui.box('mid1_56', order=1),title='device45',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device45),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device45_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device46'] = ui.tall_series_stat_card(
            box=ui.box('mid1_57', order=1),title='device46',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device46),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device46_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device47'] = ui.tall_series_stat_card(
            box=ui.box('mid1_58', order=1),title='device47',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device47),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device47_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device48'] = ui.tall_series_stat_card(
            box=ui.box('mid1_59', order=1),title='device48',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device48),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device48_rows),
            plot_zero_value=0,plot_curve='linear')

###############   6TO  E  S  C  A  L  O  N    #################
        q.page['device49'] = ui.tall_series_stat_card(
            box=ui.box('mid1_60', order=1),title='device49',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device49),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device49_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device50'] = ui.tall_series_stat_card(
            box=ui.box('mid1_61', order=1),title='device50',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device50),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device50_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device51'] = ui.tall_series_stat_card(
            box=ui.box('mid1_62', order=1),title='device51',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device51),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device51_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device52'] = ui.tall_series_stat_card(
            box=ui.box('mid1_63', order=1),title='device52',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device52),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device52_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device53'] = ui.tall_series_stat_card(
            box=ui.box('mid1_64', order=1),title='device53',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device53),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device53_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device54'] = ui.tall_series_stat_card(
            box=ui.box('mid1_65', order=1),title='device54',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=1 maximum_fraction_digits=0}}',data=dict(qux=device54),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device54_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device55'] = ui.tall_series_stat_card(
            box=ui.box('mid1_66', order=1),title='device55',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device55),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device55_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device56'] = ui.tall_series_stat_card(
            box=ui.box('mid1_67', order=1),title='device56',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device56),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device56_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device57'] = ui.tall_series_stat_card(
            box=ui.box('mid1_68', order=1),title='device57',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device57),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device57_rows),
            plot_zero_value=0,plot_curve='linear')

        q.page['device58'] = ui.tall_series_stat_card(
            box=ui.box('mid1_69', order=1),title='device58',value='={{intl qux minimum_fraction_digits=0 maximum_fraction_digits=0}}',
            aux_value='={{intl quux style="percent" minimum_fraction_digits=0 maximum_fraction_digits=0}}',data=dict(qux=device58),
            plot_type='area',plot_category='foo',plot_value='qux',plot_color='$green',plot_data=data('foo qux', 15, rows=device58_rows),
            plot_zero_value=0,plot_curve='linear')

        await q.page.save()
        await q.run(start_or_restart_refresh,q)

@app('/sims_stocksEU', mode = 'broadcast')
async def serve4(q: Q):
    route = q.args['#']
    await sims_stocksEU(q)
