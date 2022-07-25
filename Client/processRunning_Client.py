from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def processRunning(self, client):
    self.process = Tk()
    self.process.title("Process Running")       # Tựa đề của cửa sổ
    self.process.configure(bg="#FFFAF0")        # Màu nền

    def Clear():
        self.frame_process.destroy()            # Xóa frame_process

    def WatchTask():
        global frame_process                    # Khai báo biến frame_process
        global PORT                             # Khai báo biến PORT
        PORT = 1234                             # Khai báo PORT
        self.length = 0                         # Khai báo biến length
        self.ID = [''] * 1000                   # Khai báo biến ID
        self.Name = [''] * 1000                 # Khai báo biến Name
        self.Thread = [''] * 1000               # Khai báo biến Thread
        try:
            client.sendall(bytes("ProcessRunning", "utf-8"))        # Gửi thông điệp ProcessRunning
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")        # Thông báo lỗi
            self.process.destroy()                                  # Xóa cửa sổ

        # Receive data
        try:
            self.length = client.recv(1024).decode("utf-8")         # Nhận dữ liệu từ server
            self.length = int(self.length)                          # Chuyển dữ liệu từ string sang int
            for i in range(self.length):                            # Vòng lặp để nhận dữ liệu
                self.data = client.recv(1024).decode("utf-8")       # Nhận dữ liệu từ server
                self.ID[i] = self.data                              # Chuyển dữ liệu từ string sang int
                client.sendall(bytes(self.data, "utf-8"))           # Gửi dữ liệu từ client lên server

            for i in range(self.length):                            # Vòng lặp để nhận dữ liệu
                self.data = client.recv(1024).decode("utf-8")       # Nhận dữ liệu từ server
                self.Name[i] = self.data                            # Chuyển dữ liệu từ string sang int
                client.sendall(bytes(self.data, "utf-8"))           # Gửi dữ liệu từ client lên server

            for i in range(self.length):                            # Vòng lặp để nhận dữ liệu
                self.data = client.recv(1024).decode("utf-8")       # Nhận dữ liệu từ server
                self.Thread[i] = self.data                          # Chuyển dữ liệu từ string sang int
                client.sendall(bytes(self.data, "utf-8"))           # Gửi dữ liệu từ client lên server
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")        # Thông báo lỗi

        self.frame_process = Frame(self.process, bg="white", padx=20, pady=20, borderwidth=5)
        self.frame_process.grid(row=1, columnspan=5, padx=20)

        self.scrollbar = Scrollbar(self.frame_process)          # Khai báo scrollbar
        self.scrollbar.pack(side=RIGHT, fill=Y)                 # Đặt scrollbar
        self.mybar = ttk.Treeview(self.frame_process, yscrollcommand=self.scrollbar.set)        # Khai báo treeview
        self.mybar.pack()                                       # Đặt treeview
        self.scrollbar.config(command=self.mybar.yview)         # Đặt scrollbar

        self.mybar['columns'] = ("1", "2")                      # Khai báo cột
        self.mybar.column("#0", anchor=CENTER, width=200, minwidth=25)                          # Đặt cột #0
        self.mybar.column("1", anchor=CENTER, width=100)                                        # Đặt cột 1
        self.mybar.column("2", anchor=CENTER, width=100)                                        # Đặt cột 2

        self.mybar.heading("#0", text="Process Name", anchor=W)                                 # Đặt tiêu đề cột #0
        self.mybar.heading("1", text="ID", anchor=CENTER)                                       # Đặt tiêu đề cột 1
        self.mybar.heading("2", text="Counting threading", anchor=CENTER)                       # Đặt tiêu đề cột 2
        for i in range(self.length):
            self.mybar.insert(parent='', index='end', iid=0+i, text=self.Name[i], values=(self.ID[i], self.Thread[i]))                      # Đặt dữ liệu cột 1

    def KillProcess():
        self.screen_KillTask = Tk()                     # Khai báo cửa sổ
        self.screen_KillTask.geometry("300x50")         # Đặt kích thước cửa sổ
        self.screen_KillTask.title("Kill")              # Đặt tiêu đề cửa sổ

        self.EnterName = Entry(self.screen_KillTask, width=35)          # Khai báo Entry
        self.EnterName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)          # Đặt Entry
        self.EnterName.insert(END, "Nhập tên")                          # Đặt giá trị mặc định

        def PressKill():
            self.AppName = self.EnterName.get()                         # Lấy giá trị của Entry
            client.sendall(bytes("KillTask", "utf-8"))                  # Gửi dữ liệu từ client lên server
            try:
                client.sendall(bytes(self.AppName, "utf-8"))            # Gửi dữ liệu từ client lên server
                self.checkdata = client.recv(1024).decode("utf-8")      # Nhận dữ liệu từ server
                messagebox.showinfo("", "Đã đóng chương trình")         # Thông báo đã đóng chương trình
            except:
                messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")     # Thông báo lỗi

        KillButton = Button(self.screen_KillTask, bg="#FFE4E1", text="Kill", font="Helvetica 10 bold", padx=20,
                            command=PressKill, bd=5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)      # Khai báo nút Kill

    def StartTask():
        self.StartTask = Tk()
        self.StartTask.geometry("320x50")
        self.StartTask.title("Start")

        self.EnterName = Entry(self.StartTask, width=35)
        self.EnterName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.EnterName.insert(END, "Nhập Tên")                  # Đặt giá trị mặc định

        def PressStart():
            self.Name = self.EnterName.get()                    # Lấy giá trị của Entry
            client.sendall(bytes("OpenTask", "utf-8"))          # Gửi dữ liệu từ client lên server
            try:
                client.sendall(bytes(self.Name, "utf-8"))           # Gửi dữ liệu từ client lên server
                self.checkdata = client.recv(1024).decode("utf-8")  # Nhận dữ liệu từ server
                messagebox.showinfo("", "Chương trình đã bật")      # Thông báo đã bật chương trình
            except:
                messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")   # Thông báo lỗi

        StartButton = Button(self.StartTask, text="Start", bg="#F9BDC0", font="Helvetica 10 bold", padx=20, command=PressStart, bd=5).grid(row=0, column=4, padx=5, pady=5)

    Kill = Button(self.process, text="Kill", bg = "#8DDDE0", activebackground='#497172', font="Helvetica 10 bold", padx=30, pady=20, command=KillProcess, bd=5).grid(row=0, column=0, padx=8)
    Watch = Button(self.process, text="Watch", bg = "#F9BDC0", activebackground='#7e5a5c', font="Helvetica 10 bold", padx=30, pady=20, command=WatchTask, bd=5 ).grid(row=0, column=1, padx=8)
    Xoa = Button(self.process, text="Delete", bg = "#FBE698", activebackground='#776d47', font="Helvetica 10 bold", padx=30, pady=20, command=Clear, bd=5 ).grid(row=0, column=2, padx=8)
    Start = Button(self.process, text="Start", bg = "#E6E9D0", activebackground='#bec0b1', font="Helvetica 10 bold", padx=30, pady=20, command=StartTask, bd=5).grid(row=0, column=3, padx=8)
