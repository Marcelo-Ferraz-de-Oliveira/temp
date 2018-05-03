#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from wall_e.wall_e_funcoes import *
#import time
#import os
from wall_e import wall_e_funcoes
from wall_e.wall_e_funcoes import * 
import pexpect

#Abre o arquivo com os dados brutos
dir_compactados = "/media/sf_Google_Drive/Dados_Bolsa_Wall_e/"
dir_trabalho = "/media/sf_Dados_Bolsa_Wall_e/"

datafiles = lista_a_partir(lista_arquivos(dir_compactados),datetime.date(2018,4,1),datetime.date(2018,4,4))
arquivos_bugados = open(dir_trabalho+"arquivos_bugados.txt","a")
ativos_selecionados = ["DOLK18","PETR4"]##"PETR4"]

#nome_arquivo = "teste_bruto_2017-11-23"
x = 1000
for nome_arquivo in datafiles:
    data = get_data_do_arquivo(nome_arquivo)
    inicio = datetime.datetime.now()  
    arquivo_completo = dir_trabalho+nome_arquivo+".log"
    try:
        a = open(arquivo_completo)
        a.close()
        print(nome_arquivo,"já foi extraído!")
    except:
        try:
            print("Iniciando descompressão de ",nome_arquivo) 
            print(pexpect.run("tar -jxvf  "+nome_arquivo+".tar.bz2 -C "+dir_trabalho, cwd=dir_compactados, timeout = 300000))
        except:
            print("ARQUIVO NÃO EXISTE!!!!")
            continue
        print(nome_arquivo,"tempo de descompressão: ",datetime.datetime.now()-inicio)
    inicio = datetime.datetime.now()  
    
    inicializar(is_debug = False,caminho_arquivo=arquivo_completo)


    if Debug(): print("abrindo arquivo")
    try:
        bruto = open(wall_e_funcoes.nome_arquivo,"r")
    except:
        print("Erro ao abrir o arquivo!")
        continue
    grupo_ativos = Grupo_ativos()
    if Debug(): print("criando os objetos")
    #for codigo in ativos_registrados:
    #    ativo.set_ativo(codigo.upper())
    ativos_registrados = []
    ativos_rejeitados2 = []
    ativos_rejeitados = []
    #Verificando cada linha do arquivo com dados brutos...
    parar = 0
    if Debug(): print("comecou")
    linhas = ler(bruto)
    for linha in linhas:
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

        if linha.find("host") != -1 or linha.find("refused") != -1:
            for codigo in ativos_registrados:
                grupo_ativos.fazer_trade(grupo_ativos.get_ativo(codigo),zerar_tudo=True)
            linha = arrumar_linha_timestamp(linha)
            info = nome_arquivo+"-"+str(converter_utc(linha[0]))
            print(info)
            arquivos_bugados.write(info+"\n")
            arquivos_bugados.flush()
            continue
            #break
        #else:
        #    continue
        
        linha2 = linha
        linha = arrumar_linha_timestamp(linha)
        #print(linha)#if Debug(): print(linha)
        if linha[1] == "SYN":
            continue
        if linha[1].find("sqt ") != -1:
            temp = linha[1].split(" ")
            temp[1] = temp[1].upper()
            if not grupo_ativos.get_ativo(temp[1]):
                if temp[1] in ativos_selecionados:#comente para rodar todos os ativos no arquivo 
                    if temp[1] not in ativos_rejeitados:    
                        #if "DOL" in temp[1] or "WDO" in temp[1] or "IND" in temp[1] or "WIN" in temp[1]:
                        #    pass
                            #grupo_ativos.set_ativo(temp[1],step = 5, x = x)
                        #else:
                            ativos_registrados.append(temp[1])
                            grupo_ativos.set_ativo(temp[1],x = x)                            
                            #ativos_selecionados = ativos_registrados#descomente para rodar todos os ativos no arquivo
            if Debug(): print(str(linha))
            if Debug(): print(temp[1])
            if Debug(): print(ativos_registrados)
            if Debug(): print(ativos_selecionados)
            #if Debug(): input("")
        #verifica se a primeira linha corresponde a uma informação de trade
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
            '''try:
                if linha[2] == 'PETR4':
                    print(vars(grupo_ativos.get_ativo(linha[2]).transacao[1]))
                    input("")
            except:
                pass'''
            try:
                if linha[2] in ativos_selecionados:
                    #grupo_ativos.gravar_bruto(linha[2],linha2)
                    if Debug(): print(str(linha))
                    grupo_ativos.atualizar_dados(*linha)
                    #print(e)
            except Exception as e:
                print(str(e))
                continue
            
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
                if linha[2] in ativos_selecionados:
                    #grupo_ativos.gravar_bruto(linha[2],linha2)
                    if Debug(): print(str(linha))
                    grupo_ativos.atualizar_book(*linha)
                    #print(e)
            except Exception as e:
                print(str(e))
                continue
            #print("Posição 0 de compra: "+str(ativo.get_ativo("VIVT4").book.get_book("A").get_preco_agrupado())+" - "+str(ativo.get_ativo("VIVT4").book.get_book("A").get_volume_by_pos(0)))
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
        del linha

    print(nome_arquivo, "tempo de execução: ",datetime.datetime.now()-inicio)
    inicio = datetime.datetime.now()
    for codigo in ativos_registrados:
        grupo_ativos.gravar_transacoes(codigo,grupo_ativos)
    bruto.close()
    del grupo_ativos
        
    #print(pexpect.run("rm  "+nome_arquivo+".log", cwd="/media/sf_Dados_Bolsa_Wall_e/", timeout = -1))
    print(nome_arquivo, "tempo de gravação: ",datetime.datetime.now()-inicio)
    x += 100
arquivos_bugados.close()



