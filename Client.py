from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import KeystrokeMain
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

# def KeystrokeMain(client):
# 	# Tạo ra cửa sổ của Keystroke
# 		logger = ''
# 		Stroke = Tk()
# 		Stroke.title("Keystroke")  
# 		Stroke.geometry("410x320")
# 		Stroke.configure(bg = 'white')
# 		frame_stroke = Frame(Stroke, bg = "#FFEFDB", padx=20, pady = 20, borderwidth=5)
# 		frame_stroke.grid(row=1,column=0)
# 		tab = Text(Stroke, width = 50, heigh = 15)
# 		tab.grid(row = 1, column = 0, columnspan= 4)
# 		PrsHook = False
# 		PrsUnhook = False

# 		def ReceiveHook(client):
# 			data = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
# 			# string = data										# Chuyển dữ liệu thành string
# 			client.sendall(bytes(data,"utf-8"))  				# Gửi dữ liệu đến server
# 			return data

# 		def Hookkey():
# 			nonlocal PrsHook, PrsUnhook
# 			if PrsHook == True: return
# 			PrsHook = True
# 			PrsUnhook = False
# 			client.sendall(bytes("HookKey","utf-8"))
# 			checkdata = client.recv(1024).decode("utf-8")

# 		def Unhookkey():
# 			nonlocal logger, PrsUnhook, PrsHook
# 			if PrsHook == True:
# 				client.sendall(bytes("UnhookKey","utf-8"))    
# 				logger = ReceiveHook(client)
# 				client.sendall(bytes(logger,"utf-8")) 
# 				PrsUnhook = True
# 				PrsHook = False

# 		def Printkey():
# 			nonlocal logger, PrsUnhook, PrsHook
# 			if PrsUnhook == False: 
# 				client.sendall(bytes("UnhookKey","utf-8"))
# 				logger = ReceiveHook(client)
# 			tab.delete(1.0, END)
# 			tab.insert(1.0, logger)
# 			PrsUnhook = True
# 			PrsHook = False

# 		def Deletekey():
# 			tab.delete(1.0,END)
					    
# 		hook = Button(Stroke, text = "Hook", font = "Helvetica 10 bold",bg = "#FFDEAD", padx = 27, pady = 24, command = Hookkey).grid(row = 2,column = 0,sticky=E)
# 		unhook = Button(Stroke, text = "Unhook",font = "Helvetica 10 bold", bg = "#EECFA1", padx = 27, pady = 24, command = Unhookkey).grid(row = 2,column = 1,sticky=E) 
# 		prs = Button(Stroke, text = "In phím",font = "Helvetica 10 bold",bg = "#CDB38B", padx = 27, pady = 24,command = Printkey).grid(row = 2,column = 2,sticky=E)
# 		delete = Button(Stroke, text = "Delete", font = "Helvetica 10 bold", bg = "#8B795E",padx = 27, pady = 24,command = Deletekey).grid(row = 2,column = 3,sticky=E)


def Registry(client): 
	OPTION_1 = [
            "Get value",
            "Set value",
            "Delete value",
            "Create key",
            "Delete key"
        	]

	OPTION_2 = [
    		"String",
            "Binary",
            "DWORD",
            "QWORD",
            "Multi-string",
            "Expandable String"
        	]
	Register = Tk()
	Register.geometry("480x450")
	Register.title("Registry")
	Register.configure(bg = '#8B6969')
	pathing = StringVar()
	linking = ''
	browser = Entry(Register,bg = "#8B658B", width=55)
	browser.grid(row=0, column=0, padx = 10)
	regis = Text(Register,bg = "#8B658B", height = 7, width = 41)
	regis.grid(row=2, column=0, pady=10)

	def Browse():
		nonlocal pathing, linking
		fname = filedialog.askopenfilename()
		pathing.set(fname)
		browser.insert(0, fname)
		linking = browser.get()
		fileopen = open(linking,'r')
		line = fileopen.read()
		regis.insert(1.0,line)
	ButtonBrowse = Button(Register, text="Browser", font = "Helvetica 10 bold",bg = "#EEB4B4", activebackground='#F4A460',command=Browse, padx = 28)
	ButtonBrowse.grid(row=0, column=1, padx = 10)

	def RegContent():
		nonlocal regis
		client.sendall(bytes("SendingReg", "utf-8"))
		checkdata = client.recv(1024).decode("utf-8") 
		line = regis.get(1.0,END)
		client.sendall(bytes(line,"utf-8"))
		checkdata = client.recv(1024).decode("utf-8")
	ContentButton = Button(Register, text="Gửi nội dung", font = "Helvetica 10 bold",bg = "#EEB4B4",activebackground='#F4A460',height = 4, command = RegContent, padx = 15, pady = 28)
	ContentButton.grid(row=2, column=1, padx = 10)

	SecondFrame = LabelFrame(Register, text="Sửa giá trị trực tiếp")
	SecondFrame.grid(row=3, columnspan = 2, padx = 0, pady = 0)

	def changeFunction(event):
		if getFunction.get() == "Get value":
			Name.grid_forget()
			Value.grid_forget()
			infomation.grid_forget()
			Name.grid(row=2, column=0, sticky = W)

		elif getFunction.get() == "Set value":
			Name.grid_forget()
			Value.grid_forget()
			infomation.grid_forget()
			Name.grid(row=2, column=0, sticky = W)
			Value.grid(row=2, column=0, sticky = N)
			infomation.grid(row=2, column=0, sticky = E, padx=4)       
		elif getFunction.get() == "Delete value":
			Name.grid_forget()
			Value.grid_forget()
			infomation.grid_forget()
			Name.grid(row=2, column=0, sticky = W)

		elif getFunction.get() == "Create key":
			Name.grid_forget()
			Value.grid_forget()
			infomation.grid_forget()

		elif getFunction.get() == "Delete key":
			Name.grid_forget()
			Value.grid_forget()
			infomation.grid_forget()

    # Sửa giá trị trực tiếp
	getFunction = ttk.Combobox(SecondFrame, value=OPTION_1)
	getFunction.insert(0, "Chọn chức năng")
	getFunction.bind("<<ComboboxSelected>>", changeFunction)
	getFunction.grid(row=0,column=0,ipadx=160, sticky=W)
	path = Entry(SecondFrame, width=77)
	path.insert(0, "Đường dẫn")
	path.grid(row=1, column=0, pady=10)
	Name = Entry(SecondFrame, width = 24)
	Name.insert(0, "Name value")
	Name.grid(row=2, column=0, sticky = W)
	Value = Entry(SecondFrame, width = 25)
	Value.insert(0, "Value")
	Value.grid(row=2, column=0, sticky = N)
	infomation = ttk.Combobox(SecondFrame, value=OPTION_2)
	infomation.insert(0, "Kiểu dữ liệu")
	infomation.grid(row=2, column=0, sticky = E, padx=4)
	Thongbao = Frame(SecondFrame)
	Thongbao.grid(row=3, column=0)
	Noti = Canvas(Thongbao, height=150, width =440)
	Noti.pack(side=LEFT, fill=BOTH, expand=1)
	Lenh = Frame(Noti)
	Noti.create_window((0,0), window=Lenh, anchor="nw")

	def ButtonGui():
		if getFunction.get() == "Get value":
			client.sendall(bytes("GettingValueReg","utf-8"))
			NameVal = Name.get()
			Links = path.get()
			client.sendall(bytes(NameVal,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8") 
			data = client.recv(1024).decode("utf-8")
			client.sendall(bytes("Da nhan", "utf-8"))

			if data == "Khong tim thay":
				chuoi = Label(Lenh, text="Không tìm thấy")
				chuoi.pack(side = BOTTOM)
			else: 
				chuoi = Label(Lenh, text=data)
				chuoi.pack(side = BOTTOM)

		elif getFunction.get() == "Set value":
			client.sendall(bytes("SettingValueReg","utf-8"))
			NameVal = Name.get()
			Links = path.get()
			client.sendall(bytes(NameVal,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")	
			Kieudulieu = infomation.get()
			client.sendall(bytes(Kieudulieu, "utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			values = Value.get()
			client.sendall(bytes(values,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")

			status = client.recv(1024).decode("utf-8")
			print("status")
			client.sendall(bytes("Da nhan", "utf-8"))
			if status == "succeed":
				chuoi = Label(Lenh, text="Set giá trị thành công")
				chuoi.pack(side = BOTTOM)
			elif status == "Sai duong dan":
				chuoi = Label(Lenh, text="Sai đường dẫn")
				chuoi.pack(side = BOTTOM)
			else:   
				chuoi = Label(Lenh, text="Lỗi giá trị")
				chuoi.pack(side = BOTTOM)

		elif getFunction.get() == "Create key":
			client.sendall(bytes("CreatingKey","utf-8"))
			Links = path.get()
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			data = client.recv(1024).decode("utf-8")
			client.sendall(bytes("Da nhan","utf-8"))
			if data == "Da tao thanh cong":
				chuoi = Label(Lenh, text="Đã tạo thành công")
				chuoi.pack(side = BOTTOM)          
			else: 
				chuoi = Label(Lenh, text="Sai đường dẫn")
				chuoi.pack(side = BOTTOM)

		elif getFunction.get() == "Delete value":
			client.sendall(bytes("DeletingValueReg","utf-8"))
			Links = path.get()
			NameVal = Name.get()
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			client.sendall(bytes(NameVal,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			client.sendall(bytes("Gui noi dung","utf-8"))            
			data = client.recv(1024).decode("utf-8")
			chuoi = Label(Lenh, text=data)
			chuoi.pack(side = BOTTOM)
			client.sendall(bytes("In thanh cong","utf-8"))

		elif getFunction.get() == "Create key":
			client.sendall(bytes("CreatingKey","utf-8"))
			Links = path.get()
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			data = client.recv(1024).decode("utf-8")
			client.sendall(bytes("Da nhan","utf-8"))
			chuoi = Label(Lenh, text=data)
			chuoi.pack(side = BOTTOM)        

		elif getFunction.get() == "Delete key":
			client.sendall(bytes("DeletingKey","utf-8"))
			Links = path.get()
			client.sendall(bytes(Links,"utf-8"))
			checkdata = client.recv(1024).decode("utf-8")
			data = client.recv(1024).decode("utf-8")
			client.sendall(bytes("Da nhan","utf-8"))
			if data == "Da xoa thanh cong":
				chuoi = Label(Lenh, text="Đã xoá thành công")
				chuoi.pack(side = BOTTOM)          
			else: 
				chuoi = Label(Lenh, text="Sai đường dẫn")
				chuoi.pack(side = BOTTOM)                
	def ButtonXoa():
		for widget in Lenh.winfo_children(): widget.destroy()

	BelowButton = Frame(SecondFrame)
	send = Button(BelowButton, text="Gửi",activebackground='#8B7D7B',font = "Helvetica 10 bold",bg = "#BC8F8F", command = ButtonGui)
	send.grid(row=0, column=0, ipadx = 35)
	delete = Button(BelowButton, text="Xoá",activebackground='#8B7D7B',font = "Helvetica 10 bold",bg = "#BC8F8F", command = ButtonXoa)
	delete.grid(row=0, column=1, ipadx = 35)
	BelowButton.grid(sticky=S)
	Register.mainloop()


class GUI:
	def __init__(self):
		self.Window = Tk()
		self.Window.withdraw()
		self.Window.configure(bg="#FFFAF0")
	# Hộp thoại đăng nhập IP
		self.login = Toplevel()
		self.login.configure(bg = "#fff")
	# Tạo tiêu đề cho hộp thoại
		self.login.title("User")
		self.login.resizable(width = False,height = False)
		self.login.configure(width = 600,height = 550)
		
	# Tạo label
		self.pls = Label(self.login, text = "Nhập địa chỉ IP để tiếp tục:", compound="center", bg ="#fff",font = "Helvetica 15 bold")
		self.pls.place(relx = 0.05,rely = 0.1)
	# Tạo một hộp thoại để client nhập IP
		Id = StringVar()
		self.entryName = Entry(self.login, textvariable = Id, bg ="#FFFAF0", font = "Helvetica 14")
		self.entryName.place(relx = 0.501,rely = 0.105)
		# set the focus of the curser
		self.entryName.focus()

	# Tạo nút nhấn, khi nhấn nút =>  dữ liệu sẽ được gửi đến server thông qua socket
		self.go = Button(self.login,text = "Kết nối",width =18 ,bg = "#d3d3d3",font = "Helvetica 14 bold",command = (lambda : self.Connection_handling(self.entryName.get())), bd = 5, activebackground='#F4A460')
		self.go.place(relx = 0.3,rely = 0.2)
		self.Window.mainloop()
		
	def Control(self, client): # Các hộp thoại chức năng điều khiển
	# Process Running
		self.process = Button(self.login, text = "Process Running", bg = "#0d54b0", height =16, font=('Helvetica 10 bold'), command =(lambda : self.processRunning(client)), bd = 5, activebackground='#F4A460')
		self.process.place(relx = 0.02, rely = 0.35)
	# App Running
		self.app = Button (self.login, text ="App Running", bg = "#fee5c6",width =38,height =4, font=('Helvetica 10 bold'), command = (lambda : self.appRunning(client)), bd = 5, activebackground='#F4A460')
		self.app.place(relx = 0.24, rely = 0.35)
	# Tắt máy
		self.shut = Button(self.login,text ="Shut Down", bg = "#c6c2c2", width =12, height =5, font=('Helvetica 10 bold'), command = (lambda : self.shutDown(client)), bd = 5, activebackground='#F4A460')
		self.shut.place(relx = 0.24, rely = 0.52)
	# Chụp màn hình
		self.capture = Button(self.login, text ="Screen Capture",bg = "#2baf2b", width =23, height =5, font=('Helvetica 10 bold'), command = (lambda : self.takePicture(client)), bd = 5, activebackground='#F4A460')
		self.capture.place(relx = 0.44, rely = 0.52)
	#  Sửa registry
		self.fix =Button(self.login, text="Edit registry",bg = "#00acee",height =3 , width =38, font=('Helvetica 10 bold'), command = (lambda : self.editRegistry(client)), bd = 5, activebackground='#F4A460')
		self.fix.place(relx = 0.24, rely = 0.72)
	# Keystroke
		self.key = Button(self.login, text ="Keystroke",bg = "#ffcc2f", height =11, width =11,font=('Helvetica 10 bold'), command = (lambda : self.keyStroke(client)), bd = 5, activebackground='#F4A460')
		self.key.place(relx = 0.79, rely = 0.35)
	# Thoát
		self.escape = Button(self.login, text ="Exit",bg = "#ef5734",height =3, width =11,font=('Helvetica 10 bold'), command = (lambda : self.exist(client)), bd = 5, activebackground='#F4A460')
		self.escape.place(relx = 0.79, rely = 0.72)      
		# self.top.mainloop()
	

	# Từ control gọi đến Shutdown 
	def shutDown(self, client):
		try:
			client.send(bytes("Shutdown",'utf-8'))		# Gửi thông điệp "shut down" đến server, server sẽ tự động tắt máy trong 30s
		except:
			messagebox.showinfo(" ", "Lỗi kết nối ")	# Nếu lỗi kết nối thì thông báo lỗi

	#Chụp ảnh màn hình
	def takePicture(self, client): 
		self.Screenshot = Toplevel()					# Tạo 1 hộp thoại mới
		self.Screenshot.title("ScreenShot")			# Đặt tiêu đề cho hộp thoại
		self.Screenshot.resizable(width = False,height = False)
		self.Screenshot.configure(bg = "#C0C0C0")		# Đặt màu nền cho hộp thoại
		self.Screenshot.configure(width = 1100, height = 610)
	#Hàm nhận ảnh từ server trả về
		def ReceivePicture(): 	
			try:
				client.sendall(bytes("TakePicture","utf-8"))		# Gửi thông điệp "TakePicture" đến server
			except:
				messagebox.showinfo(" ", "Lỗi kết nối ")			# Nếu lỗi kết nối thì thông báo lỗi
				self.Screenshot.destroy()							# Sau đó, đóng hộp thoại Screenshot lại

			self.file = open("scrshot.png", 'wb')					# Tạo file ảnh mới
			self.data = client.recv(40960000)						# Nhận dữ liệu từ server
			self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
			self.img = ImageTk.PhotoImage(Image.open("scrshot.png"))	# Tạo ảnh từ file ảnh     
			self.canvas.create_image(0,0, anchor=NW, image=self.img)	# Vẽ ảnh lên canvas
			self.file.close()											# Đóng file ảnh
	#Hàm lưu ảnh
		def SavePicture(): 
			self.myScreenShot = open("scrshot.png",'rb')				# Tạo file ảnh mới
			self.data = self.myScreenShot.read()						# Đọc dữ liệu từ file ảnh
			self.fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[("PNG", ".png")])		# Đặt tên file ảnh và nhấn Save
			self.myScreenShot.close()						# Đóng file ảnh

			self.file = open(str(self.fname) + '.png','wb')			# Tạo file ảnh mới
			self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
			self.file.close()										# Đóng file ảnh
			os.remove("scrshot.png") 								# Xóa file ảnh cũ
		
		def DontSavePicture():
			os.remove("scrshot.png") 								# Xóa file ảnh cũ
			self.Screenshot.destroy()								# Đóng hộp thoại Screenshot lại
	#Tạo canvas   
		self.canvas = Canvas(self.Screenshot, bg = "white", width = 900, height = 531) 	# Tạo canvas mới   
		self.canvas.place(relx = 0,rely = 0)    											# Vẽ ảnh chụp màn hình lên canvas
	#Tạo button Chụp ảnh	
		self.cap = Button(self.Screenshot,text="Chụp", bg = "#008080", font = "Helvetica 15 bold",width=15,height=21,borderwidth=5,command = ReceivePicture, bd = 5, activebackground='#F4A460') #Nút chụp hình
		self.cap.place(relx=0.822, rely=0)

	#Tạo button Lưu ảnh
		self.Save = Button(self.Screenshot, text="Lưu",bg = "#FFCC99",font = "Helvetica 15 bold",width=65,height=2,borderwidth=5,command=SavePicture, bd = 5, activebackground='#F4A460')#Nút luu ảnh
		self.Save.place(relx=0, rely=0.88)

	#Tạo button Không lưu ảnh
		self.DontSave = Button(self.Screenshot, text="Không Lưu",bg = "#FFCC99",font = "Helvetica 15 bold", width=24, height=2,borderwidth=5,command=DontSavePicture, bd = 5, activebackground='#F4A460')#Nút luu ảnh
		self.DontSave.place(relx= 0.725, rely = 0.88)
		self.Screenshot.mainloop()

# Hàm khởi động các chương trình (Watch, Kill, Start)
	def appRunning(self, client):	
		self.app = Tk()	
		self.app.title("App Running")
		self.app.configure (bg = "white")
	# Hàm xóa tác vụ	
		def XoaTask():
			self.frame_app.destroy()		# Xóa frame_app
	# Hiển thị các tác vụ
		def WatchTask():
			global frame_app
			global PORT
			PORT = 1234
			self.length = 0 				#Danh sách các app đang chạy
			self.ID = [''] * 100 			#Mảng lưu ID của app
			self.Name = [''] * 100 			#Mảng lưu tên app
			self.Thread = [''] * 100 		#Mảng lưu luồng
			try:
				client.sendall(bytes("AppRunning","utf-8"))			# Gửi yêu cầu lấy danh sách app đang chạy
			except:
				messagebox.showinfo("Warning!", "Lỗi kết nối ")		# Thông báo lỗi kết nối
				self.app.destroy()									# Đóng app

			#Receive data
			try:
				self.length = client.recv(1024).decode("utf-8")
				self.length = int(self.length)
				for i in range(self.length):
					self.data = client.recv(1024).decode("utf-8")
					self.ID[i] = self.data
					client.sendall(bytes(self.data,"utf-8"))

				for i in range(self.length):
					self.data = client.recv(1024).decode("utf-8")
					self.Name[i] = self.data
					client.sendall(bytes(self.data,"utf-8"))

				for i in range(self.length):
					self.data = client.recv(1024).decode("utf-8")
					self.Thread[i] = self.data
					client.sendall(bytes(self.data,"utf-8"))
			except:
				box = messagebox.showinfo("!Warning", "Lỗi kết nối ")

			self.frame_app = Frame(self.app, bg = "white", padx=20, pady = 20, borderwidth=5)
			self.frame_app.grid(row=1,columnspan=5,padx=20)
			# from tkinter import ttk

			self.scrollbar = Scrollbar(self.frame_app)
			self.scrollbar.pack(side=RIGHT,fill=Y)
			self.mybar = ttk.Treeview(self.frame_app, yscrollcommand=self.scrollbar.set)
			self.mybar.pack()
			self.scrollbar.config(command=self.mybar.yview)

			self.mybar['columns'] = ("1","2") 
			self.mybar.column("#0", anchor=CENTER, width =200,minwidth=25)
			self.mybar.column("1", anchor=CENTER, width=100)
			self.mybar.column("2", anchor=CENTER, width=100)

			self.mybar.heading("#0", text="App Name", anchor=W)
			self.mybar.heading("1",text = "ID", anchor=CENTER)
			self.mybar.heading("2", text = "Counting threading", anchor=CENTER)
			for i in range(self.length):
				self.mybar.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))

		def KillWindow():
			self.KillTask = Tk()
			self.KillTask.geometry("300x50")
			self.KillTask.title("Kill")
			self.EnterName = Entry(self.KillTask, width = 35)
			self.EnterName.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )
			self.EnterName.insert(END,"Nhập tên")

			def PressKill():
				self.AppName = self.EnterName.get()
				client.sendall(bytes("KillTask","utf-8"))
				try:
					client.sendall(bytes(self.AppName,"utf-8"))
					self.checkdata = client.recv(1024).decode("utf-8")
					if (self.checkdata == "Da xoa tac vu"):
						messagebox.showinfo("", "Đã đóng chương trình")
					else:
						messagebox.showinfo("", "Không tìm thấy chương trình")
				except:
					messagebox.showinfo("", "Không tìm thấy chương trình")

			KillButton = Button(self.KillTask, text = "Kill", bg = "#FFE4E1",font = "Helvetica 10 bold",padx = 20, command = PressKill, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

		def StartTask():
			self.StartTask = Tk()
			self.StartTask.geometry("300x50")
			self.StartTask.title("Start")

			self.EnterName = Entry(self.StartTask, width = 35)
			self.EnterName.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
			self.EnterName.insert(END,"Nhập Tên")

			def PressStart():
				self.Name = self.EnterName.get()
				client.sendall(bytes("OpenTask","utf-8"))
				try:
					client.sendall(bytes(self.Name,"utf-8"))
					self.checkdata = client.recv(1024).decode("utf-8")
					if (self.checkdata == "Da mo"):
						messagebox.showinfo("", "Chương trình đã bật")
					else:
						messagebox.showinfo("", "Không tìm thấy chương trình")
				except:
					messagebox.showinfo("", "Không tìm thấy chương trình")

			StartButton = Button(self.StartTask, text = "Start",bg = "#FFE4E1",font = "Helvetica 10 bold", padx = 20, command = PressStart, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

		Kill = Button( self.app, text = "Kill",bg = "#00FFFF",font = "Helvetica 11 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5, activebackground='#F4A460').grid(row = 0, column = 0, padx = 10)
		Watch = Button(self.app, text = "Watch",bg = "#00EEEE",font = "Helvetica 11 bold", padx = 30,  pady = 20, command = WatchTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 1, padx = 10)
		Xoa = Button(self.app, text =  "Delete",bg = "#00CDCD", font = "Helvetica 11 bold",padx = 30, pady = 20, command = XoaTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 2, padx = 10)
		Start = Button(self.app, text="Start", bg = "#008B8B", font = "Helvetica 11 bold",padx = 30, pady = 20, command = StartTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 3, padx = 10)

# Hàm khởi động các process (Watch, Kill, Start)
	def processRunning(self, client):
		try:
			self.process = Tk()
			self.process.configure(bg = "#FFFAF0")
			self.process.title("Process Running")
			
			def XoaTask():
				self.frame_process.destroy()

			def WatchTask():
				global frame_process
				global PORT
				PORT = 1234
				self.length = 0
				self.ID = [''] * 100000
				self.Name = [''] * 100000
				self.Thread = [''] * 100000
				try:
					client.sendall(bytes("ProcessRunning","utf-8"))
				except:
					messagebox.showinfo("!Warning", "Lỗi kết nối ")
					self.process.destroy()

				#Receive data
				try:
					self.length = client.recv(1024).decode("utf-8")
					self.length = int(self.length)
					for i in range(self.length):
						self.data = client.recv(1024).decode("utf-8")
						self.ID[i] = self.data
						client.sendall(bytes(self.data,"utf-8"))

					for i in range(self.length):
						self.data = client.recv(1024).decode("utf-8")
						self.Name[i] = self.data
						client.sendall(bytes(self.data,"utf-8"))

					for i in range(self.length):
						self.data = client.recv(1024).decode("utf-8")
						self.Thread[i] = self.data
						client.sendall(bytes(self.data,"utf-8"))
				except:
					box = messagebox.showinfo("!Warning", "Lỗi kết nối ")

				self.frame_process = Frame(self.process, bg = "white",padx=20, pady = 20, borderwidth=5)
				self.frame_process.grid(row=1,columnspan=5,padx=20)
				# from tkinter import ttk

				self.scrollbar = Scrollbar(self.frame_process)
				self.scrollbar.pack(side=RIGHT,fill=Y)
				self.mybar = ttk.Treeview(self.frame_process, yscrollcommand=self.scrollbar.set)
				self.mybar.pack()
				self.scrollbar.config(command=self.mybar.yview)

				self.mybar['columns'] = ("1","2") 
				self.mybar.column("#0", anchor=CENTER, width =200,minwidth=25)
				self.mybar.column("1", anchor=CENTER, width=100)
				self.mybar.column("2", anchor=CENTER, width=100)

				self.mybar.heading("#0", text="Process Name", anchor=W)
				self.mybar.heading("1",text = "ID", anchor=CENTER)
				self.mybar.heading("2", text = "Counting threading", anchor=CENTER)
				for i in range(self.length):
					self.mybar.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))

			def KillWindow():
				self.KillTask = Tk()
				self.KillTask.geometry("300x50")
				self.KillTask.title("Kill")

				self.EnterName = Entry(self.KillTask, width = 35)
				self.EnterName.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )
				self.EnterName.insert(END,"Nhập tên")

				def PressKill1():
					self.AppName = self.EnterName.get()
					client.sendall(bytes("KillTask","utf-8"))
					try:
						
						client.sendall(bytes(self.AppName,"utf-8"))
						self.checkdata = client.recv(1024).decode("utf-8")
						messagebox.showinfo("", "Đã đóng chương trình")
					except:
						messagebox.showinfo("", "Không tìm thấy chương trình")

				KillButton = Button(self.KillTask, bg = "#FFE4E1",text = "Kill", font = "Helvetica 10 bold", padx = 20, command = PressKill1, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

			def StartTask():
				self.StartTask = Tk()
				self.StartTask.geometry("300x50")
				self.StartTask.title("Start")

				self.EnterName = Entry(self.StartTask, width = 35)
				self.EnterName.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
				self.EnterName.insert(END,"Nhập Tên")

				def PressStart1():
					self.Name = self.EnterName.get()
					client.sendall(bytes("OpenTask","utf-8"))
					try:
						client.sendall(bytes(self.Name,"utf-8"))
						self.checkdata = client.recv(1024).decode("utf-8")
						messagebox.showinfo("", "Chương trình đã bật")
					except:
						messagebox.showinfo("", "Không tìm thấy chương trình")

				StartButton = Button(self.StartTask, text = "Start", bg = "#FFE4E1",font = "Helvetica 10 bold", padx = 20, command = PressStart1).grid(row=0, column=4, padx=5, pady=5)

			Kill = Button( self.process, text = "Kill", bg = "#2E8B57",font = "Helvetica 10 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5, activebackground='#F4A460').grid(row = 0, column = 0, padx = 0)
			Watch = Button(self.process, text = "Watch",bg = "#54FF9F",font = "Helvetica 10 bold",  padx = 30,  pady = 20, command = WatchTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 1, padx = 0)
			Xoa = Button(self.process, text =  "Delete", bg = "#4EEE94",font = "Helvetica 10 bold", padx = 30, pady = 20, command = XoaTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 2, padx = 0)
			Start = Button(self.process, text="Start", bg = "#43CD80", font = "Helvetica 10 bold", padx = 30, pady = 20, command = StartTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 3, padx = 0)

		except:
			messagebox.showinfo("!Warning", "Lỗi kết nối ")

# Hàm chỉnh sửa các Registry
	def editRegistry(self, client):
		try:
			Registry(client)	# Đọc hàm Registry

		except:
			messagebox.showinfo("!Warning", "Lỗi kết nối ")

# Hàm theo dõi bàn phím (Hoạt động như Keylogger)
	def keyStroke(self, client):
		KeystrokeMain(client)		# Đọc hàm KeystrokeMain

# Hàm thoát	chương trình	
	def exist(self, client):
			try:
				client.send(bytes("Exit", 'utf-8'))			# Gửi thông điệp để thoát khỏi chương trình 
			except:
				messagebox.showinfo("!Warning", "Lỗi kết nối ")
			client.close()								# Đóng kết nối
			self.Window.destroy()						# Đóng cửa sổ

# Hàm xử lý kết nối giữa server - client
	def Connection_handling(self, HOST):
		client = socket(AF_INET,SOCK_STREAM)
	#Kiểm tra lỗi kết nối bằng cách dùng try và except
		try: 
			client.connect((HOST, 1234))				# Kết nối tới server
			client.send(bytes("Success", 'utf-8'))		# Gửi thông điệp thành công
			messagebox.showinfo("Successful!!!", "Kết nối server thành công")		#Nếu đúng sẽ hiển thị thông báo thành công
			rcv = Thread(target=self.Control(client))				# Sau đó gọi đến hàm Control để hiển thị các nút điều khiển
			rcv.start()
		except:     
			messagebox.showinfo(" Error! ", "Không thể kết nối đến server")  # Nếu lỗi thì in ra màn hình, sau đó đóng kết nối client
			client.close()
if __name__ == "__main__":		# Nếu chương trình được chạy tự động thì sẽ chạy hàm main
	GUI()						# Gọi hàm GUI để hiển thị các nút điều khiển
