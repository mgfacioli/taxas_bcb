#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 09:13:52 2021

@author: mgfacioli

@purpose:  testes para projeto de captura e processamento de informacoes do banco central do brasil - taxas e indices

"""

import TaxasBCB
import matplotlib.pyplot as plt


def grafico_linha(df, titulo, subtitulo, x, y, x_label, y_label):
    fig, ax = plt.subplots(1, figsize=(10,8), facecolor='#fccd68')
    ax.set_facecolor('#e7a2fc')
    #Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #plt.ylim(0, 15)
    plt.title(f'{titulo}\n{subtitulo}', fontsize = 18,  c='k')
    plt.xlabel(f'\n{x_label}', fontsize = 14, c='k')
    plt.ylabel(f'\n{y_label}', fontsize = 14, c = 'k')
    line_1, = plt.plot(df.index, df[x], label = df.columns[0], linestyle='dashed')
    line_2, = plt.plot(df.index, df[y], label = df.columns[1], linestyle='dotted')
    plt.legend(handles=[line_1, line_2])
    plt.savefig('/media/mgfacioli/mgf32g/Python/Projetos/financas/financeiras/' + titulo + '.png')

    return None


##############################################################################
# Entrada do progrma
def main():
    # dt_inicio_consulta = '2021-01-01'
    # dt_fim_consulta    = '2021-09-30'
    
    # # vamos comecar carregando o cdi do periodo em analise
    # cdi = busca_taxa_bcb(12)
    # selic = busca_taxa_bcb(11)
    
    # cdi.info()
    # selic.info()
    
    # merge_outer = pd.merge(cdi, selic, how='outer', left_index=True, right_index=True)
    # merge_inner = pd.merge(cdi, selic, how='inner', left_index=True, right_index=True)
    # merge_inner.rename(columns={'valor_x': 'CDI', 'valor_y': 'Selic'}, inplace=True)
    # merge_inner['diff'] = merge_inner['CDI'] - merge_inner['Selic']
    
    # grafico_linha(merge_inner, '01 CDI x Selic - Dia a Dia - 1986 a 2021', 'Fonte: Banco Central do Brasil', 'CDI', 'Selic', 'Data', 'CDI/Selic')
    
    # merge92x93x94 = merge_inner['1992':'1994']
    
    # grafico_linha(merge92x93x94, '02 CDI x Selic - Dia a Dia - 1992 a 1994', 'Fonte: Banco Central do Brasil', 'CDI', 'Selic', 'Data', 'CDI/Selic')
    
    # merge_2010x2021 = merge_inner['2010':'2021']

    # grafico_linha(merge_2010x2021, '03 CDI x Selic - Dia a Dia - 2010 a 2021', 'Fonte: Banco Central do Brasil', 'CDI', 'Selic', 'Data', 'CDI/Selic')

    
    # resultado = merge_inner.groupby(merge_inner.index.year)['diff'].agg(['std', 'max', 'min'])

    # resultado.to_csv('/media/mgfacioli/mgf32g/Python/Projetos/financas/financeiras/CDIxSelic.csv', sep = ';', decimal = ',')

    cdi = TaxasBCB.TaxasBcb()
    cdidf = cdi.retorna_taxa(data_inicio = '2021-01-01', data_fim= '2021-09-30')
    cdi._url
    cdi.taxa_acumulada()


    ipca = TaxasBcb(codigo=433)
    dfipca = ipca.retorna_taxa()    

if __name__ == '__main__':
    main()