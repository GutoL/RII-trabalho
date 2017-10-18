# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:21:54 2017

@author: guto
"""

import nltk
from removeAcentos import remover_acentos

marcasList = ["wolksvagem","wv","chevrolet","ford","mercedes","ferrari","audi",
          "renault"]
          
coresList = ["azul","vermelho","branco","prata","verde","cinza","amarelo","marinho",
             "preto"]

combustivelList = ["gasolina","flex","alcool"]

cambioList = ["manual","automatico","c-manual","c-automatico"]

direcaoList = ["mecanica", "hidraulica", "dm", "dh"]

opcionaisList = ['radio', 'CD', 'MP3', 'alarme', 'airbag','travas',
                 'vidro','eletrica','bluetooth','abs','sensor','couro', 'roda','liga',
                 'completo','re']

negacaoList = ['sem','menos','exceto']
arList = ['ar','arcond','ar condicionado', 'condicionado', 'ac']
################################## Classes ##################################################

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


class Document(object):
    def __init__(self,head,body):
        self.head = head
        self.body = body
    
    def __init__(self):
        a=1

################################### Methods #################################################
        
'''def evaluateToken(token,lista):
   
    if token.lower() in lista:
        return True
    return False'''


def evaluateToken(token,lista):
        
    stemmer = nltk.stem.RSLPStemmer()
    
    for item in lista:
        
        if stemmer.stem(token.lower()) == stemmer.stem(item.lower()):
            return True
        
    return False


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
    
##################################### Pre processing ###############################################
file = open("corpus-real.txt","r")

lines = []

documents = []
document = Document()

for line in file:
    if (len(line)>1):
        line = line.replace('/',' ')
        lines.append(remover_acentos(line))

file.close
typeOfLine = 0

for line in lines:
    if typeOfLine == 0:
        head = line.split(" ")
        document.head =  head
        typeOfLine = 1
    else:
        body = line.split(",")
        document.body = body
        typeOfLine = 0
        documents.append(document)
        document = Document()
    

newBody = []
newDocuments = []
tokkens = []
    
for doc in documents:
    for body in doc.body:
        tokens = body.split(" ")
        
        for token in tokens:
            if token is not "":
                tokkens.append(token)
        
        newBody.append(tokkens)
        tokkens = []        
    
    newDocument = Document()
    newDocument.head = doc.head
    newDocument.body = newBody
    newDocuments.append(newDocument)
    newBody = []
    
################################### Extract ############################################################

i=1
carros = []

for doc in newDocuments:
    
    carro = Car()
    modelo = ''
    marca = 'N/I'
    motor = 'N/I'
    ano = 'N/I'
    
    fuel = 'N/I'
    cambio = 'N/I'
    preco = 'N/I'
    arcond = 'N/I'
    direcao = 'N/I'
    cor = ''
    km = 'N/I'
    opcionais = ''
   
    for field in doc.head:
        
        field = field.replace('\n','')
        
        
        #get motor power
        if (is_number(field) and "." in field)or(field == "V8" or field == "V12"):
            motor = field
            continue
        
        # get mark
        if evaluateToken(field,marcasList):
            marca = field
            continue
    
        # get model
        if  not is_number(field):
            modelo = modelo+field+" "
    
        #get year
        if is_number(field):
            
            if(int(field)>1000):
                ano = field
                continue
            elif int(field) > 30:
                ano = "19"+field
                continue
            else:
                ano = "20"+field
                continue
    
    for fields in doc.body:
        
                
        for x in xrange(len(fields)):
            
            fields[x] = fields[x].replace('.','')
            field = field.replace('\n','')
            
            
            # get air conditioning
            if evaluateToken(fields[x],negacaoList):
                
                if len(fields) > 1 and evaluateToken(fields[x+1],arList):
                    arcond = "Não"
                    continue
                
            if "ar" == fields[x] and arcond != "Não":
                arcond = "Sim"
                continue
            
            
            
            #get fuel type
            if evaluateToken(fields[x],combustivelList):
                fuel = fields[x]
                continue
            
            #get car exchange ¯\_(ツ)_/¯
            if evaluateToken(fields[x],cambioList):
                cambio = fields[x]
                continue
                
            #get price
            if "R$" in fields[x]:
                
                if len(fields)==1:
                    preco = fields[x]
                    continue
                else:
                    preco = fields[x]+fields[x+1]
                continue
            
            # get steering type
            if evaluateToken(fields[x],direcaoList):
                if fields[x] == "dm":
                    direcao = "Mecanica"
                    
                elif fields[x] == "dh":
                    direcao = "hidraulica"
                else:
                    direcao = fields[x]
                
            #get color
            if evaluateToken(fields[x],coresList):
                    cor = cor+fields[x]+" "
                    continue
            
            #get km
            #print fields[x]
            if ("km" in fields[x] or "kms" in fields[x]):
                km = fields[x-1]
                continue
                
            #get optional :v
            if(evaluateToken(fields[x],opcionaisList)):
                opcionais = opcionais + fields[x]+" "
                continue
 
################################### Print ############################################################           
    
    carro.marca = marca
    carro.modelo = modelo
    carro.motor = motor
    carro.ano = ano
    
    carro.combustivel = fuel
    carro.cambio = cambio
    carro.preco = preco 
    carro.arCond = arcond
    carro.direcao = direcao
    
    if(cor == ""):
        carro.cor = "N/I"
    else: carro.cor = cor
    
    carro.km = km
    
    if(opcionais == ""):
        carro.opcionais = "N/I"
    else: carro.opcionais = opcionais
    
    carros.append(carro)
            

print "-------------------------------------------------------------"    
        
for car in carros:
    print "Marca: "+car.marca
    print "Modelo: "+car.modelo
    print "Motor: "+car.motor
    print "Ano: "+car.ano
    print "Combustivel: "+car.combustivel
    print "Cambio: "+car.cambio
    print "Preco: "+car.preco
    print "Ar condicionado: "+car.arCond
    print "Tipo de direcao: "+car.direcao
    print "Cor: "+car.cor
    print "Km: "+car.km
    print "Opcionais: "+car.opcionais
    print "\n"

    
    
