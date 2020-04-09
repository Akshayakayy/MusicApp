#!/bin/python

import os
import sqlite3

conn=sqlite3.connect('musicdatabase.db')

c=conn.cursor()


for dirpath,dirnames,filenames in os.walk('/home/souvik/webApp/static/audios'):
    for filename in filenames:
        k=dirpath.split('/')
        url=dirpath[12:]
        song=filename[0:-4]
        genre=k[6]
        params=(song,genre,url)
        c.execute("INSERT INTO links VALUES(NULL,?,?,?)",params)



conn.commit()
conn.close()
