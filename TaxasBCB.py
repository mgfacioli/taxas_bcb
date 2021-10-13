#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:12:23 2021

@author: mgfacioli

@purpose: projeto de captura e processamento de informacoes do banco central do brasil - taxas e indices

"""


##############################################################################
# importando modulos
import pandas as pd

__author__ = """\n""".join(['Marcelo G Facioli (mgfacioli@yahoo.com.br)'])
__version__ = "0.0.1"


##############################################################################
# definindo funcoes do projeto

class TaxasBcb(object):
    def __init__(self, url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json', codigo = 11):
            self.url = url.format(codigo)
            self.codigo = str(codigo)         
            try:
                self.taxa = pd.read_json(self.url)
                self.taxa['data'] = pd.to_datetime(self.taxa['data'], dayfirst=True)
                self.taxa.set_index('data', inplace=True)
            except:
                print(f"taxa {self.codigo} nao encontrado.") 
                
    def get_subperiodo(self, data_inicio=None, data_fim=None, acc = False):
        return self.SubPeriodo(self, data_inicio, data_fim, acc)

    
    class SubPeriodo(object):
        def __init__(self, outer, data_inicio=None, data_fim=None, acc = False):
            self.outerClass = outer
            self.data_inicio = pd.to_datetime(data_inicio)
            self.data_fim = pd.to_datetime(data_fim)
            self.acc = acc
            self.__taxa_acumulada = 0

        def create_subper(self):
            try:
                if self.data_fim == None:
                    if self.data_inicio == None:
                        subper = self.outerClass.taxa[self.taxa.index[0]:self.taxa.index[-1]]
                    else:
                        subper = self.outerClass.taxa[self.data_inicio:self.taxa.index[-1]]
                else:
                    if self.data_inicio == None:
                        subper = self.outerClass.taxa[self.taxa.index[0]:self.data_fim]
                    else:
                        subper = self.outerClass.taxa[self.data_inicio:self.data_fim]
                return subper            
            except ValueError as Verr:
                print("Data desconhecida: " + str(Verr))                

                    
        def create_acc_subper(self):
            if self.acc:
                df = self.create_subper().copy()
                df['indice'] = ((df.iloc[:] / 100) + 1)
                df['indice_acc'] = df['indice'].cumprod()                
                return df


        def get_acc_return_tax(self):
            return round(((self.create_acc_subper().iloc[-1][2])-1)*100, 4)