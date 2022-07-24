import os
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
from PIL import Image

def screenCapture(self, client): 
		self.Screenshot = Toplevel()					# Tạo 1 hộp thoại mới
		self.Screenshot.title("ScreenShot")			# Đặt tiêu đề cho hộp thoại
		self.Screenshot.resizable(width = False,height = False)
		self.Screenshot.configure(bg = "#C0C0C0", width = 1085, height = 610)		# Đặt màu nền cho hộp thoại
	#Hàm nhận ảnh từ server trả về
		def ReceivePicture(): 	
			try:
				client.sendall(bytes("screenCapture","utf-8"))		# Gửi thông điệp "screenCapture" đến server
			except:
				messagebox.showinfo("Error !!!", "Lỗi kết nối")			# Nếu lỗi kết nối thì thông báo lỗi
				self.Screenshot.destroy()							# Sau đó, đóng hộp thoại Screenshot lại

			self.file = open("picture.png", 'wb')					# Tạo file ảnh mới
			self.data = client.recv(20126062)						# Nhận dữ liệu từ server
			self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
			self.img = ImageTk.PhotoImage(Image.open("picture.png"))	# Tạo ảnh từ file ảnh     
			self.canvas.create_image(0,0, anchor=NW, image=self.img)	# Vẽ ảnh lên canvas
			self.file.close()											# Đóng file ảnh
	#Hàm lưu ảnh
		def SavePicture(): 
			self.myScreenShot = open("picture.png",'rb')				# Tạo file ảnh mới
			self.data = self.myScreenShot.read()						# Đọc dữ liệu từ file ảnh
			self.fname = filedialog.asksaveasfilename(title=u'Save file', filetypes=[("PNG", ".png")])		# Đặt tên file ảnh và nhấn Save
			self.myScreenShot.close()						# Đóng file ảnh

			self.file = open(str(self.fname) + '.png','wb')			# Tạo file ảnh mới
			self.file.write(self.data)								# Ghi dữ liệu vào file ảnh
			self.file.close()										# Đóng file ảnh
			os.remove("picture.png") 								# Xóa file ảnh cũ
			self.Screenshot.destroy()								# Đóng hộp thoại Screenshot lại			
		
		def DontSavePicture():
			os.remove("picture.png") 								
			self.Screenshot.destroy()			

	#Tạo canvas   
		self.canvas = Canvas(self.Screenshot, bg = "white", width = 1080, height = 531) 	# Tạo canvas mới   
		self.canvas.place(relx = 0,rely = 0)   		# Vẽ ảnh chụp màn hình lên canvas
		
	#Tạo button Chụp ảnh	
		self.cap = Button(self.Screenshot,text="Chụp", bg = "#8DDDE0", font = "Helvetica 15 bold",width=40,height=2,borderwidth=5,command = ReceivePicture, bd = 5, activebackground='#497172') #Nút chụp hình
		self.cap.place(relx=0, rely=0.88)

	#Tạo button Lưu ảnh
		self.Save = Button(self.Screenshot, text="Lưu",bg = "#F9BDC0",font = "Helvetica 15 bold",width=26,height=2,borderwidth=5,command=SavePicture, bd = 5, activebackground='#7e5a5c')#Nút luu ảnh
		self.Save.place(relx=0.4522, rely=0.88)

	#Tạo button Không lưu ảnh
		self.DontSave = Button(self.Screenshot, text="Không Lưu",bg = "#FBE698",font = "Helvetica 15 bold", width=21, height=2,borderwidth=5,command=DontSavePicture, bd = 5, activebackground='#F4A460')#Nút luu ảnh
		self.DontSave.place(relx= 0.7521, rely = 0.88)
		self.Screenshot.mainloop()
		os.remove("picture.png") 


