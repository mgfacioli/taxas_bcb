#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:12:23 2021

@author: mgfacioli

@purpose: Brazil's central bank information capture and 
            processing project - rates and indices 

"""

__author__ = """\n""".join(['Marcelo G Facioli (mgfacioli@yahoo.com.br)'])
__version__ = "0.0.1"


##############################################################################
# modules
import pandas as pd


##############################################################################
# project classes

class BcbTables(object):
    """
    Attributes
    ----------
    url : 
        The URL string to Brazilian Central Bank data api.
        The default is 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'
        where '11' is the code to CDI (Interbank Deposit Certificate) table.
    bcb_table_code : integer, optional
        The code of the desired table (see https://www.bcb.gov.br/estatisticas/indecoreestruturacao
        for a complete list.)
        Some examples:
            11 - CDI (Interbank Deposit Certificate)
            12 - Selic (Brazil economy's basic interest rate)
            188 - INPC (National consumer price index)
            433 - IPCA (Broad National Consumer Price Index).
    
    Methods
    -------
    get_subperiod (begin_date=None, end_date=None, acc = False)
        Creates an object instance that contains a subperiod of the selected  
        table.    
    """
    def __init__(self, 
                 url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json', 
                 bcb_table_code = 11):
        """
        Parameters
        ----------
        url : 
            The URL string to Brazilian Central Bank data api.
            The default is 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'
            where '11' is the code to CDI (Interbank Deposit Certificate) table.
        bcb_table_code : integer, optional
            The code of the desired table (see https://www.bcb.gov.br/estatisticas/indecoreestruturacao
            for a complete list.)
        """
        self.url = url.format(bcb_table_code)
        self.bcb_table_code = str(bcb_table_code)         
        try:
            self.table = pd.read_json(self.url)
            self.table['data'] = pd.to_datetime(self.table['data'], dayfirst=True)
            self.table.set_index('data', inplace=True)
        except:
            print(f"Table code {self.bcb_table_code} not found.") 
                
    def get_subperiod(self, begin_date=None, end_date=None, acc = False):
        """Creates an object instance that contains a subperiod of the selected  
            table in the creation of BcbTables instance, starting with 
            begin_date and ending with end_date.

        Parameters
        ----------
        begin_date : date, optional
            Start date of the desired subperiod. 
            The default is None.
        end_date : date, optional
            End date of the desired subperiod.
            The default is None.
        acc : boolean, optional
            Defines whether or not the subperiod can be accumulated. 
            The default is False.

        Returns
        -------
        Pandas list
            Create an object with a selected subperiod
        """
        return self.SubPeriod(self, begin_date, end_date, acc)

    
    class SubPeriod(object):
        def __init__(self, outer, begin_date=None, 
                     end_date=None, acc = False):
            self.outerClass = outer
            self.begin_date = pd.to_datetime(begin_date)
            self.end_date = pd.to_datetime(end_date)
            self.acc = acc
            self.__accumulated_rate = 0

        def create_subper(self):
            '''
            Returns
            -------
            subper : Pandas DataFrame
                DESCRIPTION. Returns a DataFrame containing the daily 
                             values for the selected BCB table.
            '''
            try:
                if self.end_date == None:
                    if self.begin_date == None:
                        subper = self.outerClass.table[self.outerClass.table.index[0]:self.outerClass.table.index[-1]]
                    else:
                        subper = self.outerClass.table[self.begin_date:self.outerClass.table.index[-1]]
                else:
                    if self.begin_date == None:
                        subper = self.outerClass.table[self.outerClass.table.index[0]:self.end_date]
                    else:
                        subper = self.outerClass.table[self.begin_date:self.end_date]
                return subper            
            except ValueError as Verr:
                print("Unknown date: " + str(Verr))                
                    
        def create_acc_subper(self):
            '''        
            Returns
            -------
            acc_subper : Pandas DataFrame
                DESCRIPTION. Returns a DataFrame containing daily
                             values, index rate and accmulated rate
                             to the selected BCB table.
            '''
            if self.acc:
                acc_subper = self.create_subper().copy()
                acc_subper['indice'] = ((acc_subper.iloc[:] / 100) + 1)
                acc_subper['indice_acc'] = acc_subper['indice'].cumprod()                
                return acc_subper

        def get_acc_return_tax(self):
            '''
            Returns
            -------
            numpy.float64
                DESCRIPTION. Returns the accmulated rate as percetual
                             to selected BCB table and subperiod.
            '''
            return_tax = round(((self.create_acc_subper().iloc[-1][2])-1)*100, 4)
            return print(f'{return_tax}%')
              
        def group_by_subper(self, period_type = 'M'):
            '''
            Parameters
            ----------
            period_type : string, optional
                DESCRIPTION. The Pandas offset string to group the subperiod. 
                             The default is 'M'.
                             Examples:
                                M = Group by Months.
                                Y = Group by Year.

            Returns
            -------
            by_subper : Pandas DataFrame
                DESCRIPTION. Returns the selected subperiod grouped 
                by some pandas offset strings (see 
                https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases), 
                as long as it makes sense.

            '''
            by_subper = self.create_acc_subper().copy()
            by_subper = by_subper.iloc[by_subper.reset_index().groupby(by_subper.index.to_period(period_type))['data'].idxmax()]
            by_subper['indice_periodo'] = (by_subper['indice_acc'] / by_subper['indice_acc'].shift(1))    
            by_subper['indice_periodo'][0] =  by_subper['indice_acc'][0]
            return by_subper
        
        