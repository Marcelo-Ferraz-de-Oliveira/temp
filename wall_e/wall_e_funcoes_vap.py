
class Volume (object):
    def __init__(self):
        self.A = 0
        self.V = 0
        self.I = 0
        self.L = 0

class VAP (object):
    def __init__(self):
        self.precos = []
        self.tipos = ["A","V","I","L"]
        pass
    def __set_preco(self,preco):
        setattr(self,"n"+str(preco),Volume())
        self.precos.append(preco)
        return True
    def __get_preco(self,preco):
        return getattr(self,"n"+str(preco), None)
    def add_volume(self,preco,tipo,volume):
        global app
        objeto = self.__get_preco(preco)
        if objeto:
            setattr(objeto,tipo, getattr(self.__get_preco(preco),tipo)+volume)
        else:
            self.__set_preco(preco)
            setattr(self.__get_preco(preco),tipo, getattr(self.__get_preco(preco),tipo)+volume)
        #lista = []
        #for x in self.precos:
        #    lista.append([x,int(self.get_volume(x,"A")),int(self.get_volume(x,"V"))])        
        #app.Criar_barras(lista)
        return True

    def del_volume(self,preco,tipo,volume):
        objeto = self.__get_preco(preco)
        if objeto:
            setattr(objeto,tipo, getattr(self.__get_preco(preco),tipo)-volume)
        else:
            self.__set_preco(preco)
            setattr(self.__get_preco(preco),tipo, getattr(self.__get_preco(preco),tipo)-volume)
        return True
    def get_volume(self,preco,tipo):
        return getattr(self.__get_preco(preco), tipo, 0)
