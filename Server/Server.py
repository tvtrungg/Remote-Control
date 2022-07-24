from threading import Thread
import socket
import os
import pyautogui
from tkinter import *
import Keystroke_SV, ReceiveRegistry_SV, GetValueReg_SV, SetValue_SV, DeleteRegValue_SV, CreateKey_SV, DeleteKey_SV


def readRequest (Client):
    request =""
    try:
        request = Client.recv(1024).decode('utf-8')
        # recieve request from client
    finally:
        return request

 #ACCEPT_THREAD = Thread(target = waitingConnection())
# Choose a port that is free
def broadcast(msg, prefix=""):  
    for sock in clients:
        sock.send(bytes(prefix, "utf-8") + msg)

def takeRequest (Client):
    while True:
        Request = readRequest(Client)
        print(Request)
        if not Request:
            Client.close()
            break
        print("--> Got a request\n")
        #Chụp màn hình rồi gửi lại cho client
        if "TakePicture" == Request:
            image = pyautogui.screenshot()
            #image = image.resize((600,600)) 
            image.save("scrshot.png")
            try:
                # open image ======
                myfile = open('scrshot.png', 'rb')
                bytess = myfile.read()
                #gửi dữ liệu cho ảnh
                Client.sendall(bytess)
                myfile.close()
            except:
                print("Khong the chup man hinh")
        elif "Shutdown" == Request:
            os.system("shutdown /s /t 30")
            Client.send(bytes("Da tat may", "utf-8"))
            print("ShutDown")
        elif "ProcessRunning" == Request:
            print("ProcessRunning")
            '''c=0
            Name = ['' for i in range(100000)]
            ID = ['' for i in range(100000)]
            Thread = ['' for i in range(100000)]
            for process in psutil.process_iter ():
                c = c+1
                Name[c] = str(process.name ())
                ID[c] = str(process.pid)
                Thread[c] = str(process.num_threads())

            Client.sendall(bytes(str(c), "utf-8"))
            for i in range(c):
                Client.sendall(bytes(ID[i],"utf-8"))
                checkdata = Client.recv(1024)
            for i in range(c):
                Client.sendall(bytes(Name[i], "utf-8"))
                checkdata = Client.recv(1024)
            for i in range(c):
                Client.sendall(bytes(Thread[i], "utf-8"))
                checkdata = Client.recv(1024)'''
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            count = 0
            length = 0
            Name = ['' for i in range(100000)]
            ID = ['' for i in range(100000)]
            Thread = ['' for i in range(100000)]
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
            # server.close()
            break

def waitingConnection():

    print("Waiting for Client")
    
    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "connected!")
        Thread(target = takeRequest, args = (client,)).start()


SERVER =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind((socket.gethostbyname(socket.gethostname()), 1234))
print("server is working on ", (socket.gethostbyname(socket.gethostname())))
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
     top.title("Server")
     top.geometry("150x150")
     top.button = Button(top, text ="Mở Server",font=('Arial Bold', 13), command = action, bd = 10, bg='#c4ceff', activebackground='#8fa2ff' )
     top.button.pack(fill=BOTH, pady=5, padx=5, expand=True)
     top.mainloop()

if __name__ == "__main__":
    main()
   