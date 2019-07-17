# -*- coding: utf-8 -*-

import sqlite3
import os

class Database():
    def __init__(self, name):
        self.name = name
        exists = os.path.isfile(self.name)
        self.connect_db()
        if not exists:
            self.setup_db()
    
    def connect_db(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
    
    def setup_db(self):
        # create table Books
        self.cur.execute("CREATE TABLE IF NOT EXISTS Books (id INTEGER PRIMARY KEY," \
                                                      "title TEXT," \
                                                      "author TEXT," \
                                                      "year INTEGER," \
                                                      "isbn TEXT)")
        # add some examples
        self.add_book("The Secret History", "Donna Tartt", 1993, "978-0804111355")
        self.add_book("Joyland", "Stephen King", 2013, "978-1781162644")
        self.add_book("Tschick", "Wolfgang Herrndorf", 2012, "978-3499256356")
        self.add_book("Agnes", "Peter Stamm", 2009, "978-3596179121")
        
        
    def add_book(self, title, author, year, isbn):
        self.cur.execute("INSERT INTO Books (title, author, year, isbn) VALUES (?, ?, ?, ?)", (title, author, year, isbn))
        self.con.commit()
    
    def update_book(self, book_id, author, year, isbn):
        self.cur.execute("UPDATE Books SET author=?, year=?, isbn=? WHERE id=?"),(author, year, isbn, book_id)
        self.con.commit()
    
    def delete_book(self, book_id):
        self.cur.execute("DELETE FROM Books WHERE id=?",(book_id,))
        self.con.commit()
    
    def query_db(self, sql_qry="SELECT * FROM Books"):
        self.cur.execute(sql_qry)
        return self.cur.fetchall()

    def __del__(self):
        self.con.close()