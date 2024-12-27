#import redis,json 
from h2o_wave import Q, app, main, ui, AsyncSite,site,data
import sys
# adding Folder to the system path
sys.path.insert(0, '/home/adrian/ws/wave/cassia/libs')
from funcApp import ipGlobal, ipRedis

data_rows = []

data_rows_keycount = 0

msg = []

columns3 = []

bandShow = 0

# Create columns for our issue table.
columns1 = [
    ui.table_column(name='delete', label='No.', sortable=True, searchable=True, max_width='50'),
    ui.table_column(name='text',  label='Group', sortable=True, searchable=True, max_width='120'),
    ui.table_column(name='text1', label='Time', sortable=True, searchable=True, max_width='150'),
    ui.table_column(name='text4', label='Host', sortable=True, searchable=True, max_width='650'),
    ui.table_column(name='text3', label='IP', sortable=True, searchable=True, max_width='110'),
    ui.table_column(name='text2', label='Problem', sortable=True, searchable=True, max_width='220'),
    ui.table_column(name='text5', label='Status Host', sortable=True, searchable=True, max_width='100')
]

zapi = ""
groupCompAft, clockCompAft, hostCompAft, ipCompAft, problemCompAft, enabledCompAft = "","","","","",""
groupCompBef, clockCompBef, hostCompBef, ipCompBef, problemCompBef, enabledCompBef = "","","","","",""

ings, nombings = [], []
listIngs = []
def truncate(num, decimal):
    my_digits = 10**decimal  #raise 10 to the number of decimal places
    #shifting the decimal part and converting to integer
    int_val = int(num* my_digits)
    #return the truncated value
    return int_val/my_digits