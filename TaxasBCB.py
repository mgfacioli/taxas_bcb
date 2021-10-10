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
#import matplotlib.pyplot as plt


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


    def __indice_acumulado(self, taxa):
        taxa['indice'] = ((taxa.iloc[:] / 100) + 1)
        taxa['indice_acc'] = taxa['indice'].cumprod()
        return taxa
                
        
    def retorna_taxa(self,  data_inicio=None, data_fim=None, acumular = True):
        try:
            self.__data_inicio = data_inicio
            self.__data_fim = data_fim
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
            
            if acumular == True:
                self.__subtaxa = TaxasBcb.__indice_acumulado(self, self.__subtaxa.copy())
            
            return self.__subtaxa
            
        except ValueError as Verr:
            print("Data desconhecida: " + str(Verr))                
        except:
            print(f"taxa {self._codigo} nao encontrado.")    
  
    def taxa_acumulada(self):
        return round(((self.__subtaxa.iloc[-1][2])-1)*100, 4)

    
# def grafico_linha(df, titulo, subtitulo, x, y, x_label, y_label):
#     fig, ax = plt.subplots(1, figsize=(10,8), facecolor='#fccd68')
#     ax.set_facecolor('#e7a2fc')
#     #Hide the right and top spines
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     #plt.ylim(0, 15)
#     plt.title(f'{titulo}\n{subtitulo}', fontsize = 18,  c='k')
#     plt.xlabel(f'\n{x_label}', fontsize = 14, c='k')
#     plt.ylabel(f'\n{y_label}', fontsize = 14, c = 'k')
#     line_1, = plt.plot(df.index, df[x], label = df.columns[0], linestyle='dashed')
#     line_2, = plt.plot(df.index, df[y], label = df.columns[1], linestyle='dotted')
#     plt.legend(handles=[line_1, line_2])
#     plt.savefig('/media/mgfacioli/mgf32g/Python/Projetos/financas/financeiras/' + titulo + '.png')

#     return None
   