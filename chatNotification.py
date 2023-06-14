import customtkinter as ctk
from playsound import playsound
from time import sleep
import os
from asset import Icon_Objects,Image_Objects

# loading dll directories to avoid dll not found error
os.add_dll_directory(os.getcwd())

# icon accept Image object from Image.open
class Notification(ctk.CTkToplevel):

    def __init__(self,
                app_name,
                title,
                msg,
                duration,
                icon,
                *arg,
                **kwargs
                ):
        super().__init__(*arg,**kwargs)
        
        # setting const
        self.app_name = app_name
        self.title=title
        self.msg=msg
        self.duration=duration
        self.icon=icon
        self.geometry("+%d+%d"%(600,300))

        

    def toast(self):
        
        self.wm_overrideredirect(True)

        self.frame=ctk.CTkFrame(self,fg_color="#020c1c")
        self.frame.pack(pady=0,
                        padx=0,
                        fill="both"
                        )

        
        self.app_name_frame = ctk.CTkFrame(self.frame,fg_color='grey35')
        self.app_name_frame.pack(fill="x",expand=True)

        # icon box
        ic_img = ctk.CTkImage(Icon_Objects["icon-live-chat"])
        self.icon_lab = ctk.CTkLabel(self.app_name_frame,
                                    text="",
                                    image=ic_img
                                    )
        self.icon_lab.pack(side="left",
                            padx=10,
                            anchor="n",
                            fill='x'
                            )


        # app name 
        self.app_lab = ctk.CTkLabel(self.app_name_frame,
                                    text=self.app_name,
                                    anchor="w",
                                    font=ctk.CTkFont(family="ERASMD",size=15)
                                    )
        self.app_lab.pack(side='left',
                            padx=10,
                            anchor="n",
                            fill='x'
                            )

        # closing icon
        close_img = ctk.CTkImage(Image_Objects["remove"],size=(25,25))
        self.close_lab = ctk.CTkLabel(self.app_name_frame,
                                    text="",
                                    image = close_img,
                                    )
        self.close_lab.pack(side="right",
                            padx=5,
                            pady=1,
                            anchor="e",
                            fill='x'
                            )
        self.close_lab.bind("<Button-1>",self.close)


        

        # title box
        self.title_lab=ctk.CTkLabel(self.frame,
                                text=self.title,
                                anchor="w",
                                font=ctk.CTkFont(weight="bold",
                                                family="ERASBD",
                                                size=15)
                                )
        self.title_lab.pack(fill='x',padx=17)

        
        # message box
        self.msg_lab = ctk.CTkLabel(self.frame,
                                    text=self.msg,
                                    fg_color="grey24",
                                    anchor="center",
                                    font=ctk.CTkFont(family="ERASLGHT",size=13),
                                    corner_radius=50
                                    )
        self.msg_lab.pack(fill="both",
                        ipady=5,
                        ipadx=5,
                        pady=3,
                        padx=10
                        )

        
        # close the window once the time is up
        cur_dir = os.path.dirname(__file__)
        paths = os.path.join(cur_dir,"music","pop-notification.mp3")
        paths = paths.split("\\")
        paths = "\\\\".join(paths)
        try:
            playsound(paths)
        except:
            try:
                playsound(paths)
            except:
                print("Sound is not playing!")
        
        self.after(self.duration*1000,self.destroy)

    def close(self,event):
        self.destroy()

if __name__ == "__main__":

    app = ctk.CTk()
    
    
    def notify():
        notification = Notification(app,app_name="Chat Applcation",
                                    title="Conformation Info",
                                    msg="Password Restoration Successful !",
                                    duration=4,
                                    icon=Icon_Objects["icon-live-chat"]
                                    )
        notification.toast()
       

    btn = ctk.CTkButton(app,command=notify)
    btn.pack()


    app.mainloop()