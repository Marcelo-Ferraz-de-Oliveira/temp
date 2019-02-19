#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from wall_e.wall_e_funcoes import *
#import time
#import os
from wall_e import wall_e_funcoes
from wall_e.wall_e_funcoes import * 
import pexpect
import multiprocessing
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from tornado.gen import multi
import gc
import os
import glob
#import gevent

preco = multiprocessing.Value('f',0.0)


app = Flask(__name__)
app.secret_key = 'enois'

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

@app.route('/')
def index():

    #return render_template('lista.html, titulo="Jogos",jogos=lista)
    return render_template('index.html')


@app.route('/_add_numbers')
def add_numbers():
    global preco
    return jsonify(result=round(preco.value,2))


#Abre o arquivo com os dados brutos
dir_compactados = "/media/sf_Google_Drive/Dados_Bolsa_Wall_e/"
dir_trabalho = "/media/sf_Google_Drive/Dados_Bolsa_Wall_e/Resultados/"
dir_temp = "/home/marcelo/Documentos/"

datafiles = lista_a_partir(lista_arquivos(dir_compactados),datetime.date(2017,1,1),datetime.date(2019,12,31))
arquivos_bugados = open(dir_trabalho+"arquivos_bugados.txt","w")
ativos_selecionados_iniciais = ["PETR4","VALE3","ABEV3","B3SA3","BBAS3","BBDC4","ITUB4","BOVA11","BRFS3","ITSA4","PETR3","BBDC3","CSNA3","EMBR3","GOAU4","USIM5"]##"PETR4"]

#nome_arquivo = "teste_bruto_2017-11-23"

def Ler_negocio(nome_arquivo,dir_trabalho,dir_temp,ativos_selecionados):
    ativos_prontos = []
    for ativo in ativos_selecionados:
        arquivo = dir_trabalho+nome_arquivo+".log.pasta/"+ativo+"*"
        #print(arquivo)
        if glob.glob(arquivo):
            ativos_prontos.append(ativo)
    #print(ativos_prontos)
    for ativo in ativos_prontos:
        #print(ativo)
        ativos_selecionados.remove(ativo)
        #print(ativos_selecionados)
    if not ativos_selecionados:
        print("Dia já executado! "+nome_arquivo)
        return 0
    else:
        print("Executando leitura de: ",ativos_selecionados)
        #return 0

    print("começando",nome_arquivo)
    x = 1000
    #data = get_data_do_arquivo(nome_arquivo)
    inicio = datetime.datetime.now()  
    arquivo_completo = dir_trabalho+nome_arquivo+".log"
    arquivo_temp = dir_temp+nome_arquivo+".log"
    try:
        a = open(arquivo_temp)
        a.close()
        print(nome_arquivo,"já foi extraído!")
    except:
        try:
            print("Iniciando descompressão de ",nome_arquivo) 
            print(pexpect.run("tar -jxvf  "+nome_arquivo+".tar.bz2 -C "+dir_temp, cwd=dir_compactados, timeout = 300000))
        except:
            print("ARQUIVO NÃO EXISTE!!!!")
            return 0
        print(nome_arquivo,"tempo de descompressão: ",datetime.datetime.now()-inicio)
    inicio = datetime.datetime.now()  
    
    inicializar(is_debug = False,caminho_arquivo=arquivo_completo)


    if Debug(): print("abrindo arquivo")
    try:
        bruto = open(arquivo_temp,"r")
    except:
        print("Erro ao abrir o arquivo!")
        return 0
    grupo_ativos = Grupo_ativos()
    if Debug(): print("criando os objetos")
    #for codigo in ativos_registrados:
    #    ativo.set_ativo(codigo.upper())
    ativos_registrados = []
    #ativos_rejeitados2 = []
    #ativos_rejeitados = []
    #Verificando cada linha do arquivo com dados brutos...
    #parar = 0
    if Debug(): print("comecou")
    linhas = ler(bruto)
    ultima_linha = None
    esta_sqt = 0
    for linha in linhas:
        if "fim de arquivo" in linha: break
    #for linha in bruto:
        #posicao = bruto.tell()
        #linhas = ler(bruto)
        
            #time.sleep(0.01)
        #bruto.seek(posicao)
        #continue
        #retira o simbolo !, que é o indicador de final de registro da cedro
        
        
        #TESTA PARA VERIFICAR SE O ARQUIVO NÃO FOI INTERROMPIDO NO MEIO ("CONNECTION CLOSED BY FOREIGN HOST")
        #if linha.find("refused") != -1:
        #    print(nome_arquivo)
        #    arquivos_bugados.write(nome_arquivo+"connection refused\n")
        #    arquivos_bugados.flush()
        #    break
        #else:
            #continue

        if len(linha) > 1000:
            print("Linha muito longa! Será descartada!")
            continue
        
        if linha.find("host") != -1 or linha.find("refused") != -1:
            for codigo in ativos_registrados:
                grupo_ativos.fazer_trade(grupo_ativos.get_ativo(codigo),zerar_tudo=True)
            linha = arrumar_linha_timestamp(linha)
            info = str(converter_utc(linha[0]))
            print("Falha em: "+info,linha)
            print("Última linha:",ultima_linha)
            
            
            arquivos_bugados.write(info+"\n")
            arquivos_bugados.flush()
            continue
            #break
        #else:
        #    continue
        if "Trying" in linha:
            continue
        linha = arrumar_linha_timestamp(linha)
        #print(linha)#if Debug(): print(linha)
        if linha[1] == "SYN":
            continue
        if (linha[1].find("sqt ") != -1) or (linha[1].find("bqt ") != -1):
            if esta_sqt == 0: 
                esta_sqt = 1
            temp = linha[1].split(" ")
            temp[1] = temp[1].upper()
            if not grupo_ativos.get_ativo(temp[1]):
                if (temp[1] in ativos_selecionados):#comente para rodar todos os ativos no arquivo 
                    #if temp[1] not in ativos_rejeitados:    
                        #    pass
                            #grupo_ativos.set_ativo(temp[1],step = 5, x = x)
                        #else:
                            ativos_registrados.append(temp[1])
                            grupo_ativos.set_ativo(temp[1],x = x)
                            #ativos_selecionados = ativos_registrados#descomente para rodar todos os ativos no arquivo
        else:
            if esta_sqt == 1:
                #print(ativos_registrados)
                if  not ativos_registrados:
                    print("Todos os ativos já foram lidos, saindo! ", nome_arquivo)
                    print(pexpect.run("rm  "+nome_arquivo+".log", cwd=dir_temp, timeout = -1))
                    return 0
                else:
                    esta_sqt = 3
                    print("Analisando os ativos de : ",nome_arquivo,ativos_registrados)
            if Debug(): print(str(linha))
            if Debug(): print(temp[1])
            if Debug(): print(ativos_registrados)
            if Debug(): print(ativos_selecionados)
            #if Debug(): input("")
        #verifica se a primeira linha corresponde a uma informação de trade
        if linha[1] == "V":
            try:
                if linha[2] in ativos_registrados:
                    #grupo_ativos.gravar_bruto(linha[2],linha2)
                    if Debug(): print(str(linha))
                    grupo_ativos.atualizar_gqt(*linha)
                    #print(e)
            except Exception as e:
                print(str(e))
                print("Erro na linha:", linha)
                #input("")
                continue            
                raise
        if linha[1] == "T":
            #if linha[3] == "88" and linha[4] == "F":
            #    break
            #if linha[3] == "105958":
                #parar = 1
            #    pass
            #if ativo.get_ativo(linha[1]).book.A.pre_book == False:
                #parar = 1
            #    pass
            #print(str(linha))
            try:
                if linha[2] in ativos_registrados:
                    #grupo_ativos.gravar_bruto(linha[2],linha2)
                    if Debug(): print(str(linha))
                    grupo_ativos.atualizar_dados(*linha)
                    #preco_externo.value = grupo_ativos.get_ativo(linha[2]).transacao[-1].preco
                    #input("")
                    #print(e)
            except Exception as e:
                print(str(e))
                print("Erro na linha:",linha)
                continue
                raise
            #if parar == 1:
            #    input("")
            #    pass
#            if len(ativo.get_ativo(linha[1]).transacao) > 1:
#                print(str(ativo.get_ativo(linha[1]).transacao[len(ativo.get_ativo(linha[1]).transacao)-1]))
        elif linha[1] == "B":
            #if ativo.get_ativo(linha[1]).book.A.pre_book == False:
                #parar = 1
            #    pass
            #if linha[2] == "U":
                #parar = 1
                #pass
            #try:
                #if linha[2] == "D" and linha[3] == "2":
                    #parar = 1
                    #pass
                #else:
                    #parar = 0
                    #pass
            #except:
                #pass
            #try:
                #if linha[5] == "12.78" or linha[6] == "12,78":
                    #parar = 1
            #        pass
                #else:
                    #parar = 0
            #        pass
            #except:
            #    pass
            #print(str(linha))
            try:
                if linha[2] in ativos_registrados:
                    #grupo_ativos.gravar_bruto(linha[2],linha2)
                    if Debug(): print(str(linha))
                    grupo_ativos.atualizar_book(*linha)
                    #print(e)
            except Exception as e:
                #raise
                print(str(e))
                print("Erro na linha:",linha)
                #raise
                continue
            #print("Posirção 0 de compra: "+str(ativo.gnome_arquivoet_ativo("VIVT4").book.get_book("A").get_preco_agrupado())+" - "+str(ativo.get_ativo("VIVT4").book.get_book("A").get_volume_by_pos(0)))
            #print("Posição 0 de venda: "+str(ativo.get_ativo("VIVT4").book.get_book("V").get_preco_agrupado())+" - "+str(ativo.get_ativo("VIVT4").book.get_book("V").get_volume_by_pos(0)))
            #try:
            #    book_venda = ""
            #    book_compra = ""
            #    for x in range(0,20): 
            #        book_venda = book_venda + str(ativo.get_ativo("VIVT4").book.get_book("V").entrada[x])
            #        book_compra = book_compra + str(ativo.get_ativo("VIVT4").book.get_book("A").entrada[x])
            #except:
            #    pass
            #print("Posição no book de compra original :"+ book_compra)
            #print("Posição no book de venda original :"+book_venda)
            #if parar == 1:
                #input("")
            #    pass
        ultima_linha = linha
        del linha

    print(nome_arquivo, "tempo de execução: ",datetime.datetime.now()-inicio)
    inicio = datetime.datetime.now()
    for codigo in ativos_registrados:
        grupo_ativos.gravar_transacoes(codigo,grupo_ativos)
        #del grupo_ativos.get_ativo(codigo)
    bruto.close()
    del grupo_ativos
    gc.collect()
        
    print(pexpect.run("rm  "+nome_arquivo+".log", cwd=dir_temp, timeout = -1))
    print(nome_arquivo, "tempo de gravação: ",datetime.datetime.now()-inicio)
    x += 100 

    
pool = multiprocessing.Pool(processes=3)
for nome_arquivo in datafiles:
    print(nome_arquivo)
    pool.apply_async(Ler_negocio, args=([nome_arquivo, dir_trabalho, dir_temp, ativos_selecionados_iniciais]))
pool.close()
pool.join()

    #Ler_negocio(nome_arquivo, dir_trabalho, dir_temp)
#app.run(host = "0.0.0.0",port=8080,debug=False)
#arquivos_bugados.close()


