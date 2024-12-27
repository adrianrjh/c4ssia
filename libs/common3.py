import json 
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

# Create columns for our issue table.
columns = [
    ui.table_column(name='delete', label='No.', sortable=True, searchable=True, max_width='50'),
    ui.table_column(name='text',  label='Municipio', sortable=True, searchable=True, max_width='100'),
    ui.table_column(name='text1', label='Tipo', sortable=True, searchable=True, max_width='80'),
    ui.table_column(name='text2', label='Afiliciación', sortable=True, searchable=True, max_width='170'),
    ui.table_column(name='text3', label='ID Reset', sortable=True, searchable=True, max_width='140'),
    ui.table_column(name='text4', label='IMEI', sortable=True, searchable=True, max_width='150'),
    ui.table_column(name='text5', label='Teléfono', sortable=True, searchable=True, max_width='100'),
    ui.table_column(name='text6', label='SIM', sortable=True, searchable=True, max_width='200'),
    ui.table_column(name='text7', label='No. Serie', sortable=True, searchable=True, max_width='240')
]

comboboxMuni = ['ARMERÍA', 'COLIMA', 'COMALA', 'COQUIMATLÁN', 'CUAUHTÉMOC', 'IXTLAHUACÁN', 'MANZANILLO', 'MINATITLÁN', 'TECOMÁN', 'VILLA DE ÁLVAREZ']
comboboxTipo = ['POSTE']

resetMuni, resetTipo, resetAfi, resetID, resetIMEI, resetTel, resetSIM, resetSerie = '','','','','','','',''

combomarca,combosabor,comboboxSabor="seleccionar"," ",[]
rescombomarca,rescombosabor=" "," "
nobatchs, notanques, nobebida, ings, nombings,cajas = 0, 0, 0, [], [], 0
batchesD = 0
batchesS = 0
data_rows, data_rows_first, data_rows_keycount = [], [], 0
cafeina,stevia,acidocitrico,agave,tapioca,flavorOca1,flavor2,goma,agua,batches,tanques = 0,0,0,0,0,0,0,0,0,0,0
cafeinaTotal, steviaTotal, acidocitricoTotal, agaveTotal, tapiocaTotal, flavorOca1Total, flavor2Total, gomaTotal, aguaTotal = 0,0,0,0,0,0,0,0,0
nflavorOca1,nflavorOca2 = "", ""

def truncate(num, decimal):
    my_digits = 10**decimal  #raise 10 to the number of decimal places
    #shifting the decimal part and converting to integer
    int_val = int(num* my_digits)
    #return the truncated value
    return int_val/my_digits