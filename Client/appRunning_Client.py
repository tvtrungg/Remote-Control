from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def application_function(self, client):				
		self.app = Tk()						# Tạo hộp thoại
		self.app.title("App Running")		# Tạo tiêu đề
		self.app.configure (bg = "white")	# Tạo màu nền
	# Hàm clear màn hình						
		def Clear():						
			self.app_activity.destroy()		# Xóa app_activity
	# Hiển thị các app đang chạy
		def Watch_App():
			global app_activity				# Tạo biến app_activity
			global PORT						# Tạo biến PORT
			PORT = 1234						# Gán giá trị cho biến PORT
			self.length = 0 				#Danh sách các app đang chạy
			self.ID = [''] * 1000 			#Mảng lưu ID của app
			self.Name = [''] * 1000 			#Mảng lưu tên app
			self.Thread = [''] * 1000 		#Mảng lưu luồng
			try:
				client.sendall(bytes("Watch_AppRunning","utf-8"))			# Gửi yêu cầu lấy danh sách app đang chạy
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
				messagebox.showinfo("Error !!!", "Lỗi kết nối ")	# Thông báo lỗi kết nối

			self.app_activity = Frame(self.app, bg = "white", padx=20, pady = 20, borderwidth=5)	# Tạo app_activity
			self.app_activity.grid(row=1,columnspan=5,padx=20)										# Thêm app_activity vào app

			self.scrollbar = Scrollbar(self.app_activity)											# Tạo scrollbar
			self.scrollbar.pack(side=RIGHT,fill=Y)												# Thêm scrollbar vào app_activity
			self.content_Treeview = ttk.Treeview(self.app_activity, yscrollcommand=self.scrollbar.set)		# Tạo treeview
			self.content_Treeview.pack()																	# Thêm treeview vào app_activity
			self.scrollbar.config(command=self.content_Treeview.yview)										# Thêm scrollbar vào treeview

			self.content_Treeview['columns'] = ("1","2") 													# Thêm cột vào treeview
			self.content_Treeview.column("#0", anchor=CENTER, width =200,minwidth=25)						# Thiết lập chiều rộng cột #0
			self.content_Treeview.column("1", anchor=CENTER, width=100)									# Thiết lập chiều rộng cột 1
			self.content_Treeview.column("2", anchor=CENTER, width=100)									# Thiết lập chiều rộng cột 2

			self.content_Treeview.heading("#0", text="App Name", anchor=W)									# Thiết lập tiêu đề cột #0
			self.content_Treeview.heading("1", text="ID", anchor=CENTER)									# Thiết lập tiêu đề cột 1
			self.content_Treeview.heading("2", text="Thread", anchor=CENTER)					# Thiết lập tiêu đề cột 2
			for i in range(self.length):														# Vòng lặp lấy dữ liệu
				self.content_Treeview.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))	# Thêm dữ liệu vào treeview
	# Hàm dừng 1 app
		def Kill_App():
			self.screen_KA = Tk()				# Tạo một cửa sổ mới
			self.screen_KA.geometry("320x50")	# Thiết lập kích thước cửa sổ
			self.screen_KA.title("Kill")			# Thiết lập tiêu đề của cửa sổ
			self.Name_input = Entry(self.screen_KA, width = 35)		# Tạo một ô nhập vào
			self.Name_input.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )		# Thêm ô nhập vào vào cửa sổ
			self.Name_input.insert(END,"Nhập tên")			# Thiết lập giá trị mặc định cho ô nhập

			Kill_Button = Button(self.screen_KA, text = "Kill", bg = "#FFE4E1",font = "Helvetica 10 bold",padx = 20, command = Kill_Func, bd = 5, activebackground='#877776').grid(row=0, column=4, padx=5, pady=5)	# Thêm nút Kill vào cửa sổ
	
		def Kill_Func():
				self.AppName = self.Name_input.get()										# Lấy giá trị từ ô nhập
				client.sendall(bytes("Kill_Task","utf-8"))								# Gửi dữ liệu từ server
				try:
					client.sendall(bytes(self.AppName,"utf-8"))					# Gửi dữ liệu từ server
					self.checkdata = client.recv(1024).decode("utf-8")			# Nhận dữ liệu từ server
					if (self.checkdata == "Da xoa tac vu"):						# Kiểm tra dữ liệu nhận được
						messagebox.showinfo("", "Đã đóng chương trình")			# Thông báo đã đóng chương trình
					else:
						messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")		# Thông báo không tìm thấy chương trình
				except:
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")			# Thông báo không tìm thấy chương trình
	# Hàm khởi động 1 app
		def Start_App():
			self.screen_Start = Tk()								# Tạo một cửa sổ mới
			self.screen_Start.geometry("320x50")				# Thiết lập kích thước cửa sổ
			self.screen_Start.title("Start")					# Thiết lập tiêu đề của cửa sổ

			self.Name_input = Entry(self.screen_Start, width = 35)	# Tạo một ô nhập vào
			self.Name_input.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)	# Thêm ô nhập vào vào cửa sổ
			self.Name_input.insert(END,"Nhập Tên")			# Thiết lập giá trị mặc định cho ô nhập

			Start_Button = Button(self.screen_Start, text = "Start",bg = "#F9BDC0",font = "Helvetica 10 bold", padx = 20, command = PressStart, bd = 5, activebackground='#836264').grid(row=0, column=4, padx=5, pady=5)

		def PressStart():
				self.Name = self.Name_input.get()									# Lấy giá trị từ ô nhập
				client.sendall(bytes("OpenTask","utf-8"))							# Gửi dữ liệu từ server
				try:
					client.sendall(bytes(self.Name,"utf-8"))				# Gửi dữ liệu từ server
					self.checkdata = client.recv(1024).decode("utf-8")		# Nhận dữ liệu từ server
					if (self.checkdata == "opened"):							# Kiểm tra dữ liệu nhận được
						messagebox.showinfo("", "Chương trình đã bật")		# Thông báo đã mở chương trình
					else:
						messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")		# Thông báo không tìm thấy chương trình
				except:
					messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")	# Thông báo không tìm thấy chương trình

		Start = Button(self.app, text="Start", bg = "#E6E9D0", activebackground='#bec0b1', font = "Helvetica 11 bold",padx = 30, pady = 20, command = Start_App, bd = 5).grid(row = 0, column = 0, padx = 8)
		Watch = Button(self.app, text = "Watch",bg = "#F9BDC0", activebackground='#7e5a5c',font = "Helvetica 11 bold", padx = 30,  pady = 20, command = Watch_App, bd = 5).grid(row = 0, column = 1, padx = 8)
		Kill = Button( self.app, text = "Kill",bg = "#8DDDE0", activebackground='#497172',font = "Helvetica 11 bold", padx = 30,  pady = 20, command= Kill_App, bd = 5).grid(row = 0, column = 2, padx = 8)
		Delete = Button(self.app, text =  "Delete",bg = "#FBE698", activebackground='#776d47', font = "Helvetica 11 bold",padx = 30, pady = 20, command = Clear, bd = 5).grid(row = 0, column = 3, padx = 8)
