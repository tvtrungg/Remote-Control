from threading import Thread
import socket       # thư viện socket
import os
import pyautogui
from tkinter import *
import Keystroke_SV

#AF_INET        : cho biết đang yêu cầu một socket Internet Protocol(IP), cụ thể là IPv4
#SOCK_STREAM    : chỉ loại kết nối TCP IP hoặc UDP . Chương trình nhóm em sẽ chạy trên một cổng kết nối TCP
#bind()         : Phương thức này gắn kết địa chỉ (host,port) tới Socket
#listen()       : Phương thức này cho phép một cái chờ kết nối từ một các client.
#accept()       : Phương thức này chấp nhận một cách thụ động kết nối TCP Client, đợi cho tới khi kết nối tới.
#recv()         : Phương thức này nhận TCP message.
#send()         : Phương thức này gửi TCP message.
#close()        : Phương thức này đóng kết nối.
#gethostbyname(): Trả về hostname.

PORT = 1234     # Đặt cổng kết nối
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       # Tạo socket 
SERVER.bind((SERVER_IP, PORT))     # Tạo địa chỉ IP server và thiết lập công kết nối
print("Server đang chạy: ", (SERVER_IP))                       # In ra địa chỉ server

def read_Request (Client):   # Hàm đọc yêu cầu từ client
    request =""
    try:
        request = Client.recv(1024).decode('utf-8')     # Nhận yêu cầu từ phía client
        # recv(): 	Phương thức này nhận TCP message.
    except:
        print("Error !!!, Không nhận được yêu cầu từ client")
    finally:
        return request

def take_Request (Client):   # Hàm nhận yêu cầu từ client
    while True:
        Request = read_Request(Client)
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
                Client.sendall(bytess)                      # Gửi file cho client 
                myfile.close()
            except:
                print("Không chụp được màn hình")

        elif "Watch_ProcessRunning" == Request:     
            import subprocess
            # Lệnh powershell để lấy thông tin của các process đang chạy
            cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'   
            ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)            # Tạo process
            count = 0                                                               # Đếm số lượng process
            length = 0                                                              # Đếm chiều dài của process
            Name = ['' for i in range(10000)]                              # Tạo mảng chứa tên process
            ID = ['' for i in range(10000)]                                # Tạo mảng chứa ID process
            Thread = ['' for i in range(10000)]                           # Tạo mảng chứa số lượng thread
            for line in ProccessProc.stdout:                                        # Đọc dữ liệu từ process
                if line.rstrip():                                                   # Xóa kí tự trắng
                    if count < 2:                                                   # Đếm số lượng process
                        count += 1                                                  # Đếm số lượng process
                        continue                                                    # Bỏ qua dòng đầu tiên
                    msg = str(line.decode().rstrip().lstrip())                      # Chuyển dữ liệu từ bytes sang string
                    msg = " ".join(msg.split())                                     # Xóa kí tự trắng
                    lists = msg.split(" ", 3)                                       # Tách dữ liệu theo khoảng trắng
                    ID[length] = lists[0]                                    # Lấy ID process
                    Name[length] = lists[1]                                  # Lấy tên process
                    Thread[length] = lists[2]                                # Lấy số lượng thread
                    length += 1                                              # Đếm chiều dài của process

            Client.sendall(bytes(str(length),"utf-8"))                      # Gửi số lượng process

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))                                            # Gửi ID process về client
                checkdata = Client.recv(1024)                                # recv(): 	Phương thức này nhận TCP message.
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))                                         # Gửi tên process về client  
                checkdata = Client.recv(1024)                                # recv(): 	Phương thức này nhận TCP message.
            for i in range(length):
                Client.sendall(bytes(Thread[i], "utf-8"))                                       # Gửi số lượng thread về client
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client

        elif "Watch_AppRunning" == Request:
            import subprocess   
            # Lệnh powershell để lấy thông tin của các app đang chạy                                           
            cmd = 'powershell "Get-Process |where {$_.mainWindowTItle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'       
            openCMD = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)                 # Gọi cmd
            count = 0
            length = 0
            Name = ['' for i in range(100)]                         # Tạo mảng chứa tên process
            ID = ['' for i in range(100)]                           # Tạo mảng chứa ID process
            Thread = ['' for i in range(100)]                       # Tạo mảng chứa số lượng thread
            for line in openCMD.stdout:                             # Duyệt dữ liệu
                if line.rstrip():                                   # Kiểm tra dữ liệu
                    if count < 2:                         # Kiểm tra dữ liệu đầu tiên
                        count += 1                       # Đếm số lượng dòng
                        continue                             # Bỏ qua dòng đầu tiên
                    msg = str(line.decode().rstrip().lstrip())                 # Chuyển dữ liệu từ bytes sang string
                    msg = " ".join(msg.split())                                # Xóa khoảng trắng
                    lists = msg.split(" ", 3)                                  # Chuyển dữ liệu thành mảng
                    ID[length] = lists[0]                                      # Lấy ID process
                    Name[length] = lists[1]                                    # Lấy tên process
                    Thread[length] = lists[2]                                  # Lấy số lượng thread
                    length += 1                                                # Đếm số lượng process

            Client.sendall(bytes(str(length),"utf-8"))                         # Gửi số lượng process

            for i in range(length):
                Client.sendall(bytes(ID[i],"utf-8"))                                 # Gửi ID process
                checkdata = Client.recv(1024)                                          # Nhận dữ liệu từ client
            for i in range(length):
                Client.sendall(bytes(Name[i], "utf-8"))                                     # Gửi tên process
                checkdata = Client.recv(1024)                                                   # Nhận dữ liệu từ client
            for i in range(length):                                                              
                Client.sendall(bytes(Thread[i], "utf-8"))                                   # Gửi số lượng thread
                checkdata = Client.recv(1024)                                               # Nhận dữ liệu từ client
        
        elif "OpenTask" == Request: #Mở app
            import subprocess
            mode = 0o666            # Thiết lập mode (quyền truy cập tệp bát phân. 0o trong ES6 đại diện hệ bát phân)
            flags = os.O_RDWR | os.O_CREAT              # Thiết lập cờ (cờ đọc và ghi)
            m = Client.recv(1024)                       # Nhận yêu cầu mở app/process
            msg = str(m)                                # Chuyển dữ liệu từ bytes sang string
            msg = msg[2:]                               # Xóa kí tự 'b' từ đầu dữ liệu
            msg = msg[:len(msg)-1]                      # Xóa kí tự '\n' đầu dữ liệu
                                                              
            try:
                cmd = 'powershell start ' + msg                 # Tạo process
                subprocess.call(cmd)                            # Gọi process và thực thi
                Client.send(bytes("opened", "utf-8"))                            # Gửi thông báo đã mở
                #send(): 	Phương thức này truyền TCP message.
            except:
                Client.send(bytes("Not found", "utf-8"))                         # Gửi thông báo không tìm thấy
                #send(): 	Phương thức này truyền TCP message.

        elif "Kill_Task" == Request: #Xóa
            m = Client.recv(1024)                           # Nhận ID process
            msg = str(m)                                    # Chuyển dữ liệu từ bytes sang string
            msg = msg[2:]                                   # Xóa kí tự 'b' từ đầu dữ liệu
            msg = msg[:len(msg)-1]                          # Xóa kí tự '\n'
            print(str(msg))                                 # In ID process
            from subprocess import call                             # Import thư viện call để gọi lệnh kill process
            taskkillexe = "c:/windows/system32/taskkill.exe"            # Đường dẫn taskkill.exe
            taskkillparam = (taskkillexe, '/F',  '/IM', msg + '.exe')   # Truyền tham số vào taskkill.exe
            taskkillexitcode = call(taskkillparam)          # Gọi taskkill.exe
            Client.send(bytes("Da xoa tac vu", "utf-8"))    # Gửi thông báo đã xóa
        
        elif "HookKey" == Request:                                                            # Hook key
            Client.sendall(bytes("Đã nhận", "utf-8"))                                         # Gửi thông báo đã nhận
            Keystroke_SV.Keystroke(Client)                                                    # Gọi hàm Keystroke

        elif "Shutdown" == Request:
            os.system("shutdown /s /t 40")            # Tắt máy trong vòng 40s

        elif "Exit" == Request:
            Client.sendall(bytes("Đã thoát", "utf-8"))                                        # Gửi thông báo đã thoát
            break                                                                           

def waiting():    # Hàm chờ kết nối
    print("Chờ các kết nối từ client...")                               
    while True:
        client, Address = SERVER.accept()        # Chờ kết nối từ client  
        #accept(): Phương thức này chấp nhận một cách thụ động kết nối TCP Client, đợi cho tới khi kết nối tới.
        print("Client", Address, "---> Đã kết nối !!!")                                         
        Thread(target = take_Request, args = (client,)).start()       # Tạo thread cho client

def listenAndclose():
    try:
        SERVER.listen()                                                                         # Đợi kết nối
        ACCEPT_THREAD = Thread(target = waiting())                                    # Tạo thread
        ACCEPT_THREAD.start()       #Khởi động thread                                           
        ACCEPT_THREAD.join()        #Đợi cho thread kết thúc
    except:
        print("Error !!!, Server đã dừng")
    finally:
        SERVER.close()          # Đóng socket

def interface():
    top = Tk()                                                           # Tạo cửa sổ
    top.title("Server Connection")                                       # Đặt tiêu đề
    top.geometry("160x65")                                               # Đặt kích thước
    btn1= PhotoImage(file='./img/button/anh2a.png')                      # Đặt hình ảnh
    btn2= PhotoImage(file='./img/button/anh1a.png')
    def on_enter(event):
        top.button.config(image=btn2)   # Hình hiển thị khi chưa hover                                    
    def on_leave(event):
        top.button.config(image=btn1)   # Hình hiển thị khi hover

    top.button = Button(top, image=btn1,bg="#fff", command = listenAndclose, relief="flat", bd=0, highlightthickness=0, activebackground="#f7f7f7")
    top.button.pack(pady=5, padx=5, expand=True)                     # Đặt kích thước và vị trí
    
    top.button.bind("<Enter>", on_enter)        #Đặt sự kiện khi chuột đến button
    top.button.bind("<Leave>", on_leave)        #Đặt sự kiện khi chuột ra khỏi button
    top.mainloop()

if __name__ == "__main__":          # Chạy chương trình
    interface()
   