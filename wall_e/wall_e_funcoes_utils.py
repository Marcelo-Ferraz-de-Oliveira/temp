'''
Created on 9 de nov de 2017

@author: marcelo
'''
import datetime
#from tkinter import *
from os import listdir
from time import sleep



compra = "A"
venda = "V"
direto = "I"
leilao = "L"
bugado = "B"
recuperado = "R"



def lista_arquivos(pasta):

    lista = listdir(pasta)

    filtrada = []

    for item in lista:
        if '.tar.bz2' in item: 
            parte = item.split('.')
            filtrada.append(parte[0])
    
    return sorted(filtrada)

def lista_a_partir(lista,data,data2):
    filtrada = []
    for item in lista:
        item_splitado = item.split("_")[2]
        if item_splitado >= str(data) and item_splitado <=str(data2):
            filtrada.append(item)
    
    return sorted(filtrada)

def get_data_do_arquivo(arquivo):
    item_splitado = arquivo.split("_")[2]
    return item_splitado


def inv(valor):
    if valor == compra:
        return venda
    if valor == venda:
        return compra

def condit_sum(a,b,direcao):
    if direcao == compra:
        return a+b
    if direcao == venda:
        return a-b




def Str_to_sec(data):
    data_str = str(data)
    if len(data_str) == 5: 
        hora = int(data_str[0:1])
        minuto = int(data_str[1:3])
        segundo = int(data_str[3:5])
    else:
        hora = int(data_str[0:2])
        minuto = int(data_str[2:4])
        segundo = int(data_str[4:6])
    return int(datetime.timedelta(0,segundo,0,0,minuto,hora).total_seconds())

def Sec_to_str(data):
    tempo = str(datetime.timedelta(seconds=int(data)))
    return tempo.replace(":","")

def ler(arquivo):
    while True:
        antes = arquivo.tell()
        linha = arquivo.readline()
        if not linha:
            #break
            sleep(0.01)
            break
            continue
        if '\n' not in linha:
            #arquivo.seek(antes)
            sleep(0.01)
            print("linha sem barra n")
            print(linha)
            pass
            #break
            #continue
        yield linha

def arrumar_linha_timestamp(string):
    temp = string.replace("!","")
    #temp = temp.replace("\r","")
    temp = temp.replace("\n","")
    temp = temp.split(":")
    if temp: 
        try:
            if (int(temp[-1]) > 1300000000000000): 
                temp.insert(0,temp[-1])
                del temp[-1]
            else: temp.insert(0,0)
        except Exception as e:
            print(e)
            print(string)
            #input(" ")
    return temp

def converter_utc(tempo_epoch):
    return datetime.datetime.fromtimestamp(int(tempo_epoch)/1000000)




class Preco_grafico(object):
    def __init__(self,root):
        pass
        #self.canvas = Canvas(root,height=10,width=900)
        #self.label = Label(root,text=str(0),height=1)
        #self.label2 = Label(root,text=str(0),height=1)
        #self.hora = Label(root,text=str(0),height=1)

class Janela:
    def __init__(self, root):
        self.root = root
        self.barra = []
    def Add_barra(self,preco,a,v,hora,root):
        objeto = getattr(self,"n"+str(preco),None)
        if not objeto:
            setattr(self,"n"+str(preco),Preco_grafico(self.root))
            objeto = getattr(self,"n"+str(preco),None)
        tamanho  = len(self.barra)
        self.barra.append(preco)
        print(tamanho)
        objeto.canvas.grid(row=tamanho,column=1)
        objeto.canvas.delete("all")
        objeto.canvas.create_rectangle(0,0,a/2000,100,fill="#00ff00")
        objeto.canvas.create_rectangle(a/2000,0,(v+a)/2000,100,fill="#ff0000")
        objeto.label["text"] = str(preco)
        objeto.label.grid(row=tamanho,column=0)
        objeto.label2["text"] = str(int(a)+int(v))
        objeto.label2.grid(row=tamanho,column=2)
        objeto.label3.grid(row=tamanho+1,column=1)
    def Criar_barras(self,entradas):
        self.barra = []
        entradas = list(entradas)
        #print (entradas)
        for x in sorted(entradas, reverse=True):
            #print(x)
            self.Add_barra(float(x[0]),int(x[1]),int(x[2]),int(x[3]),self.root)
        self.root.update()


corretoras_dict = {
    1:0,
    3:0,
    4:0,
    8:0,
    10:0,
    13:0,
    15:0,
    16:0,
    18:0,
    21:0,
    23:0,
    27:0,
    29:0,
    33:0,
    37:0,
    39:0,
    40:0,
    41:0,
    45:0,
    54:0,
    58:0,
    59:0,
    63:0,
    72:0,
    74:0,
    77:0,
    83:0,
    85:0,
    86:0,
    88:0,
    90:0,
    92:0,
    93:0,
    106:0,
    107:0,
    110:0,
    114:0,
    115:0,
    120:0,
    122:0,
    127:0,
    129:0,
    131:0,
    133:0,
    147:0,
    172:0,
    173:0,
    174:0,
    177:0,
    181:0,
    186:0,
    187:0,
    190:0,
    191:0,
    226:0,
    227:0,
    234:0,
    238:0,
    251:0,
    262:0,
    308:0,
    359:0,
    386:0,
    442:0,
    683:0,
    711:0,
    713:0,
    735:0,
    820:0,
    979:0,
    1089:0,
    1099:0,
    1106:0,
    1130:0,
    1570:0,
    1982:0,
    2197:0,
    2361:0,
    2379:0,
    2492:0,
    2570:0,
    2640:0,
    3371:0,
    3522:0,
    3762:0,
    3794:0,
    3802:0,
    5497:0
    }


now = datetime.datetime.now()

if now >= datetime.datetime(2017,8,16) and now < datetime.datetime(2017,10,18):
    indice = str("v17")
if now >= datetime.datetime(2017,10,18) and now < datetime.datetime(2017,12,13):
    indice = str("z17")
if now >= datetime.datetime(2017,12,13) and now < datetime.datetime(2018,2,14):
    indice = str("g18")
if now >= datetime.datetime(2018,2,14) and now < datetime.datetime(2018,4,18):
    indice = str("j18")
if now >= datetime.datetime(2018,4,18) and now < datetime.datetime(2018,6,13):
    indice = str("m18")
if now >= datetime.datetime(2018,6,13) and now < datetime.datetime(2018,8,15):
    indice = str("q18")
if now >= datetime.datetime(2018,8,15) and now < datetime.datetime(2018,10,17):
    indice = str("v18")
if now >= datetime.datetime(2018,10,14) and now < datetime.datetime(2018,12,12):
    indice = str("z18")
if now >= datetime.datetime(2018,12,12) and now < datetime.datetime(2019,2,13):
    indice = str("g19")

#gera automaticamente o final do código do Dólar Futuro

def Dolar(now,tipo):
    if now >= str(datetime.datetime(2017,7,30)) and now < str(datetime.datetime(2017,8,31)):
        dolar = str("u17")
    if now >= str(datetime.datetime(2017,8,31)) and now < str(datetime.datetime(2017,9,29)):
        dolar = str("v17")
    if now >= str(datetime.datetime(2017,9,29)) and now < str(datetime.datetime(2017,10,31)):
        dolar = str("x17")
    if now >= str(datetime.datetime(2017,10,31)) and now < str(datetime.datetime(2017,11,30)):
        dolar = str("z17")
    if now >= str(datetime.datetime(2017,11,30)) and now < str(datetime.datetime(2017,12,29)):
        dolar = str("f18")
    if now >= str(datetime.datetime(2017,12,29)) and now < str(datetime.datetime(2018,1,31)):
        dolar = str("g18")
    if now >= str(datetime.datetime(2018,1,31)) and now < str(datetime.datetime(2018,2,28)):
        dolar = str("h18")
    if now >= str(datetime.datetime(2018,2,28)) and now < str(datetime.datetime(2018,3,29)):
        dolar = str("j18")
    if now >= str(datetime.datetime(2018,3,29)) and now < str(datetime.datetime(2018,4,30)):
        dolar = str("k18")
    if now >= str(datetime.datetime(2018,4,30)) and now < str(datetime.datetime(2018,5,30)):
        dolar = str("m18")
    if now >= str(datetime.datetime(2018,5,30)) and now < str(datetime.datetime(2018,6,29)):
        dolar = str("n18")
    if now >= str(datetime.datetime(2018,6,29)) and now < str(datetime.datetime(2018,7,31)):
        dolar = str("q18")
    if now >= str(datetime.datetime(2018,7,31)) and now < str(datetime.datetime(2018,8,31)):
        dolar = str("u18")
    if now >= str(datetime.datetime(2018,8,31)) and now < str(datetime.datetime(2018,9,28)):
        dolar = str("v18")
    if now >= str(datetime.datetime(2018,9,28)) and now < str(datetime.datetime(2018,10,31)):
        dolar = str("x18")
    if now >= str(datetime.datetime(2018,10,31)) and now < str(datetime.datetime(2018,11,30)):
        dolar = str("z18")
    if now >= str(datetime.datetime(2018,11,30)) and now < str(datetime.datetime(2018,12,28)):
        dolar = str("f19")
    if tipo == 1: return "DOL"+dolar.upper()
    if tipo == 2: return "WDO"+dolar.upper()

'''def Indice(now):
    if now >= str(datetime.datetime(2017,8,16)) and now < str(datetime.datetime(2017,10,18)):
        indice = str("v17")
    if now >debug = False
= str(datetime.datetime(2017,10,18)) and now < str(datetime.datetime(2017,12,13)):
        indice = str("z17")
    if now >= str(datetime.datetime(2017,12,13)) and now < str(datetime.datetime(2018,2,14)):
        indice = str("g18")
    if now >= str(datetime.datetime(2018,2,14)) and now < str(datetime.datetime(2018,4,18)):
        indice = str("j18")
    if now >= str(datetime.datetime(2018,4,18)) and now < str(datetime.datetime(2018,6,13)):
        indice = str("m18")
    if now >= str(datetime.datetime(2018,6,13)) and now < str(datetime.datetime(2018,8,15)):
        indice = str("q18")
    if now >= str(datetime.datetime(2018,8,15)) and now < str(datetime.datetime(2018,10,17)):
        indice = str("v18")
    if now >= str(datetime.datetime(2018,10,14)) and now < str(datetime.datetime(2018,12,12)):
        indice = str("z18")
    if now >= str(datetime.datetime(2018,12,12)) and now < str(datetime.datetime(2019,2,13)):
        indice = str("g19")
    return indice
'''