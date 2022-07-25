import winreg as winreg
from tkinter import *

def SetValue(Client):
    Name = Client.recv(1024).decode("utf-8")        # Nhận tên của thuộc tính
    Client.sendall(bytes("Confirm","utf-8"))        # Gửi thông điệp đến server
    Links = Client.recv(1024).decode("utf-8")       # Nhận đường dẫn từ server
    Client.sendall(bytes("Confirm","utf-8"))        # Gửi thông điệp đến server
    data_type = Client.recv(1024).decode("utf-8")   # Nhận kiểu dữ liệu từ server
    Client.sendall(bytes("xac nhan","utf-8"))       # Gửi thông điệp đến server
    Value = Client.recv(2048).decode("utf-8")       # Nhận giá trị từ server
    Client.sendall(bytes("Confirm","utf-8"))        # Gửi thông điệp đến server

    Reg = Links.split("\\", 1)                      # Tách đường dẫn ra tên của hệ thống và đường dẫn tới thuộc tính
    check = True                                    # Biến kiểm tra
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT        # Nếu đường dẫn là HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER      # Nếu đường dẫn là HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE    # Nếu đường dẫn là HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS                    # Nếu đường dẫn là HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG  # Nếu đường dẫn là HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Path dont exist", "utf-8"))                       # Gửi thông điệp đến server
        checkdata = Client.recv(1024).decode("utf-8")                           # Nhận thông điệp từ server
        return
    REG_PATH = Reg[1]                                                           # Lấy đường dẫn tới thuộc tính
    with winreg.ConnectRegistry(None, linkReg) as REG_LINK:                     # Kết nối đến hệ thống
        try:    
            with winreg.OpenKey(REG_LINK, REG_PATH, 0, winreg.KEY_WRITE) as REG_KEY:    # Mở thuộc tính
                if data_type == "String": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_SZ,Value)            # Gán giá trị cho thuộc tính
                elif data_type == "Binary": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_BINARY,Value.encode('latin-1'))  # Gán giá trị cho thuộc tính
                elif data_type == "DWORD": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_DWORD,int(Value))    # Gán giá trị cho thuộc tính
                elif data_type == "QWORD": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_QWORD,int(Value))    # Gán giá trị cho thuộc tính
                elif data_type == "Multi-string": 
                    arr = value.split()                                                 # Tách giá trị thành mảng
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_MULTI_SZ,arr)        # Gán giá trị cho thuộc tính
                elif data_type == "Expandable String": 
                    winreg.SetValueEx(REG_KEY, Name, 0, winreg.REG_EXPAND_SZ,Value)     # Gán giá trị cho thuộc tính
                else:
                    Client.sendall(bytes("fail", "utf-8"))                              # Gửi thông điệp đến server
                    checkdata = Client.recv(1024).decode("utf-8")                       # Nhận thông điệp từ server
                    return
                Client.sendall(bytes("succeed", "utf-8"))                               # Gửi thông điệp đến server
                checkdata = Client.recv(1024).decode("utf-8")                           # Nhận thông điệp từ server
            winreg.CloseKey(REG_KEY)                                                    # Đóng thuộc tính
        except WindowsError:                                                       
            Client.sendall(bytes("Path dont exist", "utf-8"))                           # Gửi thông điệp đến server
            checkdata = Client.recv(1024).decode("utf-8")                               # Nhận thông điệp từ server
