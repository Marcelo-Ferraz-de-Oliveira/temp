'''
Created on 19 de fev de 2019

@author: marcelo
'''
import os
import glob

ativo = 'PETR4'
dir_base = "/media/sf_Google_Drive/Dados_Bolsa_Wall_e/Resultados/"
lista_toda = os.listdir(dir_base)

for item in lista_toda:
    if "dado_bruto" in item:
        dir = item
        data = item.split(".")[0].split("_")[2]
        dir_atual = dir_base+dir
        arquivos = os.listdir(dir_atual)
        for arquivo in arquivos:
            print(arquivo)
            if data not in arquivo:
                os.rename(
                    os.path.join(dir_atual,arquivo),
                    os.path.join(dir_atual,data+"."+arquivo))
                novos = os.listdir(dir_atual)
                for novo in novos:
                    if arquivo in novo:
                        print(novo)
#print(dias_disp)
#print(diretorios)


'''
dias_disp = !ls -al {dir_base} | grep "^d"

#print(dias_disp)
for dia in dias_disp:
  dia_filtrado = dia.split(" ")
  for item in dia_filtrado:
    if 'dado' in item:
      dia_filtrado = item
      break
    continue
  nome_pasta = dia_filtrado
  dia_filtrado = dia_filtrado.split(".")  
  dia_filtrado = dia_filtrado[0].split("_")[2]
  print(dia_filtrado)
  #!mv {dir_base+nome_pasta+"/*"} {dir_base+nome_pasta+"/"+dia_filtrado+"*"}
  conteudo = !ls -l {dir_base+nome_pasta}
  for arquivo in conteudo[1:]:
    arquivo = arquivo.split(" ")[-1]
    print(arquivo)
    if dia_filtrado not in arquivo:
      !mv {dir_base+nome_pasta+"/"+arquivo} {dir_base+nome_pasta+"/"+dia_filtrado+"."+arquivo}
      !ls {dir_base+nome_pasta+"/"+dia_filtrado+"."+arquivo}

'''
