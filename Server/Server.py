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
            new_image = image.resize((1084, 530))
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
            
        elif "ProcessRunning" == Request:
            import subprocess
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)            # Tạo process
            count = 0                                                                           # Đếm số lượng process
            length = 0                                                                          # Đếm chiều dài của process
            Name = ['' for i in range(10000)]                                                   # Tạo mảng chứa tên process
            ID = ['' for i in range(10000)]                                                     # Tạo mảng chứa ID process
            Thread = ['' for i in range(10000)]                                                 # Tạo mảng chứa số lượng thread
            for line in ProccessProc.stdout:                                                    # Đọc dữ liệu từ process
                if line.rstrip():                                                               # Xóa kí tự trắng
                    if count < 2:                                                               # Đếm số lượng process
                        count += 1                                                              # Đếm số lượng process
                        continue                                                                # Bỏ qua dòng đầu tiên
                    msg = str(line.decode().rstrip().lstrip())                                  # Chuyển dữ liệu từ bytes sang string
                    msg = " ".join(msg.split())                                                 # Xóa kí tự trắng
                    lists = msg.split(" ", 3)                                                   # Tách dữ liệu theo khoảng trắng
                    ID[length] = lists[0]                                                       # Lấy ID process
                    Name[length] = lists[1]                                                     # Lấy tên process
                    Thread[length] = lists[2]                                                   # Lấy số lượng thread
                    length += 1                                                                 # Đếm chiều dài của process

            Client.sendall(bytes(str(length),"utf-8"))                                          # Gửi số lượng process

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))                                            # Gửi ID process
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))                                         # Gửi tên process
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))                                       # Gửi số lượng thread
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client

        elif "KillTask" == Request: #Xóa
            print("KillTask")
            m = Client.recv(1024)                                                               # Nhận ID process
            msg = str(m)                                                                        # Chuyển dữ liệu từ bytes sang string
            msg = msg[2:]                                                                       # Xóa kí tự 'b'
            msg = msg[:len(msg)-1]                                                              # Xóa kí tự '\n'
            print(str(msg))                                                                     # In ID process
            from subprocess import call                                                         # Import thư viện call
            taskkillexe = "c:/windows/system32/taskkill.exe"                                    # Đường dẫn taskkill.exe
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')                           # Tham số tham số
            taskkillexitcode = call(taskkillparam)                                              # Gọi taskkill.exe
            Client.send(bytes("Da xoa tac vu", "utf-8"))                                        # Gửi thông báo đã xóa
        elif "OpenTask" == Request: #Mở app
            import subprocess
            mode = 0o666                                                                        # Thiết lập mode
            flags = os.O_RDWR | os.O_CREAT                                                      # Thiết lập flags
            m = Client.recv(1024)                                                               # Nhận tên app
            msg = str(m)                                                                        # Chuyển dữ liệu từ bytes sang string
            msg = msg[2:]                                                                       # Xóa kí tự 'b'
            msg = msg[:len(msg)-1]                                                              # Xóa kí tự '\n'
            print(str(msg))                                                                     # In tên app
            try:
                cmd = 'powershell start ' + msg                                                 # Tạo process
                subprocess.call(cmd)                                                            # Gọi process
                Client.send(bytes("opened", "utf-8"))                                           # Gửi thông báo đã mở
            except:
                Client.send(bytes("Not found", "utf-8"))                                        # Gửi thông báo không tìm thấy

        elif "AppRunning" == Request:
            import subprocess                                                                   # Import thư viện subprocess
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'       # Tạo câu lệnh
            openCMD = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)                 # Gọi cmd
            count = 0
            length = 0
            Name = ['' for i in range(100)]                                                     # Tạo mảng chứa tên process
            ID = ['' for i in range(100)]                                                       # Tạo mảng chứa ID process
            Thread = ['' for i in range(100)]                                                   # Tạo mảng chứa số lượng thread
            for line in openCMD.stdout:                                                         # Duyệt dữ liệu
                if line.rstrip():                                                               # Kiểm tra dữ liệu
                    if count < 2:                                                               # Kiểm tra dữ liệu đầu tiên
                        count += 1                                                              # Đếm số lượng dòng
                        continue                                                                # Bỏ qua dòng đầu tiên
                    msg = str(line.decode().rstrip().lstrip())                                  # Chuyển dữ liệu từ bytes sang string
                    msg = " ".join(msg.split())                                                 # Xóa khoảng trắng
                    lists = msg.split(" ", 3)                                                   # Chuyển dữ liệu thành mảng
                    ID[length] = lists[0]                                                       # Lấy ID process
                    Name[length] = lists[1]                                                     # Lấy tên process
                    Thread[length] = lists[2]                                                   # Lấy số lượng thread
                    length += 1                                                                 # Đếm số lượng process

            Client.sendall(bytes(str(length),"utf-8"))                                          # Gửi số lượng process

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))                                            # Gửi ID process
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))                                         # Gửi tên process
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
            for i in range(length):                                                              
                Client.sendall(bytes(Thread[i], "utf-8"))                                       # Gửi số lượng thread
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
        elif "SendingReg" == Request: ReceiveRegistry_SV.ReceiveRegistry(Client)                # Nhận Registry
        elif "GettingValueReg" == Request: GetValueReg_SV.GetValueReg(Client)                   # Lấy giá trị Registry
        elif "SettingValueReg" == Request: SetValue_SV.SetValue(Client)                         # Thiết lập giá trị Registry
        elif "DeletingValueReg" == Request: DeleteRegValue_SV.DeleteRegValue(Client)            # Xóa giá trị Registry
        elif "CreatingKey" == Request: CreateKey_SV.CreateKey(Client)                           # Tạo key Registry
        elif "DeletingKey" == Request: DeleteKey_SV.DeleteKey(Client)                           # Xóa key Registry
        elif "HookKey" == Request:                                                              # Hook key
            Client.sendall(bytes("Đã nhận", "utf-8"))                                           # Gửi thông báo đã nhận
            Keystroke_SV.Keystroke(Client)                                                      # Gọi hàm Keystroke

        elif "Exit" == Request:
            Client.sendall(bytes("Đã thoát", "utf-8"))                                          # Gửi thông báo đã thoát
            break                                                                           

def waitingConnection():
    print("Chờ các kết nối từ client...")                               
    
    while True:
        client, Address = SERVER.accept()                                                       # Chấp nhận kết nối
        print("Client", Address, "---> Đã kết nối !!!")                                         
        Thread(target = takeRequest, args = (client,)).start()                                  # Tạo thread


SERVER =socket.socket(socket.AF_INET,socket.SOCK_STREAM)                                        # Tạo socket
SERVER.bind((socket.gethostbyname(socket.gethostname()), 1234))                                 # Đặt port
print("Server đang chạy: ", (socket.gethostbyname(socket.gethostname())))                       # In ra địa chỉ server
def action():
    try:
        SERVER.listen()                                                                         # Đợi kết nối
        ACCEPT_THREAD = Thread(target = waitingConnection())                                    # Tạo thread
        ACCEPT_THREAD.start()       #Khởi động thread                                           
        ACCEPT_THREAD.join()        #Đợi cho thread kết thúc
    except:
        print("Error !!!, Server đã dừng")
    finally:
        SERVER.close()

def main():
    top = Tk()                                                                                  # Tạo cửa sổ
    top.title("Server Connection")                                                              # Đặt tiêu đề
    top.geometry("200x200")                                                                     # Đặt kích thước
    top.configure(background = "white")                                                         # Đặt màu nền
    btn1= PhotoImage(file='./img/button/hinh1.png')                                             # Đặt hình ảnh
    btn2= PhotoImage(file='./img/button/hinh2.png')
    def on_enter(event):
        top.button.config(image=btn2)                                                           # Đặt hình ảnh
    def on_leave(event):
        top.button.config(image=btn1)

    top.button = Button(top, image=btn1,bg="#fff", command = action, relief="flat", bd=0, highlightthickness=0, activebackground="#f7f7f7")
    top.button.pack(fill=BOTH, pady=5, padx=5, expand=True)                                     # Đặt kích thước và vị trí
    
    top.button.bind("<Enter>", on_enter)                                                        # Đặt sự kiện
    top.button.bind("<Leave>", on_leave)
    top.mainloop()

if __name__ == "__main__":                                                                      # Chạy chương trình
    main()
   