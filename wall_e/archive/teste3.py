from pandas import DataFrame, read_csv

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import sys
import numpy as np

from wall_e.wall_e_funcoes import *

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


#df = pd.read_csv("/media/sf_Dados_Bolsa_Wall_e/teste_bruto_2017-11-28.log.pasta/USIM5.csv", sep=";")
#df = df.fillna(0)
#print(df.head())
#print(df['Preço'].min())
#print(df['Preço'].max())

#print (df.head())
#df = df[df['Tempo'].between(110000,123000,inclusive=True)]
#print(df)
#temp = df[df.columns[23:67]].iloc[-1].sort_values(0)


#print(temp)
#df["Preço"].plot()
#plt.show()

#df["Preço"].plot()

#max = df["Preço"].max()
#plt.annotate("aaa",xy=(1,max))

teste = [] 
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste.append(Transacao())
teste[0].id = 1
teste[1].id = 2
teste[2].id = 3
teste[3].id = 4
teste[4].id = 5
teste[5].id = 6
teste[6].id = 7
teste[7].id = 8
teste[0].corretoras.add_vol_corretora(3,8,100,"A")
teste[1].corretoras.add_vol_corretora(1982,19,100,"A")
teste[2].corretoras.add_vol_corretora(50,40,100,"A")
teste[3].corretoras.add_vol_corretora(60,70,100,"A")
teste[4].corretoras.add_vol_corretora(30,80,100,"A")
teste[5].corretoras.add_vol_corretora(10,20,100,"A")
teste[6].corretoras.add_vol_corretora(3,8,100,"A")
teste[7].corretoras.add_vol_corretora(3,8,100,"A")
dicio= {**vars(Transacao()),**corretoras_dict}
df = pd.DataFrame(columns=sorted(list(dicio.keys())))
print (df)
inicio = datetime.datetime.now()
for dado in teste:
    dicio= {**vars(dado),**dado.corretoras.get_all_corretoras()}
    #print("tempo1: ", datetime.datetime.now() - inicio)
    #inicio = datetime.datetime.now()
    #df1 = pd.DataFrame(dicio,columns=list(dicio.keys()), index=[dado.id]).drop(["corretoras"],axis=1)
    #print("tempo2: ", datetime.datetime.now() - inicio)
    #inicio = datetime.datetime.now()
    #df = pd.concat([df,df1]).fillna(0)
    #for key in dicio.keys():
    #    df.loc[dado.id,key] = dicio[key]
    #df.loc[dado.id] = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]#list(dicio.values())
    #pd.Series(dicio.values(),index=dicio.keys())
    df = df.append(dicio, ignore_index=True)
    #inicio = datetime.datetime.now()

print("tempo3: ", datetime.datetime.now() - inicio)
print(df)
    
    