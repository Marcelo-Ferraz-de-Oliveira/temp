'''
Created on 29 de mai de 2017

@author: marcelo
'''
from tkinter import *
import time

root = Tk()
#root.geometry("350x300+300+300")
class Janela:
    def __init__(self, root):
        self.root = root
        self.barra = []
    def Add_barra(self,preco,volume,root):
        tamanho  = len(self.barra)
        self.barra.append(preco)
        canvas = Canvas(root,height=10)
        canvas.grid(row=tamanho,column=1)
        canvas.create_rectangle(0,0,volume/100,100,fill="#00ff00")
        label = Label(root,text=str(preco),height=1)
        label.grid(row=tamanho,column=0)
    def Criar_barras(self,entradas):
        self.barra = []
        entradas = list(entradas)
        print (entradas)
        for x in sorted(entradas):
            print(x)
            self.Add_barra(x[0],x[1],self.root)
            


        
app = Janela(root)
entradas = [[15,1000],[15.01,20000],[15.02,30000],[15.03,40000],[15.04,20000],[15.05,10000],[15.06,5000]]
app.Criar_barras(entradas)
root.update()
time.sleep(3)    
entradas = [[15,100],[15.01,200],[15.02,300],[15.03,100],[15.04,200],[15.05,100],[15.06,100]]
app.Criar_barras(entradas)    



while True:
    root.update()
#Button(root,text="parar", width=25, command=root.destroy).pack()
#root.mainloop()








