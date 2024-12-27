from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import threading,json,time,datetime,math
import redis
from redis import StrictRedis, ConnectionError
import sys
import random
# adding Folder to the system path
sys.path.insert(0, '/home/wave/libs')
from common1 import *

async def addList(q: Q, list: ings, array: nombings):
    global nombings, columns3
    
    del q.page['lista-ing-show']

    columns3 = []
    await q.page.save()
    for x in range(0,int(len(nombings))):
        columns3.append(ui.table_column(name='text'+str(x), label=str(nombings[x]), sortable=True, searchable=True, max_width='120'))

    q.page['lista-ing'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            columns=columns3,
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
    data = []
    columns4 = [
        ui.table_column(name='text', label='', sortable=True, searchable=True, max_width='1400')
    ]

    q.page['lista-ing-show'] = ui.form_card(box=ui.box('der1_21', order=1), items=[
        ui.table(
            name='issues',
            columns=columns4,
            rows=[ui.table_row(
                name=str(dato[0]),
                cells=dato,
            )for dato in data],
            #values = ['0'],
            groupable=True,
            downloadable=True,
        )
    ])

    await q.page.save()

def calcularOCA(nf1:nflavorOca1, nf2:nflavorOca2):
    global cafeina, stevia, acidocitrico, agave, tapioca, flavorOca1, flavorOca2, goma, agua, batches, tanques, ings, nombings,cajas,batchesD, batchesS
    global cafeinaTotal, steviaTotal, acidocitricoTotal, agaveTotal, tapiocaTotal, flavorOca1Total, flavorOca2Total, gomaTotal, aguaTotal,nflavorOca1,nflavorOca2

    ings=[]
    nombings=[]
    batchesD = 0
    batchesS = 0
    if cajas == None:
        cajas = 0
    if int(cajas) > 0:
        cafeinaTotal = truncate(float((cafeina*int(cajas)/633)),3)
        steviaTotal = truncate(float((stevia*int(cajas)/633)),3)
        acidocitricoTotal = truncate(float((acidocitrico*int(cajas)/633)),3)
        agaveTotal = truncate(float((agave*int(cajas)/633)),3)
        tapiocaTotal = truncate(float((tapioca*int(cajas)/633)),3)
        flavorOca1Total = truncate(float((flavorOca1*int(cajas)/633)),3)
        flavorOca2Total = truncate(float((flavorOca2*int(cajas)/633)),3)
        gomaTotal = truncate(float((goma*int(cajas)/633)),3)
        aguaTotal = truncate(float((agua*int(cajas)/633)),3)
        sumaIngs = (cafeinaTotal+steviaTotal+acidocitricoTotal+agaveTotal+tapiocaTotal+flavorOca1Total+flavorOca2Total+aguaTotal)
        batches = round(sumaIngs/2100,0)
        if batches==0:
            batches = 1
        if batches == 1:
            batchesS = 1
            cafeinaxBatch = truncate(cafeinaTotal/batches,3)
            steviaxBatch = truncate(steviaTotal/batches,3)
            acidocitricoxBatch = truncate(acidocitricoTotal/batches,3)
            agavexBatch = truncate(agaveTotal/batches,3)
            tapiocaxBatch = truncate(tapiocaTotal/batches,3)
            flavorOca1xBatch= truncate(flavorOca1Total/batches,3)
            flavorOca2xBatch = truncate(flavorOca2Total/batches,3)
            gomaxBatch = truncate(gomaTotal/batches,3)
            aguaxBatchS = truncate(2100-(cafeinaxBatch+steviaxBatch+acidocitricoxBatch+agavexBatch+tapiocaxBatch+flavorOca1xBatch+flavorOca2xBatch),3)
            ings.append([str(batchesS),str("Simple"),str(cafeinaxBatch),str(steviaxBatch),str(acidocitricoxBatch),str(agavexBatch),str(tapiocaxBatch),str(flavorOca1xBatch),str(flavorOca2xBatch),str(gomaxBatch),str(aguaxBatchS)])
            nombings = ["No. de batchs","Tipo","Cafeina", "Stevia", "Acido Citrico", "Agave", "Tapioca", str(nf1), str(nf2), "Goma Arabiga", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(cafeinaTotal),str(steviaTotal),str(acidocitricoTotal),str(agaveTotal),str(tapiocaTotal),str(flavorOca1Total),str(flavorOca2Total),str(gomaTotal),str(aguaTotal)])
        if batches >= 2:
            batchesD = math.floor(batches/2)
            if (batchesD*2) == batches:
                batchesS = 0
            else:
                batchesS = 1
            cafeinaxBatch = truncate(cafeinaTotal/batches,3)
            steviaxBatch = truncate(steviaTotal/batches,3)
            acidocitricoxBatch = truncate(acidocitricoTotal/batches,3)
            agavexBatch = truncate(agaveTotal/batches,3)
            tapiocaxBatch = truncate(tapiocaTotal/batches,3)
            flavorOca1xBatch= truncate(flavorOca1Total/batches,3)
            flavorOca2xBatch = truncate(flavorOca2Total/batches,3)
            gomaxBatch = truncate(gomaTotal/batches,3)
            aguaxBatchS = truncate(2100-(cafeinaxBatch+steviaxBatch+acidocitricoxBatch+agavexBatch+tapiocaxBatch+flavorOca1xBatch+flavorOca2xBatch),3)
            ings.append([str(batchesS),str("Simple"),str(cafeinaxBatch),str(steviaxBatch),str(acidocitricoxBatch),str(agavexBatch),str(tapiocaxBatch),str(flavorOca1xBatch),str(flavorOca2xBatch),str(gomaxBatch),str(aguaxBatchS)])
            aguaxBatchD = truncate(2100-((cafeinaxBatch+steviaxBatch+acidocitricoxBatch+agavexBatch+tapiocaxBatch+flavorOca1xBatch+flavorOca2xBatch)*2),3)
            ings.append([str(batchesD),str("Dobles"),str(cafeinaxBatch*2),str(steviaxBatch*2),str(acidocitricoxBatch*2),str(agavexBatch*2),str(tapiocaxBatch*2),str(flavorOca1xBatch*2),str(flavorOca2xBatch*2),str(gomaxBatch*2),str(aguaxBatchD)])
            nombings = ["No. de batchs","Tipo","Cafeina", "Stevia", "Acido Citrico", "Agave", "Tapioca", str(nf1), str(nf2), "Goma Arabiga", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(cafeinaTotal),str(steviaTotal),str(acidocitricoTotal),str(agaveTotal),str(tapiocaTotal),str(flavorOca1Total),str(flavorOca2Total),str(gomaTotal),str(aguaTotal)])
        return batches, batchesS, batchesD, sumaIngs, ings, nombings

def calcularTepache():
    global tepache, stevia1, acidocitrico1, allulosa, inulina, probioticos, agua, flavorTep1, flavorTep2, flavorTep3, flavorTep4, batches, tanques, ings, nombings,cajas
    global tepacheTotal, stevia1Total, acidocitrico1Total, allulosaTotal, inulinaTotal, probioticosTotal, aguaTotal, flavorTep1Total, flavorTep2Total,flavorTep3Total, flavorTep4Total
    global combosabor
    ings=[]
    nombings=[]
    
    if cajas == None:
        cajas = 0
    if int(cajas) > 0:
        cajas = (cajas*4.26)/1000
        tepacheTotal = truncate(float(tepache*cajas),3)
        stevia1Total = truncate(float(stevia1*cajas),3)
        acidocitrico1Total = truncate(float(acidocitrico1*cajas),3)
        allulosaTotal = truncate(float(allulosa*cajas),3)
        inulinaTotal = truncate(float(inulina*cajas),3)
        probioticosTotal = truncate(float(probioticos*cajas),3)
        flavorTep1Total = truncate(float(flavorTep1*cajas),3)
        flavorTep2Total = truncate(float(flavorTep2*cajas),3)
        flavorTep3Total = truncate(float(flavorTep3*cajas),3)
        flavorTep4Total = truncate(float(flavorTep4*cajas),3)
        aguaTotal = truncate(float(agua*cajas),3)
        sumaIngs = (tepacheTotal+stevia1Total+acidocitrico1Total+allulosaTotal+inulinaTotal+flavorTep1Total+flavorTep2Total+flavorTep3Total+flavorTep4Total+aguaTotal)
        batches = round(((sumaIngs/2100)/2),0)
        if batches==0:
            batches = 1
        tepachexBatch=truncate(float(tepacheTotal/batches),3)
        stevia1xBatch=truncate(float(stevia1Total/batches),3)
        acidocitrico1xBatch=truncate(float(acidocitrico1Total/batches),3)
        allulosaxBatch=truncate(float(allulosaTotal/batches),3)
        inulinaxBatch=truncate(float(inulinaTotal/batches),3)
        probioticosxBatch=truncate(float(probioticosTotal/batches),3)
        flavorTep1xBatch=truncate(float(flavorTep1Total/batches),3)
        flavorTep2xBatch=truncate(float(flavorTep2Total/batches),3)
        flavorTep3xBatch=truncate(float(flavorTep3Total/batches),3)
        flavorTep4xBatch=truncate(float(flavorTep4Total/batches),3)
        sumaIngs_A = (tepachexBatch+stevia1xBatch+acidocitrico1xBatch+allulosaxBatch+inulinaxBatch+flavorTep1xBatch+flavorTep2xBatch+flavorTep3xBatch+flavorTep4xBatch)
        aguaxBatch = truncate((2100-sumaIngs_A),3)
        if combosabor == "STRAWBERRY HIBISCUS":
            ings.append([str(int(batches)),str("Simple"),str(tepachexBatch),str(stevia1xBatch),str(acidocitrico1xBatch),str(allulosaxBatch),str(inulinaxBatch),str(probioticosxBatch),str(flavorTep1xBatch),str(flavorTep2xBatch),str(flavorTep3xBatch),str(flavorTep4xBatch),str(aguaxBatch)])
            nombings = ["No. de batchs","Tipo","Tepache", "Stevia", "Acido Citrico", "Allulosa", "Inulina", "Probioticos", "Pineapple Flavor PP","Hibiscus Extract", "Hibiscus Berry Flavor", "Strawberry Flavor", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(tepacheTotal),str(stevia1Total),str(acidocitrico1Total),str(allulosaTotal),str(inulinaTotal),str(probioticosTotal),str(flavorTep1Total),str(flavorTep2Total),str(flavorTep3Total),str(flavorTep4Total),str(aguaTotal)])
        if combosabor == "MANGO MANDARIN":
            ings.append([str(int(batches)),str("Simple"),str(tepachexBatch),str(stevia1xBatch),str(acidocitrico1xBatch),str(allulosaxBatch),str(inulinaxBatch),str(probioticosxBatch),str(flavorTep1xBatch),str(flavorTep2xBatch),str(flavorTep3xBatch),str(aguaxBatch)])
            nombings = ["No. de batchs","Tipo","Tepache", "Stevia", "Acido Citrico", "Allulosa", "Inulina", "Probioticos", "Pineapple Flavor PP", "Mango JP Flavor", "Citrus Flavor", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(tepacheTotal),str(stevia1Total),str(acidocitrico1Total),str(allulosaTotal),str(inulinaTotal),str(probioticosTotal),str(flavorTep1Total),str(flavorTep2Total),str(flavorTep3Total),str(aguaTotal)])
        if combosabor == "PRICKLY PEAR":
            ings.append([str(int(batches)),str("Simple"),str(tepachexBatch),str(stevia1xBatch),str(acidocitrico1xBatch),str(allulosaxBatch),str(inulinaxBatch),str(probioticosxBatch),str(flavorTep1xBatch),str(flavorTep2xBatch),str(flavorTep3xBatch),str(flavorTep4xBatch),str(aguaxBatch)])
            nombings = ["No. de batchs","Tipo","Tepache", "Stevia", "Acido Citrico", "Allulosa", "Inulina", "Probioticos", "Pineapple Flavor PP", "Peach Flavor", "Lime Flavor", "Prickly Pear Flavor", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(tepacheTotal),str(stevia1Total),str(acidocitrico1Total),str(allulosaTotal),str(inulinaTotal),str(probioticosTotal),str(flavorTep1Total),str(flavorTep2Total),str(flavorTep3Total),str(flavorTep4Total),str(aguaTotal)])
        if combosabor == "PIÑA":
            ings.append([str(int(batches)),str("Simple"),str(tepachexBatch),str(stevia1xBatch),str(acidocitrico1xBatch),str(allulosaxBatch),str(inulinaxBatch),str(probioticosxBatch),str(flavorTep1xBatch),str(flavorTep2xBatch),str(aguaxBatch)])
            nombings = ["No. de batchs","Tipo","Tepache", "Stevia", "Acido Citrico", "Allulosa", "Inulina", "Probioticos", "Pineapple Flavor PP","Pineapple Flavor Bell", "Agua Osmotica"] 
            ings.append([str(int(batches)),str("TOTAL"),str(tepacheTotal),str(stevia1Total),str(acidocitrico1Total),str(allulosaTotal),str(inulinaTotal),str(probioticosTotal),str(flavorTep1Total),str(flavorTep2Total),str(aguaTotal)])
        concTotal = batches*2100
        aguaExtra = ((sumaIngs-concTotal)*0.4)
        concTotal1 = concTotal+aguaExtra
        return batches, sumaIngs, ings, nombings, concTotal, aguaExtra, concTotal1

def calcularSalutaris(flavor: nFlavorSal):
    global azucar, sucralosa, benzoato, citrato, acidocitrico2, alcohol, flavorSal1, agua, batches, tanques, ings, nombings,cajas
    global azucarTotal, sucralosaTotal, benzoatoTotal, citratoTotal, acidocitrico2Total, alcoholTotal, flavorSal1Total, aguaTotal, nFlavorSal

    ings=[]
    nombings=[]
    
    if cajas == None:
        cajas = 0
    if int(cajas) > 0:
        cajas = (cajas*4.26)/1000
        azucarTotal = truncate(float(azucar*cajas),3)
        sucralosaTotal = truncate(float(sucralosa*cajas),3)
        benzoatoTotal = truncate(float(benzoato*cajas),3)
        citratoTotal = truncate(float(citrato*cajas),3)
        acidocitrico2Total = truncate(float(acidocitrico2*cajas),3)
        alcoholTotal = truncate(float(alcohol*cajas),3)
        flavorSal1Total = truncate(float(flavorSal1*cajas),3)
        aguaTotal = truncate(float(agua*cajas),3)

        sumaIngs = (azucarTotal+sucralosaTotal+benzoatoTotal+citratoTotal+acidocitrico2Total+aguaTotal)
        batches = round(((sumaIngs/2100)/2),0)
        if batches==0:
            batches = 1
        azucarxBatch=truncate(float(azucarTotal/batches),3)
        sucralosaxBatch=truncate(float(sucralosaTotal/batches),3)
        benzoatoxBatch=truncate(float(benzoatoTotal/batches),3)
        citratoxBatch=truncate(float(citratoTotal/batches),3)
        acidocitrico2xBatch=truncate(float(acidocitrico2Total/batches),3)
        alcoholxBatch=truncate(float(alcoholTotal/batches),3)
        flavorSal1xBatch=truncate(float(flavorSal1Total/batches),3)
        sumaIngs_A = (azucarTotal+sucralosaTotal+benzoatoTotal+citratoTotal+acidocitrico2Total)
        aguaxBatch = truncate((2100-sumaIngs_A),3)
        ings.append([str(int(batches)),str("Simple"),str(azucarxBatch),str(sucralosaxBatch),str(benzoatoxBatch),str(citratoxBatch),str(acidocitrico2xBatch),str(alcoholxBatch),str(flavorSal1xBatch),str(aguaxBatch)])
        nombings = ["No. de batchs","Tipo","Azucar", "Sucralosa", "Benzoato de sodio", "Citrato de Sodio", "Acido Citrico", "Alcohol", flavor, "Agua Osmotica"] 
        ings.append([str(int(batches)),str("TOTAL"),str(azucarTotal),str(sucralosaTotal),str(benzoatoTotal),str(citratoTotal),str(acidocitrico2Total),str(alcoholTotal),str(flavorSal1Total),str(aguaTotal)])
        concTotal = batches*2100
        aguaExtra = ((sumaIngs-concTotal)*0.4)
        concTotal1 = concTotal+aguaExtra
        return batches, sumaIngs, ings, nombings, concTotal, aguaExtra, concTotal1

async def calculator(q: Q):
    print(str("starting pesado..."))
    global r,ipGlobal
    global nobatchs,notanques, listIngs
    global comboboxMarcas,comboboxSabor_OCA,comboboxSabor_TEPACHE,comboboxSabor_SALUTARIS,comboboxSabor_PUNTA,combomarca,combosabor,comboboxSabor
    global cafeina, stevia, acidocitrico, agave, tapioca, flavorOca1, flavorOca2, goma, agua, batches, tanques, ings, nombings,cajas
    global cafeinaTotal, steviaTotal, acidocitricoTotal, agaveTotal, tapiocaTotal, flavorOca1Total, flavorOca2Total, gomaTotal, aguaTotal

    global tepache, stevia1, acidocitrico1, allulosa, inulina, probioticos, agua, flavorTep1, flavorTep2, flavorTep3, flavorTep4, batches, tanques, ings, nombings,cajas, batchesS
    global tepacheTotal, stevia1Total, acidocitrico1Total, allulosaTotal, inulinaTotal, probioticosTotal, aguaTotal, flavorTep1Total, flavorTep2Total,flavorTep3Total, flavorTep4Total, nflavorTep1, nflavorTep2, nflavorTep3, nflavorTep4

    global azucar, sucralosa, benzoato, citrato, acidocitrico2, alcohol, flavorSal1, agua, batches, tanques, ings, nombings,cajas
    global azucarTotal, sucralosaTotal, benzoatoTotal, citratoTotal, acidocitrico2Total, alcoholTotal, flavorSal1Total, aguaTotal, nFlavorSal

    q.page['meta'] = ui.meta_card(box='')

    if q.args.comboboxsabor:
        combosabor=str(q.args.comboboxsabor)
        ######   V A R I A B L E S   F I J A S  O  C  A   ######
        cafeina = 1.030
        stevia = 0.278
        acidocitrico = 6.399
        agave = 64.860
        tapioca = 67.218
        goma = 16.702
        ######   V A R I A B L E S   F I J A S  T  E  P  A  C  H  E   ######
        tepache = 306.208
        stevia1 = 0.245
        acidocitrico1 = 0.868
        allulosa = 25.517
        ######   V A R I A B L E S   F I J A S  S  A  L  U  T  A  R  I  S   ######
        sucralosa = 0.1254
        benzoato = 0.252
        citrato = 0.071
        acidocitrico2 = 5.34
        ######## O  C  A  ########
        if combosabor == "BERRY ACAI":
            flavorOca1 = 3.368
            flavorOca2 = 12.025
            agua = 1955
        if combosabor == "GUAVA":
            flavorOca1 = 9.743
            flavorOca2 = 8.899
            agua = 1941
        if combosabor == "MANGO":
            flavorOca1 = 5.567
            flavorOca2 = 3.396
            agua = 1951
        if combosabor == "PRICKLY PEAR":
            flavorOca1 = 7.794
            flavorOca2 = 3.897
            agua = 1949
        ######## T  E  P  A  C  H  E  ########
        if combosabor == "STRAWBERRY HIBISCUS":
            inulina = 20.414
            probioticos = 0.227
            agua = 662.969
            flavorTep1 = 0.306
            flavorTep2 = 2.000
            flavorTep3 = 1.225
            flavorTep4 = 0.714
        if combosabor == "MANGO MANDARIN":
            inulina = 20.414
            probioticos = 0.227
            agua = 664.373
            flavorTep1 = 0.612
            flavorTep2 = 1.378
            flavorTep3 = 0.851
            flavorTep4 = 0.000
        if combosabor == "PRICKLY PEAR":
            inulina = 20.3144
            probioticos = 0.227
            agua = 633.08
            flavorTep1 = 0.817
            flavorTep2 = 0.204
            flavorTep3 = 0.561
            flavorTep4 = 2.552
        if combosabor == "PIÑA":
            inulina = 20.413
            probioticos = 0.1133
            agua = 633.218
            flavorTep1 = 2.0413
            flavorTep2 = 2.0413
        ######## T  E  P  A  C  H  E  ########
        if combosabor == "TORONJA":
            azucar = 10.549
            agua = 955.093
            flavorSal1 = 2.096
            alcohol = 34.056
        if combosabor == "PIÑA COLADA":
            azucar = 9.9584
            agua = 956.6601
            flavorSal1 = 0.9669
            alcohol = 33.8153
        if combosabor == "LIMONADA HIERBABUENA":
            azucar = 9.9542
            agua = 957.0370
            flavorSal1 = 0.6698
            alcohol = 33.817
        await q.page.save()

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

        combosabor=val
        combomarca=str(q.args.comboboxmarca)

        q.page['comboboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value=str(q.args.comboboxmarca), choices=comboboxMarcas1,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value=str(val), choices=comboboxSabor,trigger=True),
                ui.spinbox(name='cajas', label='No de cajas a formular: : ', value=3144, disabled = False, max=10000, min=0),
            ],
        )
        await q.page.save()          

    if q.args.addIng:
        if combomarca != "seleccionar" and combosabor != "seleccionar":
            cajas = q.args.cajas
            #######     O   C   A   #######
            if combosabor == "BERRY ACAI":
                listIngs = calcularOCA("Raspberry Flavor", "Acai Flavor")
                if listIngs != None:
                    if listIngs[3] == 0:
                        tanques = 0
                    if listIngs[3] <= 16000:
                        tanques = 1
                    if listIngs[3] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[3],2))
            if combosabor == "GUAVA":
                listIngs = calcularOCA("Guava Flavor", "Passion Fruit Flavor")
                if listIngs != None:
                    if listIngs[3] == 0:
                        tanques = 0
                    if listIngs[3] <= 16000:
                        tanques = 1
                    if listIngs[3] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[3],2))
            if combosabor == "MANGO":
                listIngs = calcularOCA("Mango JP Flavor", "Mango 05 Flavor")
                if listIngs != None:
                    if listIngs[3] == 0:
                        tanques = 0
                    if listIngs[3] <= 16000:
                        tanques = 1
                    if listIngs[3] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[3],2))
            if combosabor == "PRICKLY PEAR":
                listIngs = calcularOCA("Prickly Pear Flavor", "Lime Flavor")
                if listIngs != None:
                    if listIngs[3] == 0:
                        tanques = 0
                    if listIngs[3] <= 16000:
                        tanques = 1
                    if listIngs[3] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[3],2))
            #######     T  E  P  A  C  H  E   #######
            if combosabor == "STRAWBERRY HIBISCUS":
                listIngs = calcularTepache()
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            if combosabor == "MANGO MANDARIN":
                listIngs = calcularTepache()
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            if combosabor == "PRICKLY PEAR":
                listIngs = calcularTepache()
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            if combosabor == "PIÑA":
                listIngs = calcularTepache()
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            #######     S  A  L  U  T  A  R  I  S   #######
            if combosabor == "TORONJA":
                listIngs = calcularSalutaris("Toronja Flavor")
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            if combosabor == "PIÑA COLADA":
                listIngs = calcularSalutaris("Piña Colada Flavor")
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            if combosabor == "LIMONADA HIERBABUENA":
                listIngs = calcularSalutaris("Mojito Flavor")
                if listIngs != None:
                    if listIngs[6] == 0:
                        tanques = 0
                    if listIngs[6] <= 16000:
                        tanques = 1
                    if listIngs[6] > 16000:
                        tanques = 2
                    q.page['noBebida'].value = float(truncate(listIngs[4],2))
            #######     P   D   #######
            if combosabor == "MUSANITA BANANO":
                listIngs = calcularPD()
            if combosabor == "MUSANITA FRAMBUESA":
                listIngs = calcularPD()
            if combosabor == "MUSANITA MANGO":
                listIngs = calcularPD()
            if combosabor == "MUSANITA HIGO":
                listIngs = calcularPD()
            if combosabor == "CANTARITO TORONJA":
                listIngs = calcularPD()
            if combosabor == "CANTARITO MANGO":
                listIngs = calcularPD()
            if combosabor == "CANTARITO PIÑA":
                listIngs = calcularPD()
            if combosabor == "AGUA COCO":
                listIngs = calcularPD()
            
            if listIngs != None:
                q.page['noBatches'].value = int(listIngs[0])
                q.page['noTanques'].value = int(tanques)
                
            if combomarca == "OCA":
                if listIngs != None:
                    del q.page['aguaExtra']
                    del q.page['totalConc']
                    del q.page['totalPT']
                    await q.run(addList, q, listIngs[4], listIngs[5])
    
            if combomarca == "TEPACHE":
                if listIngs != None:
                    q.page['aguaExtra'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=1),
                        title='AGUA EXTRA',
                        value=f'{listIngs[5]:.0f}',
                    )
                    q.page['totalConc'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=2),
                        title='TOTAL CONCENTRADO + AGUA',
                        value=f'{listIngs[6]:.2f}',
                    )
                    q.page['totalPT'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=3),
                        title='TOTAL PRODUCTO TERMINADO',
                        value=f'{listIngs[1]:.2f}',
                    )
                    await q.run(addList, q, listIngs[2], listIngs[3])
            if combomarca == "SALUTARIS":
                if listIngs != None:
                    q.page['aguaExtra'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=1),
                        title='AGUA EXTRA',
                        value=f'{listIngs[5]:.0f}',
                    )
                    q.page['totalConc'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=2),
                        title='TOTAL CONCENTRADO + AGUA',
                        value=f'{listIngs[6]:.2f}',
                    )
                    q.page['totalPT'] = ui.small_stat_card(
                        box=ui.box('der1_22', order=3),
                        title='TOTAL PRODUCTO TERMINADO',
                        value=f'{listIngs[1]:.2f}',
                    )
                    await q.run(addList, q, listIngs[2], listIngs[3])
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
                                ui.zone('der1_1', size='20%', direction=ui.ZoneDirection.ROW, zones=[
                                        ui.zone('der1_11', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_12', direction=ui.ZoneDirection.ROW),
                                        ui.zone('der1_13', direction=ui.ZoneDirection.ROW)
                                ]),
                                ui.zone('der1_2',size='60%', zones=[
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
            title='Calculador',
            subtitle='Equipo de Formulación',
            items=[
            ],
        )

        q.page['comboboxes'] = ui.section_card(
            box=ui.box('der1_11', order=1),
            title='',
            subtitle='',
            items=[
                ui.combobox(name='comboboxmarca', label='Marca', value='seleccionar', choices=comboboxMarcas1,trigger=True),
                ui.combobox(name='comboboxsabor', label='Sabor', value='seleccionar', choices=comboboxSabor,trigger=True),
                ui.spinbox(name='cajas', label='No de cajas a formular: : ', value=3144, disabled = False, max=10000, min=0),
            ],
        )

        q.page['noBatches'] = ui.small_stat_card(
            box=ui.box('der1_12', order=1),
            title='NO. DE BATCHS',
            value=f'{nobatchs}',
        )
        
        q.page['noTanques'] = ui.small_stat_card(
            box=ui.box('der1_12', order=2),
            title='NO. DE TANQUES',
            value=f'{notanques}',
        )

        q.page['noBebida'] = ui.small_stat_card(
            box=ui.box('der1_13', order=1),
            title='CONCENTRADO(lt)',
            value=f'{nobebida:.2f}',
        )

        q.page['basculaa'] = ui.section_card(
            box=ui.box('der1_13', order=2),
            title='',
            subtitle='',
            items=[
                ui.button(
                    name='addIng',
                    label='Calculate',
                    #caption=' ',
                    #width= '100px',
                    disabled = False,
                    primary=True,
                ),
            ],
        )

        content = '![Adrian](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        #content = '![Joel](http://'+ipGlobal+':10101/data/ShannonWeaver.png)'
        q.page['shannonImg'] = ui.markdown_card(
            box='izq1_1',
            title='Version 1.0 (c) 2022 Development by ',
            content= content,
        )

        await q.page.save()
        await q.run(showList,q)

@app('/calculator', mode = 'broadcast')
async def team1(q: Q):
    route = q.args['#']
    await calculator(q)