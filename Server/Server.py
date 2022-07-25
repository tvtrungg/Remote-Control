from threading import Thread
import socket
import os
import pyautogui
from tkinter import *
import Keystroke_SV, ReceiveRegistry_SV, GetValueReg_SV, SetValue_SV, DeleteRegValue_SV, CreateKey_SV, DeleteKey_SV


def readRequest (Client):
    request =""
    try:
        request = Client.recv(1024).decode('utf-8')     # Nhận yêu cầu từ phía client
    finally:
        return request


def takeRequest (Client):
    while True:
        Request = readRequest(Client)
        print("====> Yêu cầu từ server: ", Request)
        if not Request:
            Client.close()
            break

        #Chụp màn hình rồi gửi lại cho client
        if "screenCapture" == Request:
            image = pyautogui.screenshot()                  # Chụp màn hình
            new_image = image.resize((1080, 530))
            new_image.save("picture.png")                       # Lưu ảnh
            try:
                myfile = open("picture.png", 'rb')          # Mở file dạng byte 
                bytess = myfile.read()                      # Đọc file
                Client.sendall(bytess)                      # Gửi file
                myfile.close()
            except:
                print("Không chụp được màn hình")

        elif "Shutdown" == Request:
            os.system("shutdown /s /t 30")                  # Tắt máy trong vòng 30s
            print("ShutDown")
        elif "ProcessRunning" == Request:
            print("ProcessRunning")
           
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(10000)]
            ID = ['' for i in range(10000)]
            Thread = ['' for i in range(10000)]
            for line in ProccessProc.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length),"utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)

        elif "KillTask" == Request: #Xóa
            print("KillTask")
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]
            print(str(msg))
            from subprocess import call
            taskkillexe = "c:/windows/system32/taskkill.exe"
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')
            taskkillexitcode = call(taskkillparam)
            Client.send(bytes("Da xoa tac vu", "utf-8"))
        elif "OpenTask" == Request: #Mở app
            print("OpenTask")
            import subprocess
            mode = 0o666
            flags = os.O_RDWR | os.O_CREAT
            m = Client.recv(1024)
            msg = str(m)
            msg = msg[2:]
            msg = msg[:len(msg)-1]
            print(str(msg))
            print("C:/Windows/System32/" + msg + ".exe")
            cmd = 'powershell start ' + msg
            subprocess.call(cmd)
            #os.system("C:/Windows/System32/" + msg + ".exe")
            Client.send(bytes("Da mo", "utf-8"))

        elif "AppRunning" == Request:
            print("AppRunning")
            import subprocess
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            appProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100)]
            ID = ['' for i in range(100)]
            Thread = ['' for i in range(100)]
            for line in appProc.stdout:
                if line.rstrip():
                    if count < 2:
                        count += 1
                        continue
                    msg = str(line.decode().rstrip().lstrip())
                    msg = " ".join(msg.split())
                    lists = msg.split(" ", 3)
                    ID[length] = lists[0]
                    Name[length] = lists[1]
                    Thread[length] = lists[2]
                    length += 1

            Client.sendall(bytes(str(length),"utf-8"))

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)
        elif "SendingReg" == Request: ReceiveRegistry_SV.ReceiveRegistry(Client)
        elif "GettingValueReg" == Request: GetValueReg_SV.GetValueReg(Client)
        elif "SettingValueReg" == Request: SetValue_SV.SetValue(Client)
        elif "DeletingValueReg" == Request: DeleteRegValue_SV.DeleteRegValue(Client)
        elif "CreatingKey" == Request: CreateKey_SV.CreateKey(Client)
        elif "DeletingKey" == Request: DeleteKey_SV.DeleteKey(Client)
        elif "HookKey" == Request:
            print("KeyStroke")
            Client.sendall(bytes("Đã nhận", "utf-8"))
            Keystroke_SV.Keystroke(Client)

        elif "Exit" == Request:
            print("Exit")
            Client.sendall(bytes("Đã thoát", "utf-8"))
            break

def waitingConnection():

    print("Chờ các kết nối từ client...")
    
    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "---> Đã kết nối !!!")
        Thread(target = takeRequest, args = (client,)).start()


SERVER =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind((socket.gethostbyname(socket.gethostname()), 1234))
print("Server đang chạy: ", (socket.gethostbyname(socket.gethostname())))
def action():
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target = waitingConnection())
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        print("Error occured!")
    finally:
        SERVER.close()

def main():
    top = Tk()
    top.title("Server Connection")
    top.geometry("200x200")
    top.configure(background = "white")
    btn1= PhotoImage(file='hinh1.png')
    btn2= PhotoImage(file='hinh2.png')
    def on_enter(event):
        top.button.config(image=btn2)
    def on_leave(event):
        top.button.config(image=btn1)

    top.button = Button(top, image=btn1,bg="#fff", command = action, relief="flat", bd=0, highlightthickness=0, activebackground="#f7f7f7")
    top.button.pack(fill=BOTH, pady=5, padx=5, expand=True)
    
    top.button.bind("<Enter>", on_enter)
    top.button.bind("<Leave>", on_leave)
    top.mainloop()

if __name__ == "__main__":
    main()
   