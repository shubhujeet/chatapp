# # import smtplib, ssl
# # import getpass

# # port = 465  # For SSL
# # password = "SHUBHUJEET@18161"
# # receiver = "ghoshshubujeet@gmail.com"
# # sender = "shubhujeet.ghosh.18161@ves.ac.in"
# # message ="Hi this email is send via python code"

# # # Create a secure SSL context
# # context = ssl.create_default_context()

# # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
# #     server.login(sender, password)
# #     server.sendmail(sender,receiver,message)
# #     print("email sending....")
# #     # TODO: Send email here







# # from collections import deque

# # d = deque()

# # print(d)


# # d.append(4)
# # print(type(d))


# import customtkinter as ctk
# class new(ctk.CTkFrame):

#     def __init__(self,master,**kwargs):
#         super().__init__(master,**kwargs)
#         print(self.__class__.__name__)

#         self.lab = ctk.CTkLabel(self,text="check")
#         self.lab.pack()
#         pass

#     def method(self):
#         pass



# class app(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.f = new(self)
#         self.f.pack()
#         print(self.__class__.__name__)
#         self.btn = ctk.CTkButton(self,command=self.method_app)

#     def method_app(self):
#         pass

# app = app()
# app.mainloop()






# import re
# str = "1abcd"
# r1 = re.search("[A-Za-z0-9]","1abcd")
# # print(r1,f"{r1.start()}+{r1.end()}") 

# print(str[:r1.start()]+str[r1.end():])


# email = "tony@tiremove_thisger.net"
# m = re.search("remove_this", email)
# print(m)
# print(email[:m.start()] + email[m.end():])



# pas = input()
# d_count = len(pas)

# if d_count == 5 or (d_count > 5 and d_count < 8):
#     print("very weak")
# elif d_count == 8 or (d_count > 8 and d_count < 11):
#     print("weak")
# elif d_count == 11 or (d_count > 11 and d_count <14):
#     print("good")
# elif d_count == 14 or (d_count > 14 and d_count <=20):
#     print("execellent")
# elif d_count > 20:
#     print("passwd len exeeds limits of 20 character")
# else:
#     print("must be greater")




# texts = {"[a-zA-Z0-9]+":["2121abcd13241"],

#         }

# text = "abcd@"
# # pat = "[a-zA-Z0-9]+@([a-zA-Z]{1,}[a-zA-Z0-9].){2,63}"

# pat = "([a-zA-Z]{1,}[a-zA-Z0-9].){2,10}"
# m = re.search(pat,text)


# Top level domain 2-6 letter
import re

#pat = "\A[\w!#$%&'*+/=?`{|}~^-]+(?:\.[\w!#$%&'*+/=?`{|}~^-]+)*@(?:[a-zA-Z0-9-]+\.)+[A-Z]{2,6}\Z"


#text = "abcd"
"([a-zA-Z0-9-]|[^-$])"

#pat = "(\A[^-]|[^-]$|(\A[a-zA-Z0-9])+(-[a-zA-Z0-9]+)*)"
#text = "abcd-"
#text = "abcd-" 
#pat = "[^-]$"


# pat = "\A([\w\d!#$%&'*+/=?`{|}~^-])+(?:\.[\w\d!#$%&'*+/=?`{|}~^-]+)*"
# text = "abc.dfd%*"
# pat = "((\A([a-zA-Z0-9])+(?:-[a-zA-Z0-9]+)*)+\.)+[A-Za-z]{2,6}\Z"
# text = "gma-il.com"

#--------------------------------------------------------------------
# pat = "\A([\w\d!#$%&'*+/=?`{|}~^-])+(?:\.[\w\d!#$%&'*+/=?`{|}~^-]+)*@{1}((\A([a-zA-Z0-9])+(?:-[a-zA-Z0-9]+)*)+\.)+[A-Za-z]{2,6}\Z"
# text = "ghoshshubhujeet@gmail.com"


# pat = "\A([\w\d!#$%&'*+/=?`{|}~^-])+(?:\.[\w\d!#$%&'*+/=?`{|}~^-]+)*"
# text = "ghoshshubhujeet"


# pat = "((\A([a-zA-Z0-9])+(?:-[a-zA-Z0-9]+)*)+\.)+[A-Za-z]{2,6}\Z"
# text = "gmail.com"

# pat = "\A([\w\d!#$%&'*+/=?`{|}~^-])+(?:\.[\w\d!#$%&'*+/=?`{|}~^-]+)*@((\A([a-zA-Z0-9])+(?:-[a-zA-Z0-9]+)*)+\.)+[A-Za-z]{2,6}\Z"
# text = "ghoshshubhujeet@gmail.com"



# m = re.fullmatch(pat,text)


# print(m)



#-----------------------------------------------

#email = "abcdd@gma@il.@com"

# print(email.split("@"))

# import re

# print(re.split("@",email))


# lang = input("What's the programming language you want to learn? ")

# match lang:
#     case "JavaScript":
#         print("You can become a web developer.")

#     case "Python":
#         print("You can become a Data Scientist")

#     case "PHP":
#         print("You can become a backend developer")
    
#     case "Solidity":
#         print("You can become a Blockchain developer")

#     case "Java":
#         print("You can become a mobile app developer")
#     case _:
#         print("The language doesn't matter, what matters is solving problems.")


# bad attribute "-type": must be -alpha, -transparentcolor,
#  -disabled, -fullscreen,
#  -toolwindow, or -topmost

# from tkinter import *
# from time import sleep
# win = Tk()
# win.geometry("500x500")
# #win.wm_attributes("-topmost","true")
# # win.overrideredirect(True)

# def method():
#     lab2.configure(text="")

# for i in range(10):
#     lab = Label(win,text="my text")
#     lab.pack()
    
#     lab2 = Label(win,text="txt2")
#     lab2.pack()
    
#     # lab2.after(2000,])

# win.mainloop()

# from time import sleep

# print("hi")
# print("now")


# from winotify import Notification,audio

# toast = Notification(app_id="Chat Applcation",
#                         title="Conformation",
#                         msg="Password Restoration Successful !",
#                         duration="short",
#                         icon=".\\images\\live-chat.png"
#                         )

# toast.show()



# import customtkinter as ctk

# win = ctk.CTk()

# def open_top():
#     tp = ctk.CTkToplevel(win)
#     tp.wm_overrideredirect(True)
#     btn2 = ctk.CTkButton(tp)
#     btn2.pack(pady=100,padx=100)
#     tp.after(2000,tp.destroy)
    
# btn = ctk.CTkButton(win,command=open_top)
# btn.pack()

# win.mainloop()

# import mysql.connector
# from mysql.connector import Error

# try:
#     with mysql.connector.connect(host='localhost',database='prac',user='root',password='shubhu') as connection:
#         if connection.is_connected():
#             db_Info = connection.get_server_info()
#             print("Connected to MySQL Server version ", db_Info)
#             cursor = connection.cursor()
#             cursor.execute("select * from demo2;")

#             print(cursor.rowcount)
#             record = cursor.fetchall()
#             print("You're connected to database: ", record)

# except Error as e:
#     print("Error while connecting to MySQL", e)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")



# import customtkinter as ctk
# from tkinter import *

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
        
       
#         self.var=25
#         self.textb = ctk.CTkTextbox(self,height=self.var, wrap="word")
#         self.textb.pack(fill='x')
        
#         self.textb.bind("<Return>",self.set_height,add='+')
#         self.textb.bind("<BackSpace>",self.reset_height,add="+")

#     def set_height(self,event):
#         self.var = self.var = self.var + 25 if self.var < 100 else 100
#         self.textb.configure(height=self.var)

#     def reset_height(self,event):
#         self.var = self.var = self.var - 25 if self.var > 25 else 25
#         self.textb.configure(height=self.var)

# app = App()
# app.mainloop()



# import customtkinter

# class MyFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         # add widgets onto the frame...
#         self.label = customtkinter.CTkLabel(self)
#         self.label.grid(row=0, column=0, padx=20)


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)

#         self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
#         self.my_frame.grid(row=0, column=0, sticky="nsew")


# app = App()
# app.mainloop()



# import customtkinter
# import os
# from PIL import Image


# class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, command=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.grid_columnconfigure(0, weight=1)

#         self.command = command
#         self.label_list = []
    

#     def add_item(self, item, image=None):
#         label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
     
#         if self.command is not None:
#             label.bind("<Button-1>",lambda x: self.command(item))
#         label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
#         self.label_list.append(label)
       

#     def remove_item(self, item):
#         for label, button in zip(self.label_list, self.button_list):
#             if item == label.cget("text"):
#                 label.destroy()
#                 button.destroy()
#                 self.label_list.remove(label)
#                 self.button_list.remove(button)
#                 return

# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("CTkScrollableFrame example")
#         self.grid_rowconfigure(0, weight=1)
#         self.columnconfigure(2, weight=1)

#         # create scrollable label and button frame
#         current_dir = os.path.dirname(__file__)
#         print(os.path.abspath(__file__))
#         print(os.path.dirname(__file__))
#         print(current_dir)
#         self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300, command=self.label_button_frame_event, corner_radius=0)
#         self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
#         for i in range(20):  # add items with images
#             self.scrollable_label_button_frame.add_item(f"image and item {i}", image=customtkinter.CTkImage(Image.open(os.path.join(current_dir, "test_images", "chat_light.png"))))


#     def label_button_frame_event(self, item):
#         print(f"label button frame clicked: {item}")


# if __name__ == "__main__":
#     customtkinter.set_appearance_mode("dark")
#     app = App()
#     app.mainloop()


# import customtkinter as ctk
# from asset import Image_Objects,Icon_Objects
# from encrypt import AES_Encryption
# from tkinter import *
# class ChatOpt(ctk.CTkToplevel):
#     def __init__(self,master,bt,text,*args,**kwargs):
#         super().__init__(master,*args,**kwargs)
#         self.text = text
#         self.wm_overrideredirect(True)
#         self.geometry("+%d+%d" % (bt.winfo_x()+75,bt.winfo_y()+50))
#         cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
#         self.close = ctk.CTkButton(self,text="Close  ",image=cimg,command=self.destroy,compound="right")
#         self.close.pack(fill='x')
#         eimg = ctk.CTkImage(Image_Objects["encript"],size=(25,25))
#         self.delete = ctk.CTkButton(self,text="   Encripted    ",image=eimg,command=self.encript,fg_color="transparent")
#         self.delete.pack()
#         self.msg = ctk.CTkTextbox(self,fg_color="transparent",height=50,wrap="none")
#         self.msg.pack(pady=(10,0))
    
#     def encript(self):
#         code = AES_Encryption(self.text,32)
#         encrypted_code = code.encrypt()
#         self.msg.insert(INSERT,encrypted_code)

# class ContactOpt(ctk.CTkToplevel):
#     def __init__(self,bt,*args,**kwargs):
#         super().__init__(*args,**kwargs)

#         self.wm_overrideredirect(True)
#         self.geometry("+%d+%d" % (bt.winfo_x()+75,bt.winfo_y()+50))
#         cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
#         self.close = ctk.CTkButton(self,text="Close  ",image=cimg,command=self.destroy,compound="right")
#         self.close.pack()
#         dimg = ctk.CTkImage(Image_Objects["bin"],size=(25,25))
#         self.delete = ctk.CTkButton(self,text="    Delete    ",image=dimg,fg_color="transparent")
#         self.delete.pack()
#         pimg = ctk.CTkImage(Icon_Objects["icon-user"],size=(25,25))
#         self.profile = ctk.CTkButton(self,text="     Pofile    ",image=pimg,fg_color="transparent")
#         self.profile.pack()
    

#     def delete_user(self):
#         pass
    
#     def show_user_profile(self):
#         pass



# class ProfilePage(ctk.CTkToplevel):
#     def __init__(self,master,bt,email,passwd,*args,**kwargs):
#         super().__init__(master,*args,**kwargs)

#         self.wm_overrideredirect(True)
#         self.geometry("+%d+%d" % (bt.winfo_x()+75,bt.winfo_y()+50))
#         cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
#         self.close = ctk.CTkButton(self,text="Profile                                      ",
#                         image=cimg,font=ctk.CTkFont(size=15,weight="bold"),
#                         command=self.destroy,compound="right")
#         self.close.pack(fill="x")

#         pimg = ctk.CTkImage(Icon_Objects["icon-user"],size=(50,50))
#         self.profile = ctk.CTkLabel(self,text="",image=pimg,fg_color="transparent")
#         self.profile.pack(fill='x',pady=20,padx=10)

#         ad_ic_img = ctk.CTkImage(Image_Objects["add-photo"],size=(25,25))
#         self.add_icon = ctk.CTkButton(self,text=" Add User Icon",font=ctk.CTkFont(size=15,weight="bold"),anchor="w",image=ad_ic_img,fg_color="transparent")
#         self.add_icon.pack(fill='x')

#         user_id_img = ctk.CTkImage(Image_Objects["email"],size=(25,25))
#         self.user_id = ctk.CTkLabel(self,text="   "+email,image=user_id_img,compound="left",font=ctk.CTkFont(size=15),anchor="w",fg_color="transparent")
#         self.user_id.pack(fill="x",padx=10)

#         self.user_pd_frame = ctk.CTkFrame(self,fg_color="transparent")
#         self.user_pd_frame.pack(side="left",pady=(0,10),fill='x')

#         open_eye = ctk.CTkImage(Image_Objects["visible"],size=(25,25))
#         close_eye = ctk.CTkImage(Image_Objects["not-visible"],size=(25,25))

#         def show_pd(event):
#             self.user_pw_ent.configure(show="")
#             self.eye_lab.configure(image=open_eye)
            

#         def hide_pd(event):
#             self.user_pw_ent.configure(show=".")
#             self.eye_lab.configure(image=close_eye)


#         user_pd_img = ctk.CTkImage(Image_Objects["passwd"],size=(25,25))

#         self.user_pd = ctk.CTkLabel(self.user_pd_frame,text="",image=user_pd_img,fg_color="transparent")
#         self.user_pd.pack(side="left",padx=10)

#         self.user_pw_ent = ctk.CTkEntry(self.user_pd_frame,show=".",fg_color="transparent")
#         self.user_pw_ent.pack(side="left",fill='x')
#         self.user_pw_ent.insert(0,passwd)
#         self.user_pw_ent.configure(state="disabled")

#         self.eye_lab = ctk.CTkLabel(self.user_pd_frame,text="",image=close_eye,fg_color="transparent")
#         self.eye_lab.pack(side="left",padx=10)
#         self.eye_lab.bind("<Enter>",show_pd)
#         self.eye_lab.bind("<Leave>",hide_pd)



#     def add_photo(self):
#         pass



# import customtkinter as ctk
# from asset import Image_Objects

# class AddUser(ctk.CTkToplevel):
#     def __init__(self,master,bt,*args,**kwargs):
#         super().__init__(master,*args,**kwargs)

#         self.wm_overrideredirect(True)
#         self.geometry("+%d+%d" % (bt.winfo_x()+75,bt.winfo_y()+50))
#         cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
#         self.close = ctk.CTkButton(self,text="Add New User                                               ",
#                                     image=cimg,font=ctk.CTkFont(size=12,weight="bold"),
#                                     command=self.destroy,compound="right")
#         self.close.pack(fill="x",pady=(0,20))

#         self.ref_name = ctk.CTkLabel(self,text="User Name",font=ctk.CTkFont(weight='bold'),fg_color='transparent')
#         self.ref_name.pack(anchor="w",pady=(10,0),padx=(10,0))

#         self.ref_name_ent = ctk.CTkEntry(self,width=200,fg_color="transparent")
#         self.ref_name_ent.pack(anchor="e",pady=(10,0),padx=(10,10),fill="x")

#         email_img = ctk.CTkImage(Image_Objects["email"],size=(25,25))
#         self.email_lab = ctk.CTkLabel(self,text="  Email",image=email_img,compound="left",font=ctk.CTkFont(weight="bold"),fg_color="transparent")
#         self.email_lab.pack(anchor="w",padx=(10,0),pady=(10,0))

#         self.email_ent = ctk.CTkEntry(self,width=200,fg_color="transparent")
#         self.email_ent.pack(anchor="e",padx=(10,10),pady=(10,0),fill='x')

#         self.addBtn = ctk.CTkButton(self,text=" Add ",width=50)
#         self.addBtn.pack(pady=10,anchor="se",padx=(0,10))


#     def add_user(self):
#         pass

        


# class App(ctk.CTk):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)

#         self.bt = ctk.CTkButton(self,command=self.show)
#         self.bt.pack()
        
#     def show(self):
#         # self.top = ContactOpt(self,self.bt,fg_color="grey20")
#         #self.ct = ChatOpt(self,self.bt,"hi how are You!",fg_color="grey20")
#         #self.ct.bind("<FocusOut>",self.close)
#         #self.pp = ProfilePage(self,self.bt,"abcd@gmail.com","12341234",fg_color="grey20")
#         self.au = AddUser(self,self.bt,fg_color="grey20")


#     def close(self,event):
#         print("out")
#         self.top.destroy()

# if __name__ == "__main__":
    
#     ap = App()
#     ap.mainloop()


# import numpy as np
# from PIL import Image, ImageDraw

# # Open the input image as numpy array, convert to RGB
# img=Image.open(".\\images\\chat.jpg").convert("RGB")
# npImage=np.array(img)
# h,w=img.size

# # Create same size alpha layer with circle
# alpha = Image.new('L', img.size,0)
# draw = ImageDraw.Draw(alpha)
# draw.pieslice([0,0,h,w],0,360,fill=255)

# # Convert alpha Image to numpy array
# npAlpha=np.array(alpha)

# # Add alpha layer to RGB
# npImage=np.dstack((npImage,npAlpha))

# # Save with alpha
# nimg = Image.fromarray(npImage)


# #
# # Image._show(nimg)


# class ImageMasking:
#     def __init__(self,image):   
#         self.image=image
#         self.npImg=None

#     def generate_eliptical_image(self):
#         # Open the input image as numpy array, convert to RGB
#         img=Image.open(self.image).convert("RGB")
#         npImage=np.array(img)
#         h,w=img.size

#         # Create same size alpha layer with circle
#         alpha = Image.new('L', img.size,0)
#         draw = ImageDraw.Draw(alpha)
#         draw.pieslice([0,0,h,w],0,360,fill=255)


#         # Convert alpha Image to numpy array
#         npAlpha=np.array(alpha)

#         # Add alpha layer to RGB
#         self.npImage =np.dstack((npImage,npAlpha))

#         # Save with alpha
#         return Image.fromarray(self.npImage)

#     def save(self,path):

#         Image.fromarray(self.npImage).save(path)



# myimg = ImageMasking(".\\images\\chat.jpg")
# myimg.generate_eliptical_image()
# myimg.save(".\\user_img\\newChat.png")


# import mysql.connector
# from tkinter.filedialog import askopenfilename

# img = askopenfilename(filetypes=[('jpg','*.jpg'),("png","*.png")])

# with open(img,"rb") as file:
#     data = file.read()
#     try:
#         with mysql.connector.connect(host="localhost",database="chatapp",user="root",password="shubhu") as db:

#             if db.is_connected():
#                 cursor=db.cursor()
#                 email = "abcd@gmail.com"
#                 #insert into demo3 values("abcd");
#                 cursor.execute("""update user set ic = %s where id=%s""",(data,email))
#                 db.commit()
#                 print("1st half")
#                 cursor.execute("select * from user where id='abcd@gmail.com';")
#                 record = cursor.fetchone()
#                 print(record[1])
#                 cursor.close()
#                 with open(".\\user_img\\db_img.png","wb") as file:
#                     file.write(record[1])
#                 print("complete")

#     except:
#         print("Error:")
# from tkinter import *
# from tkinter.filedialog import askopenfile,askopenfilename
# import os
# # file = askopenfilename(mode="rb",filetypes=[('jpg','*.jpg'),("png","*.png")])

# f = askopenfilename(filetypes=[('jpg','*.jpg'),("png","*.png")])
# if f == "":
#     print("No file")
# else:
#     print(os.path.getsize(f))


# if file is not None:
#     data = file.read()
#     print(len(data))

# print((1,"",2))


# import mysql.connector

# with mysql.connector.connect(host="localhost",database="prac",user="root",password="shubhu") as db:
#     if db.is_connected():
#         cursor = db.cursor()
#         cursor.execute("""select * from demo3 where id = 3""")
#         record = cursor.fetchall()
#         cursor.close()
#         print(record)

#         if record[0][1] == b"":
#             print("bstring")





# import customtkinter as ctk

# win = ctk.CTk()

# def mymethod(event):
#     print("mythod ctrl+enter")
#     val = btn.get("1.0","end-1c")
#     if val == "":
#         print("empty")

# def mymethod2(event):
#     print("mymethod enter")

# def method3(event):
    
#     if event.char is not " ":
#         print(event.char)

# btn = ctk.CTkTextbox(win,wrap='word')
# btn.pack()
# btn.bind("<Control-Return>",mymethod,add="+")
# btn.bind("<Return>",mymethod2,add="+")
# btn.bind("<Key>",method3,add="+")

# win.mainloop()


# import os
# import re
# print(os.path.isfile(".\\user_img\\user_photo.png"))
# cur_dir = os.path.dirname(__file__)
# paths = os.path.join(cur_dir,"music","pop-notification.mp3")
# paths = paths.split("\\")
# paths = "\\\\".join(paths)
# print(paths)

# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()

# with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
#                 if db.is_connected():
#                     cursor=db.cursor()
#                     sql_query = """select * from user where id = '%s';""" % ("pqer")
#                     cursor.execute(sql_query)
#                     u_record = cursor.fetchone()
#                     print(u_record)



# import os

# cdir = os.path.dirname(__file__)
# print(os.path.join(cdir,"Scripts","python.exe"))

# import random
# with open(".\\dataset\\TextData.txt","r") as file:
#     data = file.read()
#     data = data.split(" ")
#     newData = []
#     for word in data:
#         if word not in newData:
#             newData.append(word)
#     print(random.choices(newData,k=10))



# import json
# import os

json_str = {"name":"","passwd":"","rem":""}
# with open("data.json","w") as file:
#     json.dump(json_str,file)

# with open("data.json","r") as file:
#     data = json.load(file)
#     print(data["rem"])

#     if data["rem"] == "":
#         print("none")

# print(os.path.isfile("data.json") is False)



# | bheem@gmail.com    |
# | myname@gmail.com   |
# | newname@gmail.com  |
# | ninja@gmail.com    |
# | perman@gmail.com   |
# | vikram@gmail.com   |
# | yourname@gmail.com


from threading import Thread


def method1():
    
    for i in range(100):
        print(f"method:  1-{i}")


def method2():
    for i in range(100):
        print(f"method:  2-{i}")


Thread(target = method1).start()
Thread(target = method2).start()