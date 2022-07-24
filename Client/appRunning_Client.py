from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

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
			self.ID = [''] * 1000 			#Mảng lưu ID của app
			self.Name = [''] * 1000 			#Mảng lưu tên app
			self.Thread = [''] * 1000 		#Mảng lưu luồng
			try:
				client.sendall(bytes("AppRunning","utf-8"))			# Gửi yêu cầu lấy danh sách app đang chạy
			except:
				messagebox.showinfo("Error !!!", "Lỗi kết nối")		# Thông báo lỗi kết nối
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
				box = messagebox.showinfo("Error !!!", "Lỗi kết nối ")

			self.frame_app = Frame(self.app, bg = "white", padx=20, pady = 20, borderwidth=5)
			self.frame_app.grid(row=1,columnspan=5,padx=20)

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
						messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")
				except:
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")

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
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")

			StartButton = Button(self.StartTask, text = "Start",bg = "#FFE4E1",font = "Helvetica 10 bold", padx = 20, command = PressStart, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

		Kill = Button(self.app, text = "Kill",bg = "#00FFFF",font = "Helvetica 11 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5, activebackground='#F4A460').grid(row = 0, column = 0, padx = 10)
		Watch = Button(self.app, text = "Watch",bg = "#00EEEE",font = "Helvetica 11 bold", padx = 30,  pady = 20, command = WatchTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 1, padx = 10)
		Xoa = Button(self.app, text =  "Delete",bg = "#00CDCD", font = "Helvetica 11 bold",padx = 30, pady = 20, command = XoaTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 2, padx = 10)
		Start = Button(self.app, text="Start", bg = "#008B8B", font = "Helvetica 11 bold",padx = 30, pady = 20, command = StartTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 3, padx = 10)
