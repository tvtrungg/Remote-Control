from tkinter import *

def ReceiveRegistry(Client):
    import subprocess                                  # Import thư viện subprocess
    Client.sendall(bytes("Confirm","utf-8"))           # Gửi thông điệp đến server
    data = Client.recv(1024).decode("utf-8")           # Nhận thông điệp từ server
    Client.sendall(bytes("Confirm","utf-8"))           # Gửi thông điệp đến server
    fileopen = open("File.reg","w")                    # Tạo file File.reg
    fileopen.write(data)                               # Ghi dữ liệu vào file File.reg
    cmd = 'powershell reg import File.reg'             # Câu lệnh để import dữ liệu từ file File.reg
    subprocess.Popen(cmd, shell=True)                  # Thực thi câu lệnh
