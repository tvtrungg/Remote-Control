from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import sys
from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
from PIL import Image
import Keystroke_Client				# KeyStroke.py
import Registry_Client				# Registry.py
import processRunning_Client		# processRunning.py
import appRunning_Client			# appRunning.py
import screenCapture_Client			# screenCapture.py

class GUI:
	def __init__(self):
		self.Home = Tk()
		self.Home.withdraw()
		self.Home.configure(bg="#FFFAF0")
	# Hộp thoại đăng nhập IP
		self.login = Toplevel()
		self.login.configure(bg = "#fff")
	# Tạo tiêu đề cho hộp thoại
		self.login.title("Login")
		self.login.resizable(width = False,height = False)		# Không cho phép thay đổi kích thước của hộp thoại
		self.login.configure(width = 600,height = 550)			# Kích thước của hộp thoại
		
	# Tạo label
		self.labelIP = Label(self.login, text = "Nhập địa chỉ IP để tiếp tục:", compound="center", bg ="#fff",font = "Helvetica 15 bold")
		self.labelIP.place(relx = 0.05,rely = 0.1)

	# Tạo input text IP
		self.input_IP = Entry(self.login, textvariable = StringVar(), bg ="#FFFAF0", font = "Helvetica 14")
		self.input_IP.place(relx = 0.501,rely = 0.105)

	# Tạo nút nhấn, khi nhấn nút =>  dữ liệu sẽ được gửi đến server thông qua socket
		self.go = Button(self.login,text = "Kết nối", width =18 ,bg = "#d3d3d3",font = "Helvetica 14 bold",command = (lambda : self.Connection_handling(self.input_IP.get())), bd = 5, activebackground='#F4A460')
		self.go.place(relx = 0.3,rely = 0.2)
		self.Home.mainloop()
		
	def Control(self, client): # Các hộp thoại chức năng điều khiển
	# Process Running
		self.process = Button(self.login, text = "Process Running", bg = "#0d54b0", height =16, font=('Helvetica 10 bold'), command =(lambda : self.processRunning(client)), bd = 5, activebackground='#F4A460')
		self.process.place(relx = 0.02, rely = 0.35)
	# App Running
		self.app = Button (self.login, text ="App Running", bg = "#fee5c6",width =38,height =4, font=('Helvetica 10 bold'), command = (lambda : self.appRunning(client)), bd = 5, activebackground='#F4A460')
		self.app.place(relx = 0.24, rely = 0.35)
	# Chụp màn hình
		self.capture = Button(self.login, text ="Screen Capture",bg = "#2baf2b", width =23, height =5, font=('Helvetica 10 bold'), command = (lambda : self.screenCapture(client)), bd = 5, activebackground='#F4A460')
		self.capture.place(relx = 0.44, rely = 0.52)
	#  Sửa registry
		self.fix =Button(self.login, text="Edit registry",bg = "#00acee",height =3 , width =38, font=('Helvetica 10 bold'), command = (lambda : self.editRegistry(client)), bd = 5, activebackground='#F4A460')
		self.fix.place(relx = 0.24, rely = 0.72)
	# Keystroke
		self.key = Button(self.login, text ="Keystroke",bg = "#ffcc2f", height =11, width =11,font=('Helvetica 10 bold'), command = (lambda : self.keyStroke(client)), bd = 5, activebackground='#F4A460')
		self.key.place(relx = 0.79, rely = 0.345)
	# Tắt máy
		self.shut = Button(self.login,text ="Shut Down", bg = "#c6c2c2", width =12, height =5, font=('Helvetica 10 bold'), command = (lambda : self.shutDown(client)), bd = 5, activebackground='#F4A460')
		self.shut.place(relx = 0.24, rely = 0.52)
	# Thoát
		self.escape = Button(self.login, text ="Exit",bg = "#ef5734",height =3, width =11,font=('Helvetica 10 bold'), command = (lambda : self.exist(client)), bd = 5, activebackground='#F4A460')
		self.escape.place(relx = 0.79, rely = 0.72)      
		# self.top.mainloop()
	
#Hàm chụp ảnh màn hình
	def screenCapture(self, client):
		try:
			screenCapture_Client.screenCapture(self, client)	# Đọc hàm screenCapture
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")
	
# Hàm khởi động các chương trình (Watch, Kill, Start)
	def appRunning(self, client):
		try:
			appRunning_Client.appRunning(self, client)	# Đọc hàm appRunning
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")
	
# Hàm khởi động các process (Watch, Kill, Start)
	def processRunning(self, client):
		try:
			processRunning_Client.processRunning(self, client)	# Đọc hàm Registry
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")


# Hàm chỉnh sửa các Registry
	def editRegistry(self, client):
		try:
			Registry_Client.RegistryEdit(client)	# Đọc hàm RegistryEdit
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")


# Hàm theo dõi bàn phím (Hoạt động như Keylogger)
	def keyStroke(self, client):
		try:
			Keystroke_Client.keystroke(client)		# Đọc hàm keystroke của file Keystroke_Client
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")


# Hàm Shutdown 
	def shutDown(self, client):
		try:
			client.send(bytes("Shutdown",'utf-8'))		# Gửi thông điệp "shut down" đến server, server sẽ tự động tắt máy trong 30s
		except:
			messagebox.showinfo(" ", "Lỗi kết nối ")	# Nếu lỗi kết nối thì thông báo lỗi

# Hàm thoát	chương trình	
	def exist(self, client):
			try:
				client.send(bytes("Exit", 'utf-8'))			# Gửi thông điệp để thoát khỏi chương trình 
			except:
				messagebox.showinfo("Error !!!", "Lỗi kết nối ")
			client.close()								# Đóng kết nối
			self.Home.destroy()						# Đóng cửa sổ


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