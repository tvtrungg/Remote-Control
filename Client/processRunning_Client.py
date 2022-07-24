from tkinter import Tk, W, E
from tkinter.ttk import Frame, Label, Button, Entry
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

def processRunning(self, client):
    self.process = Tk()
    self.process.title("Process Running")
    self.process.configure(bg="#FFFAF0")

    def XoaTask():
        self.frame_process.destroy()

    def WatchTask():
        global frame_process
        global PORT
        PORT = 1234
        self.length = 0
        self.ID = [''] * 1000
        self.Name = [''] * 1000
        self.Thread = [''] * 1000
        try:
            client.sendall(bytes("ProcessRunning", "utf-8"))
        except:
            messagebox.showinfo("Error !!!", "Lỗi kết nối ")
            self.process.destroy()

        # Receive data
        try:
            self.length = client.recv(1024).decode("utf-8")
            self.length = int(self.length)
            for i in range(self.length):
                self.data = client.recv(1024).decode("utf-8")
                self.ID[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))

            for i in range(self.length):
                self.data = client.recv(1024).decode("utf-8")
                self.Name[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))

            for i in range(self.length):
                self.data = client.recv(1024).decode("utf-8")
                self.Thread[i] = self.data
                client.sendall(bytes(self.data, "utf-8"))
        except:
            box = messagebox.showinfo("Error !!!", "Lỗi kết nối ")

        self.frame_process = Frame(self.process, bg="white", padx=20, pady=20, borderwidth=5)
        self.frame_process.grid(row=1, columnspan=5, padx=20)

        self.scrollbar = Scrollbar(self.frame_process)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.mybar = ttk.Treeview(
            self.frame_process, yscrollcommand=self.scrollbar.set)
        self.mybar.pack()
        self.scrollbar.config(command=self.mybar.yview)

        self.mybar['columns'] = ("1", "2")
        self.mybar.column("#0", anchor=CENTER, width=200, minwidth=25)
        self.mybar.column("1", anchor=CENTER, width=100)
        self.mybar.column("2", anchor=CENTER, width=100)

        self.mybar.heading("#0", text="Process Name", anchor=W)
        self.mybar.heading("1", text="ID", anchor=CENTER)
        self.mybar.heading("2", text="Counting threading", anchor=CENTER)
        for i in range(self.length):
            self.mybar.insert(parent='', index='end', iid=0+i,
                              text=self.Name[i], values=(self.ID[i], self.Thread[i]))

    def KillWindow():
        self.KillTask = Tk()
        self.KillTask.geometry("300x50")
        self.KillTask.title("Kill")

        self.EnterName = Entry(self.KillTask, width=35)
        self.EnterName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.EnterName.insert(END, "Nhập tên")

        def PressKill1():
            self.AppName = self.EnterName.get()
            client.sendall(bytes("KillTask", "utf-8"))
            try:

                client.sendall(bytes(self.AppName, "utf-8"))
                self.checkdata = client.recv(1024).decode("utf-8")
                messagebox.showinfo("", "Đã đóng chương trình")
            except:
                messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")

        KillButton = Button(self.KillTask, bg="#FFE4E1", text="Kill", font="Helvetica 10 bold", padx=20,
                            command=PressKill1, bd=5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

    def StartTask():
        self.StartTask = Tk()
        self.StartTask.geometry("300x50")
        self.StartTask.title("Start")

        self.EnterName = Entry(self.StartTask, width=35)
        self.EnterName.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.EnterName.insert(END, "Nhập Tên")

        def PressStart1():
            self.Name = self.EnterName.get()
            client.sendall(bytes("OpenTask", "utf-8"))
            try:
                client.sendall(bytes(self.Name, "utf-8"))
                self.checkdata = client.recv(1024).decode("utf-8")
                messagebox.showinfo("", "Chương trình đã bật")
            except:
                messagebox.showinfo("Error !!!", "Không tìm thấy chương trình")

        StartButton = Button(self.StartTask, text="Start", bg="#FFE4E1", font="Helvetica 10 bold", padx=20, command=PressStart1, bd=5).grid(row=0, column=4, padx=5, pady=5)

    Kill = Button(self.process, text="Kill", bg="#2E8B57", font="Helvetica 10 bold", padx=30, pady=20, command=KillWindow, bd=5, activebackground='#F4A460').grid(row=0, column=0, padx=0)
    Watch = Button(self.process, text="Watch", bg="#54FF9F", font="Helvetica 10 bold", padx=30, pady=20, command=WatchTask, bd=5, activebackground='#F4A460').grid(row=0, column=1, padx=0)
    Xoa = Button(self.process, text="Delete", bg="#4EEE94", font="Helvetica 10 bold", padx=30, pady=20, command=XoaTask, bd=5, activebackground='#F4A460').grid(row=0, column=2, padx=0)
    Start = Button(self.process, text="Start", bg="#43CD80", font="Helvetica 10 bold", padx=30, pady=20, command=StartTask, bd=5, activebackground='#F4A460').grid(row=0, column=3, padx=0)
