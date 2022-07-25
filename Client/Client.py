from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from PIL import Image
import Keystroke_Client				# KeyStroke.py
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
		self.login.geometry("650x650")
		self.background= PhotoImage(file='./img/button/background.png')
		self.mylabel = Label(self.login, image=self.background)
		self.mylabel.place(x=0, y=0, relwidth=1, relheight=1)
	# Tạo label
		self.labelIP = Label(self.login, text = "Nhập địa chỉ IP để tiếp tục:", compound="center", bg ="#fff",font = "Helvetica 15 bold")
		self.labelIP.place(relx = 0.05,rely = 0.1)
	# Tạo input text IP
		self.input_IP = Entry(self.login, textvariable = StringVar(), bg ="#FFFAF0", font = "Helvetica 14")
		self.input_IP.place(relx = 0.501,rely = 0.105)
	# Tạo nút nhấn, khi nhấn nút =>  dữ liệu sẽ được gửi đến server thông qua socket
		self.connect = Button(self.login,text = "Kết nối", width =18 ,bg = "#d3d3d3",font = "Helvetica 14 bold",command = (lambda : self.Connection_handling(self.input_IP.get())), bd = 5, activebackground='#F4A460')
		self.connect.place(relx = 0.3,rely = 0.2)		# Tọa độ x, y của nút nhấn

		self.Home.mainloop()							# Chạy hệ thống
		
	def Controller(self, Client): # Các hộp thoại chức năng điều khiển
	# Process Running
		self.btn1= PhotoImage(file='./img/button/1.png')                      # Đặt hình ảnh
		self.process = Button(self.login, image = self.btn1, command =(lambda : self.processRunning(Client)), bd = 0, bg = "#fff")
		self.process.place(relx = 0.04, rely = 0.35)
	# App Running
		self.btn2= PhotoImage(file='./img/button/2.png')                      # Đặt hình ảnh
		self.app = Button (self.login, image=self.btn2, command = (lambda : self.appRunning(Client)), bd = 0, bg = "#fff")
		self.app.place(relx = 0.24, rely = 0.35)
	# Chụp màn hình
		self.btn3= PhotoImage(file='./img/button/2.png')                      # Đặt hình ảnh
		self.capture = Button(self.login,  image=self.btn3, command = (lambda : self.screenCapture(Client)), bd = 0, bg = "#fff")
		self.capture.place(relx = 0.24, rely = 0.706)
	# Keystroke
		self.btn4= PhotoImage(file='./img/button/1.png')                      # Đặt hình ảnh
		self.key = Button(self.login, image = self.btn4, command = (lambda : self.keyStroke(Client)), bd = 0, bg = "#fff")
		self.key.place(relx = 0.765, rely = 0.35)
	# Tắt máy
		self.btn5= PhotoImage(file='./img/button/3.png')                      # Đặt hình ảnh
		self.shut = Button(self.login, image = self.btn5, command = (lambda : self.shutDown(Client)), bd = 0, bg= "#fff")
		self.shut.place(relx = 0.24, rely = 0.525)
	# Thoát
		self.btn6= PhotoImage(file='./img/button/3.png')                      # Đặt hình ảnh
		self.escape = Button(self.login, image = self.btn6, command = (lambda : self.exist(Client)), bd = 0,bg = "#fff")
		self.escape.place(relx = 0.504, rely = 0.525)      
	
#Hàm chụp ảnh màn hình
	def screenCapture(self, Client):
		try:
			screenCapture_Client.screenCapture(self, Client)	# Đọc hàm screenCapture
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối")		# Thông báo lỗi nếu hàm lỗi
	
# Hàm khởi động các chương trình (Watch, Kill, Start)
	def appRunning(self, Client):
		try:
			appRunning_Client.appRunning(self, Client)	# Đọc hàm appRunning
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")
	
# Hàm khởi động các process (Watch, Kill, Start)
	def processRunning(self, Client):
		try:
			processRunning_Client.processRunning(self, Client)	# Đọc hàm processRunning
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")

# Hàm theo dõi bàn phím (Hoạt động như Keylogger)
	def keyStroke(self, Client):
		try:
			Keystroke_Client.keystroke(Client)		# Đọc hàm keystroke của file Keystroke_Client
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")


# Hàm Shutdown 
	def shutDown(self, Client):
		try:
			Client.send(bytes("Shutdown",'utf-8'))		# Gửi thông điệp "shut down" đến server, server sẽ tự động tắt máy trong 30s
			messagebox.showinfo("Success", "Máy tính sẽ tắt sau 30s")	# Thông báo thành công
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")	# Nếu lỗi kết nối thì thông báo lỗi

# Hàm thoát	chương trình	
	def exist(self, Client):
		try:
			Client.send(bytes("Exit", 'utf-8'))			# Gửi thông điệp để thoát khỏi chương trình 
		except:
			messagebox.showinfo("Error !!!", "Lỗi kết nối ")
		Client.close()							# Đóng kết nối
		self.Home.destroy()						# Đóng cửa sổ


# Hàm xử lý kết nối giữa server - Client
	def Connection_handling(self, HOST):
		Client = socket(AF_INET,SOCK_STREAM)
	#Kiểm tra lỗi kết nối bằng cách dùng try và except
		try: 
			Client.connect((HOST, 1234))				# Kết nối tới server
			# Client.send(bytes("Success", 'utf-8'))		# Gửi thông điệp thành công
			messagebox.showinfo("Successful !!!", "Kết nối server thành công")		#Nếu đúng sẽ hiển thị thông báo thành công
			rcv = Thread(target=self.Controller(Client))				# Sau đó gọi đến hàm Controller để hiển thị các nút điều khiển
			rcv.start()
		except:     
			messagebox.showinfo(" Error!!!", "Không thể kết nối đến server")  # Nếu lỗi thì in ra màn hình, sau đó đóng kết nối client
			Client.close()


if __name__ == "__main__":		# Nếu chương trình được chạy tự động thì sẽ chạy hàm main
	GUI()						# Gọi hàm GUI để hiển thị các nút điều khiển