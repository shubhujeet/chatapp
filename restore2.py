import customtkinter as ctk
from asset import Image_Objects,Icon_Objects
from authentication import Email_Authentication,Password_Authentication
import re
import mysql.connector
from mysql.connector import Error
import random
from chatNotification import Notification


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
                                    fg_color="transparent"
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
        self.email_ent.insert(0,"abcd@gmail.com")
    

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
        self.conf_passwd_ent.insert(0,"12341234")


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


    
    def send_otp(self):
        print("otp sending method")
        pass

    def reset_passwd(self):
        # otp prompting for otp
        if self.all_good_conf():

            if (self.otp_label == None and self.otp_box == None) or\
            (not self.otp_label.winfo_exists() and not self.otp_box.winfo_exists()):
                
                print("request to reset password")
                self.otp = random.randint(000000,999999)
                print(self.otp)

                # TODO send email

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
        pass
        # self.right_container = Login(self.master)
        # self.right_container.pack(side="left",
        #                             fill="both",
        #                             expand=True
        #                             )
        # self.destroy()


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
                    notification = Notification(self,
                                                app_name="Chat Application",
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




if __name__ == "__main__":

    app = ctk.CTk()
    r = Restore(app)
    r.pack()

    app.mainloop()