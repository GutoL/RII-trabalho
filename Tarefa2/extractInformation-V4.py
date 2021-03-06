# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:21:54 2017

@author: guto
"""

import nltk
import compare_output
#import sys,csv
from removeAcentos import remover_acentos

marcasList = ["wolksvagem","wv","chevrolet","ford","mercedes","ferrari","audi",
          "renault"]
          
coresList = ["azul","vermelho","branco","prata","verde","cinza","amarelo","marinho",
             "preto", "onix"]

combustivelList = ["gasolina","flex","alcool"]

cambioList = ["manual","automatico","c-manual","c-automatico"]

direcaoList = ["mecanica", "hidraulica", "dm", "dh"]

opcionaisList = ['radio', 'CD', 'MP3', 'alarme', 'airbag','travas',
                 'vidro','eletrica','bluetooth','abs','sensor','couro', 'roda','liga',
                 're', 'vte', '2p','4p', '2portas', '4portas', '4pts']

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
        virgula = True    
        include = True        
        
        for x in xrange(len(fields)):
            
            fields[x] = fields[x].replace('.','')
            fields[x] = fields[x].replace('\n','')
            
            
            # get air conditioning
            if evaluateToken(fields[x],negacaoList):
                
                if len(fields) > 1 and evaluateToken(fields[x+1],arList):
                    arcond = "Não"
                    virgula = False   
                    #continue
                
            if ("ar" == fields[x]) and arcond != "Não":
                arcond = "Sim"
                virgula = False                
                continue
            
            
            
            #get fuel type
            elif evaluateToken(fields[x],combustivelList):
                fuel = fields[x]
                virgula = False
                continue
            
            #get car exchange ¯\_(ツ)_/¯
            elif evaluateToken(fields[x],cambioList):
                cambio = fields[x]
                virgula = False
                continue
                
            #get price
            elif "R$" in fields[x]:
                
                if len(fields)==1:
                    preco = fields[x]+",00"
                    virgula = False
                    include = False
                    continue
                else:
                    preco = fields[x]+fields[x+1]+",00"
                    virgula = False
                    include = False
                    continue
            
            # get steering type
            elif evaluateToken(fields[x],direcaoList):
                if fields[x] == "dm":
                    direcao = "Mecanica"
                    virgula = False
                    continue
                    
                elif fields[x] == "dh":
                    direcao = "hidraulica"
                    virgula = False
                    continue
                else:
                    direcao = fields[x]
                    virgula = False
                    continue
                
            #get color
            elif evaluateToken(fields[x],coresList):
                    cor = cor+fields[x]+" "
                    virgula = False
                    continue
                
            
            #get km
            #print fields[x]
            elif ("km" in fields[x] or "kms" in fields[x]):
                km = fields[x-1]
                virgula = False
                include = False
                continue
            
            #get optional :v
            #elif(evaluateToken(fields[x],opcionaisList)):
            else:
                
                # get conditional air if complete
                if evaluateToken(fields[x],['completo']):
                    arcond = "Sim"
                    
                if(fields[x]=='2p' or fields[x]=='4p' or fields[x]=='2portas' or fields[x]=='4portas' or fields[x]=='2pts' or fields[x]=='4pts'):
                    num_p=fields[x][:1]
                    fields[x]=num_p+" "+"portas"
                elif(fields[x]=="vte"):
                    fields[x]="vidros e travas eletricas"

                if include == True and not is_number(fields[x]) and '00' != fields[x]:
                    opcionais = opcionais + fields[x]+" "
                    continue
        
        if virgula == True :
            #print opcionais,
            opcionais = opcionais + ", "
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

    if(opcionais == "" or opcionais == " " or opcionais == ", " ):
        carro.opcionais = "N/I"
    #O opcionais.split cria uma lista separando os opcionais por virgulas
    #filter aplica a função lambda na lista, removendo todos os espaços em branco dela
    #map pega cada elemento b da lista e retira os espaços antes e depois deste (ex: ' basico ' se torna 'basico')
    #finalmente, damos um join com os elementos da lista criados, criando uma string sem demasiada quantidade de virgulas e espaços
    else: carro.opcionais = ", ".join(map(lambda b : b.strip(), filter(lambda a : a!= ' ', opcionais.split(","))))
    
    
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
print "Resultados por extração:"
for i in xrange(1,len(car_list_wrapper)+1):
       
        print "Extração\t{Valor esperado}"

        

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
        
        if carros[i-1].opcionais[-2] == ",":
            carros[i-1].opcionais = carros[i-1].opcionais[:-2]
            
        print "Opcionais: " + carros[i-1].opcionais+"\t{"+car_list_expected[i-1]['Opcionais']+"}"
        print ""
                
        
        #print "Índices:"
        #print "Precisão: "+str(precision_list[i-1]*100)+"%"
        #print "Cobertura: " + str(coverage_list[i - 1]*100)+"%"
        print "----------------------------------------"

print "Resultado geral"
print "Média da precisão: "+str((sum(precision_list)/len(precision_list))*100)+"%"
print "Média da cobertura: "+str((sum(coverage_list)/len(coverage_list))*100)+"%"

expected_fields,filled_fields,precise_fields=compare_output.compare_outputs_per_field(car_list_wrapper,car_list_expected)
#a nomenclatura é count_expected_fields (cef), count_filled_fields (cff) e assim por diante
cef,cff,cpf=0,0,0
print "------------------------------"
print "Resultados por campo:"
for comp in car_list_wrapper[0].keys():
    print comp
    print "Precisão: "+ str(precise_fields[comp]) +"/"+str(filled_fields[comp])
    print "Cobertura: "+str(precise_fields[comp])+"/"+str(expected_fields[comp])
    cef+=expected_fields[comp]
    cff+=filled_fields[comp]
    cpf+=precise_fields[comp]
    print ""

print "Resultado geral"
print "Média da precisão: "+str(cpf)+"/"+str(cff)
print "Média da cobertura: "+str(cpf)+"/"+str(cef)