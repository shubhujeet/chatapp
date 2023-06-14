import random
from time import sleep
import customtkinter as ctk
from chatNotification import Notification
from authentication import Email_Authentication,Password_Authentication
from asset import Image_Objects,Icon_Objects
import mysql.connector 
from mysql.connector import Error

import mysql.connector
from mysql.connector import Error


class Login(ctk.CTkFrame):

    def __init__(self,master,**kwargs):
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
        self.email_ent.insert(0,"ghoshshubhujeet@gmail.com")
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
        self.passwd_ent.insert(0,"12341234")


        self.passwd_ent.bind("<FocusIn>",self.check_p_safety,add="+")
        self.passwd_ent.bind("<FocusOut>",self.check_p_safety,add="+")
        self.passwd_ent.bind("<Return>",self.check_p_safety,add="+")
        self.passwd_ent.bind("<Leave>",self.check_p_safety,add="+")


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



    def get_login_email_ent(self):
        return str(self.email_ent.get())

    def get_login_passwd_ent(self):
        return str(self.passwd_ent.get())

    def get_isRemember(self):
        return str(self.check_box.get())


    def all_good_conf(self):
        return self.email_flag and self.passwd_flag

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

    def register_user(self,event):
        print("register")
        pass
        # container = Registration_Form(self.master)
        # container.pack(side="left",
        #                             fill="both",
        #                             expand=True
        #                             )
        # for wid in self.winfo_children():
        #     wid.destroy()
        # self.destroy()




    def restore_passwd(self,event):
        print("restore")
        pass
        # container = Restore(self.master)
        # container.pack(side="left", 
        #                             fill="both", 
        #                             expand=True
        #                             )

        # for wid in self.winfo_children():
        #     wid.destroy()
        # self.destroy()



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

            # TODO database call
            try:
                with mysql.connector.connect(host="localhost",database="chatapp",user="root",password="shubhu") as db:
                    
                    if db.is_connected():
                        cursor=db.cursor()
                        cursor.execute("select id,password,remember from user_login where id = '%s';" % uid)
                        record = cursor.fetchone()
                        print(record)
                        if record != None:
                            if record[0] == uid:
                                print("match")
                                print(rem)
                                cursor.execute("update user_login set remember='%s' where id='%s';" % (rem,uid))
                                print("rem update successful!")
                                db.commit()
                                cursor.execute("select * from user_login where id = '%s';" % uid)
                                rec = cursor.fetchone()
                                cursor.close()
                                print(rec)

                                notification = Notification(self,
                                                            app_name="Chat Application",
                                                            title="Conformation Info",
                                                            msg="Login Successfull !",
                                                            duration=4,
                                                            icon=Icon_Objects['icon-live-chat'],
                                                            )
                                notification.toast()
                            else:
                               
                                print("prompting message")
                                prompt_text = " -x-  No Such User, Register Now !! "
                                self.prompt_message.configure(text=prompt_text,
                                                            fg_color="grey35"
                                                            )
                                # refresh after 4 sec
                                self.prompt_message.after(4000,reset_label)





                        else:
                            
                            print("prompting message")
                            prompt_text = " -x-  No Such User, Register Now !! "
                            self.prompt_message.configure(text=prompt_text,
                                                        fg_color="grey35"
                                                        )
                            # refresh after 4 sec
                            self.prompt_message.after(4000,reset_label)


            except Error as e:
                print(e)
           
                print("prompting message")
                prompt_text = " -x-  No Such User, Register Now !! "
                self.prompt_message.configure(text=prompt_text,
                                            fg_color="grey35"
                                            )
                # refresh after 4 sec
                self.prompt_message.after(4000,reset_label)




        else:
            print("prompting message")
            prompt_text = " -x-  Check Invalid Entries !! "
            self.prompt_message.configure(text=prompt_text,
                                        fg_color="grey35"
                                        )
            # refresh after 4 sec
            self.prompt_message.after(4000,reset_label)




if __name__ == "__main__":
    
    app = ctk.CTk()
    f = Login(app)
    f.pack()

    app.mainloop()