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
