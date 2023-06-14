from PIL import Image


# dictionary for storing image object
objects = {}
ic_objects = {}

# listing required images
image_assets = (
    ("chat"   ,     ".\\images\\chat.jpg"),
    ("remove" ,     ".\\images\\remove.png"),
    ('yes'    ,     ".\\images\\yes.png"),
    ('eye'    ,     ".\\images\\eyeImg2.png"),
    ("back"   ,     ".\\images\\back.png"),
    ("threat" ,     ".\\images\\threat.png"),
    ('very-weak',   ".\\images\\very-weak.png"),
    ("weak"   ,     ".\\images\\weak.png"),
    ("good"   ,     ".\\images\\good.png"),
    ("excellent",   ".\\images\\excellent.png"),
    ("wow"    ,     ".\\images\\wow.png"),
    ("live-chat",   ".\\images\\wow.png"),
    ("send-message",".\\images\\send-message.png"),
    ("add-user"    ,".\\images\\add-user.png"),
    ("bin"         ,".\\images\\bin.png"),
    ("encript"     ,".\\images\\encript.png"),
    ("email"       ,".\\images\\email.png"),
    ("passwd"      ,".\\images\\passwd.png"),
    ("add-photo"   ,".\\images\\add-photo.png"),
    ("visible"     ,".\\images\\visible.png"),
    ("not-visible" ,".\\images\\not-visible.png"),
    ("user"        ,".\\images\\user.png"),
    ("welcome"     ,".\\images\\welcome.png"),
    ("logout"      ,".\\images\\logout.png")
    )


# icon assets
icon_assets = (
    ("icon-user"     ,   ".\\images\\icon-user.ico"),
    ("icon-live-chat",   ".\\images\\icon-live-chat.ico")
)


# loading images
for name,img in image_assets:
    objects[name] = Image.open(img)    


# loading icons
for ic_name,ic in icon_assets:
    ic_objects[ic_name] = Image.open(ic)

# Image Object tuple
Image_Objects = objects

# Icon Object tuple
Icon_Objects = ic_objects
