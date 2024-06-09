import tkinter as tk
from tkinter import ttk 
from lab13 import DatabaseIntegration
window = tk.Tk()
db = DatabaseIntegration('lab13/currency.db')
currencies = db.get_all_currencies()


window.title("Currency exchaner")
window.geometry('500x500')
ttk.Label(window, text = "Select the currency :", 
          font = ("Times New Roman", 10)).grid(column = 0, 
          row = 5, padx = 10, pady = 25)
n = tk.StringVar() 
currency_chosen = ttk.Combobox(window, width = 27, textvariable = n) 
currency_chosen['values'] = [x[0] for x in db.get_all_currencies()]
currency_chosen.bind('<<ComboboxSelected>>', lambda event: label_selected.config(text=materialDict[var_material.get()]))
  
currency_chosen.grid(column = 1, row = 5) 
currency_chosen.current() 
window.mainloop()