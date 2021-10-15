#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 09:13:52 2021

@author: mgfacioli

@purpose:  testes para projeto de captura e processamento de informacoes do banco central do brasil - taxas e indices

"""

#import TaxasBCB
from TaxasBCB import TaxasBcb

##############################################################################
# Entrada do progrma
def main():

    cdi = TaxasBcb(codigo=11)
    cdi.codigo
    cdi.url
    cdi.taxa
    
    cdi2021 = cdi.get_subperiodo(data_inicio = '2021-01-01', data_fim= '2021-09-30', acc=True)
    cdi2021.create_subper()
    cdi2021.create_acc_subper()
    cdi2021.get_acc_return_tax()
    cdi2021.group_by_subper()
    cdi2021.group_by_subper('Y')
    

    cdi2020 = cdi.get_subperiodo(data_inicio = '2020-01-01', data_fim= '2020-12-31', acc=True)
    cdi2020.create_subper()
    cdi2020.create_acc_subper()
    cdi2020.get_acc_return_tax()
    
    selic = TaxasBcb(codigo = 12)
    selic.codigo

    selic2020 = selic.get_subperiodo(data_inicio = '2020-01-01', data_fim= '2020-12-31', acc=True)
    selic2020.create_subper()
    selic2020.create_acc_subper()
    selic2020.get_acc_return_tax()

    ipca = TaxasBcb(codigo=433)
    ipca.url

    ipca2020 = ipca.get_subperiodo(data_inicio = '2020-01-01', data_fim= '2020-12-31', acc=True)
    ipca2020.create_subper()
    ipca2020.create_acc_subper()
    ipca2020.get_acc_return_tax()
    ipca2020.group_by_subper()
    ipca2020.group_by_subper('Y')

if __name__ == '__main__':
    main()