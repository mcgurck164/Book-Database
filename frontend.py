# -*- coding: utf-8 -*-

import tkinter as tk
from backend import Database

DB_NAME = "Books.db" 

class Gui(tk.Tk):
    
    def __init__(self, name_db):
        tk.Tk.__init__(self)
        self.BUTTON_WIDTH = 15  
        self.db = Database(name_db)
        self.build()
    
    def build(self): 
        # labels
        self.lab_title = tk.Label(self, text="Title")
        self.lab_title.grid(row=0, column=0)
        
        self.lab_author = tk.Label(self, text="Author")
        self.lab_author.grid(row=0, column=2)
        
        self.lab_year = tk.Label(self, text="Year")
        self.lab_year.grid(row=1, column=0)
        
        self.lab_isbn = tk.Label(self, text="ISBN")
        self.lab_isbn.grid(row=1, column=2)
        
        # Entry fields
        self.title_in = tk.StringVar()
        self.ent_title = tk.Entry(self, textvariable=self.title_in)
        self.ent_title.grid(row=0, column=1)
        
        self.author_in = tk.StringVar()
        self.ent_author = tk.Entry(self, textvariable=self.author_in)
        self.ent_author.grid(row=0, column=3)
        
        self.year_in = tk.StringVar()
        self.ent_year = tk.Entry(self, textvariable=self.year_in)
        self.ent_year.grid(row=1, column=1)
        
        self.isbn_in = tk.StringVar()
        self.ent_isbn = tk.Entry(self, textvariable=self.isbn_in)
        self.ent_isbn.grid(row=1, column=3)
        
        #Buttons
        self.btn_view_all = tk.Button(self, text="View All", command=self.view_all, width=self.BUTTON_WIDTH)
        self.btn_view_all.grid(row=2, column=3)
        
        self.btn_search_entry = tk.Button(self, text="Search Entry", command=self.search_entry, width=self.BUTTON_WIDTH)
        self.btn_search_entry.grid(row=3, column=3)
        
        self.btn_add_entry = tk.Button(self, text="Add Entry", command=self.add_entry, width=self.BUTTON_WIDTH)
        self.btn_add_entry.grid(row=4, column=3)
        
        self.btn_update_selected = tk.Button(self, text="Update Selected", command=self.update_selected, width=self.BUTTON_WIDTH)
        self.btn_update_selected.grid(row=5, column=3)
        
        self.btn_delete_selected = tk.Button(self, text="Delete Selected", command=self.delete_selected, width=self.BUTTON_WIDTH)
        self.btn_delete_selected.grid(row=6, column=3)
        
        self.btn_close = tk.Button(self, text="Close", command=self.close, width=self.BUTTON_WIDTH)
        self.btn_close.grid(row=7, column=3)
        
        #Listbox
        self.lbx_1 = tk.Listbox(self, height=6, width=35, selectmode=tk.SINGLE)
        self.lbx_1.grid(row=2, column=0, rowspan=6, columnspan=2)
        self.view_all()
        
        #Scrollbar
        self.scb_1 = tk.Scrollbar(self)
        self.scb_1.grid(row=2, column=2, rowspan=6)
        self.lbx_1.configure(yscrollcommand=self.scb_1.set)
        self.scb_1.configure(command=self.lbx_1.yview)
        
    def view_all(self):
        items = self.db.query_db()
        self.populate_listbox(self.lbx_1, items)
    
    def search_entry(self):
        title, author, year, isbn = self.get_entered_values()
        sql = f"SELECT * FROM Books WHERE (title = '{title}')"
        items = self.db.query_db(sql_qry=sql)
        self.populate_listbox(self.lbx_1, items)
    
    def add_entry(self):
        title, author, year, isbn = self.get_entered_values()
        if title == "" or author == "":
            return
        self.db.add_book(title, author, year, isbn)
        self.view_all()
        
    def update_selected(self):
        items = self.lbx_1.curselection()                    #list of integers
        items = [self.lbx_1.get(item) for item in items]     #list of tupels containing values for each column
        author, year, isbn = self.get_entered_values()[1:]        
        for item in items:
            book_id = item[0]
            self.db.update_book(book_id, author, year, isbn)
        self.view_all()
    
    def delete_selected(self):
        items = self.lbx_1.curselection()                    #list of integers
        items = [self.lbx_1.get(item) for item in items]     #list of tupels containing values for each column        
        for item in items:
            book_id = item[0]
            self.db.delete_book(book_id)
        self.view_all()
        
    def close(self):
        self.destroy()
        
    def get_entered_values(self):
        vals = []
        vals.append(self.title_in.get())
        vals.append(self.author_in.get())
        vals.append(self.year_in.get())
        vals.append(self.isbn_in.get())
        for i in range(0, len(vals)-1):
            vals[i]="*" if vals[i]=="" else vals[i]
        return vals
    
    def populate_listbox(self, lbx, items):
        lbx.delete(0, tk.END)
        for item in items:
            lbx.insert(tk.END, item)

if __name__ == "__main__":
    gui = Gui(DB_NAME)
    gui.mainloop()