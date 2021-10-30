#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 09:13:52 2021

@author: mgfacioli

@purpose:  testes para projeto de captura e processamento de informacoes do banco central do brasil - taxas e indices

"""

#import TaxasBCB
from TaxasBCB import BcbTables

##############################################################################
# Entrada do progrma
def main():

    cdi = BcbTables(bcb_table_code = 11)
    cdi.bcb_table_code
    cdi.url
    cdi.table
    
    cdi2021 = cdi.get_subperiod(begin_date = '2021-01-01', end_date = '2021-10-29', acc=True)
    cdi2021.create_subper()
    cdi2021.create_acc_subper()
    cdi2021.get_acc_return_tax()
    cdi2021.group_by_subper()
    cdi2021.group_by_subper('Y')
    

    cdi2020 = cdi.get_subperiod(begin_date = '2020-01-01', end_date= '2020-12-31', acc=True)
    cdi2020.create_subper()
    cdi2020.create_acc_subper()
    cdi2020.get_acc_return_tax()
    cdi2020.group_by_subper()
    
    selic = BcbTables(bcb_table_code = 12)
    selic.bcb_table_code

    selic2020 = selic.get_subperiod(begin_date = '2020-01-01', end_date= '2020-12-31', acc=True)
    selic2020.create_subper()
    selic2020.create_acc_subper()
    selic2020.get_acc_return_tax()
    

    ipca = BcbTables(bcb_table_code=433)
    ipca.url

    ipca2020 = ipca.get_subperiod(begin_date = '2020-01-01', end_date= '2020-12-31', acc=True)
    ipca2020.create_subper()
    ipca2020.create_acc_subper()
    ipca2020.get_acc_return_tax()
    ipca2020.group_by_subper()
    ipca2020.group_by_subper('Y')
    
    ipca2021 = ipca.get_subperiod(begin_date = '2021-01-01', end_date= '2021-10-31', acc=True)
    ipca2021.create_subper()
    ipca2021.create_acc_subper()
    ipca2021.get_acc_return_tax()
    ipca2021.group_by_subper()
    ipca2021.group_by_subper('Y')



if __name__ == '__main__':
    main()