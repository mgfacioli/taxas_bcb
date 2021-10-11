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

    cdi = TaxasBcb()
    cdi.codigo
    cdi.url
    cdi.taxa
    cdi.taxa_acumulada
    cdisub = cdi.get_subperiodo(data_inicio = '2021-01-01', data_fim= '2021-09-30')
    cdi.taxa_acumulada
    cdisubacc = cdi.get_subperiodo(data_inicio = '2021-01-01', data_fim= '2021-09-30', acc=True)
    cdi.taxa_acumulada


    cdi2020 = cdi.get_subperiodo('2020-01-01', '2020-12-31', acc=True)
    cdi.taxa_acumulada    
   

if __name__ == '__main__':
    main()