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
            self.taxa = pd.read_json(self.url)
            self.taxa['data'] = pd.to_datetime(self.taxa['data'], dayfirst=True)
            self.taxa.set_index('data', inplace=True)
            self.taxa_acumulada = 0

    
    def get_subperiodo(self,  data_inicio=None, data_fim=None, acc = False):
        try:       
            if data_fim == None:
                if data_inicio == None:
                    subper = self.taxa[self.taxa.index[0]:self.taxa.index[-1]]
                else:
                    subper = self.taxa[pd.to_datetime(data_inicio):self.taxa.index[-1]]
            else:
                if data_inicio == None:
                    subper = self.taxa[self.taxa.index[0]:pd.to_datetime(data_fim)]
                else:
                    subper = self.taxa[pd.to_datetime(data_inicio):pd.to_datetime(data_fim)]
            
            if acc:
                df = subper.copy()
                df['indice'] = ((df.iloc[:] / 100) + 1)
                df['indice_acc'] = df['indice'].cumprod()
                self.taxa_acumulada = round(((df.iloc[-1][2])-1)*100, 4)
                subper = df.copy()
            
            return subper
            
        except ValueError as Verr:
            print("Data desconhecida: " + str(Verr))                
        except:
            print(f"taxa {self.codigo} nao encontrado.") 
            
        
   