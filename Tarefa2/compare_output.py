from itertools import chain
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
    #print car_list
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

        for comp in car_list_output[i].keys():
            if (car_list_wrapper[i][comp] != "N/I"):
                # print car_list_wrapper[i][comp]
                filled_fields += 1

            if(car_list_output[i][comp]!="N/I"):
                output_filled_fields+=1
                #incrementa o contador se o campo no wrapper deveria ter sido preenchido
                #por isso fica dentro deste if
                if (car_list_wrapper[i][comp]!="N/I"):
                    coverage_count += 1

                wrapper_value=list(chain.from_iterable(map(lambda a : a.split(" "),map(lambda a : a.strip(),car_list_wrapper[i][comp].split(",")))))
                expected_value=list(chain.from_iterable(map(lambda a : a.split(" "),map(lambda a : a.strip(),car_list_output[i][comp].split(",")))))
                #se os campos forem iguais, o contador de precisao aumenta
                #strip() é para remover espaços posteriores, ex: comparar 'preto' e 'preto '
                if set(wrapper_value)==set(expected_value):
                    precision_count+=1

        precision=precision_count/filled_fields
        coverage=coverage_count/output_filled_fields

        precision_list.append(precision)
        coverage_list.append(coverage)

    return precision_list,coverage_list

def compare_outputs_per_field(car_list_wrapper, car_list_output):
    expected_fields = {'Cor': 0, 'Ar condicionado': 0, 'Ano': 0, 'Combustivel': 0, 'Marca': 0, 'Km': 0, 'Opcionais': 0,
                     'Cambio': 0, 'Modelo': 0, 'Tipo de direcao': 0, 'Motor': 0, 'Preco': 0}

    filled_fields={'Cor': 0, 'Ar condicionado': 0, 'Ano': 0, 'Combustivel': 0, 'Marca': 0, 'Km': 0, 'Opcionais': 0, 'Cambio':0, 'Modelo': 0, 'Tipo de direcao': 0, 'Motor': 0, 'Preco': 0}
    cover_fields = {'Cor': 0, 'Ar condicionado': 0, 'Ano': 0, 'Combustivel': 0, 'Marca': 0, 'Km': 0, 'Opcionais': 0,
                     'Cambio': 0, 'Modelo': 0, 'Tipo de direcao': 0, 'Motor': 0, 'Preco': 0}
    precise_fields = {'Cor': 0, 'Ar condicionado': 0, 'Ano': 0, 'Combustivel': 0, 'Marca': 0, 'Km': 0, 'Opcionais': 0,
                     'Cambio': 0, 'Modelo': 0, 'Tipo de direcao': 0, 'Motor': 0, 'Preco': 0}

    for i in range(0, len(car_list_wrapper)):
        for comp in car_list_output[i].keys():
            if (car_list_wrapper[i][comp] != "N/I"):
                # print car_list_wrapper[i][comp]
                filled_fields[comp]+=1

            if (car_list_output[i][comp] != "N/I"):
                expected_fields[comp]+=1
                # incrementa o contador se o campo no wrapper deveria ter sido preenchido
                # por isso fica dentro deste if
                if (car_list_wrapper[i][comp] != "N/I"):
                    cover_fields[comp]+=1


                wrapper_value = list(chain.from_iterable(
                    map(lambda a: a.split(" "), map(lambda a: a.strip(), car_list_wrapper[i][comp].split(",")))))
                expected_value = list(chain.from_iterable(
                    map(lambda a: a.split(" "), map(lambda a: a.strip(), car_list_output[i][comp].split(",")))))
                # se os campos forem iguais, o contador de precisao aumenta
                # strip() é para remover espaços posteriores, ex: comparar 'preto' e 'preto '
                if set(wrapper_value) == set(expected_value):
                    precise_fields[comp]+=1
    return expected_fields,filled_fields,precise_fields,cover_fields
