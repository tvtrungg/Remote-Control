import winreg as winreg
from tkinter import *

def GetValueReg(Client):
    Name = Client.recv(1024).decode("utf-8")                                # Nhận tên của Registry
    Client.sendall(bytes("Confirm","utf-8"))                                # Gửi thông điệp đến server
    Links = Client.recv(1024).decode("utf-8")                               # Nhận đường dẫn từ server
    Client.sendall(bytes("Confirm","utf-8"))                                # Gửi thông điệp đến server
    Reg = Links.split("\\",1)                                               # Tách đường dẫn
    check = True                                                            # Kiểm tra đường dẫn
    if Reg[0] == "HKEY_CLASSES_ROOT": linkReg = winreg.HKEY_CLASSES_ROOT    # Nếu đường dẫn là HKEY_CLASSES_ROOT
    elif Reg[0] == "HKEY_CURRENT_USER": linkReg = winreg.HKEY_CURRENT_USER  # Nếu đường dẫn là HKEY_CURRENT_USER
    elif Reg[0] == "HKEY_LOCAL_MACHINE": linkReg = winreg.HKEY_LOCAL_MACHINE    # Nếu đường dẫn là HKEY_LOCAL_MACHINE
    elif Reg[0] == "HKEY_USERS": linkReg = winreg.HKEY_USERS                # Nếu đường dẫn là HKEY_USERS
    elif Reg[0] == "HKEY_CURRENT_CONFIG": linkReg = winreg.HKEY_CURRENT_CONFIG  # Nếu đường dẫn là HKEY_CURRENT_CONFIG
    else:
        Client.sendall(bytes("Path dont exist", "utf-8"))                   # Nếu đường dẫn không tồn tại
        checkdata = Client.recv(1024).decode("utf-8")                       # Nhận thông điệp từ server
        return
    REG_PATH = Reg[1]                                 # Lấy đường dẫn
    with winreg.ConnectRegistry(None, linkReg) as REG_LINK:                # Kết nối đến Registry
        try:                                                        # Nếu đường dẫn không tồn tại
            with winreg.OpenKey(REG_LINK, REG_PATH, 0, winreg.KEY_READ) as REG_KEY: # Mở đường dẫn
                i = 0   
                while True:
                    try:
                        value = winreg.EnumValue(REG_KEY, i)         # Lấy giá trị
                        if value[0] == Name:                         # Nếu tên giá trị trùng với tên cần lấy
                            Client.sendall(bytes(value[1],"utf-8"))  # Gửi giá trị đến server
                            checkdata = Client.recv(1024).decode("utf-8")   # Nhận thông điệp từ server
                            break
                        i += 1
                    except:
                        Client.sendall(bytes("Khong tim thay", "utf-8"))        # Nếu không tìm thấy
                        check = Client.recv(1024).decode("utf-8")       # Nhận thông điệp từ server
                        break
            winreg.CloseKey(REG_KEY)                        # Đóng đối tượng
        except WindowsError:
            Client.sendall(bytes("Path dont exist", "utf-8"))   # Nếu đường dẫn không tồn tại
            checkdata = Client.recv(1024).decode("utf-8")       # Nhận thông điệp từ server
   