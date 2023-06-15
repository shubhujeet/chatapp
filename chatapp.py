import os
import re
import ssl
import sys
import json
import socket
import random
import smtplib
import numpy as np
from tkinter import *
import mysql.connector 
from time import sleep
from server import Server
import customtkinter as ctk
from subprocess import Popen
from threading import Thread
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from mysql.connector import Error
from encrypt import AES_Encryption
from email.message  import EmailMessage
from chatNotification import Notification
from asset import Image_Objects,Icon_Objects
from tkinter.filedialog import askopenfilename
from authentication import Email_Authentication,Password_Authentication


# laoding environment variable
load_dotenv()


# class for producing circular icons
class ImageMasking:
    def __init__(self,image):   
        self.image=image
        self.npImg=None

    def generate_eliptical_image(self):
        # Open the input image as numpy array, convert to RGB
        img=Image.open(self.image).convert("RGB")
        npImage=np.array(img)
        h,w=img.size

        # Create same size alpha layer with circle
        alpha = Image.new('L', img.size,0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0,0,h,w],0,360,fill=255)


        # Convert alpha Image to numpy array
        npAlpha=np.array(alpha)

        # Add alpha layer to RGB
        self.npImage =np.dstack((npImage,npAlpha))

        # Save with alpha
        return Image.fromarray(self.npImage)

    def save(self,path):

        Image.fromarray(self.npImage).save(path)




# class for right click opts on messages

class ChatOpt(ctk.CTkToplevel):
    def __init__(self,master,CF,chat_id,text,*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        
        # setting constant
        self.CF = CF
        self.chat_id = chat_id
        self.text = text
        self.wm_overrideredirect(True)
        self.geometry("+%d+%d" % (600,300))
        cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
        self.close = ctk.CTkButton(self,text="Close  ",image=cimg,command=self.destroy,compound="right")
        self.close.pack(fill='x')

        del_img = ctk.CTkImage(Image_Objects["bin"],size=(15,15))
        self.del_btn = ctk.CTkButton(self,text="Delete Chat",command=self.delete_chat,image=del_img,compound="left")
        self.del_btn.pack()
        
        eimg = ctk.CTkImage(Image_Objects["encript"],size=(25,25))
        self.encript_btn = ctk.CTkButton(self,text="   Encripted    ",image=eimg,command=self.encript,fg_color="transparent")
        self.encript_btn.pack()

        self.msg = ctk.CTkTextbox(self,fg_color="transparent",height=50,wrap="none")
        self.msg.pack(pady=(10,0))
    
    def encript(self):
        code = AES_Encryption(self.text,32)
        encrypted_code = code.encrypt()
        self.msg.insert(INSERT,encrypted_code)

    def delete_chat(self):
        self.CF.remove_chat(self.chat_id)


# class for right click opt on contacts

class ContactOpt(ctk.CTkToplevel):
    def __init__(self,master,SCF,log_user,contact_id,contact_icon,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # constant setting up
        self.SCF = SCF
        self.login_user = log_user
        self.contact_id = contact_id
        self.contact_icon = contact_icon
        self.wm_overrideredirect(True)
        self.geometry("+%d+%d" % (300,150))

        # gui creation
        cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
        self.close = ctk.CTkButton(self,text="Close  ",image=cimg,command=self.destroy,compound="right")
        self.close.pack()

        dimg = ctk.CTkImage(Image_Objects["bin"],size=(25,25))
        self.delete = ctk.CTkButton(self,text="    Delete    ",command=self.delete_user,image=dimg,fg_color="transparent")
        self.delete.pack()

        pimg = ctk.CTkImage(Icon_Objects["icon-user"],size=(25,25))
        self.profile = ctk.CTkButton(self,text="     Pofile    ",command=self.show_user_profile,image=pimg,fg_color="transparent")
        self.profile.pack()
    

    def delete_user(self):
        self.SCF.remove_contact(self.contact_id)
        # TODO database call
        try:
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                if db.is_connected():
                    cursor = db.cursor()
                    sql_query="""delete from contact where cid = '%s';""" % (self.contact_id)
                    cursor.execute(sql_query)
                    db.commit()
                    cursor.close()
        
        except Error as e:
            print("Eror while deleting contact!",e)

    def show_user_profile(self):
        pp = ProfilePage(self.login_user,self.contact_id,self.contact_icon)



# class for displaying profile window

class ProfilePage(ctk.CTkToplevel):
    def __init__(self,log_user,email,icon,name_label=None,passwd=None,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.log_user = log_user
        self.name_label = name_label
        self.email = email
        self.wm_overrideredirect(True)
        self.geometry("+%d+%d" % (700,200))
        cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
        self.close = ctk.CTkButton(self,text="Profile                                      ",
                        image=cimg,font=ctk.CTkFont(size=15,weight="bold"),
                        command=self.destroy,compound="right")
        self.close.pack(fill="x")

        if icon is None :
            pimg = ctk.CTkImage(Icon_Objects["icon-user"],size=(50,50))
        else:
            pimg = ctk.CTkImage(Image.open(icon),size=(50,50))

        self.profile = ctk.CTkLabel(self,text="",image=pimg,fg_color="transparent")
        self.profile.pack(fill='x',pady=20,padx=10)

        if self.log_user == email:
            ad_ic_img = ctk.CTkImage(Image_Objects["add-photo"],size=(25,25))
            self.add_icon = ctk.CTkButton(self,text=" Add User Icon",command=self.add_photo,font=ctk.CTkFont(size=15,weight="bold"),anchor="w",image=ad_ic_img,fg_color="transparent")
            self.add_icon.pack(fill='x')

        user_id_img = ctk.CTkImage(Image_Objects["email"],size=(25,25))
        self.user_id = ctk.CTkLabel(self,text="   "+email,image=user_id_img,compound="left",font=ctk.CTkFont(size=15),anchor="w",fg_color="transparent")
        self.user_id.pack(fill="x",padx=10)

        if self.log_user == email:
            self.user_pd_frame = ctk.CTkFrame(self,fg_color="transparent")
            self.user_pd_frame.pack(side="left",pady=(0,10),fill='x')

            open_eye = ctk.CTkImage(Image_Objects["visible"],size=(25,25))
            close_eye = ctk.CTkImage(Image_Objects["not-visible"],size=(25,25))

            def show_pd(event):
                self.user_pw_ent.configure(show="")
                self.eye_lab.configure(image=open_eye)
                

            def hide_pd(event):
                self.user_pw_ent.configure(show=".")
                self.eye_lab.configure(image=close_eye)

        
            user_pd_img = ctk.CTkImage(Image_Objects["passwd"],size=(25,25))

            self.user_pd = ctk.CTkLabel(self.user_pd_frame,text="",image=user_pd_img,fg_color="transparent")
            self.user_pd.pack(side="left",padx=10)

            self.user_pw_ent = ctk.CTkEntry(self.user_pd_frame,show=".",fg_color="transparent")
            self.user_pw_ent.pack(side="left",fill='x')
            self.user_pw_ent.insert(0,passwd)
            self.user_pw_ent.configure(state="disabled")

            self.eye_lab = ctk.CTkLabel(self.user_pd_frame,text="",image=close_eye,fg_color="transparent")
            self.eye_lab.pack(side="left",padx=10)
            self.eye_lab.bind("<Enter>",show_pd)
            self.eye_lab.bind("<Leave>",hide_pd)

        else:
            None

    def add_photo(self):
        file = askopenfilename(filetypes=[('jpg','*.jpg'),("png","*.png")])
        
        if len(file) > 4290000000 :
            print("alert")
            notification = Notification(app_name="Chat Application",
                                        title="Alert !",
                                        msg="File size too big !",
                                        duration=3,
                                        icon=Image_Objects["remove"]
                                        )
            notification.toast()

        elif file == "":
            print("no file selected!")
            notification = Notification(app_name="Chat Application",
                                        title="Alert !",
                                        msg="No file selected !",
                                        duration=3,
                                        icon=Image_Objects["remove"]
                                        )
            notification.toast()

        else:
            locald = self.log_user.split(".")
            locald = locald[0]
            locald = f".\\user_img\\{locald}.png"

            userImg = ImageMasking(file)
            userImg.generate_eliptical_image()
            userImg.save(locald)

            pimg = ctk.CTkImage(Image.open(locald),size=(50,50))
            self.profile.configure(image=pimg)
            self.name_label.configure(image=pimg)

            with open(locald,"rb") as file:
                data = file.read()
                print(len(data))
                try:
                    with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                        if db.is_connected():
                            cursor = db.cursor()
                            # TODO update query change
                            #print(type(self.email))
                            cursor.execute("""update user set ic = %s where id=%s""",(data,self.email))
                            db.commit()
                            cursor.close()

                            notification = Notification(app_name="ChatApp",
                                                        title="Info",
                                                        msg = "Profile Icon changed Successfully!",
                                                        duration=4,
                                                        icon=Image_Objects["user"]
                                                        )
                            notification.toast()



                except Error as e:
                    print("Error while updating icon to database ProfilePage:",e)

            

# class for adding new contact who have an account in chatapp

class AddUser(ctk.CTkToplevel):
    def __init__(self,master,login_user,CF,bt,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

        
        self.CF = CF
        self.login_user = login_user
        self.wm_overrideredirect(True)
        self.geometry("+%d+%d" % (bt.winfo_x()+75,bt.winfo_y()+50))
        cimg = ctk.CTkImage(Image_Objects["remove"],size=(15,15))
        self.close = ctk.CTkButton(self,text="Add New User                                               ",
                                    image=cimg,font=ctk.CTkFont(size=12,weight="bold"),
                                    command=self.destroy,compound="right")
        self.close.pack(fill="x",pady=(0,20))


        self.ref_name = ctk.CTkLabel(self,text="User Name",font=ctk.CTkFont(weight='bold'),fg_color='transparent')
        self.ref_name.pack(anchor="w",pady=(10,0),padx=(10,0))

        self.ref_name_ent = ctk.CTkEntry(self,width=200,fg_color="transparent")
        self.ref_name_ent.pack(anchor="e",pady=(10,0),padx=(10,10),fill="x")

        email_img = ctk.CTkImage(Image_Objects["email"],size=(25,25))
        self.email_lab = ctk.CTkLabel(self,text="  Email",image=email_img,compound="left",font=ctk.CTkFont(weight="bold"),fg_color="transparent")
        self.email_lab.pack(anchor="w",padx=(10,0),pady=(10,0))

        self.email_ent = ctk.CTkEntry(self,width=200,fg_color="transparent")
        self.email_ent.pack(anchor="e",padx=(10,10),pady=(10,0),fill='x')

        self.addBtn = ctk.CTkButton(self,text=" Add ",width=50,command=self.add_user)
        self.addBtn.pack(pady=10,anchor="se",padx=(0,10))



    def add_user(self):
        class UserNotFound(Exception):
            pass

        email = self.email_ent.get()
        u_name = self.ref_name_ent.get()
        u_icon = None
        print(email,u_name)
        print(self.login_user)

        # TODO database call
        try:
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                if db.is_connected():
                    cursor=db.cursor()

                    sql_query = """select * from user where id = '%s';""" % (email)
                    cursor.execute(sql_query)
                    u_record = cursor.fetchone()
                    if u_record == None:
                        raise UserNotFound
                    else:
                        u_icon = u_record[1]
                        cursor.execute("""insert into contact(cid,cic,cname,contact_of) values(%s,%s,%s,%s)""",(email,u_icon,u_name,self.login_user))
                        db.commit()
                        cursor.close()
                        print("user added")
                        notification = Notification(app_name="Chat Application",
                                        title="Info",
                                        msg =f"User added successfully to your contact:{email}",
                                        duration=4,
                                        icon=Image_Objects["user"]
                                        )
                        notification.toast()

                        locd=None
                        if u_icon !=None and u_icon != b"":
                            locd = email.split(".")
                            locd = locd[0]
                            locd = f".\\user_img\\{locd}.png"
                            with open(locd,"wb") as file:
                                file.write(u_icon)

                        self.CF.add_contact(email,locd)


        except Error as e:
            print(e)
            print(e.errno)
            if e.errno == 1062:
                print("catched") 

    
        except UserNotFound:
            notification = Notification(app_name="Chat Application",
                                        title="Info",
                                        msg =f"No Such user is registered on ChatApp:{email}",
                                        duration=4,
                                        icon=Image_Objects["remove"]
                                        )
            notification.toast()

        
# class for providing recommendation      

class RecommendationFrame(ctk.CTkScrollableFrame):
    def __init__(self,master,command=None,**kwargs):
        super().__init__(master,**kwargs)
        
        # setting constant
        self.command=command
        self.ref_bt = []

    def add_suggestion(self,suggestion):
        s_btn = ctk.CTkButton(self,text=suggestion)
        if self.command is not None:
            s_btn.bind("<Button-1>",lambda x:self.command(suggestion))
        s_btn.pack(side="left",padx=10,pady=2)
        self.ref_bt.append(s_btn)




# class for creating list of contacts

class ScrollableContactFrame(ctk.CTkScrollableFrame):
    def __init__(self,master,command=None,bind_command=None,**kwargs):
        super().__init__(master,**kwargs)

        self.command=command
        self.bind_command=bind_command
        self.contact_list = []
    
    def add_contact(self,contact,icon=None):
        if icon == None:
            im_icon = ctk.CTkImage(Icon_Objects["icon-user"],size=(20,20))
        else:
            im_icon = ctk.CTkImage(Image.open(icon),size=(20,20))

        button = ctk.CTkButton(self, text=contact, image=im_icon,font=ctk.CTkFont(size=15),height=50,fg_color="transparent", compound="left", anchor="w")
        if self.command is not None:
            button.configure(command=lambda:self.command(contact,icon))
        if self.bind_command is not None:
            button.bind("<Button-3>",lambda x:self.bind_command(contact,icon))
        button.pack(side='top',anchor="w",fill='x',pady=(0,10))
        self.contact_list.append(button)

    def remove_contact(self,contact):
        for conn in self.contact_list:
            if contact == conn.cget("text"):
                conn.destroy()
                self.contact_list.remove(conn)
                return 



# class for creating chat window with chats

class ScrollableChatFrame(ctk.CTkScrollableFrame):
    def __init__(self,master,login_user,command=None,**kwargs):
        super().__init__(master,**kwargs)

        # setting up constant
        self.login_user = login_user
        self.command=command
        self.chat_book = []
        self.chat_id = []
    
    def add_chat(self,m_id,msg,contact_user,icon=None):

        if icon == None:
            im_icon = ctk.CTkImage(Image_Objects["icon-user"],size=(20,20))
        else:
            im_icon = ctk.CTkImage(Image.open(icon),size=(20,20))

        label = ctk.CTkLabel(self, text=msg, image=im_icon, compound="left", padx=5, anchor="w")
        
        if self.command is not None:
            label.bind("<Button-3>",lambda x:self.command(msg,m_id))
        if self.login_user == contact_user:
            label.pack(anchor="e",pady=10,padx=(0,20))
        else:
            label.pack(anchor="w",pady=10,padx=(20,0))
        self.chat_book.append(label)
        self.chat_id.append(m_id)

    def remove_chat(self,m_id):
        for chat, cid in zip(self.chat_book, self.chat_id):
            if m_id == cid :
                msg="message is deleted"
                chat.configure(text=msg)
                # TODO database call
                try:
                    with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                        if db.is_connected():
                            cursor = db.cursor()
                            sql_query="""delete from message where mid=%s""" %(m_id)
                            cursor.execute(sql_query)
                            db.commit()
                            cursor.close()
                            return

                except Error as e:
                    print("Error while deleting message from chat frame",e)


# The main class which holds the other class of the Main Body of the chatapp

class Chat_App(ctk.CTkFrame):

    def __init__(self,master,log_user,**kwargs):
        super().__init__(master,**kwargs)

        # constant
        self.master = master
        self.log_user = log_user
        self.profile_window = None
        self.toplevel_window = None
        self.loger_img = "my_image"
        self.h_var = 50
        bimg = None
        self.my_image_path= "my_image"
        # TODO database call
        try:
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv('user_name'),password=os.getenv("passwd_db")) as db:
                if db.is_connected():
                    cursor = db.cursor()
                    sql_query="""select ic from user where id = '%s';""" % (self.log_user)
                    cursor.execute(sql_query)
                    bimg = cursor.fetchone()
                    cursor.close()
                    # print(bimg[0])
                    if bimg[0] == b'':
                        print("no image icon")
                        None
                    else: 
                        print("image exists")  
                        locald = self.log_user.split(".")
                        locald = locald[0]
                        
                        self.loger_img = f".\\user_img\\{locald}.png"

                        with open(self.loger_img,"wb") as file:
                            file.write(bimg[0])
                        self.my_image_path = self.loger_img
        except Error as e:
            print("Error while fetching login user icon:",e)


        # loading Image and icons
        if os.path.isfile(self.loger_img):
            self.my_image = ctk.CTkImage(Image.open(self.loger_img),size=(40,40))
        else:    
            self.my_image = ctk.CTkImage(Image_Objects["user"],size=(40,40))
        
        self.add_user_img = ctk.CTkImage(Image_Objects["add-user"],size=(40,40))
        self.log_out_img = ctk.CTkImage(Image_Objects["logout"],size=(40,40))
        self.bg_img = ctk.CTkImage(Image_Objects["welcome"],size=(300,300))

        # tab frame 
        self.tabFrame = ctk.CTkFrame(self,
                                    corner_radius=0,
                                    fg_color="#1d1f1e",
                                    border_width=1,
                                    border_color="grey20"
                                    )
        self.tabFrame.pack(side="top",
                            fill="x",
                            ipady=10
                            )

        # TODO fetch the name and icon based on login user

        self.add_user_btn = ctk.CTkLabel(self.tabFrame,text="",
                                    image=self.add_user_img
                                    )
        self.add_user_btn.pack(side="left",
                            pady=(0,10),
                            padx=(20,0))

        self.add_user_btn.bind("<Button-1>",self.add_user)



        self.log_out_btn = ctk.CTkLabel(self.tabFrame,text="",
                                        image=self.log_out_img,
                                        compound="right"
                                        )
        self.log_out_btn.pack(side="right",
                                pady=(0,10),
                                padx=(0,20)
                                )
        self.log_out_btn.bind("<Button-1>",self.log_out_window)


        self.nameLabel = ctk.CTkLabel(self.tabFrame, 
                                    fg_color="transparent",
                                    text="  "+self.log_user,
                                    font=("ARLRDBD",25),
                                    image=self.my_image,
                                    compound="left",
                                    )
        self.nameLabel.pack(anchor="center",
                            pady=(10,0),
                            padx=10
                            )

        self.nameLabel.bind("<Button-1>",self.show_log_profile)
                    

        # Frames
        self.leftFrame = ScrollableContactFrame(self,
                        command=self.show_chat,
                        bind_command=self.show_contact_opt,
                        scrollbar_button_color="#1f0507",
                        corner_radius=0,
                        fg_color="#1d1f1e",
                        border_width=0,
                        width=300,
                        )
        self.leftFrame.pack(side="left", fill="y", padx=0, pady=0) 

        my_contacts = None
        # TODO database call
        try:
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:

                if db.is_connected():
                    cursor=db.cursor()
                    sql_query = """create table if not exists contact(cid varchar(300) not null, cic longblob, cname varchar(1000),contact_of varchar(300) not null,foreign key (cid) references user(id));"""
                    cursor.execute(sql_query)
                    sql_query = """select * from contact where contact_of = '%s';""" % (self.log_user)
                    cursor.execute(sql_query)
                    my_contacts = cursor.fetchall()
                    cursor.close()

        except Error as e:
            print("Error while creating and loading cntact:",e)

        if my_contacts == None:
            my_contacts = []

        for i in range(len(my_contacts)):
            c_email = my_contacts[i][0]
            c_icon = my_contacts[i][1]
            img_file=None

            if c_icon == b"":
                img_file = None
            else:
                img_file = f".\\user_img\\contact{i}.png"
                with open(img_file,"wb") as file:
                    file.write(c_icon)

            self.leftFrame.add_contact(c_email,img_file)

        # home of the chat frame
        self.rightFrame = ctk.CTkFrame(self,
                                        corner_radius=0, 
                                        fg_color="#473d3e"
                                        )
        self.rightFrame.pack(side="left", 
                            fill='both',
                            expand=True, 
                            padx=0,
                            pady=0
                            )

        self.welcome_lab = ctk.CTkLabel(self.rightFrame,image=self.bg_img,text="")
        self.welcome_lab.pack(fill="both",expand=True)


        
        self.chat_win = ctk.CTkFrame(self.rightFrame,
                                    corner_radius=0, 
                                    fg_color="#473d3e"
                                    )


        self.chat_Frame = ScrollableChatFrame(self.chat_win,
                                                login_user=self.log_user, 
                                                command=self.show_chat_opt,
                                                corner_radius=0, 
                                                scrollbar_button_color="#1f0507"
                                                )

        self.messageFrame = ctk.CTkFrame(self.chat_win,
                                        fg_color="#1d1f1e",
                                        corner_radius=0,
                                        height=self.h_var,
                                        border_width=1,
                                        border_color="grey20"
                                        )         

                                     
        
        self.recommendationLab = ctk.CTkLabel(self.messageFrame,text="Recommendation:",anchor="w",font=ctk.CTkFont(weight="bold"))
        self.recommendationBox = RecommendationFrame(self.messageFrame, height=50,command=self.go_with_suggestion, orientation="horizontal",scrollbar_button_color="black")


        self.messageBox = ctk.CTkTextbox(self.messageFrame,height=self.h_var,fg_color="grey22", font=ctk.CTkFont(size=12),wrap="word")                                         

        self.messageBox.bind("<Return>",self.set_height,add='+')
        self.messageBox.bind("<BackSpace>",self.reset_height,add="+")
        self.messageBox.bind("<Control-Return>",self.send_message,add="+")
        self.messageBox.bind("<Control-KeyPress-Tab>",self.show_recommendation,add="+")

        send_img = ctk.CTkImage(Image_Objects["send-message"],size=(25,25))
        self.sendBtn = ctk.CTkButton(self.messageFrame, text="",command=self.send_message,image=send_img,fg_color="transparent",hover_color="grey35")



    # Implementation of required methods

    def go_with_suggestion(self,sugg_word):
        print(sugg_word)
        self.messageBox.insert("end",sugg_word)

    def add_user(self,event):  
        au = AddUser(self, login_user=self.log_user, CF=self.leftFrame, bt = self.add_user_btn,fg_color="grey20")

    def log_out_window(self,event):
        
        pdir = os.path.dirname(__file__)
        pext = os.path.join(pdir,"Scripts","python.exe")
        
        Popen([pext,"chatapp.py"])
        sys.exit(0)

    def send_message(self,event=None):
        my_msg = self.messageBox.get("1.0","end-1c")
        
        self.messageBox.delete("1.0","end-1c")

        code=AES_Encryption(my_msg,32)
        code=code.encrypt()
        print(code)

        # receiver icon
        r_icon = None

        # TODO database call
        if my_msg == "":
            None
        else:
            try:
                luser = self.log_user
                with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                    if db.is_connected():
                        cursor = db.cursor()
                        sql_query = """insert into message(sen,rec,msg,mkey,mtag,mnonce) values(%s,%s,%s,%s,%s,%s);""" 
                        col =  (luser,receiverCon,code[1],code[0],code[2],code[3])
                        cursor.execute(sql_query,col)
                        db.commit()
                        sql_query = """select ic from user where id = '%s';""" % (receiverCon)
                        cursor.execute(sql_query)
                        r_icon = cursor.fetchone()
                        cursor.close()
                        print("message send")
           
            except Error as e:
                print("Error while sending message from messageBox to database:",e)
            
            r_icon_path = None

            if r_icon != b"" or r_icon != None:
                #print(r_icon)
                depackRec= receiverCon.split(".")
                name = depackRec[0]
                r_icon_path =f".\\user_img\\{name}.png" 
                with open(r_icon_path,"wb") as file:
                    file.write(r_icon[0])

            self.show_chat(receiverCon,r_icon_path)


    def show_recommendation(self,event):
        #log_user_msg = self.messageBox.get("1.0","end-1c")

        for wid in self.recommendationBox.winfo_children():
            wid.pack_forget()

        suggestion_list = None
        data = "sample"
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
                client.connect(("localhost",9999))
                client.send(data.encode())
                sugg_str = client.recv(1024).decode()
                suggestion_list = sugg_str.split(",")
                print(suggestion_list)
                for i in range(len(suggestion_list)):
                    self.recommendationBox.add_suggestion(suggestion_list[i])

                client.close()
            
        except socket.error as err:
            print("Error while creating socket connection:",err)



    def show_log_profile(self,event):
        print("displaying profile")
        # TODO database call
        record = None
        try:
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                if db.is_connected():
                    cursor = db.cursor()
                    sql_query = """select * from user where id='%s';""" % (self.log_user)
                    cursor.execute(sql_query)
                    record = cursor.fetchone()
                    cursor.close()
                    print("Record fetcing successful!")

        except Error as e:
            print("Error while fetching data for profile on loging label click:",e)


        # print("This is fetched record:",record)
        email = record[0]
        icon = record[1]
        password = record[2]
        print(email,password)

        if icon == b'':
            print("no ic in profile call")
            icon = None
        else:
            print("ic found")
            with open(self.loger_img,"wb") as file:
                file.write(icon)
            icon = self.loger_img


        pp = ProfilePage(log_user=self.log_user, email=email, icon=icon, name_label=self.nameLabel, passwd=password,fg_color="grey20")


    def show_chat_opt(self,msg,m_id):
        print("msg",msg,":",m_id)
        cnto = ChatOpt(self,self.chat_Frame,m_id,msg,fg_color="grey20")


    def show_contact_opt(self,contact_id,cont_icon):
        print("contact is on right_click:",contact_id)
        cnto = ContactOpt(self,self.leftFrame,self.log_user,contact_id,cont_icon,fg_color="grey20")

    def set_height(self,event):
        self.h_var = self.h_var = self.h_var + 25 if self.h_var < 100 else 100
        self.messageBox.configure(height=self.h_var)

    def reset_height(self,event):
        self.h_var = self.h_var = self.h_var - 25 if self.h_var > 50 else 50
        self.messageBox.configure(height=self.h_var)
        
    def show_chat(self,contact=None,con_icon=None):
        print("contact :",contact)

        global receiverCon 
        
        receiverCon = contact
        
        for wid in self.rightFrame.winfo_children():
            wid.pack_forget()

        for wid in self.chat_Frame.winfo_children():
            wid.pack_forget()

        # TODO database call
        # database call for message
        my_chats = None

        try: 
            with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                if db.is_connected():
                    cursor = db.cursor()
                    cursor.execute("""select * from message where sen='%s' and rec='%s' or sen='%s' and rec='%s' order by mid asc;""" %(self.log_user,contact,contact,self.log_user))
                    my_chats = cursor.fetchall()
                    cursor.close()
                    print(my_chats)
                    print("hey chat")
                    
        except Error as e:
            print(e)
            # if e.errno == 1045:
            #     print("error 1045")

        
        # conforming visiblity fo the frame
        self.chat_win.pack(side="left", 
                            fill='both',
                            expand=True, 
                            padx=0,
                            pady=0
                            )


        # Scrollable chatFrame visiblity
       
        self.chat_Frame.pack(side="top",
                            fill="both", 
                            expand=True
                            )
        
        my_chats = [] if my_chats == None else my_chats
        # TODO for loop for adding chat on chatframe
        for i in range(len(my_chats)):
            # TODO database call
            pic = None
            
            if self.log_user == my_chats[i][1]:
                
                if os.path.isfile(self.my_image_path):
                    pic = self.my_image_path
                else:
                    pic = ".\\images\\user.png"
                
            elif con_icon == None:
                pic = None
            else:
                pic = con_icon

            # print(my_chats)


            # Decrypting message
            encrypted_text=AES_Encryption(key=my_chats[i][4],ciphertext=my_chats[i][3],tag=my_chats[i][5],nonce=my_chats[i][6])
            decrypted_text = encrypted_text.decrypt()
            
            # print(pic)
            self.chat_Frame.add_chat(m_id=my_chats[i][0],msg=decrypted_text,contact_user=my_chats[i][1],icon=pic)


        # setting up message Frame
        
        self.messageFrame.pack(side="bottom",fill="x", anchor='s',ipady=8,ipadx=5)

        self.recommendationLab.pack(side="top",fill="x",anchor="w",pady=5,padx=10)
        self.recommendationBox.pack(side="top",fill='x',padx=10,expand=True)
        
        self.messageBox.pack(side="left", fill='x', padx=10, pady=(0,40),expand=True)
        
        
        self.sendBtn.pack(fill="both",anchor="center",pady=(5,45),padx=(0,10))


    def encript_message(self,messg):
        print("encripting message")
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            self.toplevel_window = ctk.CTkToplevel(self)
            self.toplevel_window.geometry("400x300")
            self.toplevel_window.title("Encripted Message")

            self.label = ctk.CTkLabel(self.toplevel_window, text=message)
            self.label.pack(fill="both", padx=20, pady=20)


        else:
            self.toplevel_window.focus() 



class Login_Image_Container(ctk.CTkFrame):

    def __init__(self,master,image,**kwargs):
        super().__init__(master,**kwargs)

        # label to hold image
        self.left_con_img = ctk.CTkLabel(self,    
                                        image=image, 
                                        text=""
                                        )
        self.left_con_img.pack(fill="both", 
                                expand=True
                                )



class Login(ctk.CTkFrame):

    def __init__(self,master,leftContainer=None,**kwargs):
        super().__init__(master,**kwargs)


        # constant setting up
        self.master = master
        self.my_font = "TCMI____"
        self.btn_text = "Login"
        self.page_title = "Chat Application"
        self.prompt_message = None
        self.warn_color = "#f5163f"
        self.email_flag=False
        self.passwd_flag = False
        self.leftContainer = leftContainer


        # login ui

        self.prompt_message = ctk.CTkLabel(self,
                                            text="",
                                            text_color="#bb55f2",
                                            font=ctk.CTkFont(size=15)
                                            )
        self.prompt_message.pack(side="top",
                                fill='x',
                                ipady=5,
                                ipadx=5
                                )


        self.title_lab = ctk.CTkLabel(self,
                                text=self.page_title, 
                                justify="left",
                                font=ctk.CTkFont(family=self.my_font,
                                                weight="bold",
                                                size=40
                                                )
                                )
        self.title_lab.pack(side="top",
                        anchor="ne", 
                        pady=50, 
                        padx=75
                        )


        self.email_lab = ctk.CTkLabel(self,
                                    text="Email",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=18
                                                    ),
                                    anchor="w"
                                    ) 
        self.email_lab.pack(side="top", 
                            pady=20, 
                            padx=68, 
                            fill='x'
                            )


        self.lemail_ent = ctk.CTkEntry(self,
                                    placeholder_text="abcd@gmail.com",
                                    height=30,
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=17
                                                    )
                                    )
        self.lemail_ent.pack(side="top", 
                            anchor="ne", 
                            pady=5,
                            padx=68, 
                            fill='x'
                            )

        self.lemail_ent.bind("<Enter>",self.check_email_validity,add="+")
        self.lemail_ent.bind("<Return>",self.check_email_validity,add="+")
        self.lemail_ent.bind("<Leave>",self.check_email_validity,add="+")

        self.email_warning = ctk.CTkLabel(self,
                                            text="",
                                            text_color=self.warn_color,
                                            font=ctk.CTkFont(size=15)
                                            )
        self.email_warning.pack(side="top",
                                pady=5,
                                padx=68,
                                anchor="ne",
                                fill='x'
                                )


        self.passwd_lab = ctk.CTkLabel(self,
                                    text="Password",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=18
                                                    ),
                                    anchor="w"               
                                    ) 
        self.passwd_lab.pack(side="top", 
                                pady=20, 
                                padx=68, 
                                fill='x'
                                )


        self.lpasswd_ent = ctk.CTkEntry(self,
                                        placeholder_text="",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=20),
                                        show="."
                                        )
        self.lpasswd_ent.pack(side="top", 
                                pady=5, 
                                padx=68, 
                                fill='x'
                                )

        self.lpasswd_ent.bind("<Return>",self.check_p_safety,add="+")
        self.lpasswd_ent.bind("<Leave>",self.check_p_safety,add="+")


        self.passwd_warning = ctk.CTkLabel(self,
                                            text = "",
                                            image = None,
                                            compound = "left"
                                            )
        self.passwd_warning.pack(side="top",
                                    fill="x",
                                    pady=5
                                    )



        self.login_btn = ctk.CTkButton(self, text=self.btn_text,command=self.login_user)
        self.login_btn.pack(side="top", 
                            pady=20, 
                            padx=90
                            )


        self.check_var = ctk.StringVar(value = "yes")
        self.check_box = ctk.CTkCheckBox(self, 
                                         text=" Remember me",
                                         variable=self.check_var,
                                         onvalue="yes",
                                         offvalue="no",
                                         checkbox_width=20,
                                         checkbox_height=20,
                                         border_width=2,
                                         font=ctk.CTkFont(family=self.my_font,
                                                            size=13
                                                            )
                                        )
        self.check_box.pack(side="top", 
                            pady=15, 
                            padx=72, 
                            fill='x'
                            )


        self.forgot_passwd = ctk.CTkLabel(self,
                                            text=" Forgot Password?",
                                            text_color="#2276f5",
                                            anchor='e',
                                            font=ctk.CTkFont(size=13)
                                             )
        self.forgot_passwd.pack(side="top",
                                fill="x",
                                pady=10,
                                padx=100
                                )
        self.forgot_passwd.bind("<Button-1>",self.restore_passwd )


        self.create_new_ac = ctk.CTkLabel(self,
                                            text=" Create New Account!",
                                            text_color="#2276f5",
                                            anchor="e",
                                            font=ctk.CTkFont(size=14)
                                            )
        self.create_new_ac.pack(side="top",
                                fill="x",
                                pady=0,
                                padx=100
                                )

        self.create_new_ac.bind("<Button-1>",self.register_user)


        self.json_data = {"email":"","passwd":"","rem":""}

        if os.path.isfile("data.json") is False:
            with open("data.json","w") as file:
                json.dump(json_data,file)


        with open("data.json","r") as file:
            data = json.load(file)
            
            if data["rem"] == "yes":
                self.lemail_ent.insert(0,data["email"])
                self.lpasswd_ent.insert(0,data["passwd"])

        
    def get_login_email_ent(self):
        return str(self.lemail_ent.get())

    def get_login_passwd_ent(self):
        return str(self.lpasswd_ent.get())

    def get_isRemember(self):
        return str(self.check_box.get())


    def all_good_conf(self):
        return self.email_flag and self.passwd_flag

    def check_p_safety(self,event):
        print(self.lpasswd_ent.get())
        passwd = str(self.lpasswd_ent.get())
        pass_safety = Password_Authentication(passwd)
        pass_safety = pass_safety.check_safety()

        
        match pass_safety:
            case "very_weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["very-weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" very weak !",
                                                text_color=self.warn_color,
                                                image = warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )
                
            case "weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" weak !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "good":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["good"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Good !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "excellent":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["excellent"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Excellent !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "large":
                # passwd_flag will remain False
                warn_img = ctk.CTkImage(Image_Objects["wow"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Too Large !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case _:
                # passwd_flag will remin False
                warn_img = ctk.CTkImage(Image_Objects["threat"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Security Threat !",
                                                text_color= self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )


    def check_email_validity(self,event):
        print(self.lemail_ent.get())
        email = str(self.lemail_ent.get())
        auth_email = Email_Authentication(email)
        response = auth_email.check_validity()

        match response:
            case "match":
                self.email_flag = True
                self.email_warning.configure(text="")
                
            case "invalid_domain_add":
                war_text = "x Invalid domain for the email!"
                self.email_warning.configure(text=war_text)
            
            case "invalid_local_add":
                war_text = "x Invalid local address for the email!"
                self.email_warning.configure(text=war_text)
                
            case "invalid_email":
                war_text = "x Invalid Email id!"
                self.email_warning.configure(text=war_text)
                
            case _:
                self.email_warning.configure(text="")


    def register_user(self,event):
        print("register")
        rcontainer = Register(self.master)
        rcontainer.pack(side="left", fill="both", expand=True)
        for widg in self.winfo_children():
            widg.pack_forget()
        self.pack_forget()


    def restore_passwd(self,event):
        print("restore")
        container = Restore(self.master)
        container.pack(side="left", fill="both", expand=True)
        for wid in self.winfo_children():
            wid.pack_forget()
        self.pack_forget()


    def login_user(self):
        def reset_label():
                self.prompt_message.configure(text="",fg_color="transparent")

        if self.all_good_conf():
            print(self.get_login_email_ent())
            print(self.get_login_passwd_ent())
            print(self.get_isRemember())
            uid = self.get_login_email_ent()
            pswd = self.get_login_passwd_ent()
            rem = self.get_isRemember()
            self.json_data['email'] = uid
            self.json_data["passwd"] = pswd
            self.json_data["rem"] = rem

            with open("data.json","w") as file:
                json.dump(self.json_data,file)

            # TODO database call
            try:
                with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                    
                    if db.is_connected():
                        cursor=db.cursor()
                        sql_query1 = """create table if not exists user(id varchar(300) primary key, ic longblob, password varchar(1000) not null, remember varchar(3));"""
                        cursor.execute(sql_query1)
                        db.commit()
                        sql_query2 = """create table if not exists message(mid int primary key auto_increment, sen varchar(300) not null, rec varchar(300), msg longblob,mkey longblob, mtag longblob, mnonce longblob);"""
                        cursor.execute(sql_query2)
                        db.commit()
                        cursor.execute("select id,password,remember from user where id = '%s';" % uid)
                        record = cursor.fetchone()
                        print(record)
                        if record != None:
                            if record[0] == uid:
                                print("match")
                                print(rem)
                                cursor.execute("update user set remember='%s' where id='%s';" % (rem,uid))
                                print("rem update successful!")
                                db.commit()
                                cursor.close()
                                # print(rec)
                                
                                notification = Notification(app_name="Chat Application",
                                                            title="Conformation Info",
                                                            msg="Login Successfull !",
                                                            duration=4,
                                                            icon=Icon_Objects['icon-live-chat'],
                                                            )
                                notification.toast()

                                for wid in self.master.winfo_children():
                                    wid.pack_forget()
                                
                                if self.leftContainer != None:
                                    self.leftContainer.pack_forget()

                                f = Chat_App(self.master,uid)
                                f.pack(fill='both',expand=True)


                            else:
                                print("prompting message")
                                prompt_text = " -x-  No Such User, Register Now !! "
                                self.prompt_message.configure(text=prompt_text,fg_color="grey35")
                                # refresh after 4 sec
                                self.prompt_message.after(4000,reset_label)


                        else:
                            print("prompting message")
                            prompt_text = " -x-  No Such User, Register Now !! "
                            self.prompt_message.configure(text=prompt_text, fg_color="grey35")
                            # refresh after 4 sec
                            self.prompt_message.after(4000,reset_label)


            except Error as e:
                print(e)
                print("prompting message")
                prompt_text = " -x-  No Such User, Register Now !! "
                self.prompt_message.configure(text=prompt_text, fg_color="grey35")
                # refresh after 4 sec
                self.prompt_message.after(4000,reset_label)

        else:
            print("prompting message")
            prompt_text = " -x-  Check Invalid Entries !! "
            self.prompt_message.configure(text=prompt_text, fg_color="grey35")
            # refresh after 4 sec
            self.prompt_message.after(4000,reset_label)


#===============================================================================================




class Register(ctk.CTkFrame):

    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)


        # setting up constant
        self.master = master
        self.email_flag = False
        self.passwd_flag = False
        self.passwd_conf_flag = False   
        self.warn_color="#f5163f"  
        self.my_font = "TCMI____" 
        self.btn_text = "Create" 
        self.page_title = "Create New A/c"


        # loading Images,icons
        self.back_img = ctk.CTkImage(Image_Objects["back"],size=(25,25))
        self.conf_img = ctk.CTkImage(Image_Objects["yes"], size=(25,25))
        self.deny_img = ctk.CTkImage(Image_Objects["remove"], size=(25,25))
        

        # Back button 
        self.hold_back_frame = ctk.CTkFrame(self,
                                            fg_color="transparent"
                                            )
        self.hold_back_frame.pack(side="top",
                                    pady=1,
                                    padx=1,
                                    fill='x'
                                    )


        self.back_btn = ctk.CTkButton(self.hold_back_frame,
                                    text="",
                                    width=20,
                                    hover_color="grey35",
                                    image=self.back_img,
                                    compound='left',
                                    fg_color="transparent",
                                    command=self.undo_page_register
                                    )
        self.back_btn.pack(side="top",
                            pady=0,
                            padx=0,
                            anchor="w"
                            )


        # prompt message area
        self.prompt_message = ctk.CTkLabel(self,
                                            text="",
                                            text_color="#bb55f2",
                                            font=ctk.CTkFont(size=15)
                                            )
        self.prompt_message.pack(side="top",
                                fill='x',
                                ipady=5,
                                ipadx=5
                                )


        # user page ui 
        self.page_title = ctk.CTkLabel(self,
                                    text=self.page_title, 
                                    justify="left",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=40
                                                    )
                                    )
        self.page_title.pack(side="top",
                        anchor="ne", 
                        pady=10, 
                        fill='x'
                        )


        self.email_lab = ctk.CTkLabel(self,
                                    text="Email",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=18
                                                    ),
                                    anchor="w"
                                    ) 
        self.email_lab.pack(side="top", 
                            pady=17, 
                            padx=68, 
                            fill='x'
                            )


        self.remail_ent = ctk.CTkEntry(self,
                                    placeholder_text="abcd@gmail.com",
                                    height=30,
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=17
                                                    )
                                    )
        self.remail_ent.pack(side="top", 
                            anchor="ne", 
                            pady=5,
                            padx=68, 
                            fill='x'
                            )
    

        self.remail_ent.bind("<Enter>",self.check_email_validity,add="+")
        self.remail_ent.bind("<Return>",self.check_email_validity,add="+")
        self.remail_ent.bind("<Leave>",self.check_email_validity,add="+")

        self.email_warning = ctk.CTkLabel(self,
                                            text="",
                                            text_color=self.warn_color,
                                            font=ctk.CTkFont(size=15)
                                            )
        self.email_warning.pack(side="top",
                                pady=5,
                                padx=68,
                                anchor="ne",
                                fill='x'
                                )


        self.passwd_lab = ctk.CTkLabel(self,
                                        text="Password",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=18
                                                        ),
                                        anchor="w"
                                                    
                                        ) 
        self.passwd_lab.pack(side="top", 
                                pady=20, 
                                padx=68, 
                                fill='x'
                                )


        self.rpasswd_ent = ctk.CTkEntry(self,
                                        placeholder_text="",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=20),
                                        show="."
                                        )
        self.rpasswd_ent.pack(side="top", 
                                pady=5, 
                                padx=68, 
                                fill='x'
                                )
        

        self.rpasswd_ent.bind("<Enter>",self.check_p_safety,add="+")
        self.rpasswd_ent.bind("<Return>",self.check_p_safety,add="+")
        self.rpasswd_ent.bind("<Leave>",self.check_p_safety,add="+")

        self.passwd_warning = ctk.CTkLabel(self,
                                            text = "",
                                            image = None,
                                            compound = "left"
                                            )
        self.passwd_warning.pack(side="top",
                                    fill="x",
                                    pady=5
                                    )



        self.conf_frame = ctk.CTkFrame(self,
                                        height=30,
                                        fg_color="transparent"
                                        )
        self.conf_frame.pack(side="top",
                                fill="x",
                                padx=68,
                                pady=20
                                )
        

        self.conf_passwd_lab = ctk.CTkLabel(self.conf_frame,
                                        text="Confirm Password",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=18
                                                        ),
                                        anchor="w"
                                                    
                                        ) 
        self.conf_passwd_lab.pack(side="left", 
                                pady=0, 
                                padx=0, 
                                fill='x'
                                )


        self.conf_label = ctk.CTkLabel(self.conf_frame,
                                        text="",
                                        )
        self.conf_label.pack(side="left",
                                padx=20
                                )


        self.rconf_passwd_ent = ctk.CTkEntry(self,
                                        placeholder_text="",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=20),
                                        show="."
                                        )
        self.rconf_passwd_ent.pack(side="top", 
                                pady=5, 
                                padx=68, 
                                fill='x'
                                )

        self.rconf_passwd_ent.bind("<Return>",self.check_pass,add="+")
        self.rconf_passwd_ent.bind("<Leave>",self.check_pass,add="+")

        self.push_btn = ctk.CTkButton(self, 
                                        text=self.btn_text,
                                        command=self.register_user
                                        )
        self.push_btn.pack(side="top", 
                            pady=20, 
                            padx=90
                            )



    def get_email_ent(self)-> str:
        return str(self.remail_ent.get())

    def get_passwd_ent(self)-> str:
        return str(self.rpasswd_ent.get())

    def get_conf_passwd_ent(self)-> str:
        return str(self.rconf_passwd_ent.get())


    def all_good_conf(self)-> bool:
        return self.email_flag and self.passwd_flag and self.passwd_conf_flag

    def undo_page_register(self): 
        print(self.master)  
        frame = Login(self.master)
        frame.pack(side="left",fill="both",expand=True)
        for wid in self.winfo_children():
            wid.pack_forget()
        self.pack_forget()


    def check_pass(self,event):
        print("checking password")
        if str(self.rconf_passwd_ent.get()) == "":
            None
        elif str(self.rpasswd_ent.get()) == str(self.rconf_passwd_ent.get()):
            self.passwd_conf_flag = True
            self.conf_label.configure(image=self.conf_img)
        else:
            self.conf_label.configure(image=self.deny_img)

    

    def check_p_safety(self,event):
        print(self.rpasswd_ent.get())
        passwd = str(self.rpasswd_ent.get())
        pass_safety = Password_Authentication(passwd)
        pass_safety = pass_safety.check_safety()

        
        match pass_safety:
            case "very_weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["very-weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" very weak !",
                                                text_color=self.warn_color,
                                                image = warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )
                
            case "weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" weak !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "good":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["good"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Good !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "excellent":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["excellent"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Excellent !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "large":
                # passwd_flag will remain False
                warn_img = ctk.CTkImage(Image_Objects["wow"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Too Large !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case _:
                # passwd_flag will remin False
                warn_img = ctk.CTkImage(Image_Objects["threat"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Security Threat !",
                                                text_color= self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )


    def check_email_validity(self,event):
        print(self.remail_ent.get())
        email = str(self.remail_ent.get())
        auth_email = Email_Authentication(email)
        response = auth_email.check_validity()

        match response:
            case "match":
                self.email_flag = True
                self.email_warning.configure(text="")
                
            case "invalid_domain_add":
                war_text = "x Invalid domain for the email!"
                self.email_warning.configure(text=war_text)
            
            case "invalid_local_add":
                war_text = "x Invalid local address for the email!"
                self.email_warning.configure(text=war_text)
                
            case "invalid_email":
                war_text = "x Invalid Email id!"
                self.email_warning.configure(text=war_text)
                
            case _:
                self.email_warning.configure(text="")




    def register_user(self):
        def reset_label():
            self.prompt_message.configure(text="",fg_color="transparent")

        if self.all_good_conf():
            print(self.get_email_ent())
            print(self.get_conf_passwd_ent())
            
            uid = self.get_email_ent()
            pswd = self.get_conf_passwd_ent()

            # TODO data base call

            try:
                with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv('database_name'),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                    if db.is_connected():
                        cursor=db.cursor()
                        sql_query="insert into user (id,ic,password,remember) values ('%s',%s,'%s','%s');" % (uid,b"",pswd," ")
                        cursor.execute(sql_query)
                        db.commit()
                        cursor.close()
                        notification = None
                        if notification == None or not notification.winfo_exists():
                            notification = Notification(app_name="Chat Application",
                                                        title="Conformation Info",
                                                        msg="Registration Successfull !",
                                                        duration=4,
                                                        icon=Icon_Objects['icon-live-chat'],
                                                        )
                            notification.toast()
                        else:
                            notification.focus()

                        self.undo_page_register()

            except Error as e:
                print(e)
                print("Error while registering!")
                print("prompting message")
                prompt_text = " -x- User Already Exists !!"
                self.prompt_message.configure(text=prompt_text,fg_color="grey35")
                # reset to new prompt label
                self.prompt_message.after(4000,reset_label)

        else:
            print("prompting message")
            prompt_text = " -x-  Check Invalid Entries !! "
            self.prompt_message.configure(text=prompt_text,fg_color="grey35")
            # reset to new prompt label
            self.prompt_message.after(4000,reset_label)


#====================================================================================================





class ChatEmail:
    def __init__(self,email_sender,email_sender_passwd,email_receiver,subject,body):
        self.email_sender=email_sender,
        self.email_passwd=email_sender_passwd,
        self.email_receiver=email_receiver,
        self.subject=subject
        self.body=body
        self.em = EmailMessage()

    def send(self):
        
        # generating email body
        self.em["From"] = self.email_sender
        self.em["To"] = self.email_receiver
        self.em["Subject"] = self.subject
        self.em.set_content(self.body)

        # preparing connection to send                
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp: 
            smtp.login(self.email_sender, self.email_passwd)
            
            # sending email
            smtp.sendmail(email_sender, email_receiver, em.as_string())


#===============================================================================




class Restore(ctk.CTkFrame):

    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)


        # setting up constant
        self.email_flag = False
        self.passwd_flag = False
        self.passwd_conf_flag = False   
        self.warn_color="#f5163f"  
        self.my_font = "TCMI____" 
        self.btn_text = "Create" 
        self.page_title = "Restore Password"
        self.back_btn = None
        self.otp = None
        self.otp_box = None
        self.otp_label = None
        self.submit_detail = None
        self.prompt_message = None
 
        

        # loading Images,icons
        self.back_img = ctk.CTkImage(Image_Objects["back"],size=(25,25))
        self.conf_img = ctk.CTkImage(Image_Objects["yes"], size=(25,25))
        self.deny_img = ctk.CTkImage(Image_Objects["remove"], size=(25,25))
        

        # Back button 
        self.hold_back_frame = ctk.CTkFrame(self,
                                            fg_color="transparent"
                                            )
        self.hold_back_frame.pack(side="top",
                                    pady=1,
                                    padx=1,
                                    fill='x'
                                    )


        self.back_btn = ctk.CTkButton(self.hold_back_frame,
                                    text="",
                                    width=20,
                                    hover_color="grey35",
                                    image=self.back_img,
                                    compound='left',
                                    fg_color="transparent",
                                    command=self.undo_page
                                    )
        self.back_btn.pack(side="top",
                            pady=0,
                            padx=0,
                            anchor="w"
                            )


        # prompt message area
        self.prompt_message = ctk.CTkLabel(self,
                                            text="",
                                            text_color="#bb55f2",
                                            font=ctk.CTkFont(size=15)
                                            )
        self.prompt_message.pack(side="top",
                                fill='x',
                                ipady=5,
                                ipadx=5
                                )


        # user page ui 
        self.page_title = ctk.CTkLabel(self,
                                    text=self.page_title, 
                                    justify="left",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=40
                                                    )
                                    )
        self.page_title.pack(side="top",
                        anchor="ne", 
                        pady=10, 
                        fill='x'
                        )


        self.email_lab = ctk.CTkLabel(self,
                                    text="Email",
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=18
                                                    ),
                                    anchor="w"
                                    ) 
        self.email_lab.pack(side="top", 
                            pady=17, 
                            padx=68, 
                            fill='x'
                            )


        self.email_ent = ctk.CTkEntry(self,
                                    placeholder_text="abcd@gmail.com",
                                    height=30,
                                    font=ctk.CTkFont(family=self.my_font,
                                                    size=17
                                                    )
                                    )
        self.email_ent.pack(side="top", 
                            anchor="ne", 
                            pady=5,
                            padx=68, 
                            fill='x'
                            )
    

        self.email_ent.bind("<FocusIn>",self.check_email_validity,add="+")
        self.email_ent.bind("<FocusOut>",self.check_email_validity,add="+")
        self.email_ent.bind("<Return>",self.check_email_validity,add="+")

        self.email_warning = ctk.CTkLabel(self,
                                            text="",
                                            text_color=self.warn_color,
                                            font=ctk.CTkFont(size=15)
                                            )
        self.email_warning.pack(side="top",
                                pady=5,
                                padx=68,
                                anchor="ne",
                                fill='x'
                                )


        self.passwd_lab = ctk.CTkLabel(self,
                                        text="Password",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=18
                                                        ),
                                        anchor="w"
                                                    
                                        ) 
        self.passwd_lab.pack(side="top", 
                                pady=20, 
                                padx=68, 
                                fill='x'
                                )


        self.passwd_ent = ctk.CTkEntry(self,
                                        placeholder_text="",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=20),
                                        show="."
                                        )
        self.passwd_ent.pack(side="top", 
                                pady=5, 
                                padx=68, 
                                fill='x'
                                )


        self.passwd_ent.bind("<FocusIn>",self.check_p_safety,add="+")
        self.passwd_ent.bind("<FocusOut>",self.check_p_safety,add="+")
        self.passwd_ent.bind("<Return>",self.check_p_safety,add="+")


        self.passwd_warning = ctk.CTkLabel(self,
                                            text = "",
                                            image = None,
                                            compound = "left"
                                            )
        self.passwd_warning.pack(side="top",
                                    fill="x",
                                    pady=5
                                    )



        self.conf_frame = ctk.CTkFrame(self,
                                        height=30,
                                        fg_color="transparent"
                                        )
        self.conf_frame.pack(side="top",
                                fill="x",
                                padx=68,
                                pady=20
                                )
        

        self.conf_passwd_lab = ctk.CTkLabel(self.conf_frame,
                                        text="Confirm Password",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=18
                                                        ),
                                        anchor="w"
                                                    
                                        ) 
        self.conf_passwd_lab.pack(side="left", 
                                pady=0, 
                                padx=0, 
                                fill='x'
                                )


        self.conf_label = ctk.CTkLabel(self.conf_frame,
                                        text="",
                                        )
        self.conf_label.pack(side="left",
                                padx=20
                                )


        self.conf_passwd_ent = ctk.CTkEntry(self,
                                        placeholder_text="",
                                        font=ctk.CTkFont(family=self.my_font,
                                                        size=20),
                                        show="."
                                        )
        self.conf_passwd_ent.pack(side="top", 
                                pady=5, 
                                padx=68, 
                                fill='x'
                                )


        self.conf_passwd_ent.bind("<FocusIn>",self.check_pass,add="+")
        self.conf_passwd_ent.bind("<FocusOut>",self.check_pass,add="+")
        self.conf_passwd_ent.bind("<Return>",self.check_pass,add="+")
        self.conf_passwd_ent.bind("<Leave>",self.check_pass,add="+")

        self.push_btn = ctk.CTkButton(self, 
                                        text=self.btn_text,
                                        command = self.reset_passwd 
                                        )
        self.push_btn.pack(side="top", 
                            pady=20, 
                            padx=90
                            )


    def get_otp_ent(self)-> str:
        return str(self.otp_box.get())

    def get_email_ent(self)-> str:
        return str(self.email_ent.get())

    def get_passwd_ent(self)-> str:
        return str(self.passwd_ent.get())

    def get_conf_passwd_ent(self)-> str:
        return str(self.conf_passwd_ent.get())
       
    def all_good_conf(self)-> bool:
        return self.email_flag and self.passwd_flag and self.passwd_conf_flag

    def check_pass(self,event):
        print("checking password")
        if str(self.conf_passwd_ent.get()) == "":
            None
        elif str(self.passwd_ent.get()) == str(self.conf_passwd_ent.get()):
            self.passwd_conf_flag = True
            self.conf_label.configure(image=self.conf_img)
        else:
            self.conf_label.configure(image=self.deny_img)

    

    def check_p_safety(self,event):
        print(self.passwd_ent.get())
        passwd = str(self.passwd_ent.get())
        pass_safety = Password_Authentication(passwd)
        pass_safety = pass_safety.check_safety()

        
        match pass_safety:
            case "very_weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["very-weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" very weak !",
                                                text_color=self.warn_color,
                                                image = warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )
                
            case "weak":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["weak"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" weak !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "good":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["good"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Good !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "excellent":
                self.passwd_flag=True
                warn_img = ctk.CTkImage(Image_Objects["excellent"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Excellent !",
                                                text_color="green",
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case "large":
                # passwd_flag will remain False
                warn_img = ctk.CTkImage(Image_Objects["wow"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Too Large !",
                                                text_color=self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )

            case _:
                # passwd_flag will remin False
                warn_img = ctk.CTkImage(Image_Objects["threat"],
                                        size=(25,25)
                                        )
                self.passwd_warning.configure(text=" Security Threat !",
                                                text_color= self.warn_color,
                                                image=warn_img,
                                                font=ctk.CTkFont(size=15)
                                                )


    def check_email_validity(self,event):
        print(self.email_ent.get())
        email = str(self.email_ent.get())
        auth_email = Email_Authentication(email)
        response = auth_email.check_validity()

        match response:
            case "match":
                self.email_flag = True
                self.email_warning.configure(text="")
                
            case "invalid_domain_add":
                war_text = "x Invalid domain for the email!"
                self.email_warning.configure(text=war_text)
            
            case "invalid_local_add":
                war_text = "x Invalid local address for the email!"
                self.email_warning.configure(text=war_text)
                
            case "invalid_email":
                war_text = "x Invalid Email id!"
                self.email_warning.configure(text=war_text)
                
            case _:
                self.email_warning.configure(text="")


    
    def send_otp(self,otp,receiver):
        print("otp sending method")
        email_sender=os.getenv("email_sender")
        email_passwd=os.getenv("email_passwd")
        subject = "Password Recovery Verification from ChatApp"
        body=f"""
        ChatApp received a request for password recovery\n
        Use this code to finish setting up this password recovery process: {otp}\n
        If you don't recognize, you can ignore this email.
        """
        ChatEmail(email_sender,email_passwd,receiver,subject,body)


    def reset_passwd(self):
        # otp prompting for otp
        if self.all_good_conf():

            if (self.otp_label == None and self.otp_box == None) or\
            (not self.otp_label.winfo_exists() and not self.otp_box.winfo_exists()):
                
                print("request to reset password")
                self.otp = random.randint(000000,999999)
                print(self.otp)

                # sending email to user
                self.send_otp(self.otp,self.get_email_ent())

                self.otp_label = ctk.CTkLabel(self,
                                                text="OTP",
                                                anchor="w",
                                                font=ctk.CTkFont(family=self.my_font,
                                                                size=18
                                                                )
                                                )
                self.otp_label.pack(side="top",
                                    pady=10,
                                    padx=68,
                                    fill='x'
                                    )


                self.otp_box = ctk.CTkEntry(self)
                self.otp_box.pack(side="top",
                                pady=0,
                                padx=68,
                                fill='x'    
                                )

                self.submit_detail=ctk.CTkButton(self,
                                                    text="Submit",
                                                    command=self.restore_passwd
                                                    )
                self.submit_detail.pack(side="top",
                                        pady=5,
                                        padx=90
                                        )

        else:
            def reset_label():
                self.right_container.prompt_message.configure(text="",
                                                            fg_color="transparent"
                                                            )
            print("prompting message")
            prompt_text = " -x-  Check Invalid Entries !! "
            selfprompt_message.configure(text=prompt_text,
                                                        fg_color="grey35"
                                                        )
            # reset to new prompt label
            self.prompt_message.after(4000,reset_label)


    def undo_page(self):   
        frame = Login(self.master)
        frame.pack(side="left",fill="both",expand=True)
        for wid in self.winfo_children():
            wid.pack_forget()
        self.pack_forget()


    def restore_passwd(self):
        def reset_label():
                self.prompt_message.configure(text="",
                                            fg_color="transparent"
                                                )          
        if self.all_good_conf():
            print(self.get_email_ent())
            print(self.get_conf_passwd_ent())
            print(self.get_otp_ent())

            if self.get_otp_ent() == "":
                print("empty otp")
                print("prompting message under login restoration checking otp box")
                prompt_text = " -x-  Enter OTP, send on registered email  !! "
                self.prompt_message.configure(text=prompt_text,
                                                            fg_color="grey35"
                                                            )
                # reset to new prompt label
                self.prompt_message.after(4000,reset_label)



            elif self.otp == int(str(self.get_otp_ent())):
                print("Your password has been successfully restored")
                if self.all_good_conf():
                    # TODO database call


                    #############################
                    ############################
                    #########################
                    self.undo_page()
                    notification = Notification(app_name="Chat Application",
                                                title="Conformation Info",
                                                msg="Password Restoration Successfull !",
                                                duration=4,
                                                icon=Icon_Objects['icon-live-chat'],
                                                )
                    notification.toast()


                else:
                    print("prompting message under login restoration checking otp box")
                    prompt_text = " -x-  Check Invalid Entries  !! "
                    self.prompt_message.configure(text=prompt_text,
                                                                fg_color="grey35"
                                                                )
                    # reset to new prompt label
                    self.prompt_message.after(4000,reset_label)


        else:
            print("prompting message under login restoration")
            prompt_text = " -x-  Check Invalid Entries !! "
            self.prompt_message.configure(text=prompt_text,
                                                        fg_color="grey35"
                                                        )
            # reset to new prompt label
            self.prompt_message.after(4000,reset_label)

#======================================================================================================



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Constant setting up
        self.title("Chat Application")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.state("zoomed")

        # loading background image
        self.bg_img = ctk.CTkImage(Image_Objects["chat"],size=(900,777))
           
        # pre defined Left Container class 
        self.left_container = Login_Image_Container(self, 
                                            image=self.bg_img,
                                            corner_radius=0, 
                                            )
        self.left_container.pack(side="left", 
                                    fill="y", 
                                    pady=0, 
                                    padx=0
                                    )

        # right container for user interaction
        # loading predefind login page ui

        self.right_container_body=ctk.CTkFrame(self)
        self.right_container_body.pack(side="left",
                                        fill="both",
                                        expand=True
                                        )
        self.right_container = Login(self.right_container_body,leftContainer=self.left_container, corner_radius=0)
        self.right_container.pack(side="left", 
                                    fill="both", 
                                    expand=True
                                    )


        
    
if __name__ == "__main__":


    # def main_app():
    #     ctk.set_appearance_mode("dark")
    #     app = App()
    #     app.mainloop()

    # def supp_server():
    #     s = Server()
    #     s.run()

    
    # Thread(target = main_app).start
    # Thread(target = supp_server).start

    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()