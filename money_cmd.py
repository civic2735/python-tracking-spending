# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 09:52:33 2020

@author: user
"""


import sys
import pycategory_cmd
import pyrecord_cmd

#main()
entries=pyrecord_cmd.Entries()
categories=pycategory_cmd.Categories()

#What does the user want to do next
#ignore space and upcases
leave_input=False
while leave_input==False:
    command=input('What do you want to do (add/ view/ delete/ view categories/ find/ exit)?  ')\
        .strip().lower()
    
    #enter data in the form of 20200320 tissue -50, 20200320 a -50,...
    if command== 'add':
        entries.add(categories)
        
    #view and sort all data
    #ignore space and upcases
    if command== 'view':        
        sort_boll=input('Do you want to sort the entries? yes or no: ')\
            .strip().lower()
        #exception 8: invalid input
        if sort_boll not in ('yes', 'no'):
            sort_boll='no'
            sys.stderr.write('Invalid input for viewing. Set to "no" by default.\n')
        if sort_boll =='yes':
            entries.view_and_sort(True)
        if sort_boll =='no':
            entries.view_and_sort(False)
                
    #delet entries
    if command== 'delete':  
        entries.delete()
    
    if command== 'view categories':  
        categories.view_categories()
    
    if command== 'find':  
        entries.find(categories)
    
    #exit the command loop       
    if command== 'exit':
        entries.save()
        leave_input=True
    
    #excpetion 3: wrong commanding
    if command not in ('add', 'view', 'delete', 'exit','view categories','find'):
        sys.stderr.write('Invalid command. Try again.')

