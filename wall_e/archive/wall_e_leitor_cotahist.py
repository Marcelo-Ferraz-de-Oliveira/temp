from datetime import datetime
import sqlite3
arquivo = open("/home/marcelo/workspace/dados/COTAHIST.A1997", "r", encoding = "ISO-8859-1")
conn = sqlite3.connect("/home/marcelo/workspace/banco_2016.db", detect_types=sqlite3.PARSE_DECLTYPES)
#conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
#cursor.execute("drop table registro")
'''cursor.execute("""
CREATE TABLE registro(
    tipreg integer not null,
    data timestamp not null,
    codbdi integer not null,
    codneg text not null,
    tpmerc integer not null,
    nomres text not null,
    especi text not null,
    prazot integer not null,
    modref text not null,
    preabe real not null,
    premax real not null,
    premim real not null,
    premed real not null,
    preult real not null,
    preofc real not null,
    preofv real not null,
    totneg integer not null,
    quatot integer not null,
    voltot real not null,
    preexe real not null,
    indopc integer not null,
    datven timestamp not null,
    fatcot integer not null,
    ptoexe real not null,
    codisi text not null,
    dismes integer not null
    );""")'''


smll11=['FLRY3',
'QUAL3',
'ESTC3',
'BRAP4',
'SULA11',
'TIET11',
'TOTS3',
'CVCB3',
'ODPV3',
'MRVE3',
'SAPR4',
'GOAU4',
'HGTX3',
'IGTA3',
'CYRE3',
'BTOW3',
'CPLE6',
'ALUP11',
'MRFG3',
'MGLU3',
'CESP6',
'SMTO3',
'CSMG3',
'MYPK3',
'LINX3',
'DTEX3',
'GRND3',
'POMO4',
'BEEF3',
'ECOR3',
'LIGT3',
'ALPA4',
'VVAR11',
'ALSC3',
'ARZZ3',
'ELPL4',
'MPLU3',
'GOLL4',
'VLID3',
'CGAS5',
'BRPR3',
'EZTC3',
'WIZS3',
'TUPY3',
'RAPT4',
'SLCE3',
'SEER3',
'ABCB4',
'EVEN3',
'AALR3',
'RLOG3',
'MEAL3',
'LEVE3',
'ANIM3',
'QGEP3',
'FESA4',
'MILS3',
'TCSA3',
'DIRR3',
'GFSA3',
'HBOR3',
'JHSF3',
'CARD3',
'RSID3',
'ABCB10']

def arrumar_linha_cotahist(linha):
    resultado = []
    resultado.append(int(linha[0:2]))#tipo de registro
    if resultado[0] == 0:
        resultado.append(linha[2:15].rstrip())
        resultado.append(linha[15:23].rstrip())
        resultado.append(datetime(int(linha[23:27]),int(linha[27:29]),int(linha[29:31])))
    if resultado[0] == 99:
        resultado.append(linha[2:15])
        resultado.append(linha[15:23])
        resultado.append(datetime(int(linha[23:27]),int(linha[27:29]),int(linha[29:31])))
        resultado.append(int(linha[31:42]))
    if resultado[0] == 1:
        resultado.append(datetime(int(linha[2:6]),int(linha[6:8]),int(linha[8:10])))#DATA DO PREGÃO
        resultado.append(int(linha[10:12]))#CODBDI - CÓDIGO BDI
        resultado.append(linha[12:24].rstrip())#CODNEG - CÓDIGO DE NEGOCIAÇÃO DO PAPEL
        resultado.append(int(linha[24:27]))#TPMERC - TIPO DE MERCADO
        resultado.append(linha[27:39].rstrip())#NOMRES - NOME RESUMIDO DA EMPRESA EMISSORA DO PAPEL
        resultado.append(' '.join(linha[39:49].split()))# ESPECI - ESPECIFICAÇÃO DO PAPEL
        if linha[49:52].rstrip(): resultado.append(int(linha[49:52]))#PRAZOT - PRAZO EM DIAS DO MERCADO A TERMO
        else: resultado.append(0)
        resultado.append(linha[52:56].rstrip())#MODREF - MOEDA DE REFERÊNCIA
        resultado.append(float(linha[56:69])/100)#PREABE - PREÇO DE ABERTURA DO PAPEL - MERCADO NO PREGÃO
        resultado.append(float(linha[69:82])/100)#PREMAX - PREÇO MÁXIMO DO PAPEL - MERCADO NO PREGÃO
        resultado.append(float(linha[82:95])/100)#PREMIN - PREÇO MÍNIMO DO PAPEL - MERCADO NO PREGÃO
        resultado.append(float(linha[95:108])/100)#PREMED - PREÇO MÉDIO DO PAPEL - MERCADO NO PREGÃO
        resultado.append(float(linha[108:121])/100)#PREULT - PREÇO DO ÚLTIMO NEGÓCIO DO PAPEL - MERCADO NO PREGÃO
        resultado.append(float(linha[121:134])/100)#PREOFC - PREÇO DA MELHOR OFERTA DE COMPRA DO PAPEL - MERCADO
        resultado.append(float(linha[134:147])/100)#PREOFV - PREÇO DA MELHOR OFERTA DE VENDA DO PAPEL - MERCADO
        resultado.append(int(linha[147:152]))#TOTNEG - NEG. - NÚMERO DE NEGÓCIOS EFETUADOS COM O PAPEL - MERCADO NO PREGÃO
        resultado.append(int(linha[152:170]))#QUATOT - QUANTIDADE TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL - MERCADO
        resultado.append(float(linha[170:188])/100)#VOLTOT - VOLUME TOTAL DE TÍTULOS NEGOCIADOS NESTE PAPEL - MERCADO
        resultado.append(float(linha[188:201])/100)#PREEXE - PREÇO DE EXERCÍCIO PARA O MERCADO DE OPÇÕES OU VALOR DO CONTRATO PARA O MERCADO DE TERMO SECUNDÁRIO
        resultado.append(int(linha[201:202]))#INDOPC - INDICADOR DE CORREÇÃO DE PREÇOS DE EXERCÍCIOS OU VALORES DE CONRATO PARA OS MERCADOS DE OPÇÕES OU TERMO SECUNDÁRIO
        resultado.append(datetime(int(linha[202:206]),int(linha[206:208]),int(linha[208:210])))#DATVEN - DATA DO VENCIMENTO PARA OS MERCADOS DE OPÇÕES OU TERMO SECUNDÁRIO
        resultado.append(int(linha[210:217]))#FATCOT - FATOR DE COTAÇÃO DO PAPEL
        resultado.append(int(linha[217:230]))#PTOEXE - PREÇO DE EXERCÍCIO EM PONTOS PARA OPÇÕES REFERENCIADAS EM DÓLAR OU VALOR DE CONTRATO EM PONTOS PARA TERMO SECUNDÁRIO
        resultado.append(linha[230:242].rstrip())#CODISI - CÓDIGO DO PAPEL NO SISTEMA ISIN OU CÓDIGO INTERNO DO PAPEL
        resultado.append(int(linha[242:245]))#DISMES - NÚMERO DE DISTRIBUIÇÃO DO PAPEL
        
    return resultado

for linha in arquivo:
    registro = arrumar_linha_cotahist(linha)
    if registro[0] == 1: 
        cursor.execute('insert into registro values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', registro)

#    print(linha_arrumada)
conn.commit()
conn.close()    