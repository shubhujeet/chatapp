
# ChatApp

A simple chat application model build using python.


## Features

- Use (CTRL+TAB) to get recomendation
- Use Right-Click to open opts available on User Logo, Contacts, Messages
- Use (CTRL+Enter) shorcut key to send messages 
- User can add profile image which will auto crop in elliptical shape
- Authentication and Authoration is implemented
- AES Encryption is used to encrypt Chat messages
- OTP will be send on registered email for restoring passwd
- Remember me helps to quick login process is enabled
- User can add user in his contact using id which another user is registered on app
- Before running the program server.py needs to be run to show recommendation(recomendation is just sample not implemented  using ML)



## Screenshots




## Info

The main file to run the application is chatapp.py,
The server file needs to be run using diffent shell to get recommendation.

Email: abcd@gmail.com
 
    Local Address checking specification
    -abcd => local address
    -gmail.com => domain address

    -checks local address not start with "." nor end with "." 
    -there should no ".." two continuous sequence of "." dot
    -any special character from the given character set as [!#$%&'*+/=?`{|}~^-]
   
    Domain Address checking specification
    -checks domain should not start with "-" nor end with "-"
    -ending domain name should have atleast 2-6 characters only from the english alphabet
    -there is no special character allowed in domin other than "-","."
    -also two "." dot are not supported yet

Password: <your password>
 
    -Password should be >= 5 character
    -It should be <= 20

### Password Restoration:

At the time of password Restoration eamil will be send to registered email id but error handling if email id does not exist is not implemented yet

### .env
    email_sender  = <email_from_which_chat_app_will_send_emai>
    email_passwd  = <app_password_generated_from_above_gmail_ac>
    host_name     = <localhost> or <your_prefered_host>
    database_name = <database_name_where_chat_app_will_store_data>
    user_name     = <database_login_user_id>
    passwd_db     = <database_access_pwd>
