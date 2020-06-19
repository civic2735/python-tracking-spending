# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 10:38:51 2020

@author: user
"""


import tkinter
import pycategory
import pyrecord

#main()
entries=pyrecord.Entries()
categories=pycategory.Categories()
del_bool=False

root=tkinter.Tk()
f=tkinter.Frame(root,width=1600, height=900)
f.pack_propagate(0)
f.grid(row=0, column=0)


scrollbar1=tkinter.Scrollbar(f, orient=tkinter.HORIZONTAL)
scrollbar1.grid(row=1,column=0,columnspan=4,sticky= 'ew')
result_box=tkinter.Listbox(f,width=45, height=25,\
                           xscrollcommand=scrollbar1.set,font=('Courier',12))
result_box.grid(row=0,column=0, columnspan=4)
scrollbar1.config(command=result_box.xview)

ballance_str=tkinter.StringVar()
ballance_label=tkinter.Label(f,textvariable=ballance_str)
ballance_label.grid(row=2,column=0, columnspan=2)

#===========================================================================
#view record
def view_records_fun():
    temp_list=entries.view_and_sort(False)
    refresh_fun()
    for i, v in enumerate(temp_list):
        result_box.insert(i,v)
    ballance_str.set(temp_list[-1])
    global del_bool
    del_bool=True
    
view_records=tkinter.Button(f,text='view records',command=view_records_fun)
view_records.grid(row=2,column=3)

#============================================================================
#view categories
def view_categ_fun():
    categ_str=[i for i in categories.view_categories()]
    refresh_fun()
    for i, v in enumerate(categ_str):
        result_box.insert(i,v) 
    global del_bool
    del_bool=False
    
view_categ=tkinter.Button(f,text='view_categories',command=view_categ_fun)
view_categ.grid(row=2,column=2)

#===========================================================================
#add
add_str=tkinter.StringVar()
add_win=tkinter.Entry(f,textvariable=add_str)
add_win.grid(row=3,column=0,columnspan=3)

def add_fun():
    temp_add=add_win.get()
    entries.add(temp_add, categories)
    refresh_fun()
    view_records_fun()
    
add_button=tkinter.Button(f,text='add',command=add_fun)
add_button.grid(row=3,column=3)

#=====================================================================
# delete that is selected
def delete_fun(del_bool=False):
    if del_bool==True:
        #delete_enum=result_box.curselection()
        delete_index=int(result_box.curselection()[0])
        del(entries._entries[delete_index])
        refresh_fun()
        view_records_fun()
    else:
        tkinter.messagebox.showerror('ERROR','cannot delete here')
        
delete_button=tkinter.Button(f,text='delete',command=lambda:delete_fun(del_bool))
delete_button.grid(row=5,column=0)

#=====================================================================
#find categories
find_str=tkinter.StringVar()
find_win=tkinter.Entry(f,textvariable=find_str)
find_win.grid(row=4,column=0,columnspan=3)

def find_fun():
    find_category=find_win.get()
    temp_entries=entries.find(find_category,categories)
    refresh_fun()
    for i, v in enumerate(temp_entries):
        result_box.insert(i,v)
    ballance_str.set(temp_entries[-1])
    global del_bool
    del_bool=False
        
find_button=tkinter.Button(f,text='find category',command=find_fun)
find_button.grid(row=4,column=3)

#=====================================================================
#clear listbox
def refresh_fun():
    result_box.delete(0,tkinter.END)
    ballance_str.set('')
refresh=tkinter.Button(f,text='refresh',command=refresh_fun)
refresh.grid(row=5,column=3)

#=====================================================================

f.mainloop()
entries.save()




