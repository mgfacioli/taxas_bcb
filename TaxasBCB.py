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
            self._url = url.format(codigo)
            self._codigo = str(codigo)
            self.__data_inicio = None
            self.__data_fim = None
            self.__subtaxa = None
            self.__acumular = None


    def __indice_acumulado(self, taxa):
        taxa['indice'] = ((taxa.iloc[:] / 100) + 1)
        taxa['indice_acc'] = taxa['indice'].cumprod()
        return taxa
                
        
    def retorna_taxa(self,  data_inicio=None, data_fim=None, acumular = True):
        try:
            self.__data_inicio = data_inicio
            self.__data_fim = data_fim
            self.__acumular = acumular
            taxa = pd.read_json(self._url)
            taxa['data'] = pd.to_datetime(taxa['data'], dayfirst=True)
            taxa.set_index('data', inplace=True)
            
            if data_fim == None:
                if self.__data_inicio == None:
                    self.__subtaxa = taxa[taxa.index[0]:taxa.index[-1]]
                else:
                    self.__subtaxa = taxa[pd.to_datetime(self.__data_inicio):taxa.index[-1]]
            else:
                if self.__data_inicio == None:
                    self.__subtaxa = taxa[taxa.index[0]:pd.to_datetime(self.__data_fim)]
                else:
                    self.__subtaxa = taxa[pd.to_datetime(self.__data_inicio):pd.to_datetime(self.__data_fim)]
            
            if self.__acumular:
                self.__subtaxa = TaxasBcb.__indice_acumulado(self, self.__subtaxa.copy())
            
            return self.__subtaxa
            
        except ValueError as Verr:
            print("Data desconhecida: " + str(Verr))                
        except:
            print(f"taxa {self._codigo} nao encontrado.")    
  
    def taxa_acumulada(self):
        if self.__acumular:
            return round(((self.__subtaxa.iloc[-1][2])-1)*100, 4)
        else:
            print('Para obter a taxa acumulada, o parametro acumular do metodo retorna_taxa deve ser True.')


   