#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import datetime
#import datetime
import os
from wall_e.wall_e_funcoes_utils import *
from wall_e.wall_e_funcoes_barra import *
from wall_e.wall_e_funcoes_vap import *
from wall_e.wall_e_funcoes_book import *
from wall_e.wall_e_funcoes_trade import *
from wall_e.wall_e_funcoes_corretoras import *
#root.geometry("350x300+300+300")

import copy
            
import pandas as pd

debug = False


def Debug():
    global debug
    return debug

root = None        
app = None
nome_arquivo = ""
resultado_trades = None
def inicializar(is_debug=False,caminho_arquivo=""):
    global debug
    global nome_arquivo 
    global resultado_trades
    global root
    global app
    #root = Tk()        
    #app = Janela(root)
    #root.minsize(width=1000,height=500)
    #root.update()
    debug = is_debug
    nome_arquivo = caminho_arquivo
    if not os.path.exists(nome_arquivo+".pasta"):
        os.makedirs(nome_arquivo+".pasta")
    #resultado_trades = open(nome_arquivo+".pasta/resultado_trades.csv","w")







class Transacao(object):
    def __init__(self, corretoras = None ):#Corretoras()):
        self.nome = ""
        self.id = 0
        self.tempo = 0
        self.preco = 0.0
        self.volume = 0
        self.bid = 0.0
        self.ask = 0.0
        self.comprador = 0
        self.vendedor = 0
        self.direcao = 0
        self.direto = 0
        self.bug = ""
        self.acm_agr = 0
        self.tempo_msc = 0
        self.trade_direcao = 0
        self.trade_preco = 0.0
        self.trade_stop = 0.0
        self.trade_gain = 0.0
        self.trade_resultado = 0.0
        self.ordem_orig = 0
        self.vol_ts = 0#volume total por segundo
        self.vol_vs = 0#volume de venda por segundo
        self.vol_cs = 0#volume de compra por segundo
        #self.corretoras = copy.deepcopy(corretoras)
        self.venda1 = 0
        self.venda2 = 0
        self.venda3 = 0
        self.venda4 = 0
        self.venda5 = 0
        self.pvenda1 = 0
        self.pvenda2 = 0
        self.pvenda3 = 0
        self.pvenda4 = 0
        self.pvenda5 = 0
        self.compra1 = 0
        self.compra2 = 0
        self.compra3 = 0
        self.compra4 = 0
        self.compra5 = 0
        self.pcompra1 = 0
        self.pcompra2 = 0
        self.pcompra3 = 0
        self.pcompra4 = 0
        self.pcompra5 = 0
        
    


class Ativos(object):
    def __init__(self,ativo,step = 0.01,x = 1000,gqt = True):
        #armazena a agressão acumulada
        #é atualizada em toda linha que há uma atualização de direção ("V" ou "A")
        self.trade_atual = Trade()
        #self.agr_acumulada = 0
        self.novo_negocio = False
        self.mudou_bid_ask = ""
        self.transacao = []
        self.transacao_gqt = []
        self.ind_transacao = 0
        self.book_cancelado = []
        self.dado_bruto = [0]*200
        self.book = Book_completo()
        self.vap = VAP()
        self.agr_real = 0       
        self.timeslot = [0,[0]]#tempo epoch em segundos / indice da variável transacao
        self.acm_min = 0
        self.acm_max = 0
        self.interv_tempo = []
        self.primeira_hora = 0
        self.acm_total = 0
        self.step = step
        self.barras = Barras(5,self.step)
        self.ultimo_5 = 0
        self.indicador_trade = Indicador()
        self.x = x
        self.y = 0
        self.is_gqt = gqt
        self.book_quebrado = []
        self.logfile = ""
        self.logfilesimples = ""
        self.loggqt = ""
        self.logvap = ""
        self.logtempo = ""
        self.logcandle = ""
        self.logcandlep = ""
        self.bruto_separado = ""
        for x in range (0,68400):#quantidade de segundos em 19 horas:
            self.interv_tempo.append([])           

class Grupo_ativos(object):
    def __init__(self):
        self.ativos = []
        self.contador_hora = 8
        pass
        
    def get_ativo(self,ativo):
        return getattr(self,ativo, None)
    def set_ativo(self,ativo,step = 0.01,x=1000):
        setattr(self,ativo,Ativos(ativo,step,x))
        self.ativos.append(ativo)
        if debug: print(str(getattr(self,ativo)))
    def gravar_linha_bruta(self,ativo,linha):
        self.get_ativo(ativo).logfile_bruto.write(linha)        
    def gravar_bruto(self,papel,linha):
        ativo = self.get_ativo(papel)
        ativo.bruto_separado.write(linha)
        ativo.bruto_separado.flush()
    def add_book_cancelado(self,papel,preco,volume,direcao,agressor):
        
        ativo = self.get_ativo(papel)
        tamanho = len(ativo.transacao)
        pos = tamanho-1
        ativo 
        #if debug: print(pos,"-",len(getattr(self,ativo).transacao))
        while pos > 0:
            #if debug: print(str(getattr(self,ativo).transacao[pos]))

            if ativo.transacao[pos].direto=="S":
                
                pos = pos - 1
            else:
                pos = pos + 1
                break
        else:
            pos = pos + 1
        while True:
            if pos < tamanho and pos != 0:
                if float(preco) == ativo.transacao[pos].preco and int(volume) == ativo.transacao[pos].volume and (int(agressor) in (ativo.transacao[pos].comprador, ativo.transacao[pos].vendedor)):
                    if debug: print("negocio recuperado: "+ativo.transacao[pos].id)                               
                    ativo.transacao[pos].direto = "N"
                    self.atualizar_indicadores(ativo,direcao+"R",pos=pos)
                    ativo.transacao[pos].bug = "recuperado"
                    if pos == tamanho: self.fazer_trade(ativo)#faz o trade apenas ao final da recuperação dos trades, evitando leituras incorretas de indicadores
                    break

                else:
                    pos = pos +1
            else:
                ativo.book_cancelado.append([preco,volume,direcao,agressor])        
                break
        
    
    def fazer_trade(self,ativo,zerar_tudo=False):
        pass
    '''  absorcao = 1
        inversao = 2
        acumulado = 3
        boletada = 4
        tempo_exclusao = 60000000
        p = len(ativo.transacao)-1
        if p > 10 : hora = int(ativo.transacao[p].tempo)
        else: hora = 0
        if hora > 162500 or zerar_tudo == True:
            if ativo.trade_atual.direcao in (compra,venda):
                quantidade = round(ativo.trade_atual.dinheiro/ativo.trade_atual.preco/100)*100
                volume_financeiro = ativo.trade_atual.preco*quantidade
                custo_op = (volume_financeiro*0.00024942)+2.5
                ativo.trade_atual.resultado += condit_sum(ativo.trade_atual.resultado, ((ativo.trade_atual.preco - float(ativo.book.get_book(ativo.trade_atual.direcao).entrada[0][0]))*quantidade)-(custo_op*2), ativo.trade_atual.direcao)
                ativo.trade_atual.preco = float(ativo.book.get_book(ativo.trade_atual.direcao).entrada[0][0])
                ativo.trade_atual.stop = 0
                ativo.trade_atual.gain = 0
                ativo.trade_atual.direcao = direto
                print("Saida de "+ativo.trade_atual.direcao+":",hora,ativo.transacao[-1].nome,ativo.trade_atual.preco,quantidade,volume_financeiro,custo_op)
            return True
        #escora = 150000
        preco_inicial = 0
        preco_final = 0
        acm_inicial = 0
        acm_final = 0
        inicio = 1
        ultimo_5_c = 0
        ultimo_5_v = 0
        ranking_corretoras = Corretoras()
        if hora and hora < 162500 and float(ativo.book.get_book("V").entrada[0][0]) - float(ativo.book.get_book("A").entrada[0][0]) < 0.05 and ativo.book.get_book("A").get_volume_by_pos(0) < 10000:
            ativo.ultimo_5 = 0
            for x in ativo.interv_tempo[Str_to_sec(hora)-61:Str_to_sec(hora)]:#hora-301
                for registro in x :
                    ativo.ultimo_5 += ativo.transacao[registro-1].vol_ts
                    ultimo_5_c += ativo.transacao[registro-1].vol_cs
                    ultimo_5_v += ativo.transacao[registro-1].vol_vs
            #       if abs(int(ativo.transacao[registro-1].ordem_orig)) > abs(boletada): boletada = int(ativo.transacao[registro-1].ordem_orig)
                    if inicio: 
                        preco_inicial = ativo.transacao[registro-1].preco
                        acm_inicial = ativo.transacao[registro-1].acm_agr
                        inicio = 0
                        
            #preco_final = float(ativo.transacao[p].preco)
            #acm_final = float(ativo.transacao[p].acm_agr)         
        
        
        
        
        
        ativo.indicador_trade.excluir_antigos(ativo.transacao[-1].tempo_msc,tempo_exclusao)
        
        if ultimo_5_c > 10000:
            ativo.indicador_trade.add_indicador(acumulado,ultimo_5_c,ativo.transacao[-1].tempo_msc)
                
        if ultimo_5_v < -10000:
            ativo.indicador_trade.add_indicador(acumulado,ultimo_5_v,ativo.transacao[-1].tempo_msc)
        
        if ativo.transacao[-1].ordem_orig > 5000 or ativo.transacao[-1].ordem_orig < -5000:
            ativo.indicador_trade.add_indicador(boletada,ativo.transacao[-1].ordem_orig,ativo.transacao[-1].tempo_msc)
            
        
        
        
        
        
        if (ativo.trade_atual.direcao == "I" and 
            hora > 105959 and hora < 162000 and 
            ativo.transacao[-1].acm_agr != 0 #and
            #abs(acm_inicial) > 100000 and 
            #abs(acm_inicial-acm_final) > 10000 # and ativo.acm_total/abs(ativo.transacao[-1].acm_agr) < 5:
            ):
            if p > 10:
                #print(ativo.vap.get_volume(ativo.transacao[p].preco,"A")+ ativo.vap.get_volume(ativo.transacao[p].preco,"V"))
                #print(ativo.transacao[-1].acm_agr,ativo.acm_total/30)
                #print(preco_final, preco_inicial)
                #print(ativo.transacao[-1].acm_agr, -ativo.primeira_hora/12)
                if (
                ((
                ativo.indicador_trade.soma_indicadores() < -100
                #ativo.ultimo_5 < -(ativo.primeira_hora)/20 and
                #ativo.transacao[-1].acm_agr < ativo.acm_total/40 and
                #abs(preco_final - preco_inicial) > float(ativo.transacao[p].preco)/800 and
                #abs(preco_final - float(ativo.book.get_book("A").entrada[0][0])) < abs(preco_inicial - float(ativo.book.get_book("A").entrada[0][0])) and
                #boletada <= -10000 and
                #ativo.vap.get_volume(ativo.transacao[p].preco,"A")+ ativo.vap.get_volume(ativo.transacao[p].preco,"V") < (ativo.primeira_hora)/5 and
                #ativo.book.get_book("A").get_volume_by_pos(0) < 10000 #and
                #(ativo.book.get_book("V").get_volume_by_pos(1) > escora or
                #ativo.book.get_book("V").get_volume_by_pos(2) > escora or
                #ativo.book.get_book("V").get_volume_by_pos(3) > escora or
                #ativo.book.get_book("V").get_volume_by_pos(4) > escora)
                #ativo.vap.get_volume(float(ativo.transacao[p].preco)+0.01,"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco)+0.01,"V") > 1000000 and
                #ativo.vap.get_volume(float(ativo.transacao[p].preco)+0.02,"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco)+0.02,"V") > 1000000 and
                )) and
                #ativo.transacao[p-1].direcao == "Z" and
                #float(ativo.transacao[p].preco) > 11 and
                #float(ativo.transacao[p].trade_resultado) > -150 and
                hora > 101000):
                    print(ativo.indicador_trade.valores)
                    #print("Entrada de venda:",ativo.transacao[-1][0],ativo.ultimo_5, float(ativo.book.get_book("A").entrada[0][0]))
                    #print("primeira hora ",ativo.primeira_hora)
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(6), ativo.book.get_book("V").get_volume_by_pos(6))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(5), ativo.book.get_book("V").get_volume_by_pos(5))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(4), ativo.book.get_book("V").get_volume_by_pos(4))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(3), ativo.book.get_book("V").get_volume_by_pos(3))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(2), ativo.book.get_book("V").get_volume_by_pos(2))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(1), ativo.book.get_book("V").get_volume_by_pos(1))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(0), ativo.book.get_book("V").get_volume_by_pos(0))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(0), ativo.book.get_book("A").get_volume_by_pos(0))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(1), ativo.book.get_book("A").get_volume_by_pos(1))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(2), ativo.book.get_book("A").get_volume_by_pos(2))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(3), ativo.book.get_book("A").get_volume_by_pos(3))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(4), ativo.book.get_book("A").get_volume_by_pos(4))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(5), ativo.book.get_book("A").get_volume_by_pos(5))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(6), ativo.book.get_book("A").get_volume_by_pos(6))

                    if float(ativo.book.get_book("V").entrada[0][0]) - float(ativo.book.get_book("A").entrada[0][0]) < 0.05:
                        ativo.trade_atual.direcao = "V"
                        ativo.trade_atual.preco = float(ativo.book.get_book("A").entrada[0][0])
                        ativo.acm_min = int(ativo.transacao[p].acm_agr)
                        ativo.trade_atual.acumulado_atual = int(ativo.transacao[p].acm_agr)
                        for x in range(0,5):
                            #if ativo.book.get_book("V").get_volume_by_pos(x) > escora:
                            #    ativo.trade_atual.stop = float(ativo.book.get_book("V").get_preco_by_pos(x))
                            #    break
                            ativo.trade_atual.stop = float(ativo.book.get_book("V").get_preco_by_pos(5))
                        ativo.acm_min = int(ativo.transacao[p].acm_agr)
                        quantidade = round(ativo.trade_atual.dinheiro/ativo.trade_atual.preco/100)*100
                        volume_financeiro = ativo.trade_atual.preco*quantidade
                        custo_op = (volume_financeiro*0.00024942)+2.5
                        print("Entrada de venda:",hora,ativo.transacao[-1].nome,ativo.trade_atual.preco,quantidade,volume_financeiro,custo_op)
                    #ativo.trade_atual.gain = ativo.trade_atual.preco - ativo.trade_atual.preco*ativo.trade_atual.fator
                if (
                ((
                ativo.indicador_trade.soma_indicadores() > 100
                #ativo.ultimo_5 > (ativo.primeira_hora)/20 and
                #ativo.transacao[-1].acm_agr > ativo.acm_total/40 and
                #boletada >= 10000 and
                #abs(preco_final - preco_inicial) > float(ativo.transacao[p].preco)/800 and
                #abs(preco_final - float(ativo.book.get_book("A").entrada[0][0])) < abs(preco_inicial - float(ativo.book.get_book("A").entrada[0][0])) and
                #ativo.vap.get_volume(ativo.transacao[p].preco,"A")+ ativo.vap.get_volume(ativo.transacao[p].preco,"V") < (ativo.primeira_hora)/5 and
                #ativo.book.get_book("V").get_volume_by_pos(0) < 10000 #and
                #(ativo.book.get_book("A").get_volume_by_pos(1) > escora or
                #ativo.book.get_book("A").get_volume_by_pos(2) > escora or
                #ativo.book.get_book("A").get_volume_by_pos(3) > escora or
                #ativo.book.get_book("A").get_volume_by_pos(4) > escora)
                #ativo.vap.get_volume(float(ativo.transacao[p].preco)-0.01,"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco)-0.01,"V") > 1000000 and
                #ativo.vap.get_volume(float(ativo.transacao[p].preco)-0.02,"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco)-0.02,"V") > 1000000 and
                )) and
                #ativo.transacao[p-1].direcao != "L" and 
                #float(ativo.transacao[p].preco) > 11 and
                #float(ativo.transacao[p].trade_resultado) > -150 and
                hora > 101000):
                    print(ativo.indicador_trade.valores)
                    #print("Entrada de compra:",ativo.transacao[-1][0],ativo.transacao[-1].acm_agr, ativo.acm_total/10,float(ativo.book.get_book("V").entrada[0][0]))
                    #print("primeira hora ",ativo.primeira_hora)
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(6), ativo.book.get_book("V").get_volume_by_pos(6))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(5), ativo.book.get_book("V").get_volume_by_pos(5))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(4), ativo.book.get_book("V").get_volume_by_pos(4))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(3), ativo.book.get_book("V").get_volume_by_pos(3))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(2), ativo.book.get_book("V").get_volume_by_pos(2))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(1), ativo.book.get_book("V").get_volume_by_pos(1))
                    #print("V",ativo.book.get_book("V").get_preco_by_pos(0), ativo.book.get_book("V").get_volume_by_pos(0))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(0), ativo.book.get_book("A").get_volume_by_pos(0))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(1), ativo.book.get_book("A").get_volume_by_pos(1))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(2), ativo.book.get_book("A").get_volume_by_pos(2))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(3), ativo.book.get_book("A").get_volume_by_pos(3))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(4), ativo.book.get_book("A").get_volume_by_pos(4))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(5), ativo.book.get_book("A").get_volume_by_pos(5))
                    #print("A",ativo.book.get_book("A").get_preco_by_pos(6), ativo.book.get_book("A").get_volume_by_pos(6))
                    if float(ativo.book.get_book("V").entrada[0][0]) - float(ativo.book.get_book("A").entrada[0][0]) < 0.05:
                        ativo.trade_atual.direcao = "A"
                        ativo.trade_atual.preco = float(ativo.book.get_book("V").entrada[0][0])
                        ativo.trade_atual.acumulado_atual = int(ativo.transacao[p].acm_agr)
                        for x in range(0,5):
                            #if ativo.book.get_book("A").get_volume_by_pos(x) > escora:
                            #    ativo.trade_atual.stop = float(ativo.book.get_book("A").get_preco_by_pos(x))
                            #    break
                            ativo.trade_atual.stop = float(ativo.book.get_book("A").get_preco_by_pos(5))
                        ativo.acm_max = int(ativo.transacao[p].acm_agr)
                        quantidade = round(ativo.trade_atual.dinheiro/ativo.trade_atual.preco/100)*100
                        volume_financeiro = ativo.trade_atual.preco*quantidade
                        custo_op = (volume_financeiro*0.00024942)+2.5
                        print("Entrada de compra:",hora,ativo.transacao[-1].nome,ativo.trade_atual.preco,quantidade,volume_financeiro,custo_op)
                    #ativo.trade_atual.gain = ativo.trade_atual.preco + ativo.trade_atual.preco*ativo.trade_atual.fator
        elif ativo.trade_atual.direcao == "V":
            #if ativo.acm_min > int(ativo.transacao[p].acm_agr): ativo.acm_min = ativo.transacao[p].acm_agr 
            
            if ativo.trade_atual.stop - ativo.trade_atual.preco*ativo.trade_atual.fator*2 > float(ativo.book.get_book("V").entrada[0][0]):
                ativo.trade_atual.stop = float(ativo.book.get_book("V").entrada[0][0]) + ativo.trade_atual.preco*ativo.trade_atual.fator                

            if ((#ativo.ultimo_5 > (ativo.primeira_hora)/40 and
                ativo.indicador_trade.soma_indicadores() >= 50
                 #abs(ativo.trade_atual.acumulado_atual - ativo.transacao[p].acm_agr) > abs(ativo.trade_atual.acumulado_atual)/5
                 #preco_final - preco_inicial > float(ativo.transacao[p].preco)/400 #and                 
                 #ativo.vap.get_volume(float(ativo.transacao[p].preco),"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco),"V") > (ativo.primeira_hora)/5
                 ) or
                #ativo.trade_atual.preco - ativo.trade_atual.preco*ativo.trade_atual.fator*3 > float(ativo.book.get_book("V").entrada[0][0]) or
                #boletada >= 50000 #or
                ativo.trade_atual.stop < float(ativo.book.get_book("V").entrada[0][0])
                ):
                #print(ativo.ultimo_5, preco_final - preco_inicial)
                ativo.trade_atual.direcao = "I"
                quantidade = round(ativo.trade_atual.dinheiro/ativo.trade_atual.preco/100)*100
                volume_financeiro = ativo.trade_atual.preco*quantidade
                custo_op = (volume_financeiro*0.00024942)+2.5
                ativo.trade_atual.resultado += ((ativo.trade_atual.preco - float(ativo.book.get_book("V").entrada[0][0]))*quantidade)-(custo_op*2)
                ativo.trade_atual.preco = float(ativo.book.get_book("V").entrada[0][0])
                ativo.trade_atual.stop = 0
                ativo.trade_atual.gain = 0
                print("Saida de venda:",hora,ativo.transacao[-1].nome,ativo.trade_atual.preco,quantidade,volume_financeiro,custo_op)
        elif ativo.trade_atual.direcao == "A":
            #if ativo.acm_max < ativo.transacao[p].acm_agr: ativo.acm_max = ativo.transacao[p].acm_agr 
            
            if ativo.trade_atual.stop + ativo.trade_atual.preco*ativo.trade_atual.fator*2 < float(ativo.book.get_book("A").entrada[0][0]):
                ativo.trade_atual.stop = float(ativo.book.get_book("A").entrada[0][0]) - ativo.trade_atual.preco*ativo.trade_atual.fator               
            if ((#ativo.ultimo_5 < -(ativo.primeira_hora)/40 and 
                 ativo.indicador_trade.soma_indicadores() <= -50
                 #abs(ativo.trade_atual.acumulado_atual - ativo.transacao[p].acm_agr) > abs(ativo.trade_atual.acumulado_atual)/5
                 #preco_final - preco_inicial < -float(ativo.transacao[p].preco)/400 #and
                 #ativo.vap.get_volume(float(ativo.transacao[p].preco),"A")+ ativo.vap.get_volume(float(ativo.transacao[p].preco),"V") > (ativo.primeira_hora)/5
                 ) or
                #mudar depois para stop no book
                #ativo.trade_atual.preco + ativo.trade_atual.preco*ativo.trade_atual.fator*3 < float(ativo.book.get_book("A").entrada[0][0]) or
                #boletada <= -50000 #or
                ativo.trade_atual.stop > float(ativo.book.get_book("A").entrada[0][0])
                ):

            #if (ativo.trade_atual.stop > float(ativo.book.get_book("A").entrada[0][0]) ):#or                ativo.ultimo_5 < -100000):
                ativo.trade_atual.direcao = "I"
                quantidade = round(ativo.trade_atual.dinheiro/ativo.trade_atual.preco/100)*100
                volume_financeiro = ativo.trade_atual.preco*quantidade
                custo_op = (volume_financeiro*0.00024942)+2.5
                ativo.trade_atual.resultado += ((ativo.trade_atual.preco - float(ativo.book.get_book("A").entrada[0][0]))*(-1)*quantidade)-(custo_op*2)
                ativo.trade_atual.preco = float(ativo.book.get_book("A").entrada[0][0])
                ativo.trade_atual.stop = 0
                ativo.trade_atual.gain = 0
                print("Saida de compra:",hora,ativo.transacao[-1].nome,ativo.trade_atual.preco,quantidade,volume_financeiro,custo_op)
        return True'''
                    
    def add_transacao(self,nome_ativo,*negocio):
        #global corretoras_dict
        #corretora_temp = corretoras_dict.copy()
        ativo = self.get_ativo(nome_ativo)
        '''if ativo.transacao:
            temp2 = Transacao(ativo.transacao[-1].corretoras)
        else:
            temp2 = Transacao()'''
        temp2 = Transacao()
        temp2.nome = str(nome_ativo)#0
        temp2.id = int(negocio[8])#1
        temp2.tempo = int(negocio[5])#2
        temp2.preco = float(negocio[2])#3 - preco
        temp2.volume = int(negocio[7])#4 - volume
        temp2.bid = float(negocio[3])#5 - bid
        temp2.ask = float(negocio[4])#6 - ask
        temp2.comprador = int(negocio[62])#7 - comprador
        temp2.vendedor = int(negocio[63])#8 - vendedor
        temp2.direcao = str(negocio[132])#9 - direcao
        temp2.direto = str(negocio[133])#10 - direto
        temp2.bug = str(negocio[134])#11 - bug
        temp2.acm_agr = int(negocio[161])#12 - acumulado_agr
        temp2.tempo_msc = int(negocio[150])#13 - tempo_msc
        temp2.trade_direcao = str(ativo.trade_atual.direcao)#14
        temp2.trade_preco = float(ativo.trade_atual.preco)#15
        temp2.trade_stop = float(ativo.trade_atual.stop)#16
        temp2.trade_gain = float(ativo.trade_atual.gain)#17
        temp2.trade_resultado = float(ativo.trade_atual.resultado)#18
        temp2.ordem_orig = int(negocio[160])#19 - ordem original
        temp2.vol_cs = int(negocio[180])#21 - volume de compra por segundo
        temp2.vol_vs = int(negocio[181])#22 - volume de venda por segundo
        temp2.vol_ts = int(negocio[182])#23 - volume total por segundo
        temp2.venda1 = ativo.book.get_book('V').get_volume_by_pos(0)
        temp2.venda2 = ativo.book.get_book('V').get_volume_by_pos(1)
        temp2.venda3 = ativo.book.get_book('V').get_volume_by_pos(2)
        temp2.venda4 = ativo.book.get_book('V').get_volume_by_pos(3)
        temp2.venda5 = ativo.book.get_book('V').get_volume_by_pos(4)
        temp2.compra1 = ativo.book.get_book('A').get_volume_by_pos(0)
        temp2.compra2 = ativo.book.get_book('A').get_volume_by_pos(1)
        temp2.compra3 = ativo.book.get_book('A').get_volume_by_pos(2)
        temp2.compra4 = ativo.book.get_book('A').get_volume_by_pos(3)
        temp2.compra5 = ativo.book.get_book('A').get_volume_by_pos(4)
        temp2.pvenda1 = ativo.book.get_book('V').get_preco_by_pos(0)
        temp2.pvenda2 = ativo.book.get_book('V').get_preco_by_pos(1)
        temp2.pvenda3 = ativo.book.get_book('V').get_preco_by_pos(2)
        temp2.pvenda4 = ativo.book.get_book('V').get_preco_by_pos(3)
        temp2.pvenda5 = ativo.book.get_book('V').get_preco_by_pos(4)
        temp2.pcompra1 = ativo.book.get_book('A').get_preco_by_pos(0)
        temp2.pcompra2 = ativo.book.get_book('A').get_preco_by_pos(1)
        temp2.pcompra3 = ativo.book.get_book('A').get_preco_by_pos(2)
        temp2.pcompra4 = ativo.book.get_book('A').get_preco_by_pos(3)
        temp2.pcompra5 = ativo.book.get_book('A').get_preco_by_pos(4)

        #if negocio[2] != "0" and negocio[132] != "0" and negocio[132] != 0: #and int(negocio[5])<165500:
            #if temp.direcao == "V":
                #temp[4] = str(int(temp[4])*(-1))
        ativo.transacao.append(temp2)
        #print(len(ativo.transacao))
        ativo.interv_tempo[Str_to_sec(temp2.tempo)].append(temp2.id)
        if int(temp2.tempo) < 110000: 
            ativo.primeira_hora += int(temp2.volume)
            ativo.indicador_trade.divisores = [1,1,1,ativo.primeira_hora/ativo.x,ativo.primeira_hora/(ativo.x*3.1)]
        ativo.acm_total += int(temp2.volume)    #input("")

    def atualizar_indicadores(self,ativo,direcao,pos=-1):
        #hora = int(ativo.transacao[pos].tempo)
        if len(ativo.transacao) > 1:
            if ativo.transacao[pos].tempo != ativo.transacao[pos-1].tempo:
                ativo.transacao[pos].vol_cs = 0
                ativo.transacao[pos].vol_vs = 0
                ativo.transacao[pos].vol_ts = 0
            else:
                ativo.transacao[pos].vol_cs = ativo.transacao[pos-1].vol_cs
                ativo.transacao[pos].vol_vs = ativo.transacao[pos-1].vol_vs
                ativo.transacao[pos].vol_ts = ativo.transacao[pos-1].vol_ts

        
        
        if direcao == "AR":
            ativo.vap.del_volume(float(ativo.transacao[pos].preco),ativo.transacao[pos].direcao,int(ativo.transacao[pos].volume))             
            ativo.barras.add_volume(int(ativo.transacao[pos].volume)*(-1),float(ativo.transacao[pos].preco),ativo.transacao[pos].direcao)            
            #ativo.transacao[pos].corretoras = copy.deepcopy(ativo.transacao[pos-1].corretoras)
            
            
            
            ativo.transacao[pos].acm_agr = ativo.transacao[pos-1].acm_agr - int(ativo.transacao[pos].volume)                        
            
            if int(ativo.transacao[pos].tempo) == int(ativo.transacao[pos-1].tempo):
                ativo.transacao[pos].vol_cs =  ativo.transacao[pos-1].vol_cs - ativo.transacao[pos].volume
             
            else:
                ativo.transacao[pos].vol_cs =  ativo.transacao[pos].volume*(-1) 
                            
            ativo.transacao[pos].direcao = "V"
            #negócio original
            if (int(ativo.transacao[pos].tempo_msc) - int(ativo.transacao[pos-1].tempo_msc) < 600000 and 
                ativo.transacao[pos].vendedor == ativo.transacao[pos-1].vendedor and
                ativo.transacao[pos].direcao == ativo.transacao[pos-1].direcao
            ):
                ativo.transacao[pos].ordem_orig = (ativo.transacao[pos].volume*(-1)) + ativo.transacao[pos-1].ordem_orig
                ativo.transacao[pos-1].ordem_orig = 0
                #iguala o tempo epoch caso esteja diferente, para permitir a análise por tempo
                ativo.transacao[pos].tempo_msc = ativo.transacao[pos-1].tempo_msc
            else:
                ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume*(-1)

        if direcao == "VR":
            ativo.vap.del_volume(float(ativo.transacao[pos].preco),ativo.transacao[pos].direcao,int(ativo.transacao[pos].volume))
            ativo.barras.add_volume(int(ativo.transacao[pos].volume)*(-1),float(ativo.transacao[pos].preco),ativo.transacao[pos].direcao)
            #ativo.transacao[pos].corretoras = copy.deepcopy(ativo.transacao[pos-1].corretoras)
            
            ativo.transacao[pos].acm_agr = ativo.transacao[pos-1].acm_agr + int(ativo.transacao[pos].volume)
            
            if int(ativo.transacao[pos].tempo) == int(ativo.transacao[pos-1].tempo):
                ativo.transacao[pos].vol_vs =  ativo.transacao[pos-1].vol_vs + ativo.transacao[pos].volume 
            else:
                ativo.transacao[pos].vol_vs =  ativo.transacao[pos].volume
            
            
            ativo.transacao[pos].direcao = "A"
            #negócio original
            if (int(ativo.transacao[pos].tempo_msc) - int(ativo.transacao[pos-1].tempo_msc) < 600000 and 
                ativo.transacao[pos].comprador == ativo.transacao[pos-1].comprador and
                ativo.transacao[pos].direcao == ativo.transacao[pos-1].direcao
            ):
                ativo.transacao[pos].ordem_orig = ativo.transacao[pos].ordem_orig + ativo.transacao[pos-1].ordem_orig
                ativo.transacao[pos-1].ordem_orig = 0
                #iguala o tempo epoch caso esteja diferente, para permitir a análise por tempo
                ativo.transacao[pos].tempo_msc = ativo.transacao[pos-1].tempo_msc
            else:
                ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume
            
            
        
        if direcao == "A":
                    ativo.transacao[pos].direcao = "V"
                    
                    if len(ativo.transacao)>1:
                        ativo.transacao[pos].acm_agr = int(ativo.transacao[pos-1].acm_agr) - int(ativo.transacao[pos].volume)
                        
                        if int(ativo.transacao[pos].tempo) == int(ativo.transacao[pos-1].tempo):
                            ativo.transacao[pos].vol_vs =  ativo.transacao[pos-1].vol_vs-ativo.transacao[pos].volume 
                        else:
                            ativo.transacao[pos].vol_vs = ativo.transacao[pos].volume*(-1)
                        
                        
                        if (int(ativo.transacao[pos].tempo_msc) - int(ativo.transacao[pos-1].tempo_msc) < 600000 and 
                            ativo.transacao[pos].vendedor == ativo.transacao[pos-1].vendedor and 
                            ativo.transacao[pos].direcao == ativo.transacao[pos-1].direcao
                        ):
                            ativo.transacao[pos].ordem_orig = (ativo.transacao[pos].volume*(-1))+ ativo.transacao[pos-1].ordem_orig
                            ativo.transacao[pos-1].ordem_orig = 0
                            #iguala o tempo epoch caso esteja diferente, para permitir a análise por tempo
                            ativo.transacao[pos].tempo_msc = ativo.transacao[pos-1].tempo_msc
                        else:
                            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume*(-1)
                    else:
                        ativo.transacao[pos].acm_agr = ativo.transacao[pos].volume*(-1)
                        ativo.transacao[pos].vol_vs = ativo.transacao[pos].volume*(-1)
                    
                    
                    #datacomp_anterior = [0,#0
                    #             0,#1
                    #             ativo.transacao[-1].comprador,#2
                    #             ativo.transacao[-1].comprador,#3
                    #             ativo.transacao[-1].tempo_msc,#4
                    #             ativo.transacao[-1].volume,#5
                    #             ativo.transacao[-1].ordem_orig]#6

            #if hora < 110000: ativo.primeira_hora += int(ativo.transacao[pos].volume)
        if direcao == "V":
                    ativo.transacao[pos].direcao = "A"
                    
                    if len(ativo.transacao) > 1:
                        ativo.transacao[pos].acm_agr = int(ativo.transacao[pos-1].acm_agr) + int(ativo.transacao[pos].volume)
                        
                        if int(ativo.transacao[pos].tempo) == int(ativo.transacao[pos-1].tempo):
                            ativo.transacao[pos].vol_cs =  ativo.transacao[pos-1].vol_cs + ativo.transacao[pos].volume
                        else:
                            ativo.transacao[pos].vol_cs = int(ativo.transacao[pos].volume)
                        if (int(ativo.transacao[pos].tempo_msc) - int(ativo.transacao[pos-1].tempo_msc) < 600000 and 
                            ativo.transacao[pos].comprador == ativo.transacao[pos-1].comprador and 
                            ativo.transacao[pos].direcao == ativo.transacao[pos-1].direcao
                        ):
                            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume + ativo.transacao[pos-1].ordem_orig
                            ativo.transacao[pos-1].ordem_orig = 0
                            #iguala o tempo epoch caso esteja diferente, para permitir a análise por tempo
                            ativo.transacao[pos].tempo_msc = ativo.transacao[pos-1].tempo_msc
                        else:
                            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume
                    else:
                        ativo.transacao[pos].acm_agr = int(ativo.transacao[pos].volume)
                        ativo.transacao[pos].vol_cs = int(ativo.transacao[pos].volume)
                    
                    

            #if hora < 110000: ativo.primeira_hora += int(ativo.transacao[pos].volume)
        
        if direcao == "B":
            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume
            ativo.transacao[pos].direto = "S"
            ativo.transacao[pos].bug = "bugado"
            if float(ativo.transacao[pos].preco) <= float(ativo.transacao[pos].bid):
                ativo.transacao[pos].direcao = "V"
                if len(ativo.transacao) > 1:
                    ativo.transacao[pos].acm_agr = ativo.transacao[pos-1].acm_agr - ativo.transacao[pos].volume    
                    if ativo.transacao[pos].tempo == ativo.transacao[pos-1].tempo:
                        ativo.transacao[pos].vol_vs =  ativo.transacao[pos-1].vol_vs - ativo.transacao[pos].volume
                    else:
                        ativo.transacao[pos].vol_vs = ativo.transacao[pos].volume*(-1)
                else:
                    ativo.transacao[pos].acm_agr = ativo.transacao[pos].volume*(-1)
                    ativo.transacao[pos].vol_vs = ativo.transacao[pos].volume*(-1)    
                    
            else:
                ativo.transacao[pos].direcao = "A"
                if len(ativo.transacao) > 1:
                    ativo.transacao[pos].acm_agr = int(ativo.transacao[pos-1].acm_agr) + int(ativo.transacao[pos].volume)         
                    if int(ativo.transacao[pos].tempo) == int(ativo.transacao[pos-1].tempo):
                        ativo.transacao[pos].vol_cs =  ativo.transacao[pos-1].vol_cs + ativo.transacao[pos].volume
                    else:
                        ativo.transacao[pos].vol_cs = ativo.transacao[pos].volume
                else:
                    ativo.transacao[pos].acm_agr = ativo.transacao[pos].volume
                    ativo.transacao[pos].vol_cs = ativo.transacao[pos].volume
                        
        
        if direcao == "I":
            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume
            if len(ativo.transacao) > 1: ativo.transacao[pos].acm_agr = ativo.transacao[pos-1].acm_agr
            ativo.transacao[pos].direto = "S"
            ativo.transacao[pos].direcao = "I"
            

        if direcao == "L":
            ativo.transacao[pos].direto = "N"
            ativo.transacao[pos].direcao = "L"
            ativo.transacao[pos].ordem_orig = ativo.transacao[pos].volume
            

        #registra a virada do acumulado de agressão
        
        ativo.vap.add_volume(ativo.transacao[pos].preco,ativo.transacao[pos].direcao,ativo.transacao[pos].volume)        
        ativo.barras.add_volume(ativo.transacao[pos].volume,ativo.transacao[pos].preco,ativo.transacao[pos].direcao)           
        ativo.transacao[pos].vol_ts = ativo.transacao[pos].vol_cs + ativo.transacao[pos].vol_vs
        #ativo.transacao[pos].corretoras.add_vol_corretora(ativo.transacao[pos].comprador,ativo.transacao[pos].vendedor,ativo.transacao[pos].volume,ativo.transacao[pos].direcao)

        
        
        #limpa os valores anteriores de volume por segundo

        if len(ativo.transacao) > 1:
            if ativo.transacao[pos].tempo == ativo.transacao[pos-1].tempo:
                ativo.transacao[pos-1].vol_cs = 0
                ativo.transacao[pos-1].vol_vs = 0
                ativo.transacao[pos-1].vol_ts = 0
   

        return True


    def verificar_book_cancelado(self,*linha):
        
        y = 0
        x=linha.index("T")+1
        nome_ativo = linha[x]
        ativo = self.get_ativo(nome_ativo)
        #ativo.dado_bruto[134] = ""
        #if ativo.dado_bruto[8] == "4118":
        #    input("")
        if ativo.dado_bruto[84] == "3":#indica que o ativo está em leilão
            self.add_transacao(linha[x],*ativo.dado_bruto)
            self.atualizar_indicadores(ativo,"L")
            return True

        if ativo.book_cancelado:#verifica se há algum registro de negócio cancelado do book de ofertas
            if Debug(): print(str(ativo.book_cancelado[0]))
            if ativo.dado_bruto[2] == ativo.book_cancelado[y][0] and ativo.dado_bruto[7] == ativo.book_cancelado[y][1] and (ativo.book_cancelado[y][3] in (ativo.dado_bruto[62], ativo.dado_bruto[63])):
                #nesse caso há um cancelamento de oferta no book com trade correspondente, se tratando de trade comum      
                #define que não foi direto
                if debug: print("foi trade comum")
                ativo.dado_bruto[134] = "0"
                ativo.dado_bruto[133] = "N"
                if ativo.book_cancelado[y][2] in ("A","V"):
                    self.add_transacao(linha[x],*ativo.dado_bruto)
                    self.atualizar_indicadores(ativo,ativo.book_cancelado[y][2])
                    self.fazer_trade(ativo)
                del ativo.book_cancelado[y]
                #self.gravar_transacoes(linha[1])
                return True
                
            else:
                if debug: print("foi cancelamento")
                del ativo.book_cancelado[0]
                return False

        else:
            #nesse caso, a lista de ofertas canceladas está vazia, se tratando de um direto
            if ativo.dado_bruto[62] == ativo.dado_bruto[63]:
                if debug: print("foi DIRETO")
                self.add_transacao(linha[x],*ativo.dado_bruto)
                self.atualizar_indicadores(ativo,"I")   
            else:
                if debug: print("Não foi direto")
                self.add_transacao(linha[x],*ativo.dado_bruto)
                self.atualizar_indicadores(ativo,"B")   
                
            return True


    def gravar_transacoes(self,papel,grupo_ativos):
        ativo = self.get_ativo(papel)
        #ativo.bruto_separado.close()
        if not ativo.transacao_gqt and ativo.is_gqt:
            print("GQT configurado mas não encontrado, os dados desse dia não serão usados")
            return False
        
        ativo.logfile = open(nome_arquivo+".pasta"+"/"+str(papel)+".csv","w")
        ativo.logfilesimples = open(nome_arquivo+".pasta"+"/"+str(papel)+"_SIMPLES.csv","w")
        ativo.loggqt = open(nome_arquivo+".pasta"+"/"+str(papel)+"_GQT.csv","w")
        ativo.logvap = open(nome_arquivo+".pasta"+"/"+str(papel)+"VAP.csv","w")
        ativo.logtempo = open(nome_arquivo+".pasta"+"/"+str(papel)+"TEMPO.csv","w")
        ativo.logcandle = open(nome_arquivo+".pasta"+"/"+str(papel)+"CANDLE.csv","w")
        ativo.logcandlep = open(nome_arquivo+".pasta"+"/"+str(papel)+"CANDLEP.csv","w")
        ativo.bruto_separado = open(nome_arquivo+".pasta"+"/"+str(papel)+"CANDLEP.csv","w")
        ativo.logvap.write("preco;compra;venda;direto;leilão\r\n")

        #inicio = datetime.datetime.now()
        #df = pd.DataFrame()
        #print (df)
        #for dado in ativo.transacao:
        #    dicio= {**vars(dado),**dado.corretoras.get_all_corretoras()}
        #    df1 = pd.DataFrame(dicio,columns=list(dicio.keys()), index=[dado.id]).drop(["corretoras"],axis=1)
        #    df = pd.concat([df,df1]).fillna(0)
        #df.to_csv(nome_arquivo+".pasta/resultado_trades_panda.csv",sep=";")
        #print("tempo pandas: ",datetime.datetime.now()-inicio)
        for indice, barras in enumerate(ativo.barras.barras_ind):
            for barra in barras.barras_preco:
                ativo.logcandlep.write(str(indice)+";"+str(barra.preco)+";"+str(barra.vol_c)+";"+str(barra.vol_v)+"\r\n")
            
        
        for preco in sorted(ativo.vap.precos, key=float):
            ativo.logvap.write(str(preco)+";")
            for tipo in ativo.vap.tipos:
                ativo.logvap.write(str(ativo.vap.get_volume(preco,tipo))+";")
            ativo.logvap.write("\r\n")
        ativo.logvap.flush()
        ativo.logvap.close()
        
        
        
        
        ativo.logfile.write("ativo;id negócio;Tempo;Preço;Volume;Bid;Ask;comprador;vendedor;direcao;direto;bug;acumulado agr;tempo_msc;trade_direção;trade_preço;trade_stop;trade_gain;trade_resultado;original;volume_compra;volume_venda;volume_total;")
        #if ativo.transacao: 
        #    for codigo in ativo.transacao[-1].corretoras.codigos:
        #        ativo.logfile.write(str(codigo)+";")
        ativo.logfile.write("\r\n")
        

        for dado in ativo.transacao:
            ativo.logfile.write(str(dado.nome)+";"+str(dado.id)+";"+str(dado.tempo)+";"+str(dado.preco)+";"+str(dado.volume)+";"+str(dado.bid)+";"+str(dado.ask)+";"+str(dado.comprador)+";"+str(dado.vendedor)+";"+str(dado.direcao)+";"+str(dado.direto)+";"+str(dado.bug)+";"+str(dado.acm_agr)+";"+str(dado.tempo_msc)+";"+str(dado.trade_direcao)+";"+str(dado.trade_preco)+";"+str(dado.trade_stop)+";"+str(dado.trade_gain)+";"+str(dado.trade_resultado)+";"+str(dado.ordem_orig)+";"+str(dado.vol_cs)+";"+str(dado.vol_vs)+";"+str(dado.vol_ts)+";")
            #for codigo in dado.corretoras.codigos:
            #    ativo.logfile.write(str(dado.corretoras.get_corretora(codigo).ativo + dado.corretoras.get_corretora(codigo).passivo)+";")
            ativo.logfile.write("\r\n")
        ativo.logfile.flush()
        ativo.logfile.close()
        
        
        ativo.loggqt.write("ativo;id negócio;Tempo;Preço;Volume;Bid;Ask;comprador;vendedor;direcao;direto;bug;acumulado agr;tempo_msc;trade_direção;trade_preço;trade_stop;trade_gain;trade_resultado;original;volume_compra;volume_venda;volume_total;")
        #if ativo.transacao: 
        #    for codigo in ativo.transacao[-1].corretoras.codigos:
        #        ativo.logfile.write(str(codigo)+";")
        ativo.loggqt.write("\r\n")
        

        for dado in ativo.transacao_gqt:
            ativo.loggqt.write(str(dado.nome)+";"+str(dado.id)+";"+str(dado.tempo)+";"+str(dado.preco)+";"+str(dado.volume)+";"+str(dado.bid)+";"+str(dado.ask)+";"+str(dado.comprador)+";"+str(dado.vendedor)+";"+str(dado.direcao)+";"+str(dado.direto)+";"+str(dado.bug)+";"+str(dado.acm_agr)+";"+str(dado.tempo_msc)+";"+str(dado.trade_direcao)+";"+str(dado.trade_preco)+";"+str(dado.trade_stop)+";"+str(dado.trade_gain)+";"+str(dado.trade_resultado)+";"+str(dado.ordem_orig)+";"+str(dado.vol_cs)+";"+str(dado.vol_vs)+";"+str(dado.vol_ts)+";")
            #for codigo in dado.corretoras.codigos:
            #    ativo.logfile.write(str(dado.corretoras.get_corretora(codigo).ativo + dado.corretoras.get_corretora(codigo).passivo)+";")
            ativo.loggqt.write("\r\n")
        ativo.loggqt.flush()
        ativo.loggqt.close()
        
        
        
        
        
        
        ativo.logfilesimples.write("ativo;id negócio;Tempo;Preço;Volume;Bid;Ask;comprador;vendedor;direcao;direto;tempo_msc;pcompra1;compra1;pcompra2;compra2;pcompra3;compra3;pcompra4;compra4;pcompra5;compra5;pvenda1;venda1;pvenda2;venda2;pvenda3;venda3;pvenda4;venda4;pvenda5;venda5")
        ativo.logfilesimples.write("\r\n")
        for dado in ativo.transacao:
            ativo.logfilesimples.write(str(dado.nome)+";"+str(dado.id)+";"+str(dado.tempo)+";"+str(dado.preco)+";"+str(dado.volume)+";"+str(dado.bid)+";"+str(dado.ask)+";"+str(dado.comprador)+";"+str(dado.vendedor)+";"+str(dado.direcao)+";"+str(dado.direto)+";"+str(dado.tempo_msc)+";"+str(dado.pcompra1)+";"+str(dado.compra1)+";"+str(dado.pcompra2)+";"+str(dado.compra2)+";"+str(dado.pcompra3)+";"+str(dado.compra3)+";"+str(dado.pcompra4)+";"+str(dado.compra4)+";"+str(dado.pcompra5)+";"+str(dado.compra5)+";"+str(dado.pvenda1)+";"+str(dado.venda1)+";"+str(dado.pvenda2)+";"+str(dado.venda2)+";"+str(dado.pvenda3)+";"+str(dado.venda3)+";"+str(dado.pvenda4)+";"+str(dado.venda4)+";"+str(dado.pvenda5)+";"+str(dado.venda5))
            ativo.logfilesimples.write("\r\n")
        ativo.logfilesimples.flush()
        ativo.logfilesimples.close()
        
        
        
        for x in range(Str_to_sec(83000),Str_to_sec(185958)):
            ativo.logtempo.write(Sec_to_str(x)+";")            
            for dado in ativo.interv_tempo[x]:
                ativo.logtempo.write(str(dado)+";")
            ativo.logtempo.write("\r\n")            
        ativo.logtempo.flush()
        ativo.logtempo.close()
        
        ativo.logcandle.write("TEMPO;MINIMO;MAXIMO;ABERTURA;FECHAMENTO;VOL_COMPRA;VOL_VENDA\r\n")
        inicio = True
        minimo = 100000000
        maximo = 0
        abertura = 0
        fechamento = 0
        volume_compra = 0
        volume_venda = 0
        for y in range (0,540):
            ativo.logcandle.write(Sec_to_str(Str_to_sec(93000)+(y*60))+";")            
            volume_compra = 0
            volume_venda = 0
            minimo = fechamento
            maximo = fechamento
            abertura = fechamento
            inicio = True
            for x in range(Str_to_sec(93000)+(y*60),Str_to_sec(93059)+(y*60)):
                for dado in ativo.interv_tempo[x]:
                    try:
                        verif = ativo.transacao[dado-1]
                    except:
                        continue
                    if inicio:
                        minimo = 100000000
                        maximo = 0
                        fechamento = 0
                        abertura = ativo.transacao[dado-1].preco
                        inicio = False
                    fechamento = ativo.transacao[dado-1].preco
                    if float(ativo.transacao[dado-1].preco) > maximo:
                        maximo = float(ativo.transacao[dado-1].preco)
                    if float(ativo.transacao[dado-1].preco) < minimo:
                        minimo = float(ativo.transacao[dado-1].preco)
                    if ativo.transacao[dado-1].direcao == "A":
                        volume_compra += int(ativo.transacao[dado-1].volume)
                    if ativo.transacao[dado-1].direcao == "V":
                        volume_venda += int(ativo.transacao[dado-1].volume)
            ativo.logcandle.write(str(minimo)+";"+str(maximo)+";"+str(abertura)+";"+str(fechamento)+";"+str(volume_compra)+";"+str(volume_venda)+"\r\n")
            
            
                        
        
        
        #grava o resultado financeiro dos trades
        resultado_trades = open(nome_arquivo+".pasta/resultado_trades.csv","a")
        for dados in grupo_ativos.ativos:
            ativo = self.get_ativo(dados)
            if ativo.transacao:
                resultado = ativo.transacao[-1].trade_resultado
                if Debug(): print("---------------------",dados,str(resultado),"---------------------")
                resultado_trades.write(dados+";"+str(resultado)+";"+str(ativo.x)+"\r\n")
            else:
                if Debug(): print("não há negócios em "+dados)
                pass
        resultado_trades.flush()
        resultado_trades.close()

               
    def atualizar_gqt(self,*linha):
        #deleta o timestamp
        linha = list(linha)
        linha.append(linha[0])
        del linha[0]
        ativo = self.get_ativo(linha[1])
        temp2 = Transacao()
        if linha[2] == 'A':
            temp2.nome = linha[1]#0
            temp2.id = int(int(linha[8])/10)#1
            temp2.tempo = int(linha[3])#2
            temp2.preco = float(linha[4])#3 - preco
            temp2.volume = int(linha[7])#4 - volume
            temp2.comprador = int(linha[5])#7 - comprador
            temp2.vendedor = int(linha[6])#8 - vendedor
            temp2.direcao = linha[11]
            temp2.direto = "N" if linha[10] == "0" else "S"
            temp2.bug = 0
            if not ativo.transacao_gqt:
                ativo.transacao_gqt.append(temp2)
            elif temp2.id < ativo.transacao_gqt[-1].id:
                ativo.transacao_gqt.append(temp2)
            else:
                return 0                
        if temp2.id == 1:
            print("Registro GQT realizado, iniciando correções...")
            leng = len(ativo.transacao_gqt) -1
            ativo.transacao_gqt = ativo.transacao_gqt[::-1]
            for x in range(0,leng):
                ativo.transacao_gqt[x].id = x+1    
            for x in range(0,leng):
            #verifica se o id não existe
                #if x in range(4880,4890):
                #    print(x,ativo.transacao[x-1].id+1,ativo.transacao[x].id)
                #    print(x > 0 and int(ativo.transacao[x-1].id) + 1 == x+1 and int(ativo.transacao[x].id) != x+1)
                #    input("")
                #print(x,ativo.transacao[x].id)
                try:
                    if x > 0 and int(ativo.transacao[x-1].id) + 1 == x+1 and int(ativo.transacao[x].id) != x+1:
                        ativo.transacao.insert(x,ativo.transacao_gqt[x])
                        continue
                        #print(ativo.transacao[-1].id,x)
                #verifica se é bugado ou direto
                    if ativo.transacao[x].id == x+1:
                        if ativo.transacao[x].bug == 'bugado' or ativo.transacao[x].direcao == "I":
                            ativo.transacao[x].direcao = ativo.transacao_gqt[x].direcao
                            ativo.transacao[x].direto = ativo.transacao_gqt[x].direto
                            ativo.transacao[x].bug = "recuperado_gqt"
                except:
                    ativo.transacao.insert(x,ativo.transacao_gqt[x])
                    continue
                #print(x,ativo.transacao[x].id)
            print("Correções finalizadas.")        
    
    def atualizar_dados(self,*linha):
        #adiciona o valor do timestamp em milisegundos
        ativo = self.get_ativo(linha[2])
        ativo.dado_bruto[150] = linha[0]
        #deleta o timestamp
        linha = list(linha)
        tempo_temp = converter_utc(linha[0])
        if tempo_temp.time() > datetime.time(self.contador_hora,0,0):
            print(tempo_temp,datetime.datetime.now())
            self.contador_hora += 1
        del linha[0]
        d = 3
        try:
            
            while d < len(linha): 
                ativo.dado_bruto[int(linha[d])]=linha[d+1]
                if linha[d] == "8":
                    ativo.novo_negocio = True
                    if int(linha[d+1]) == 1:
                        qtde_teorica = int(ativo.dado_bruto[83])
                        sentido_sobra = ativo.dado_bruto[56]
                        #while qtde_teorica <= 0:
                        #     p = ativo.book.get_book("A").entrada[0]
                        #     ativo.book.get_book("A").entrada[0]
                        if Debug():
                            print(qtde_teorica,sentido_sobra,ativo.dado_bruto[57],ativo.dado_bruto[82])
                            input("")
                if linha[d] == "47":#indica o mercado inscrito, esse dado só é fornecido na primeira linha de sqt
                    ativo.novo_negocio = False
                lista = ("88","84","83","82","58","59","56","57")
                dict_temp = {}
                if linha[d] in lista:
                    for item in lista:
                        dict_temp[item] = ativo.dado_bruto[int(item)]
                    #print(dict_temp,tempo_temp)
                #if linha[d] in ("88","84","83","82","58","59","56","57"):
                    #print(linha[d],linha[d+1])
                    #input("")
                    
                d = d+2
        except Exception as e:
            print(e)
            print(linha)
            #input("")
        if ativo.novo_negocio == True:
            #verifica se a linha é de um negócio válido ou registro complento anterior
            if ativo.dado_bruto[2] == "0": return 0
            if ativo.transacao:
                #if ativo.dado_bruto[8] == ativo.transacao[-1].id: return 0
                if int(ativo.dado_bruto[8]) <= int(ativo.transacao[-1].id): return 0 #corrige o bug do de volta para o futuro
            else:
                if ativo.dado_bruto[8] != "1": return 0
            #verifica o book cancelado em busca do cancelamento de oferta correspondente ao negócio
            while self.verificar_book_cancelado(self,*linha) == False:
                pass
            #self.add_transacao(linha[1],*ativo.dado_bruto)
            ativo.novo_negocio = False
            return 1


    def atualizar_book(self,*linha):
        #deleta o timestamp
        linha = list(linha)
        linha.append(linha[0])
        del linha[0]
        ativo = self.get_ativo(linha[1])
        if linha[2] == "A":
            foi_inserido = ativo.book.get_book(linha[4]).entrada.insert(int(linha[3]),[linha[5],linha[6],linha[7]])
            if Debug(): print("inserido: ",foi_inserido)
            ativo.book.get_book(linha[4]).add_volume(linha[5],int(linha[6]))
        if linha[2] == "U":
            if linha[4] == "0" and linha[3] == "0":
                newvol = int(ativo.book.get_book(linha[5]).entrada[int(linha[4])][1])-int(linha[7])
                if newvol: self.add_book_cancelado(linha[1], linha[6], str(newvol), linha[5], linha[8])
                if debug: print(str([linha[6],str(newvol),linha[5]]))
            book_temp = ativo.book.get_book(linha[5]).entrada[int(linha[4])]
            ativo.book.get_book(linha[5]).del_volume(book_temp[0],int(book_temp[1]))
            ativo.book.get_book(linha[5]).add_volume(linha[6],int(linha[7]))
            del ativo.book.get_book(linha[5]).entrada[int(linha[4])]
            ativo.book.get_book(linha[5]).entrada.insert(int(linha[3]),[linha[6],linha[7],linha[8]])
        if linha[2] == "D":
            if linha[3] == "1":
                tempbook = ativo.book.get_book(linha[4]).entrada[int(linha[5])]
                if linha[5] == "0":
                    self.add_book_cancelado(linha[1], tempbook[0], tempbook[1], linha[4], tempbook[2])
                    if debug: print(str([tempbook[0],tempbook[1],linha[4]]))
                ativo.book.get_book(linha[4]).del_volume(tempbook[0],int(tempbook[1]))
                del ativo.book.get_book(linha[4]).entrada[int(linha[5])]

            if linha[3] == "2":
                for x in range(0,int(linha[5])+1):
                    tempbook = ativo.book.get_book(linha[4]).entrada[0]
                    ativo.book.get_book(linha[4]).del_volume(tempbook[0],int(tempbook[1]))
                    self.add_book_cancelado(linha[1], tempbook[0], tempbook[1], linha[4], tempbook[2])
                    if debug: print(str([tempbook[0],tempbook[1],linha[4]]))
                    del ativo.book.get_book(linha[4]).entrada[0]
                if Debug(): print(ativo.book.get_book(linha[4]).get_preco_agrupado())
                if Debug(): input("")
            if linha[3] == "3":
                ativo.book.get_book("A").entrada = []
                ativo.book.get_book("V").entrada = []
                ativo.book.get_book("A").del_volume(0,0,tudo=True)
                ativo.book.get_book("V").del_volume(0,0,tudo=True)
                ativo.book.get_book("A").pre_book = True
                ativo.book.get_book("V").pre_book = True                
        if linha[2] == "E":
                ativo.book.get_book("A").pre_book = False
                ativo.book.get_book("V").pre_book = False
        #self.fazer_trade(ativo)        

        
        
        
        
        
        
        
        
        
        
        
        
        