# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:45:58 2017

@author: guto
"""

#http://www.nltk.org/book/ch07.html

from removeAcentos import remover_acentos

file = open("corpus.txt","r")

#print type(file)

class Car(object):
    def __init__(self, marca, modelo, km, ano,preco,motor,combustivel,cambio,
                direcao, cor, arCond,opcionais):
        self.marca = marca
        self.modelo = modelo        
        self.km = km
        self.ano = ano
        
        self.preco = preco
        self.motor = motor        
        self.combustivel = combustivel        
        self.cambio = cambio
        self.direcao = direcao
        self.cor = cor
        self.arCond = arCond
        self.opcionais = opcionais
        
    def __init__(self):
        self.marca = "N/I"
        self.modelo = "N/I"        
        self.km = "N/I"
        self.ano = "N/I"
        
        self.preco = "N/I"
        self.motor = "N/I"        
        self.combustivel = "N/I"        
        self.cambio = "N/I"
        self.direcao = "N/I"
        self.cor = "N/I"
        self.arCond = "N/I"
        self.opcionais = "N/I"

#https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
def is_number(s):
    try:
        float(s.lower()) # for int, long and float
    except ValueError:
        try:
            complex(s.lower()) # for complex
        except ValueError:
            return False

    return True

marcas = ["wolksvagen","wv","chevrolet","ford","mercedes","ferrari","audi",
          "renault"]
cores = ["azul","vermelho","branco","prata","verde","cinza","amarelo"]

combustivel = ["gasolina","flex","alcool"]

cambio = ["manual","automatico","automatica"]


def evaluateToken(token,lista):
    if token.lower() in lista:
        return True
    return False
        
        
    
lines = []

for line in file:
    if (len(line)>1):
        line = line.replace('/',' ')
        lines.append(remover_acentos(line))


typeOfLine = 0
i=1
limit = 40


carros = []
carro = Car()

for line in lines:
    '''if i > limit:
        break
    i = i +1'''
    
    modelo = ''
    marca = 'N/I'
    motor = 'N/I'
    ano = 'N/I'
    
    arcond = 'N/I'
    
    
    if typeOfLine == 0:
        tokens = line.split(' ')
        
        #print len(tokens) AQUI
        for token in tokens:
            
            token = token.replace('\n',' ')            
            
            #check motor
            if(((is_number(token) == True)and("." in token))
                or(token == "V8" or token == "V12")):
                motor = token
                continue            
            
            #check marcas
            if(evaluateToken(token,marcas)):
                #print token                
                marca = token
                continue  # returns the control to the beginning of the while loop            
            
            elif(not is_number(token)):
                modelo = modelo + token+" "  
                continue
            
            #check ano
            if((is_number(token) == True)):
                
                if(int(token)>30) and (int(token)<100):
                    ano = "19"+token
                elif(int(token)<30) and (int(token)<100):
                    ano = "20"+token
                else:
                    ano = token
                continue
        
        
        carro.marca = marca
        carro.modelo = modelo
        carro.motor = motor
        carro.ano = ano
        
        typeOfLine = 1
    
    
    elif(typeOfLine == 1):
        tokens = line.split(',')
        
        for token in tokens:
            #https://stackoverflow.com/questions/8270092/python-remove-all-whitespace-in-a-string
            token = token.strip()            
            
            # check ar condicionado
            if ("ar" == token) or ("ar cond" in token):
                arcond = "Sim"
                #continue
            
            # check preço
            if ("$" in token):
                carro.preco = "R"+token[token.index("$"):]
                #continue
            
            # check direção
            if ("direcao" in token):
                carro.direcao = token[token.index("direcao")+8:]
                #continue
            
            if "dh" in token:
                carro.direcao = "hidraulica"
                #continue
                
            elif "dm" in token:
                carro.direcao = "mecanica"
                #continue
            
            #check combustivel
            if evaluateToken(token,combustivel):
                carro.combustivel = token
                #continue
            
            #check cambio
            if evaluateToken(token,cambio):
                carro.cambio = token
                #continue            
            
          
                     
            
            
        typeOfLine = 0
        
        carro.arCond = arcond
        
        carros.append(carro)
        carro = Car()
    

for car in carros:
    print "Marca: "+str(car.marca)    
    print "Modelo: "+str(car.modelo)
    print "Motor: "+str(car.motor)
    print "Ano: "+str(car.ano)
    print "Ar condicionado: "+(car.arCond)
    print "Preço: "+(car.preco)
    print "Direção: "+(car.direcao) 
    print "Combustivel: "+(car.combustivel)
    print "Cambio: "+(car.cambio)    
    print "\n"
    

print "End"



