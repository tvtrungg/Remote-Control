from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def appRunning(self, client):				# appRunning_Client.py
		self.app = Tk()						# Tạo hộp thoại
		self.app.title("App Running")		# Tạo tiêu đề
		self.app.configure (bg = "white")	# Tạo màu nền
	# Hàm xóa tác vụ						# Tạo hàm xóa tác vụ
		def XoaTask():						# Tạo hàm xóa tác vụ
			self.frame_app.destroy()		# Xóa frame_app
	# Hiển thị các tác vụ
		def WatchTask():
			global frame_app				# Tạo biến frame_app
			global PORT						# Tạo biến PORT
			PORT = 1234						# Gán giá trị cho biến PORT
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
				self.length = client.recv(1024).decode("utf-8")		# Nhận dữ liệu từ server
				self.length = int(self.length)						# Chuyển dữ liệu từ string sang int
				for i in range(self.length):						# Vòng lặp lấy dữ liệu
					self.data = client.recv(1024).decode("utf-8")	# Nhận dữ liệu từ server
					self.ID[i] = self.data							# Gán giá trị cho mảng ID
					client.sendall(bytes(self.data,"utf-8"))		# Gửi dữ liệu từ server

				for i in range(self.length):						# Vòng lặp lấy dữ liệu
					self.data = client.recv(1024).decode("utf-8")	# Nhận dữ liệu từ server
					self.Name[i] = self.data						# Gán giá trị cho mảng Name
					client.sendall(bytes(self.data,"utf-8"))		# Gửi dữ liệu từ server

				for i in range(self.length):						# Vòng lặp lấy dữ liệu
					self.data = client.recv(1024).decode("utf-8")	# Nhận dữ liệu từ server
					self.Thread[i] = self.data						# Gán giá trị cho mảng Thread
					client.sendall(bytes(self.data,"utf-8"))		# Gửi dữ liệu từ server
			except:
				box = messagebox.showinfo("Error !!!", "Lỗi kết nối ")	# Thông báo lỗi kết nối

			self.frame_app = Frame(self.app, bg = "white", padx=20, pady = 20, borderwidth=5)	# Tạo frame_app
			self.frame_app.grid(row=1,columnspan=5,padx=20)										# Thêm frame_app vào app

			self.scrollbar = Scrollbar(self.frame_app)											# Tạo scrollbar
			self.scrollbar.pack(side=RIGHT,fill=Y)												# Thêm scrollbar vào frame_app
			self.mybar = ttk.Treeview(self.frame_app, yscrollcommand=self.scrollbar.set)		# Tạo treeview
			self.mybar.pack()																	# Thêm treeview vào frame_app
			self.scrollbar.config(command=self.mybar.yview)										# Thêm scrollbar vào treeview

			self.mybar['columns'] = ("1","2") 													# Thêm cột vào treeview
			self.mybar.column("#0", anchor=CENTER, width =200,minwidth=25)						# Thiết lập chiều rộng cột #0
			self.mybar.column("1", anchor=CENTER, width=100)									# Thiết lập chiều rộng cột 1
			self.mybar.column("2", anchor=CENTER, width=100)									# Thiết lập chiều rộng cột 2

			self.mybar.heading("#0", text="App Name", anchor=W)									# Thiết lập tiêu đề cột #0
			self.mybar.heading("1",text = "ID", anchor=CENTER)									# Thiết lập tiêu đề cột 1
			self.mybar.heading("2", text = "Counting threading", anchor=CENTER)					# Thiết lập tiêu đề cột 2
			for i in range(self.length):														# Vòng lặp lấy dữ liệu
				self.mybar.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))	# Thêm dữ liệu vào treeview

		def KillWindow():
			self.KillTask = Tk()				# Tạo một cửa sổ mới
			self.KillTask.geometry("300x50")	# Thiết lập kích thước cửa sổ
			self.KillTask.title("Kill")			# Thiết lập tiêu đề của cửa sổ
			self.EnterName = Entry(self.KillTask, width = 35)		# Tạo một ô nhập vào
			self.EnterName.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )		# Thêm ô nhập vào vào cửa sổ
			self.EnterName.insert(END,"Nhập tên")			# Thiết lập giá trị mặc định cho ô nhập

			def PressKill():
				self.AppName = self.EnterName.get()										# Lấy giá trị từ ô nhập
				client.sendall(bytes("KillTask","utf-8"))								# Gửi dữ liệu từ server
				try:
					client.sendall(bytes(self.AppName,"utf-8"))					# Gửi dữ liệu từ server
					self.checkdata = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
					if (self.checkdata == "Da xoa tac vu"):						# Kiểm tra dữ liệu nhận được
						messagebox.showinfo("", "Đã đóng chương trình")			# Thông báo đã đóng chương trình
					else:
						messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")		# Thông báo không tìm thấy chương trình
				except:
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")			# Thông báo không tìm thấy chương trình

			KillButton = Button(self.KillTask, text = "Kill", bg = "#FFE4E1",font = "Helvetica 10 bold",padx = 20, command = PressKill, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)	# Thêm nút Kill vào cửa sổ

		def StartTask():
			self.StartTask = Tk()								# Tạo một cửa sổ mới
			self.StartTask.geometry("300x50")				# Thiết lập kích thước cửa sổ
			self.StartTask.title("Start")					# Thiết lập tiêu đề của cửa sổ

			self.EnterName = Entry(self.StartTask, width = 35)	# Tạo một ô nhập vào
			self.EnterName.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)	# Thêm ô nhập vào vào cửa sổ
			self.EnterName.insert(END,"Nhập Tên")			# Thiết lập giá trị mặc định cho ô nhập

			def PressStart():
				self.Name = self.EnterName.get()									# Lấy giá trị từ ô nhập
				client.sendall(bytes("OpenTask","utf-8"))							# Gửi dữ liệu từ server
				try:
					client.sendall(bytes(self.Name,"utf-8"))				# Gửi dữ liệu từ server
					self.checkdata = client.recv(1024).decode("utf-8")		# Nhận dữ liệu từ server
					if (self.checkdata == "Da mo"):							# Kiểm tra dữ liệu nhận được
						messagebox.showinfo("", "Chương trình đã bật")		# Thông báo đã mở chương trình
					else:
						messagebox.showinfo("", "Không tìm thấy chương trình")		# Thông báo không tìm thấy chương trình
				except:
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")	# Thông báo không tìm thấy chương trình

			StartButton = Button(self.StartTask, text = "Start",bg = "#FFE4E1",font = "Helvetica 10 bold", padx = 20, command = PressStart, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

		Kill = Button( self.app, text = "Kill",bg = "#8DDDE0", activebackground='#497172',font = "Helvetica 11 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5).grid(row = 0, column = 0, padx = 8)
		Watch = Button(self.app, text = "Watch",bg = "#F9BDC0", activebackground='#7e5a5c',font = "Helvetica 11 bold", padx = 30,  pady = 20, command = WatchTask, bd = 5).grid(row = 0, column = 1, padx = 8)
		Xoa = Button(self.app, text =  "Delete",bg = "#FBE698", activebackground='#776d47', font = "Helvetica 11 bold",padx = 30, pady = 20, command = XoaTask, bd = 5).grid(row = 0, column = 2, padx = 8)
		Start = Button(self.app, text="Start", bg = "#8B795E", activebackground='#3f302a', font = "Helvetica 11 bold",padx = 30, pady = 20, command = StartTask, bd = 5).grid(row = 0, column = 3, padx = 8)
