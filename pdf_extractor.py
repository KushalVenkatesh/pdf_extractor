#!/usr/bin/python3
from PyPDF2 import PdfFileReader
import filetype
import hashlib
import sqlite3
import os
#importing necessary stuff
class Database:

    def __init__(self,dbname):
        self.dbname = dbname
        #assigning variable in constructor
    
    def Create(self):
        if not os.path.isfile(self.dbname):
            f = open(self.dbname,"wb")
            f.close()
        else:
            os.remove(self.dbname)
        #checking if file exists or not

        conn = sqlite3.connect(self.dbname)
        conn.execute('''CREATE TABLE
        Files(name TEXT NOT NULL,metadata TEXT NOT NULL,
        nop INT NOT NULL,eon TEXT NOT NULL,
        sum TEXT NOT NULL)''')
        conn.close()
        #setting up a table

    def Clear(self):
        os.remove(self.dbname)
        Create()
        #recreating a database

    def Insert(self,first,second,third,fourth,fifth):
        orders = (str(first),str(second),str(third),str(fourth),str(fifth))
        conn = sqlite3.connect(self.dbname)
        conn.execute("INSERT INTO Files VALUES(?,?,?,?,?)",orders)
        conn.commit()
        conn.close()
        #inserting data into database
        
    def Retrieve(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.execute("""SELECT * FROM Files""")
        records = cursor.fetchall()
        for row in records: 
            print("-----ROW-----")
            print("name: ",row[0])
            print("metadata: ",row[1])
            print("number of pages: ",row[2])
            print("is encrypted: ",row[3])
            print("sha1 checksum: ",row[4])
            print("-----ROW-----")
        #retrieving rows from database
            

class PdfStuff:

        def __init__(self,pdfname):
            self.pdfname = pdfname
            #assigning stuff in constructor

        def get_metadata(self):
            f = open(self.pdfname,"rb")
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            return info
            #getting metadata from file

        def number_of_pages(self):
            f = open(self.pdfname,"rb")
            pdf = PdfFileReader(f)
            nop = pdf.getNumPages()
            return nop
            #getting number of pages

        def encrypted_or_not(self):
            f = open(self.pdfname,"rb")
            pdf = PdfFileReader(f)
            if pdf.isEncrypted:
                return "yes"
            else:
                return "no"
            #checking if file is encrypted
            #or not

        def sha1_sum(self):
            file = self.pdfname.encode()
            return hashlib.sha1(file).hexdigest()
            #calculating checksum from file

if __name__ == "__main__":

    def pdf_go_brr(filename):
        db = Database("files.db")
        ps = PdfStuff(filename)
        metadata = ps.get_metadata()
        nop = ps.number_of_pages()
        eon = ps.encrypted_or_not()
        sha1sum = ps.sha1_sum()
        db.Insert(filename,metadata,nop,eon,sha1sum)
        #function that pulls data from pdf
        #and adds it to database

    def auto_mode():
        db = Database("files.db")
        db.Create()
        for file in os.listdir():
            kind = filetype.guess(file)
            if kind is not None:
                if kind.mime == "application/pdf":
                    pdf_go_brr(file)
        #looping thought files in directory
        #with checking if the file is actually
        #a pdf

        db.Retrieve()
        #and retrieving

    def single_mode(pdf_file_name):
        kind = filetype.guess(pdf_file_name)
        if kind is not None:
            if kind.mime == "application/pdf":
                ps = PdfStuff(pdf_file_name)
                print(ps.get_metadata())
                print(ps.number_of_pages())
                print(ps.encrypted_or_not())
                print(ps.sha1_sum())
        #retrieving file without db from single file

    def just_show():
        db = Database("files.db")
        db.Retrieve()
        #just showing the records from database

    #example of how to use
    #auto_mode()
    #single_mode("example.pdf")
    #just_show()
