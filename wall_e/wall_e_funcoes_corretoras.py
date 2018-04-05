
class Corretora(object):
    def __init__(self):
        self.codigo = 0
        self.passivo = 0
        self.ativo = 0
        self.leilao = 0
        self.direto = 0


class Corretoras(object):
    def __init__(self, indicadores = False,volume_total = 0):
        self.codigos = []
        self.indicadores = False
        if indicadores:
            self.indicadores = True
            self.volume_total = volume_total
            self.volume_soma = []
            self.posicao = []
            self.percentual = []
    def __add_corretora(self,codigo):
        setattr(self,"p"+str(codigo),Corretora())
        self.codigos.append(codigo)
        #print(str(self.get_corretora(codigo)))
    def get_corretora(self,codigo):
        return getattr(self,"p"+str(codigo), None)
    def get_all_corretoras(self):
        dicio = {}
        for x in self.codigos:
            dicio = {**dicio,**{x: self.get_corretora(x).ativo + self.get_corretora(x).passivo}}
        return dicio
    def add_vol_corretora(self,codigo1,codigo2,volume,direcao):
        if direcao == "L":
            return False
        if not self.get_corretora(codigo1):
            self.__add_corretora(codigo1)
        if not self.get_corretora(codigo2):
            self.__add_corretora(codigo2)
        
        corretora1 = self.get_corretora(codigo1)
        corretora2 = self.get_corretora(codigo2)
        if direcao == "A":
            corretora1.ativo += volume
            corretora2.passivo -= volume
        if direcao == "V":
            corretora2.ativo -= volume
            corretora1.passivo += volume
        if direcao == "I":
            corretora1.direto += volume
            corretora2.direto += volume
        if self.indicadores:
            for codigo, indice in enumerate(self.codigos):
                pass
