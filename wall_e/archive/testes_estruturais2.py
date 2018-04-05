"""dicionario = {12.02:[600,1000,10000],12.01:[1000,2000,3000],12.03:[800,100,4000]}
lista = ["Preço","Compra","Venda","Direto"]
for x, y in sorted(dicionario.items(), reverse=True):
    lista.append([str(x),y[0],y[1],y[2]])

print(lista)
html = open("teste.html","w")
html.write('''
    
    ''')
from datetime import datetime
import sqlite3
db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()
c.execute('create table foo (bar integer, baz timestamp)')
c.execute('insert into foo values(?, ?)', (23, datetime.now()))
c.execute('insert into foo values(?, ?)', (23, datetime(2017,1,1)))
c.execute('insert into foo values(?, ?)', (23, datetime(2016,1,1)))
c.execute('insert into foo values(?, ?)', (23, datetime(2015,1,1)))
c.execute('insert into foo values(?, ?)', (23, datetime(2014,1,1)))
c.execute('select * from foo where baz < "2016-01-01"')
for linha in c.fetchall():
    print (linha)
c.close()"""


'''from datetime import datetime
import sqlite3
ativo = []

conn = sqlite3.connect("/home/marcelo/workspace/banco_2016.db", detect_types=sqlite3.PARSE_DECLTYPES)
#conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
acoes = open("/home/marcelo/workspace/acoes.log","w")
cursor = conn.cursor()
#cursor.execute("select distinct codneg from registro where codbdi = 2 and data > '2000-01-01' and codneg not like '%34%' order by data")
#for linha in cursor.fetchall():
#    ativo.append(str(linha).replace("(","").replace(",","").replace(")","").replace("'",""))
#    ativo.append(list(linha))
cursor.execute("select codneg,max(data),avg(voltot) from registro where codbdi = 2 and codneg not like '%34%' group by codneg")
for linha in cursor.fetchall():
    if linha[2] >= 1000000 and linha[1] == '2017-09-01 00:00:00':
        ativo.append(linha[0])
    #ativo[x].append(str(resultado).replace("(","").replace(",","").replace(")","").replace("'",""))
for linha in ativo:
    print(linha)


    



#teste1 = [4.2,4.1,4,3.9,4.3,3.7]
#print (max(teste1))
#print (min(teste1))'''

'''lista = []

for x in reversed(lista):
    print(x)

lista.append("teste")
lista.append("teste2")
    
for x, y in enumerate(reversed(lista)):
    print(x,y)'''

#import datetime
#time_epoch = 1503320581271105
#data = datetime.datetime.fromtimestamp(time_epoch/1000000)
#print (data)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from wall_e.wall_e_funcoes import *
#import time
#import os

'''import datetime
import sqlite3
#from wall_e import wall_e_funcoes
#from wall_e.wall_e_funcoes import * 

for x in range(0,2):
    print(x)



transacao = [["PETR4",1,100630,13.93,100,114,88,"A","N",0,0],
             ["PETR4",2,100630,13.93,500,114,88,"A","N",0,0],
             ["PETR4",3,100631,13.93,400,114,88,"A","N",0,0],
             ["PETR4",4,100632,13.93,500,114,88,"A","N",0,0],
             ["PETR4",5,100632,13.93,900,114,88,"A","N",0,0],
             ["PETR4",6,100633,13.92,1200,8,3,"I","N",0,0],
             ["PETR4",7,100633,13.92,10000,8,3,"V","N",0,0],
             ["PETR4",8,100634,13.92,500,8,3,"V","N",0,0],
             ["PETR4",9,100635,13.92,300,8,3,"I","N",0,0],
             ["PETR4",10,100636,13.92,100,8,3,"I","N",0,0]]
hora = transacao[1][2]
segundos = Str_to_sec(hora)
volta = Sec_to_str(segundos)
print(segundos,volta)

interv_tempo = []

for x in range (0,36000):
    interv_tempo.append([])


for linha in transacao:
    interv_tempo[linha[2]].append(linha[1])

tempo_atual = transacao[-1][2]

for x in range(tempo_atual-3,tempo_atual):
    for y in interv_tempo[x]:
            print(y)
            print(transacao[y])'''

"""db = sqlite3.connect('/media/sf_Dados_Bolsa_Wall_e/banco_wall-e.db', detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()
c.execute('drop table if exists transacao')
c.execute('''
create table if not exists transacao (
    ativo text, 
    id_negocio integer primary key not null, 
    tempo integer, 
    preco real,
    volume integer, 
    comprador integer, 
    vendedor integer, 
    direcao varchar(1),
    direto varchar(1),
    bug text,
    acumulado_agr integer);
    ''')
for registro in transacao:
    c.execute('insert into transacao values(?,?,?,?,?,?,?,?,?,?,?)', registro)
db.commit()
c.execute('select * from transacao order by id_negocio desc')
for linha in c:
    if linha[7] == "I": print (linha)
    else: break
c.close()"""




#def add_volume(volume,corretora,preco):
    
#dict = {8:100}
#dict2 = {8:200}
#dict2[8] = dict[8]+dict2[8]
#dict.update(dict2)
#print(dict)
#dict[8] = dict[8]+100
#print(dict)

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

fig = plt.figure()
#ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(131)
#ax1.barh([1,2,3],[3,4,5])
ax2.axis([0,10,0,10])
plt.ion()
ax2.plot([1,2],[3,0])
plt.pause(0.5)
ax2.plot([2,3],[0,5])
plt.pause(0.5)
ax2.plot([3,4],[5,7])
plt.pause(0.5)
ax2.plot([4,5],[7,8])
plt.pause(0.5)

while True:
    plt.pause(0.5)
#plt.plot([1,2],[10,20],color='lightblue')
#plt.plot([1,2],[15,12],color='darkgreen')
#plt.xlim(0.5,4.5)
#plt.show()



        

        

