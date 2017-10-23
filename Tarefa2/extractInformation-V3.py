# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:21:54 2017

@author: guto
"""

import nltk
import compare_output
import sys,csv
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
                 'completo','re', 'vte', '2p','4p', '2portas', '4portas', '4pts']

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
                if(fields[x]=='2p' or fields[x]=='4p' or fields[x]=='2portas' or fields[x]=='4portas' or fields[x]=='2pts' or fields[x]=='4pts'):
                    num_p=fields[x][:1]
                    fields[x]=num_p+" "+"portas"
                elif(fields[x]=="vte"):
                    fields[x]="vidros e travas elétricas"
                opcionais = opcionais + fields[x] + ", "
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
    #o -2 é para tirar a vírgula e o espaço em branco no fim
    else: carro.opcionais = opcionais[:-2]
    
    carros.append(carro)
            

car_list_wrapper=[]
car_dict={}
print "-------------------------------------------------------------"    


for car in carros:
    car_dict["Marca"]=car.marca
    car_dict["Modelo"]=car.modelo
    car_dict["Motor"]=car.motor
    car_dict["Ano"]=car.ano
    car_dict["Combustivel"]=car.combustivel
    car_dict["Cambio"]=car.cambio
    car_dict["Preco"]=car.preco
    car_dict["Ar condicionado"]=car.arCond
    car_dict["Tipo de direcao"]=car.direcao
    car_dict["Cor"]=car.cor
    car_dict["Km"]=car.km
    car_dict["Opcionais"]=car.opcionais

    car_list_wrapper.append(car_dict)
    car_dict={}

car_list_expected=compare_output.read_expected_output()
precision_list,coverage_list=compare_output.compare_outputs(car_list_wrapper)
print "------------------------"
print "Resultados:"
for i in range(1,11):
        #print str(i)+"ª extração:"
        print "Extração\t{Valor esperado}"

        # print "Marca: " + carros[i-1].marca +"\t\t\t\t\t\t"+car_list_expected[i-1]['Marca']
        # print "Modelo: " + carros[i-1].modelo+"\t\t\t"+car_list_expected[i-1]['Modelo']
        # print "Motor: " + carros[i-1].motor+"\t\t\t\t\t\t"+car_list_expected[i-1]['Motor']
        # print "Ano: " + carros[i-1].ano+"\t\t\t\t\t\t"+car_list_expected[i-1]['Ano']
        # print "Combustivel: " + carros[i-1].combustivel+"\t\t\t\t\t\t"+car_list_expected[i-1]['Combustivel']
        # print "Cambio: " + carros[i-1].cambio+"\t\t\t\t\t\t"+car_list_expected[i-1]['Cambio']
        # print "Preco: " + carros[i-1].preco+"\t\t\t\t\t\t"+car_list_expected[i-1]['Preco']
        # print "Ar condicionado: " + carros[i-1].arCond+"\t\t\t\t\t\t"+car_list_expected[i-1]['Ar condicionado']
        # print "Tipo de direcao: " + carros[i-1].direcao+"\t\t\t\t\t\t"+car_list_expected[i-1]['Tipo de direcao']
        # print "Cor: " + carros[i-1].cor+"\t\t\t\t\t\t"+car_list_expected[i-1]['Cor']
        # print "Km: " + carros[i-1].km+"\t\t\t\t\t\t"+car_list_expected[i-1]['Km']
        # print "Opcionais: " + carros[i-1].opcionais+"\t\t\t\t\t\t"+car_list_expected[i-1]['Opcionais']

        print "Marca: " + carros[i-1].marca +"\t{"+car_list_expected[i-1]['Marca']+"}"
        print "Modelo: " + carros[i-1].modelo+"\t{"+car_list_expected[i-1]['Modelo']+"}"
        print "Motor: " + carros[i-1].motor+"\t{"+car_list_expected[i-1]['Motor']+"}"
        print "Ano: " + carros[i-1].ano+"\t{"+car_list_expected[i-1]['Ano']+"}"
        print "Combustivel: " + carros[i-1].combustivel+"\t{"+car_list_expected[i-1]['Combustivel']+"}"
        print "Cambio: " + carros[i-1].cambio+"\t{"+car_list_expected[i-1]['Cambio']+"}"
        print "Preco: " + carros[i-1].preco+"\t{"+car_list_expected[i-1]['Preco']+"}"
        print "Ar condicionado: " + carros[i-1].arCond+"\t{"+car_list_expected[i-1]['Ar condicionado']+"}"
        print "Tipo de direcao: " + carros[i-1].direcao+"\t{"+car_list_expected[i-1]['Tipo de direcao']+"}"
        print "Cor: " + carros[i-1].cor+"\t{"+car_list_expected[i-1]['Cor']+"}"
        print "Km: " + carros[i-1].km+"\t{"+car_list_expected[i-1]['Km']+"}"
        print "Opcionais: " + carros[i-1].opcionais+"\t{"+car_list_expected[i-1]['Opcionais']+"}"
        print "\n"

        print "Índices:"
        print "Precisão: "+str(precision_list[i-1]*100)+"%"
        print "Cobertura: " + str(coverage_list[i - 1]*100)+"%"
        print "----------------------------------------"

print "Resultado geral"
print "Média da precisão: "+str((sum(precision_list)/len(precision_list))*100)+"%"
print "Média da cobertura: "+str((sum(coverage_list)/len(coverage_list))*100)+"%"
