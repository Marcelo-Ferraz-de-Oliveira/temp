'''
Sistema para obtenção e registro de dados de ativos da BMF&BOVESPA
O sistema registra os dados de negócio e livro de ofertas dos ativos selecionados
Os dados são obtidos em "tempo real" através do sistema de cotações Cedro Crystal Datafeed
A conexão é feita via telnet nativo do linux, usando a biblioteca pexpect
Informações sobre o sistema estã disponíveis em: http://promo.cedrotech.com/crystal-data-feed-solucoes-de-market-data
Para entender a sintaxe do sistema, acesse: http://files.cedrotech.com/Downloads/Cedro/documentos/Documentacao_Crystal_Data_Feed.pdf
'''

import pexpect
from datetime import datetime, time

workdir = "/wall_e"#edite inserindo o diretório de trabalho
username = "mfogoiania"#edite inserindo seu usuário de acesso ao Crystal DataFeed
password = "102030"#edite inserindo sua senha de acesso ao Crystal DataFeed
logfile = open(workdir+"/log.txt", "a")
'''
Classe para receber os dados, adicionar um timestamp no formato unix_epoch em microsegundos ao fina de cada linha, e salvar em arquivo. 
A classe recebe como parâmetro um file handle e ela própria simula um, uma vez que o pexpect espera receber um file handle como parâmetro
'''

class TimestampedFile(object):
    def __init__(self,file):
        self.file = file
    def write(self,data):
        ts = int(((datetime.utcnow() - datetime(1970,1,1)).total_seconds())*1000000)
        data = data.decode("utf-8")#Usado para decodificar a string gerada pela biblioteca pexpect, originária do python 2.7
        data = data.replace("\r","")
        data = data.replace("\n",":"+str(ts)+"\n")
        self.file.write(data)
    def flush(self):
        self.file.flush()
    def close(self):
        self.file.close()

now = datetime.now()

#gera automaticamente o final do código do Índice Futuro
if now >= datetime(2017,8,16) and now < datetime(2017,10,18):
    indice = str("v17")
if now >= datetime(2017,10,18) and now < datetime(2017,12,13):
    indice = str("z17")
if now >= datetime(2017,12,13) and now < datetime(2018,2,14):
    indice = str("g18")
if now >= datetime(2018,2,14) and now < datetime(2018,4,18):
    indice = str("j18")
if now >= datetime(2018,4,18) and now < datetime(2018,6,13):
    indice = str("m18")
if now >= datetime(2018,6,13) and now < datetime(2018,8,15):
    indice = str("q18")
if now >= datetime(2018,8,15) and now < datetime(2018,10,17):
    indice = str("v18")
if now >= datetime(2018,10,14) and now < datetime(2018,12,12):
    indice = str("z18")
if now >= datetime(2018,12,12) and now < datetime(2019,2,13):
    indice = str("g19")

#gera automaticamente o final do código do Dólar Futuro
if now >= datetime(2017,7,30) and now < datetime(2017,8,31):
    dolar = str("u17")
if now >= datetime(2017,8,31) and now < datetime(2017,9,29):
    dolar = str("v17")
if now >= datetime(2017,9,29) and now < datetime(2017,10,31):
    dolar = str("x17")
if now >= datetime(2017,10,31) and now < datetime(2017,11,30):
    dolar = str("z17")
if now >= datetime(2017,11,30) and now < datetime(2017,12,29):
    dolar = str("f18")
if now >= datetime(2017,12,29) and now < datetime(2018,1,31):
    dolar = str("g18")
if now >= datetime(2018,1,31) and now < datetime(2018,2,28):
    dolar = str("h18")
if now >= datetime(2018,2,28) and now < datetime(2018,3,29):
    dolar = str("j18")
if now >= datetime(2018,3,29) and now < datetime(2018,4,30):
    dolar = str("k18")
if now >= datetime(2018,4,30) and now < datetime(2018,5,30):
    dolar = str("m18")
if now >= datetime(2018,5,30) and now < datetime(2018,6,29):
    dolar = str("n18")
if now >= datetime(2018,6,29) and now < datetime(2018,7,31):
    dolar = str("q18")
if now >= datetime(2018,7,31) and now < datetime(2018,8,31):
    dolar = str("u18")
if now >= datetime(2018,8,31) and now < datetime(2018,9,28):
    dolar = str("v18")
if now >= datetime(2018,9,28) and now < datetime(2018,10,31):
    dolar = str("x18")
if now >= datetime(2018,10,31) and now < datetime(2018,11,30):
    dolar = str("z18")
if now >= datetime(2018,11,30) and now < datetime(2018,12,28):
    dolar = str("f19")

#matriz com todos os ativos a serem registrados
#todos os ativos da composição do IBOVESPA, contratos de Índice e Dólar, padrão e mini, e contratos de DI futuro de maior liquidez
ativos = ["taee11",
          "flry3",
          "mglu3",#que barbaridade!
          "igta3",
          "vvar11",
          "sapr11",
          "bova11",
          "di1f19",
          "di1f20",
          "di1f21",
          "di1f22",
          "di1f23",
          "di1f24",
          "di1f25",
          "petr4",
          "goau4",
          "mrfg3",
          "ecor3",
          "itub4",
          "bbdc4",
          "usim5",
          "abev3",
          "bbas3",
          "lame4",
          "vale3",
          "petr3",
          "bbdc3",
          "b3sa3",
          "itsa4",
          "brfs3",
          "ugpa3",
          "ciel3",
          "krot3",
          "vivt4",
          "bbse3",
          "ccro3",
          "lren3",
          "jbss3",
          "radl3",
          "hype3",
          "eqtl3",
          "embr3",
          "sanb11",
          "sbsp3",
          "pcar4",
          "wege3",
          "brkm5",
          "timp3",
          "ggbr4",
          "cpfe3",
          "brml3",
          "cmig4",
          "egie3",
          "klbn11",
          "fibr3",
          "rent3",
          "rail3",
          "csna3",
          "mult3",
          "natu3",
          "estc3",
          "suzb3",
          "qual3",
          "csan3",
          "brap4",
          "elet3",
          "mrve3",
          "smls3",
          "cyre3",
          "enbr3",
          "cple6",
          "elet6"]
ativos.append("ind"+indice)
ativos.append("win"+indice)
ativos.append("dol"+dolar)
ativos.append("wdo"+dolar)
#função para iniciar a leitura dos dados via telnet, usando a biblioteca pexpect, e repassá-los à função TimeStampedFile
def rodar():
    try:
        print("Conectando em: "+str(datetime.now()))
        telconn = pexpect.spawn("telnet datafeed1.cedrofinances.com.br 81")
        telconn.logfile_read=TimestampedFile(open(workdir+"/dado_bruto.log","a"))
        telconn.delaybeforesend = 0
        telconn.expect(".")
        telconn.sendline("")
        telconn.expect(":")
        telconn.sendline(username)
        telconn.expect(":")
        telconn.sendline(password)
        telconn.expect("d")
    #faz a requisição de informações para cada ativo da lista
        for ativo in ativos:
            telconn.sendline("sqt "+ativo)
            telconn.sendline("bqt "+ativo)
    except:
        rodar()
    while 1==1:
        try:
            telconn.expect("\n")
        except pexpect.TIMEOUT:#pode ocorrer timeout caso não sejam obtidas novas informações por algum período de tempo
            pass
        except Exception as e:#em caso de outra exceção (como a queda do sistema), a função é chamada novamente para tentar uma reconexão
            print("Falha em: "+str(datetime.now()))
            print(e)
            rodar()
        if datetime.now().time() >= time(18,30,0):#encerra o sistema às 18:30 - horário de Brasília
            telconn.close()
            break

print("Iniciando em: "+str(datetime.now()))
rodar()


#inicia o sistema para coletar os dados do gqt após âs 18:30
telconn = pexpect.spawn("telnet datafeed1.cedrofinances.com.br 81")
telconn.logfile_read=TimestampedFile(open(workdir+"/dado_bruto.log","a"))
telconn.delaybeforesend = 0
telconn.expect(".")
telconn.sendline("")
telconn.expect(":")
telconn.sendline(username)
telconn.expect(":")
telconn.sendline(password)
telconn.expect("d")
#faz a requisição de gqt para cada ativo da lista
step = 50000
for ativo in ativos:
    posicao = 0
    while posicao < 2000000:
        telconn.sendline("gqt "+ativo+" N "+str(step)+" "+str(posicao)+" 1")
        posicao += step
        while 1==1:
            try:
                valor = telconn.expect([":E:1",":GQT:",pexpect.TIMEOUT])
                if valor == 0:
                    break
                if valor == 1:
                    break
            
            except Exception as e:
                print(e)
                raise



#Datar e compactar os arquivos
print(pexpect.run("mv dado_bruto.log dado_bruto_"+str(datetime.now().date())+".log", cwd=workdir, timeout = -1))
print(pexpect.run("tar -cvjf dado_bruto_"+str(datetime.now().date())+".tar.bz2 dado_bruto_"+str(datetime.now().date())+".log", cwd=workdir, timeout = 10000))
print(pexpect.run("truncate -s 0 dado_bruto.log dado_bruto_"+str(datetime.now().date())+".log", cwd=workdir, timeout = -1))   
print(pexpect.run("mv dado_bruto_"+str(datetime.now().date())+".log dado_bruto.log", cwd=workdir, timeout = -1))   
