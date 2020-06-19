# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:36:22 2020

@author: user
"""


import sys
#import time
from datetime import date
from tkinter import messagebox 

class Entry:
    def __init__(self, *entry):
        entry_tuple=tuple(entry)
        self._entry=entry_tuple
        date_list=[int(i) for i in entry_tuple[0].split('-')]
        self._date= date(*date_list)
        self._category= entry_tuple[1]
        self._item= entry_tuple[2]
        self._amount= entry_tuple[3]
        
    @property
    def date_attri(self):
        return self._date
    @property
    def category(self):
        return self._category
    @property
    def item(self):
        return self._item
    @property
    def amount(self):
        return self._amount

#============================================================================  
class Entries:
    #initialize
    initial_entries=[]
    # exception 1: cannot open file
    try:
        #load the historicl data before the data inputed this time
        fh=open('records.txt','r')
        historical_data=fh.readlines()
        for i in range(0,len(historical_data)):
            if(historical_data[i]!=''):
                initial_entries.append(tuple(historical_data[i].split()))
        fh.close()
    except	OSError as err1:
    	sys.stderr.write(str(err1))
    	sys.stderr.write('   the program can still run, and will create \
"records.txt" automatically')
    # if there is no historical data, ask initial income
# =============================================================================
#     if not initial_entries:
#         #automatically generate time and item name for initial income
#         initial_income= input('How much money do you have? ')
#         #exception 2: value error
#         try:
#             float(initial_income)
#         except ValueError:
#             initial_income=0
#             sys.stderr.write('Invalid value for money. Set to 0 by default.')
#         
#         auto_time= time.localtime()
#         initial_entries.append((str('%04d-' %auto_time.tm_year)+
#                         str('%02d-' %auto_time.tm_mon)+
#                         str('%02d' %auto_time.tm_mday),'income' ,'initial_income', 
#                         initial_income))
#     else:
#         print('Welcome back!')
# =============================================================================
    print('Welcome!')
        
    def __init__(self,entries=initial_entries):
        for i, val in enumerate(entries):
            entries[i]=Entry(*val)
        self._entries=entries        
    
    def view_and_sort(self,sort):
        #balance of cash of historical data and new data
        historical_total=0
        for i in self._entries:
            historical_total=historical_total+float(i.amount)
        
        if sort==True:
            # print & sort
            #asking parameters of sorting
            #ignore space and upcases
            sorting=input('Which do you want to sort the entries by, date, category, item or amount: ')
            sorting=sorting.strip().lower()
            key=0
            if(sorting=='date'):
                key=0
            if(sorting=='category'):
                key=1
            if(sorting=='item'):
                key=2
            if(sorting=='amount'):
                key=3
            #exception 10: invalid input
            if sorting not in ('date', 'category', 'item', 'amount'):
                sys.stderr.write('Invalid input for sorting. Set to "date" by default.\n')
            bool_reverse=False
            reversing=input('do you want to sort the entries reversely? yes or no: ')
            reversing=reversing.strip().lower()
            if(reversing=='yes'):
                bool_reverse=True
            #exception 11: invalid input
            if reversing not in ('yes', 'no'):
                sys.stderr.write('Invalid input for sorting. Set to "no" by default.\n')
            
            # in order to sort, transform cls to list
            entries_list=[]
            for i in self._entries:
                entries_list.append(i._entry)
            entries_list.sort(key=lambda entries: entries[key],
                         reverse=bool_reverse)
            print('Here\'s your expense and income records of this time:\n')
            print('date      category       description      amount')
            print('=====================================================')
            for j in entries_list:
                print(f'{j[0]}  {j[1]:<15s}  {j[2]:<15s}  {j[3]}')
            
            print('=====================================================')
            print('historical balance is %d dollars.' %historical_total)

        
        #not sort; print the original txt directly
        if sort== False:
            entries_list=[]
            print('Here\'s your expense and income records of this time:\n')
            print('date      category           description      amount')
            print('======================================================')
            for i in self._entries:
                print(f'{str(i.date_attri)}  {i.category:<15s}  {i.item:<15s} {i.amount}')
                entries_list.append(f'{str(i.date_attri)}  {i.category:<15s} {i.item:<15s}  {i.amount}')
            
            print('======================================================')
            entries_list.append('======================================================')
            print('historical balance is %d dollars.' %historical_total)
            entries_list.append('historical balance is %d dollars.' %historical_total)
            return entries_list
    
    def add(self,s,categories):
#        entry_enter=input('Add some expense or income records with date,description and amount:\
#    date1 desc1 amt1, date2 desc2 amt2, date3 desc3 amt3, ...\n')
        temp_list=s.split(',')
        bool_error= False
        # ckeck all input, if there is any error do not add any record
        for i, v in enumerate(temp_list):
            # exception 4: wrong form of input entries
            if len(v.split())==3:
                v=str(date.today())+' '+v
                temp_list[i]=v
            try:
                assert len(v.split())==4
            except AssertionError:
                sys.stderr.write('The format of a record should be like this:\
    20200416 food breakfast -50\nFail to add a record.')
                messagebox.showerror('ERROR','wrong format')
                bool_error= True
                break
            #exception 5: wrong value of input entries
            test_list=v.split()
            try:
                float(test_list[3])
            except ValueError:
                bool_error= True
                sys.stderr.write('The format of a record should be like this:\
    20200416 food breakfast -50. The amount position is not a number \nFail to add a record.')
                messagebox.showerror('ERROR','The amount position is not a number \nFail to add the records.')
                break
            #exception 12: not in categories
            if categories.is_category_valid(test_list[1]):
                pass
            else:
                bool_error= True
                sys.stderr.write('Not in the categories \nFail to add a record.')
                messagebox.showerror('ERROR','Not in the categories \nFail to add the records.')
                break
            try:
                date.fromisoformat(test_list[0])
            except:
                bool_error= True
                messagebox.showerror('ERROR','Not a date format \nFail to add the records.')
                sys.stderr.write('Not a date format \nFail to add a record.')
                break
            
        if bool_error== False:
            for l in temp_list:
                print(l)
                self._entries.append(Entry(*l.split()))
        return self._entries
    
    def delete(self):
        delete_tuple=tuple(input('Which entry do you want to delete?\
    please enter the data in such form: 2020-03-20 tissue -50\n').split())
        #count how many entries need to be deleted
        found_record=[]
        # in order to sort, transform cls to list
        entries_list=[]
        for i in self._entries:
            entries_list.append(i._entry)
            
        for i,l in enumerate(entries_list):
            if delete_tuple==l:
                found_record.append(i)
        if len(found_record)==1:
            entries_list.remove(delete_tuple)
        #delete exact number of the same entries
        elif len(found_record)>1:
            delete_int=int(input(f'You have {len(found_record)} same entries.\
    How many entrie do you want to delete? 1 or 2 or 3... '))
            #exception 9: out of range
            if delete_int> len(found_record):
                delete_int=len(found_record)
                sys.stderr.write(f'Input is out of range. Set to {len(found_record)} by default.\n')
            for j in range(0,delete_int):
                entries_list.remove(delete_tuple)
        elif len(found_record)==0:
            if len(delete_tuple)==4:
                # exception 6: the specified record does not exist
                sys.stderr.write('NOT FOUND')
            else:
                # exception 7: invalid format
                sys.stderr.write('Invalid format. Fail to delete a record.')
        
        # transform list back to cls
        for i, val in enumerate(entries_list):
            entries_list[i]= Entry(*val)
        self._entries=entries_list
        return self._entries
    
    def save(self):
        try:
            #save all the data to records.txt
            with open('records.txt','w') as fh:
                for i in self._entries:
                    temp_string=str(i.date_attri)+' '+i.category+' '+i.item+' '+str(i.amount)
                    fh.write(temp_string+'\n')
        except:
            sys.stderr.write('there is no record file, all inputs will not be saved.')
    
    def find(self, category,categories):
        """"find entries by date, categories, item, amount. it will call \
    view_all_data function to print and sort
        """
        #position_input=input('Which do you want to find the entries by, date, category, item or amount: ')
        #position_input=position_input.strip().lower()
        find_list=[]
        position_input='category'
        position=1
        if(position_input=='date'):
            position=0
            find_list=input('enter date EX:20200416 20200515: ').split()
        if(position_input=='category'):
            position=1
            #find_category=input('which categoriy do you want to find: ')
            find_list= categories.find_subcategories(category)
            #exception 13: there is no such category
            if not categories.is_category_valid(category):
                messagebox.showerror('ERROR','the category cannot be found.')
                sys.stderr.write('the category cannot be found. \n')
        if(position_input=='item'):
            position=2
            find_list=input('enter date EX:breakfast tissue: ').split()
        if(position_input=='amount'):
            position=3
            find_list=input('enter date EX:-50 100: ').split()
        #exception 10: invalid input
        if position_input not in ('date', 'category', 'item', 'amount'):
            sys.stderr.write('Invalid input for finding. Set to "category" by default.\n')
            find_list= categories.find_subcategories(input('which categoriy do you want to find: '))
        
        temp_entries=[]   
        for l in self._entries:
            temp_tuple=(l._entry)
            if temp_tuple[position] in find_list:
                temp_entries.append(temp_tuple)
                
        return Entries(temp_entries).view_and_sort(False)

            
# =============================================================================
#         if temp_entries:
#             sort_boll=input('Do you want to sort the entries? yes or no: ')\
#                     .strip().lower()
#             #exception 8: invalid input
#             if sort_boll not in ('yes', 'no'):
#                 sort_boll='no'
#                 sys.stderr.write('Invalid input for viewing. Set to "no" by default.\n')
#             if sort_boll =='yes':
#                 Entries(temp_entries).view_and_sort(True)
#             if sort_boll =='no':
#                 Entries(temp_entries).view_and_sort(False)
#         else:
#             Entries(temp_entries).view_and_sort(False)
# =============================================================================
    
    