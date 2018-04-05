#from wall_e.wall_e_funcoes_utils import *

class Preco (object):
    def __init__(self):
        self.volume = 0

class Books (object):
    #parâmetro preço é em string, e volume em int
    def __init__(self,direcao):
        self.entrada = []
        self.preco_agrupado = []
        self.pre_book = True
        self.direcao = direcao
    def get_preco_agrupado(self):
        if self.direcao == "V":
            resultado = sorted(self.preco_agrupado, key=float)
            #print ("V",resultado)
            #input("")
            return resultado
        elif self.direcao == "A":
            resultado = sorted(self.preco_agrupado, key=float, reverse=True)
            #print ("V",resultado)
            #input("")
            return resultado
        else:
            return -1
    def get_preco_by_pos(self,posicao):
        if posicao < len(self.preco_agrupado):
            if self.direcao == "V":
                return sorted(self.preco_agrupado, key=float)[posicao]
            elif self.direcao == "A":
                return sorted(self.preco_agrupado,key=float,reverse=True)[posicao]
            else:
                return -1
        else:
            return -1
    def __set_preco(self,preco):
        setattr(self,"n"+preco,Preco())
        self.preco_agrupado.append(preco)
        return True
    def __get_preco(self,preco):
        return getattr(self,"n"+preco, None)
    def __del_preco(self,preco):
        delattr(self, "n"+preco)
        self.preco_agrupado.remove(preco)
        #input("")
        return True
    def get_volume_by_pos(self,posicao):
        precos = self.get_preco_agrupado()
        #print(precos)
        #input("")
        if posicao < len(precos):
            preco = precos[posicao]
            return self.get_volume(preco)
        else:
            return 0
    def get_volume(self,preco):
        objeto = self.__get_preco(preco)
        if objeto:
            return self.__get_preco(preco).volume
        else:
            return 0
    def add_volume(self,preco,volume):
        #if debug: print(preco, self.get_volume(preco))
        objeto = self.__get_preco(preco)
        if objeto:
            objeto.volume += volume
        else:
            self.__set_preco(preco)
            self.__get_preco(preco).volume += volume
        #if debug: print(preco, self.get_volume(preco))
        #print(self.entrada)
        #print(self.get_preco_agrupado())
        #input("")
    def del_volume(self,preco,volume, tudo=False):
        #if debug: print(preco, self.get_volume(preco))
        if tudo == True:
            for valor in self.preco_agrupado:
                delattr(self, "n"+valor)
            self.preco_agrupado = []
            return True
        objeto = self.__get_preco(preco)
        if objeto:
            objeto.volume -= volume
            #if debug: print(preco, self.get_volume(preco))
            if objeto.volume <= 0:
                self.__del_preco(preco)
                #if debug: print("deletado ",preco)
            else:
                return True
        #print(self.entrada)
        #input("")
class Book_completo(object):
    def __init__(self):
        self.A = Books("A")
        self.V = Books("V")
    def get_book(self,direcao):
        return getattr(self,direcao)

