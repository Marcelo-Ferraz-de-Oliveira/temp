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


from datetime import datetime
import sqlite3
superior = 20
inferior = 20

log = open("/home/marcelo/workspace/log500000.csv","w")
conn = sqlite3.connect("/home/marcelo/workspace/banco_2016.db", detect_types=sqlite3.PARSE_DECLTYPES)
#conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()


class trade(object):
    def __init__(self):
        self.ativo = ""
        self.valor = 0
        self.stop = 0
        self.direcao = "I"
        self.data = datetime(2000,1,1)
        self.lucro = 0


def executar_consulta(acao):
    ativo = []
    cursor.execute("select * from registro where codbdi = 2 and codneg = '"+acao+"' order by data")
    for linha in cursor.fetchall():
        ativo.append(list(linha))

    x = max([superior,inferior])
    trade_unico = trade()
    while x < len(ativo):
        try:
            valores = []
            for y in range (x-superior, x-1):
                valores.append(ativo[y][9])
                valores.append(ativo[y][13])
            maximo = max(valores)
            valores = []
            for y in range(x-inferior, x-1):
                valores.append(ativo[y][9])
                valores.append(ativo[y][13])
            minimo = min(valores)
            ativo[x].append(maximo)
            ativo[x].append(minimo)
        except:
            x = x+1
            continue
        if max([ativo[x][9],ativo[x][13]]) > maximo:
            if trade_unico.direcao == "I":
                trade_unico.lucro = 0
                trade_unico.ativo = ativo[x][3]
                trade_unico.valor = ativo[x][10]
                trade_unico.stop = minimo
                trade_unico.direcao = "C"
                trade_unico.data = ativo[x][1]
                log.write(trade_unico.ativo+";"+str(trade_unico.valor)+";"+str(trade_unico.stop)+";"+str(trade_unico.direcao)+";"+str(trade_unico.data)+"\n")
                log.flush()
        if minimo > trade_unico.stop:
            if trade_unico.direcao == "C":
                trade_unico.ativo = ativo[x][3]
                trade_unico.stop = minimo
                trade_unico.data = ativo[x][1]
                #log.write(trade_unico.ativo+";"+str(trade_unico.valor)+";"+str(trade_unico.stop)+";"+str(trade_unico.direcao)+";"+str(trade_unico.data)+"\n")
        if min([ativo[x][9],ativo[x][13]]) < trade_unico.stop:
            if trade_unico.direcao == "C":
                trade_unico.lucro = - trade_unico.valor + ativo[x][11]
                trade_unico.ativo = ativo[x][3]
                trade_unico.stop = ativo[x][11]
                trade_unico.direcao = "I"
                trade_unico.data = ativo[x][1]
                log.write(trade_unico.ativo+";"+str(trade_unico.valor)+";"+str(trade_unico.stop)+";"+str(trade_unico.direcao)+";"+str(trade_unico.data)+";"+str(trade_unico.lucro)+"\n")
                log.flush()
        x = x+1









ativos = []
cursor.execute("select codneg,max(data),avg(voltot) from registro where codbdi = 2 and codneg not like '%34%' group by codneg")
for linha in cursor.fetchall():
    if linha[2] < 1000000 and linha[2] >=500000 and linha[1] == '2017-09-01 00:00:00':
        ativos.append(linha[0])
    #ativo[x].append(str(resultado).replace("(","").replace(",","").replace(")","").replace("'",""))
for linha in ativos:
    executar_consulta(linha)







