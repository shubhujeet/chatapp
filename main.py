import os
from tkinter  import Menu
import customtkinter as ctk
from asset import Image_Objects,Icon_Objects
from tkinter import *
import mysql.connector
from mysql.connector import Error
from encrypt import AES_Encryption
import numpy as np
from PIL import Image, ImageDraw
from chatNotification import Notification
from tkinter.filedialog import askopenfilename
from dotenv import load_dotenv
import socket
from subprocess import Popen
import sys


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
    def __init__(self,log_user,email,icon,passwd=None,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.log_user = log_user
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

            with open(locald,"rb") as file:
                data = file.read()
                print(len(data))
                try:
                    with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:
                        if db.is_connected():
                            cursor = db.cursor()
                            # TODO update query change
                            print(type(self.email))
                            cursor.execute("""update user set ic = %s where id=%s""",(data,self.email))
                            db.commit()
                            cursor.close()

                            notification = Notification(app_name="ChatApp",
                                                        title="Info",
                                                        msg = "Reopen the app to load Profile Icon!",
                                                        duration=4,
                                                        icon=Image_Objects["user"]
                                                        )
                            notification.toast()



                except Error as e:
                    print("Error while updating icon to database ProfilePage:",e)

            

# class for adding new contact who have an account in chatapp

class AddUser(ctk.CTkToplevel):
    def __init__(self,master,CF,bt,*args,**kwargs):
        super().__init__(master,*args,**kwargs)

    
        self.CF = CF
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
                        cursor.execute("""insert into contact(cid,cic,cname) values(%s,%s,%s)""",(email,u_icon,u_name))
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
        self.h_var = 50
        bimg = None

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
                                    text=" Shubhujeet",
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
        with mysql.connector.connect(host=os.getenv("host_name"),database=os.getenv("database_name"),user=os.getenv("user_name"),password=os.getenv("passwd_db")) as db:

            if db.is_connected():
                cursor=db.cursor()
                cursor.execute("""select * from contact""")
                my_contacts = cursor.fetchall()
                cursor.close()

        
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
        au = AddUser(self,self.leftFrame,bt = self.add_user_btn,fg_color="grey20")

    def log_out_window(self,event):
        
        pdir = os.path.dirname(__file__)
        pext = os.path.join(pdir,"Scripts","python.exe")
        
        Popen([pext,"main.py"])
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
                print(r_icon)
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

        pp = ProfilePage(self.log_user,email,icon,password,fg_color="grey20")


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
        self.h_var = self.h_var = self.h_var - 25 if self.h_var > 25 else 25
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
            
            print(pic)
            self.chat_Frame.add_chat(m_id=my_chats[i][0],msg=decrypted_text,contact_user=my_chats[i][1],icon=pic)


        # setting up message Frame
        
        self.messageFrame.pack(side="bottom",fill="x", anchor='s',ipady=8,ipadx=5)

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




if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    f = Chat_App(app,"abcd@gmail.com")
    f.pack(fill='both',expand=True)
    app.mainloop()  