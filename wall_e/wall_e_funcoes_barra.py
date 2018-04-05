'''
Created on 9 de nov de 2017

@author: marcelo
'''
class Barra_preco(object):
    def __init__(self,preco):
        self.preco = preco
        self.vol_c = 0
        self.vol_v = 0
    def add_volume_v(self,volume):
        self.vol_v += volume
    def add_volume_c(self,volume):
        self.vol_c += volume

class Barra(object):
    def __init__(self,preco):
        self.preco_inicial = preco
        self.barras_preco = []
        x = Barra_preco(preco)
        self.barras_preco.append(x)
            
            
        
class Barras(object):
    def __init__(self, p, step):#p - número de pontos da barra, step - degrau mínimo de mudança de preço do ativo
        self.p = p
        self.step = step
        self.barras_ind = []
        #x = Barra()
        #self.barras_ind.append(x)
    def __barra_by_preco(self,preco):
        for barra in self.barras_ind[-1].barras_preco:
            #print(preco,barra.preco)
            if barra.preco == preco: return barra
        return False
    
    def __add_barra(self,preco_inicial):
        x = Barra(preco_inicial)
        self.barras_ind.append(x)
    
    def __add_preco(self,preco):
        x = Barra_preco(preco)
        self.barras_ind[-1].barras_preco.append(x)
        #if Debug():print("Adicionado preco",preco)
        
    def add_volume(self,volume,preco, direcao):
        if not self.barras_ind:
            x = Barra(preco)
            self.barras_ind.append(x)
        if self.barras_ind[-1].preco_inicial + (self.p*self.step) <= preco or self.barras_ind[-1].preco_inicial - (self.p*self.step) >= preco:
            self.__add_barra(preco)
        if not self.__barra_by_preco(preco): self.__add_preco(preco)
        barra = self.__barra_by_preco(preco)
        if direcao == "A": barra.add_volume_c(volume)
        if direcao == "V": barra.add_volume_v(volume)
        #if Debug():print("Acicionado volume de venda",volume,preco)
    
if __name__ == "__main__":
    teste = Barras(5,0.01)
    teste.add_volume(100,10,"A")
    teste.add_volume(100,9.99,"V")
    teste.add_volume(200,9.98,"V")
    teste.add_volume(400,9.97,"V")
    teste.add_volume(700,9.96,"V")
    teste.add_volume(200,9.95,"V")
    teste.add_volume(200,9.94,"V")
    teste.add_volume(200,9.93,"V")
    teste.add_volume(200,9.92,"V")
    teste.add_volume(200,9.91,"V")
    teste.add_volume(200,9.90,"V")
    teste.add_volume(200,9.89,"V")
    teste.add_volume(200,9.88,"V")
    for indice, barras in enumerate(teste.barras_ind):
        for barra in barras.barras_preco:
            print(indice, barra.preco,barra.vol_c,barra.vol_v)
