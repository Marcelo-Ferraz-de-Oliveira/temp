class Trade(object):
    def __init__(self):
        self.direcao = "I"
        self.preco = 0.0
        self.stop = 0.0
        self.gain = 0.0
        self.fator = 0.0025
        self.resultado = 0
        self.dinheiro = 25000
        self.acumulado_atual = 0


class Indicador ():
    def __init__(self):
        self.valores = []
        self.divisores = [1,1,1,3000,1000]#/1300,3900
    def soma_indicadores(self):
        x = 0
        for valor in self.valores:
            x += valor[1]
        return x
    def add_indicador(self,tipo,numero,tempo_msc):
        if self.valores:
            for indice, valor in enumerate(self.valores): 
                if tipo == valor[0]:
                    if abs(numero) > abs(valor[1]):
                        del self.valores[indice]
                        self.valores.append([tipo,numero/self.divisores[tipo],tempo_msc])
                        return True
                    else:
                        return True
            self.valores.append([tipo,numero/self.divisores[tipo],tempo_msc])
        else:
            self.valores.append([tipo,numero/self.divisores[tipo],tempo_msc])
        #print(self.valores)
    def excluir_antigos(self,tempo,dif_tempo):
        houve_exclusao = False
        for indice, valor in enumerate(self.valores):
            if tempo - valor[2] > dif_tempo: #5000000:
                del self.valores[indice]
                houve_exclusao = True
                break
        if houve_exclusao: self.excluir_antigos(tempo,dif_tempo)