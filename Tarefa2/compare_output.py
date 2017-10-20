# -*- coding: utf-8 -*-
def read_expected_output():
    output=open("expected-output.txt","r")
    car_list=[]
    car={}
    #lê a primeira linha
    output.readline()
    line = output.readline()
    while line !='':
        if(line=="\n"):
            car_list.append(car)
            car={}
            line = output.readline()
        elif (line==""):
            break
        else:
            comp_splitted = line.split(":")
            #print comp_splitted
            car[comp_splitted[0]] = comp_splitted[1][1:-1]
            line = output.readline()

    car_list.append(car)
    return car_list

def compare_outputs(car_list_wrapper):
    car_list_output=read_expected_output()
    precision_list=[]
    coverage_list=[]
    #print "aqui"
    for i in range(0,len(car_list_wrapper)):
        precision_count,coverage_count=0.0,0.0
        filled_fields=0
        output_filled_fields=0
        #print car_list_output[i]
        #print car_list_wrapper[i]
        for comp in car_list_output[i].keys():
            if(car_list_output[i][comp]!="N/I"):
                output_filled_fields+=1
                #se os campos forem iguais, o contador de precisao aumenta
                #o lado direito do or é para remover espaços posteriores, ex: comparar 'preto' e 'preto '
                if((car_list_wrapper[i][comp]==car_list_output[i][comp]) or(car_list_wrapper[i][comp][:-1]==car_list_output[i][comp])):
                    precision_count+=1
                #se a lista derivada do wrapper tem um campo preenchido no componente em que a lista
                #esperada tivesse um campo preenchido, a cobertura acresce mais um
                #ele também é um campo preenchido, por isso acrescenta os campos preenchidos
                if(car_list_wrapper[i][comp]!="N/I"):
                    coverage_count+=1
                    filled_fields += 1

        #print "filled fields", filled_fields
        precision=precision_count/filled_fields
        coverage=coverage_count/output_filled_fields

        precision_list.append(precision)
        coverage_list.append(coverage)

    print "------------------------"
    print "Resultados:"
    for i in range(1,11):

        print str(i)+"ª extração:"
        print "Precisão: "+str(precision_list[i-1])
        print "Cobertura: " + str(coverage_list[i - 1])

        print ""
    print "Resultado geral"

    print "Média da precisão: "+str(sum(precision_list)/len(precision_list))
    print "Média da cobertura: "+str(sum(coverage_list)/len(coverage_list))
