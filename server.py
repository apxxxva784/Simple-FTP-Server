import tkinter as tk
from tkinter import messagebox
from socket import *
import _thread

mycolor= '#333432'
def my_server(show_1,HOST,PORT):
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)


    while True:
        show_1.insert(tk.END,"Waiting for connection...")
        show_1.insert(tk.END,"\n")

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        show_1.insert(tk.END,"connected {}".format(addr))
        show_1.insert(tk.END,"\n")

        filename='dtu.png'
        f = open(filename,'rb')
        l = f.read(1024)
        show_1.insert(tk.END,"Sending file..")
        show_1.insert(tk.END,"\n")

        while (l):
            tcpTimeClientSock.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)

        f.close()
        show_1.insert(tk.END,'File successfully sent!')
        show_1.insert(tk.END,"\n")
        tcpTimeClientSock.close()

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (LoginPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg = mycolor)
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        l_title=tk.Label(self, text="Server Software",font="Ubuntu,12",bg = mycolor, fg = 'white')
        l_title.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=30,pady=30)

        label_username = tk.Label(self, text="Username",bg = mycolor, fg = 'white')
        label_password = tk.Label(self, text="Password",bg = mycolor, fg = 'white')

        entry_username = tk.Entry(self,show="*")

        entry_password = tk.Entry(self, show="*")

        label_username.grid(row=2, column=0,sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=3, column=0,sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=2, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", bg = mycolor, fg="White",command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1,sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked():
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            if len(username) and len(password) > 2:
                # print(username, password)

                if username == "admin" and password == "admin":
                    controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                else:
                    messagebox.showerror("An Error has occurred","Invalid username or password ! ")

            else:
                messagebox.showerror("An Error has occurred","Enter Username and Password")



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True

        label = tk.Label(self, text="Server Software ", font="Ubuntu,16",bg= mycolor,fg="White")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Enter Host NAME", bg= mycolor,fg="White")
        l_host.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_host=tk.Entry(self)
        e_host.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,'127.0.0.1')


        l_port=tk.Label(self,text="Enter Port", bg= mycolor,fg="White")
        l_port.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,12121)

        message_label=tk.Label(self,text="Client Message",font=("Ubuntu,12"),bg= mycolor,fg="White")
        message_label.grid(row=3,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


        #scrollbar_y = tk.Scrollbar(self)
        #scrollbar_y.grid(row=4, column=3,rowspan=6)
        #yscrollcommand=scrollbar_y.set
        show_1=tk.Text(self,height=8, width=35, bg='white',fg="black")
        show_1.grid(row=4, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        b_connect=tk.Button(self,text="Connect",command=lambda: connect(),bg= mycolor,fg="White")
        b_connect.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")


        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v=e_host.get()
                e_port_v=int(e_port.get())


        def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0


app = Page()
app.title("Simple FTP Server")
app.mainloop()
