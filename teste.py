#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 09:13:52 2021

@author: mgfacioli

@purpose:  testes para projeto de captura e processamento de informacoes do banco central do brasil - taxas e indices

"""

import TaxasBCB


##############################################################################
# Entrada do progrma
def main():

    cdi = TaxasBCB.TaxasBcb()
    cdidf = cdi.retorna_taxa(data_inicio = '2021-01-01', data_fim= '2021-09-30')
    cdi._url
    cdi.taxa_acumulada()

    cdi2020 = cdi.retorna_taxa('2020-01-01', '2020-12-31', acumular=True)
    cdi.taxa_acumulada()    


    ipca = TaxasBcb(codigo=433)
    dfipca = ipca.retorna_taxa()    

if __name__ == '__main__':
    main()