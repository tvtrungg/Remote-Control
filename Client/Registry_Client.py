from tkinter import Tk, W, E
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import filedialog

def RegistryEdit(client): 
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
	Register = Tk()										# tạo cửa sổ mới 
	Register.geometry("480x450")						# đặt kích thước cửa sổ
	Register.title("Registry")							# đặt tiêu đề cửa sổ
	Register.configure(bg = '#d7f7fc')					# đặt màu nền cửa sổ
	Register.resizable(False, False)					# không thay đổi kích thước cửa sổ
	pathing = StringVar()								# khởi tạo biến chứa đường dẫn
	linking = ''										# khởi tạo biến chứa đường dẫn
	browser = Entry(Register,bg = "#fff5d0", width=55)	# khởi tạo ô nhập đường dẫn
	browser.grid(row=0, column=0, padx = 10)			# đặt ô nhập đường dẫn
	regis = Text(Register,bg = "#fff5d0", height = 7, width = 41)	# khởi tạo ô nhập đường dẫn
	regis.grid(row=2, column=0, pady=10)				# đặt ô nhập đường dẫn

	def Browse():
		nonlocal pathing, linking						# khởi tạo biến chứa đường dẫn
		fname = filedialog.askopenfilename()			# chọn tệp tin
		pathing.set(fname)								# đặt đường dẫn vào biến
		browser.insert(0, fname)						# đặt đường dẫn vào ô nhập
		linking = browser.get()							# lấy đường dẫn từ ô nhập
		fileopen = open(linking,'r')					# mở tệp tin
		line = fileopen.read()							# đọc tệp tin
		regis.insert(1.0,line)							# đặt đường dẫn vào ô nhập
	ButtonBrowse = Button(Register, text="Browser", font = "Helvetica 10 bold",bg = "#f8dddf", activebackground='#be9d9f',command=Browse, padx = 28)
	ButtonBrowse.grid(row=0, column=1, padx = 10)		# đặt ô nhập đường dẫn	

	def RegContent():
		nonlocal regis									# khởi tạo biến chứa đường dẫn
		client.sendall(bytes("SendingReg", "utf-8"))	# gửi lệnh đến server
		checkdata = client.recv(1024).decode("utf-8") 	# nhận dữ liệu từ server
		line = regis.get(1.0,END)						# lấy dữ liệu từ ô nhập
		client.sendall(bytes(line,"utf-8"))				# gửi dữ liệu tới server
		checkdata = client.recv(1024).decode("utf-8")	# nhận dữ liệu từ server
	ContentButton = Button(Register, text="Gửi nội dung", font = "Helvetica 10 bold",bg = "#f8dddf",activebackground='#be9d9f',height = 4, command = RegContent, padx = 15, pady = 28)
	ContentButton.grid(row=2, column=1, padx = 10)

	SecondFrame = LabelFrame(Register, text="Sửa giá trị trực tiếp")	# khởi tạo cửa sổ
	SecondFrame.grid(row=3, columnspan = 2, padx = 0, pady = 0)		# đặt cửa sổ

	def changeFunction(event):
		if getFunction.get() == "Get value":
			Name.grid_forget()							# ẩn ô nhập tên
			Value.grid_forget()							# ẩn ô nhập giá trị
			infomation.grid_forget()					# ẩn ô nhập thông tin
			Name.grid(row=2, column=0, sticky = W)		# hiện ô nhập tên

		elif getFunction.get() == "Set value":
			Name.grid_forget()							# ẩn ô nhập tên
			Value.grid_forget()							# ẩn ô nhập giá trị
			infomation.grid_forget()					# ẩn ô nhập thông tin
			Name.grid(row=2, column=0, sticky = W)		# hiện ô nhập tên
			Value.grid(row=2, column=0, sticky = N)		# hiện ô nhập giá trị
			infomation.grid(row=2, column=0, sticky = E, padx=4)       
		elif getFunction.get() == "Delete value":
			Name.grid_forget()							# ẩn ô nhập tên
			Value.grid_forget()							# ẩn ô nhập giá trị
			infomation.grid_forget()					# ẩn ô nhập thông tin
			Name.grid(row=2, column=0, sticky = W)		# hiện ô nhập tên

		elif getFunction.get() == "Create key":
			Name.grid_forget()							# ẩn ô nhập tên
			Value.grid_forget()							# ẩn ô nhập giá trị
			infomation.grid_forget()					# ẩn ô nhập thông tin

		elif getFunction.get() == "Delete key":
			Name.grid_forget()							# ẩn ô nhập tên
			Value.grid_forget()							# ẩn ô nhập giá trị
			infomation.grid_forget()					# ẩn ô nhập thông tin

    # Sửa giá trị trực tiếp
	getFunction = ttk.Combobox(SecondFrame, value=OPTION_1)		# khởi tạo ô chọn chức năng
	getFunction.insert(0, "Chọn chức năng")						# đặt giá trị mặc định
	getFunction.bind("<<ComboboxSelected>>", changeFunction)	# gọi hàm changeFunction khi chọn chức năng
	getFunction.grid(row=0,column=0,ipadx=160, sticky=W)		# đặt ô chọn chức năng
	path = Entry(SecondFrame, width=77)
	path.insert(0, "Đường dẫn")									# đặt giá trị mặc định
	path.grid(row=1, column=0, pady=10)							# đặt ô nhập đường dẫn
	Name = Entry(SecondFrame, width = 24)						# khởi tạo ô nhập tên
	Name.insert(0, "Name value")								
	Name.grid(row=2, column=0, sticky = W)
	Value = Entry(SecondFrame, width = 25)
	Value.insert(0, "Value")									
	Value.grid(row=2, column=0, sticky = N)
	infomation = ttk.Combobox(SecondFrame, value=OPTION_2)		# khởi tạo ô chọn thông tin
	infomation.insert(0, "Kiểu dữ liệu")						
	infomation.grid(row=2, column=0, sticky = E, padx=4)
	Thongbao = Frame(SecondFrame)
	Thongbao.grid(row=3, column=0)
	Noti = Canvas(Thongbao, height=150, width =440)				# khởi tạo khung hiển thị thông báo
	Noti.pack(side=LEFT, fill=BOTH, expand=1)					# đặt ô thông báo
	Lenh = Frame(Noti)											# khởi tạo khung hiển thị lệnh
	Noti.create_window((0,0), window=Lenh, anchor="nw")			# đặt ô lệnh

	def ButtonGui():
		if getFunction.get() == "Get value":						# nếu chọn chức năng lấy giá trị
			client.sendall(bytes("GettingValueReg","utf-8"))		# gửi lệnh lấy giá trị
			NameVal = Name.get()									# lấy tên giá trị
			Links = path.get()										# lấy đường dẫn
			client.sendall(bytes(NameVal,"utf-8"))					# gửi tên giá trị
			checkdata = client.recv(1024).decode("utf-8")			# nhận kết quả
			client.sendall(bytes(Links,"utf-8"))					# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")			# nhận kết quả
			data = client.recv(1024).decode("utf-8")				# nhận kết quả
			client.sendall(bytes("Da nhan", "utf-8"))				# gửi lệnh đã nhận

			if data == "Khong tim thay":
				chuoi = Label(Lenh, text="Không tìm thấy")			# nếu không tìm thấy
				chuoi.pack(side = BOTTOM)							# đặt chuỗi
			else: 
				chuoi = Label(Lenh, text=data)						# nếu tìm thấy
				chuoi.pack(side = BOTTOM)							# đặt chuỗi

		elif getFunction.get() == "Set value":
			client.sendall(bytes("SettingValueReg","utf-8"))	# gửi lệnh đặt giá trị
			NameVal = Name.get()								# lấy tên giá trị
			Links = path.get()									# lấy đường dẫn
			client.sendall(bytes(NameVal,"utf-8"))				# gửi tên giá trị
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			client.sendall(bytes(Links,"utf-8"))				# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			Kieudulieu = infomation.get()						# lấy kiểu dữ liệu
			client.sendall(bytes(Kieudulieu, "utf-8"))			# gửi kiểu dữ liệu
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			values = Value.get()								# lấy giá trị
			client.sendall(bytes(values,"utf-8"))				# gửi giá trị
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả

			status = client.recv(1024).decode("utf-8")			# nhận kết quả
			print("status")										# in kết quả
			client.sendall(bytes("Da nhan", "utf-8"))			# gửi lệnh đã nhận
			if status == "succeed":								# nếu thành công
				chuoi = Label(Lenh, text="Set giá trị thành công")		# đặt chuỗi
				chuoi.pack(side = BOTTOM)						# đặt chuỗi
			elif status == "Sai duong dan":						# nếu sai đường dẫn
				chuoi = Label(Lenh, text="Sai đường dẫn")		# đặt chuỗi
				chuoi.pack(side = BOTTOM)						# đặt chuỗi
			else:   
				chuoi = Label(Lenh, text="Lỗi giá trị")			# đặt chuỗi
				chuoi.pack(side = BOTTOM)						# đặt chuỗi

		elif getFunction.get() == "Create key":					# nếu là tạo khóa
			client.sendall(bytes("CreatingKey","utf-8"))		# gửi lệnh tạo khóa
			Links = path.get()									# lấy đường dẫn
			client.sendall(bytes(Links,"utf-8"))				# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			data = client.recv(1024).decode("utf-8")			# nhận kết quả
			client.sendall(bytes("Da nhan","utf-8"))			# gửi lệnh đã nhận
			if data == "Da tao thanh cong":
				chuoi = Label(Lenh, text="Đã tạo thành công")	# đặt chuỗi
				chuoi.pack(side = BOTTOM)          				
			else: 
				chuoi = Label(Lenh, text="Sai đường dẫn")		# đặt chuỗi
				chuoi.pack(side = BOTTOM)						

		elif getFunction.get() == "Delete value":
			client.sendall(bytes("DeletingValueReg","utf-8"))	# gửi lệnh xóa giá trị
			Links = path.get()									# lấy đường dẫn
			NameVal = Name.get()								# lấy tên giá trị
			client.sendall(bytes(Links,"utf-8"))				# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			client.sendall(bytes(NameVal,"utf-8"))				# gửi tên giá trị
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			client.sendall(bytes("Gui noi dung","utf-8"))     	# gửi lệnh gửi nội dung
			data = client.recv(1024).decode("utf-8")			# nhận kết quả
			chuoi = Label(Lenh, text=data)						
			chuoi.pack(side = BOTTOM)							# đặt chuỗi
			client.sendall(bytes("In thanh cong","utf-8"))		# gửi lệnh đã nhận

		elif getFunction.get() == "Create key":
			client.sendall(bytes("CreatingKey","utf-8"))		# gửi lệnh tạo khóa
			Links = path.get()									# lấy đường dẫn
			client.sendall(bytes(Links,"utf-8"))				# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			data = client.recv(1024).decode("utf-8")			
			client.sendall(bytes("Da nhan","utf-8"))			# gửi lệnh đã nhận
			chuoi = Label(Lenh, text=data)						# đặt chuỗi
			chuoi.pack(side = BOTTOM)        					

		elif getFunction.get() == "Delete key":
			client.sendall(bytes("DeletingKey","utf-8"))		# gửi lệnh xóa khóa
			Links = path.get()									# lấy đường dẫn
			client.sendall(bytes(Links,"utf-8"))				# gửi đường dẫn
			checkdata = client.recv(1024).decode("utf-8")		# nhận kết quả
			data = client.recv(1024).decode("utf-8")			
			client.sendall(bytes("Da nhan","utf-8"))			# gửi lệnh đã nhận
			if data == "Da xoa thanh cong":						# nếu xóa thành công
				chuoi = Label(Lenh, text="Đã xoá thành công")	# đặt chuỗi
				chuoi.pack(side = BOTTOM)          				
			else: 
				chuoi = Label(Lenh, text="Sai đường dẫn")		# đặt chuỗi
				chuoi.pack(side = BOTTOM)                
	def ButtonXoa():
		for widget in Lenh.winfo_children(): widget.destroy()		# xóa các chuỗi

	BelowButton = Frame(SecondFrame)
	send = Button(BelowButton, text="Gửi",activebackground='#5f7575',font = "Helvetica 10 bold",bg = "#aad0d1", command = ButtonGui)
	send.grid(row=0, column=0, ipadx = 35)
	delete = Button(BelowButton, text="Xoá",activebackground='#5f7575',font = "Helvetica 10 bold",bg = "#aad0d1", command = ButtonXoa)
	delete.grid(row=0, column=1, ipadx = 35)
	BelowButton.grid(sticky=S)
	Register.mainloop()
