from pyModbusTCP.client import ModbusClient
import time
from tkinter import *
from subprocess import call
import sys
import sqlite3
from sqlite3 import Error

SERVER_HOST = "192.168.72.83"  # PLC's internal IP
SERVER_PORT = 502

c = ModbusClient()
c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.open()
RowData = []

def ReadData(ADDR):

    if not c.is_open():
        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

    if c.is_open():
        regs = c.read_holding_registers(ADDR, 1)  
        RowData.append(str(regs).replace("[","").replace("]","")) # add particular memory element to the linked list

def FormatRowData():
    ct=0
    for x in range(0,3000):
        ct=ct+1
        if ct == 5: # this particular PLC's program had information in rows of 5
            ct=0
            print(RowData[x-5]+ "," + str(float(RowData[x-4])/10) + ","+ str(float(RowData[x-3])/10)+ "," +str(float(RowData[x-2])/10)+ "," +str(float(RowData[x-1])/1000))

            conn = sqlite3.connect('DL06DATA.db') # connect to DL06DATA.db 
            c = conn.cursor()
            c.execute('insert into DL06DATA VALUES ('+RowData[x-5]+','+str(float(RowData[x-4])/10)+','+str(float(RowData[x-3])/10)+','+str(float(RowData[x-2])/10)+","+str(float(RowData[x-1])/1000)+')')
            ## insert into (your table name) VALUES(?,?,?,?,?)
            conn.commit()#update the table
            conn.close()


if __name__ == "__main__":
    for x in range(850,4000): # for the DL06 this is the entire adress list 
        ReadData(x)
    FormatRowData()   
