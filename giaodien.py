from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import string
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import load_model
import sys
import pydivert
import re
from time import sleep
import threading
import cv2

def extract_url(payload_tcp, dst_port):
    if dst_port == 80:
        return extract_url_http(payload_tcp)
    if dst_port == 443:
        return extract_url_https(payload_tcp)
    

def extract_url_http(payload_tcp):
    start_string='Host: '
    end_string = '\r\nConnection'
    start_index = payload_tcp.find(start_string.encode())
    end_index = payload_tcp.find(end_string.encode())
    host = payload_tcp[start_index+6:end_index]

    start_string = 'GET '
    end_string= ' HTTP'
    start_index = payload_tcp.find(start_string.encode())
    end_index = payload_tcp.find(end_string.encode())
    path = payload_tcp[start_index+4:end_index]
    # print("hostname: ",host," path: ",path)
    url = host + path
    if len(url)!=0 and check_Format_of_URL(url.decode()):
        url = url.decode()
        return url
    return ""

def extract_url_https(payload_tcp):
    start_index = 127
    end_string = '\x00\x17'
    end_index = payload_tcp.find(end_string.encode(),start_index)
    url = payload_tcp[start_index:end_index]
    if len(url)!=0 and check_Format_of_URL(url.decode('utf-8', 'backslashreplace')):
        url = url.decode('utf-8', 'backslashreplace')
        return url
    return "1"

def check_Format_of_URL(url):
    regex = r"(?i)\b(^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$)"
    return re.compile(regex).match(url)

def tokenizer(alphabet,url_length=200):
    dictionary = {}
    reverse_dictionary = {}
    for i, c in enumerate(alphabet):
        dictionary[c]=i+1
        reverse_dictionary[i+1]=c
    return dictionary, reverse_dictionary

def load_image(image_name):
    img = tf.keras.utils.load_img(image_name, target_size=(200, 67))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    return images

def predict_phishing(line):
    this_sample=np.zeros(url_shape)
    if(line[0] == "'" and line[-1] == "'"):
        line = line[1:-1]
    line = line.replace("'","%27")
    line = line.replace(" ","%20")
    line = line.lower()
    if len ( set(line) - set(alphabet)) == 0 and len(line) < 200 and line.find('.') != -1:
        for i, position in enumerate(this_sample):
            this_sample[i][0]=1.0
        for i, char in enumerate(line):
            this_sample[i][0]=0.0
            this_sample[i][dictionary[char]]=1.0
        plt.imshow(this_sample, cmap='gray')
        dirtemp= "./temp/"
        plt.imsave(dirtemp + "check_phishing.png", this_sample)
        for filename in os.listdir("./temp/"):
            ten_image = dirtemp + filename
            array_img = load_image(ten_image)
            classes = (model.predict(array_img) > 0.5).astype("int32")
            classes_predict=np.argmax(classes,axis=1)
            if classes_predict == 1:
                return "good"
            else:
                return "bad"
    else:
        return "nope"
    return
w = pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0")
if __name__ == "__main__":
    model = load_model('./modelsave/mymodel.h5')

    model.compile(loss='sparse_categorical_crossentropy', 
                optimizer=tf.optimizers.SGD(learning_rate=0.001), 
                metrics=['accuracy'])
    alphabet = string.ascii_lowercase + string.digits + "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
    dictionary_size = len(alphabet) + 1
    url_shape = (200, dictionary_size)
    dictionary, reverse_dictionary = tokenizer(alphabet,url_length= 200)
    #--------------------------------------- BAT DAO cho TKINTER -------------------------
    window = Tk()
    window.title('N18DCAT068 APP')
    window.geometry('600x500')
    window['background']='#FBEAEB'
    # img_cv2 = cv2.imread("image_view/anti_phishing1.png")
    # cv2.imwrite("image_view/anti_phishing1.png",img_cv2)
    # background_app = PhotoImage(file = "image_view/anti_phishing1.png")
    # canvas1 = Canvas( window, width = 600,
    #              height = 500)
    # canvas1.pack(fill = "both", expand = True)
    # canvas1.create_image( 0, 0, image = background_app, 
    #                  anchor = "nw")             
    lbl = Label(window, text="Nhập URL", bg="#FBEAEB",font=("Arial Bold",10),fg="#2F3C7E")
    lbl.grid(row=0, column=0)
    lbl.place(x=0,y=50)
    #textbox
    txt = Entry(window,width=60)
    txt.grid(row=0, column=0)
    txt.place(x=100,y=50)
    #button kiểm tra phishing
    def check_phishing():
        if predict_phishing(txt.get()) == "bad":
            messagebox.showwarning('Cảnh báo',txt.get() + " là trang nguy hiểm")
        elif predict_phishing(txt.get()) == "good":
            messagebox.showinfo('Thông tin','Bạn có thể truy cập URL này')   
        else:
            messagebox.showinfo('Thông tin','Ứng dụng đang cải thiện với độ dài 200 và các ngôn ngữ khác')

    btn=Button(window,text="Kiểm tra",width= 12,height=2,command = check_phishing,bg='#2F3C7E',fg='#FBEAEB',font=("Arial Bold",10))
    btn.grid(row=0,column=0)
    btn.place(x=480,y=40)
    #button to quit program
    def confirm():
        if running1 == True:
            messagebox.showerror('Lỗi',"Vui lòng tắt chế độ Anti Phishing trước khi thoát chương trình!!!")
            return
        answer = messagebox.askyesno(title='confirmation',
                        message='Bạn có muốn thoát chương trình không?')
        # if running1 == True:
        #     messagebox.showerror('Lỗi',"Vui lòng tắt chế độ Anti Phishing trước khi thoát chương trình!!!")
        # else:
        if answer:
            window.destroy()
            os._exit(1)
        else:
            return    
                
    # btn_quit=Button(window,text="thoát",width= 0,height=0,command = confirm)
    # btn_quit.grid(row=0,column=0)
    # btn_quit.place(x=0,y=0)
    window.protocol("WM_DELETE_WINDOW", confirm)
    #Table List
    game_frame = Frame(window,bg="GREY")
    game_frame.place(x=10,y=250,width=580,height=240)
    game_scroll = Scrollbar(game_frame)
    game_scroll.pack(side=RIGHT, fill=Y)
    styletr = ttk.Style()
    styletr.configure("Treeview.Heading",background="black",foreground="#8AAAE5",relief="flat",font=("Arial BOLD",10))
    my_game = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set)
    my_game.place(x=0,y=40,width=563,height=200)
    game_scroll.config(command=my_game.yview)
    game_scroll.config(command=my_game.xview)
    #define our column
    my_game['columns'] = ('URL', 'STATUS')
    # format our column
    my_game.column("#0", width=0,  stretch=NO)
    my_game.column("URL",anchor="w", width=500)
    my_game.column("STATUS",anchor=CENTER,width=60)
    #Create Headings 
    my_game.heading("#0",text="",anchor=CENTER)
    my_game.heading("URL",text="URL",anchor=CENTER)
    my_game.heading("STATUS",text="STATUS",anchor=CENTER)
    iid=0
    
    #--------------------------------Toggle auto check
    is_on = False
    running1 = False
    allow_url_phi = []
    deny_url_phi = []
    my_label_mode = Label(window,
        text = "Anti Phishing: OFF",
        bg='#FBEAEB',
        fg = "grey",
        font = ("Helvetica BOLD", 32))
    
    my_label_mode.place(x=120,y=100)
    def print_text():
        global allow_url_phi
        global deny_url_phi
        global iid
        url_check_phi = ""
        check_allow = ""
        if running1:
            with pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0") as w:
                for packet in w:
                    payload_tcp = packet.tcp.payload
                    dst_port = packet.dst_port
                    url_name = extract_url(payload_tcp,dst_port)                   
                    for j in range(len(allow_url_phi)):
                        if allow_url_phi[j] == url_name:
                            check_allow = url_name
                            break
                    # if allow_url_phi == url_name:
                    #     w.send(packet)
                    if check_allow == url_name:                        
                        check_allow = ""
                        w.send(packet)
                        continue                    
                    for i in range(len(deny_url_phi)):    
                        if deny_url_phi[i] == url_name:
                            url_check_phi = url_name                            
                            break
                    if url_check_phi == url_name:
                        if running1 == False:                            
                            w.send(packet)
                            break                       
                        continue
                    print(url_name)
                    if url_name != "":
                        if predict_phishing(url_name) == "bad" and check_allow != url_name:
                            # messagebox.showwarning('Cảnh báo',haha + " là trang nguy hiểm")
                            answer_phishingbad = messagebox.askyesno(title='Cảnh báo lừa đảo',
                        message='Bạn có muốn tiếp tục truy cập '+ url_name +' không?')
                            if answer_phishingbad:
                                w.send(packet)
                                messagebox.showinfo('Thông báo',"Bạn có thể khóa URL lại ở danh sách bên dưới!!!")
                                allow_url_phi.append(url_name)
                                my_game.insert(parent='',index='end',iid=iid,text='',
                                                values=(url_name,'ALLOW'))
                                iid = iid + 1                                            
                            else:
                                messagebox.showinfo('Thông báo',url_name + " đã bị khóa!!!")
                                deny_url_phi.append(url_name)
                                my_game.insert(parent='',index='end',iid=iid,text='',
                                                values=(url_name,'DENY'))                                       
                                iid = iid + 1
                        elif predict_phishing(url_name) == "good":
                            w.send(packet)        
                    else:
                        if running1 == False:
                            w.send(packet)
                            break
                        continue
                    if running1 == False:
                        break
            # print_text()       
        # window.after(1000, print_text)
    def switch():
        global is_on
        global running1
        if is_on:
            on_button.config(image = off_imgbut)
            my_label_mode.config(text = "Anti Phishing: OFF",
                            fg = "grey")
            print("hahaha")
            is_on = False
            running1 = False
        else:
            on_button.config(image = on_imgbut)
            my_label_mode.config(text = "Anti Phishing: ON", fg = "green")
            # window.update()
            is_on = True
            running1 = True
            threading.Thread(target=print_text).start()
            


    on_imgbut = PhotoImage(file = "./image_view/on.png")
    off_imgbut = PhotoImage(file = "./image_view/off.png")
    on_button = Button(window, image = off_imgbut, bd = 0,bg='#FBEAEB',
                   command = switch)
    on_button.place(x=250,y=170)
    
    def allow_deny_change():
        global allow_url_phi
        global deny_url_phi
        selected=my_game.focus()
        values = my_game.item(selected,'values')
        try:
            if(values[1]== "DENY"):
                my_game.item(selected,text="",values=(values[0],"ALLOW"))
                deny_url_phi.remove(values[0])
                allow_url_phi.append(values[0])             
            elif(values[1]== "ALLOW"):
                my_game.item(selected,text="",values=(values[0],"DENY"))
                allow_url_phi.remove(values[0])
                deny_url_phi.append(values[0])
        except:
            print("haha")        

    lbl = Label(game_frame, text="DANH SÁCH CÁC URL NGUY HIỂM", font=("Arial Bold",10),width=60,height=2,bg="#8AAAE5",fg="#FFFFFF")
    lbl.place(x=74,y=0)
    img_cv2_bug = cv2.imread("./image_view/bug_button.png")
    cv2.imwrite("./image_view/bug_button.png",img_cv2_bug)
    photobug = PhotoImage(file = "image_view/bug_button.png")
    # photoimgbug = photobug.subsample(-1,-1)        
    button_change = Button(game_frame,text="Allow/Deny",width= 0,height=2,bg="#8BD8BD",fg="#243665",font=("Arial Bold",9),command = allow_deny_change)
    button_change.place(x=0,y=0)
    
    # window.after(1, threading.Thread(target=print_text).start())bg="#8AAAE5",fg="#FFE67C"
    window.mainloop()
    # os._exit(1)