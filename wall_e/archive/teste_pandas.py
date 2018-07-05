'''
Created on 29 de jan de 2018

@author: marcelo

'''
from os import listdir, path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime







dia_inicial = 0
dia_final = 5

def Str_to_sec(data):
    data_str = str(data)
    if 'na' in data_str: return 0
    if len(data_str) == 5: 
        hora = int(data_str[0:1])
        minuto = int(data_str[1:3])
        segundo = int(data_str[3:5])
    else:
        hora = int(data_str[0:2])
        minuto = int(data_str[2:4])
        segundo = int(data_str[4:6])
    return int(datetime.timedelta(0,segundo,0,0,minuto,hora).total_seconds())



def lista_arquivos(pasta):

    lista = listdir(pasta)

    filtrada = []

    for item in lista:
        if '.pasta' in item:
            #parte = item.split('.')
            #filtrada.append(item)
            parte = item.split('.')[0]
            parte2 = parte.split("_")[2]
            #print(parte2) 
            filtrada.append([parte2,item])
    
    return filtrada

dir_base = "/home/marcelo/Dados/Dados_Bolsa_Wall_e/Resultados/"
lista_dir = lista_arquivos(dir_base)
lista_dir = sorted(lista_dir,key=lambda l:l[0])[dia_inicial:dia_final]
print(lista_dir)

databases = []
arquivo = []

for pasta in lista_dir:
    arquivo = dir_base+"/"+pasta[1]+"/PETR4_SIMPLES.csv"
    pasta_base = dir_base+"/"+pasta[1]+"/"
    #print(arquivo)
    if path.isfile(arquivo):
        try:
            databases.append([pasta[0],pd.read_csv(arquivo,sep=";"),arquivo,pasta_base])
            #break
        except:
            continue

#for database in databases:
#    print(database[0],database[1].head())

novo_arquivo = arquivo[:-4]+"_EDITADO.csv"
print(novo_arquivo)



#Printa um teste
#print(df.ix[16000])

#Grava o arquivo com as alterações:
#df.to_csv(novo_arquivo,sep=";")
#abertura = df.Preço.min()
#df.Preço.apply(lambda row:(row-abertura)*10000000).plot()
#df['acumulado'].plot()
#df['Preço'].plot()
media_velocidade = []
esim = True

#for database in sorted(databases,key=lambda l:l[0]):
#    print(database[0])
#input("")

def converter_hora(hora_bruta):
    hora_crua = str(hora_bruta)
    if len(hora_crua) > 5:
        hora = hora_crua[:2]+':'+hora_crua[2:4]+':'+hora_crua[4:6]
    else:
        hora = '0'+hora_crua[:1]+':'+hora_crua[1:3]+':'+hora_crua[3:5]
    return hora

def converter_timedelta(x):
    return x.total_seconds()

for database in databases:
#    print(corretoras)
#    input("")
    pass
    
for database in databases:
    #print(database[0])
    df = database[1]
    compradores = list(dict(df.comprador.value_counts()).keys())
    vendedores = list(dict(df.vendedor.value_counts()).keys())
    corretoras = set().union(compradores,vendedores)
    df['vol_real'] = np.where(df['direcao']=='V',df['Volume'].astype(int),np.where(df['direcao']=='A',df['Volume'].astype(int),0))
    print(corretoras)
    print(df.head())
    input("")
    for corretora in corretoras:
        df[str(corretora)+"c"] = np.where(df['comprador'].astype(int)==int(corretora), df['vol_real'],0)
        df[str(corretora)+"v"] = np.where(df['vendedor'].astype(int)==int(corretora), df['vol_real'].apply(lambda x: x*(-1)),0)
        df[str(corretora)+"c"] = df[str(corretora)+"c"].cumsum()
        df[str(corretora)+"v"] = df[str(corretora)+"v"].cumsum()
        df[str(corretora)] = df[str(corretora)+"c"] + df[str(corretora)+"v"]
        df.drop([str(corretora)+"c",str(corretora)+"v"],axis=1,inplace=True)
        #print(df[str(corretora)])
    #df = df.fillna(method="ffill")
    print(df.head())
    print(df.tail())
    input("")
    #Calcula o acumulado da agressão:
    #print(pd.to_datetime(df['Tempo']))
    #input("")
    df['Tempo'] = pd.to_datetime(database[0]+' '+df['Tempo'].apply(converter_hora))
    #print(df['Tempo'])
    range_tempo = pd.date_range(list(df["Tempo"])[0],list(df["Tempo"])[-1],freq="S")
    #print (range_tempo)
    #input("")
    #print(database[2:4])
    df['vol_real'] = np.where(df['direcao']=='V',-df['Volume'].astype(int),np.where(df['direcao']=='A',df['Volume'].astype(int),0))
    df['vol_negativo'] = np.where(df['direcao']=='V',-df['Volume'].astype(int),0)
    df['vol_positivo'] = np.where(df['direcao']=='A',df['Volume'].astype(int),0)
    df['acumulado'] = df.vol_real.cumsum()
    df['acumulado_positivo'] = df.vol_positivo.cumsum()
    df['acumulado_negativo'] = df.vol_negativo.cumsum()
    df['Preço'] = df['Preço'].astype(float)
    correlato = df[['Preço','acumulado']]
    print("Dia:",database[3])
    print("Correlação:",df.corr(method='spearman').Preço['acumulado'])
    dfs = df[['Tempo','Preço','acumulado','acumulado_positivo','acumulado_negativo']].drop_duplicates(subset='Tempo',keep='last')
    dfs.index = pd.DatetimeIndex(dfs.Tempo)
    dfs = dfs.reindex(range_tempo,fill_value=None)
    dfs.Tempo = dfs.index
    dfs = dfs.fillna(method="ffill")
    #print(dfs[:30])
    #input("")
    dfs['vol_negativo']=dfs['acumulado_negativo']-dfs['acumulado_negativo'].shift(1)
    dfs['vol_positivo']=dfs['acumulado_positivo']-dfs['acumulado_positivo'].shift(1)
    dfs['dif_data'] = dfs['Tempo'] - dfs['Tempo'].shift(1)
    dfs['dif_data'] = dfs['dif_data'].apply(converter_timedelta)
    #print(dfs['dif_data'])
    #input('')
    dfs['velocidade'] = (dfs['acumulado'] - dfs['acumulado'].shift(1))/dfs['dif_data'] 
    #print(dfs['velocidade'].median(), dfs['velocidade'].std(), dfs['velocidade'].abs().mean())
    abertura = dfs.iloc[0].Preço
    #media = dfs['velocidade'].abs().mean()
    media_velocidade.append(dfs['velocidade'].abs().mean())
    if len(media_velocidade) > 5:
        media = np.mean(media_velocidade[-6:-1])
    else:
        media = 1000000000000000
    dfs['escore'] = np.where(dfs['velocidade']>=10*media, 1,np.where(dfs['velocidade']<(-10*media),-1,0))
    #dfs['escore2'] = np.where(dfs['velocidade']<50*media, 1,np.where(dfs['velocidade']<(-100*media),-1,0))
    periodos = 5
    dfs['escore_acm'] =  dfs['escore']+dfs['escore'].shift(1)+dfs['escore'].shift(2)+dfs['escore'].shift(3)+dfs['escore'].shift(4)
    dfs['escore_acm'] = np.where(dfs['escore_acm'] >=5,1,0)
    esim = True
    if esim:
        dfs['vol_positivo'].apply(lambda row:20*row).plot()
        dfs['vol_negativo'].apply(lambda row:20*row).plot()
        dfs['acumulado'].apply(lambda row:row).plot()
        dfs.Preço.apply(lambda row:(row-abertura)*10000000).plot()
        #dfs['vol_positivo'].apply(np.log).plot()
        #dfs['vol_negativo'].apply(np.log).plot()
        #dfs['acumulado'].apply(np.log).plot()
        #dfs.Preço.apply(np.log).plot()
        #dfs.escore_acm.apply(lambda row:row*1000000).plot()
        #dfs['escore'].apply(lambda row:row*5000000).plot()
        #dfs['escore_acm'].apply(lambda row:row*2000000).plot()
        plt.grid(True)
        plt.show()
        dfs.to_csv(novo_arquivo,sep=';')
        #input("")
    
    #break
    #dfs['acumulado'].plot()
    
    #break





