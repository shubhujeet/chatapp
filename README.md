
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

![Screenshot (1005)](https://github.com/shubhujeet/chatapp/assets/92719242/c386d79c-579a-4ec5-a45b-eea43ff5bd7f)
Login Page

![Screenshot (1009)](https://github.com/shubhujeet/chatapp/assets/92719242/10f4d888-be04-4ad1-8834-d3f7bad79d29)
Home Page

![Screenshot (1010)](https://github.com/shubhujeet/chatapp/assets/92719242/10ab0b90-c4d1-4708-8ff5-12192e13c889)
Adding user to our contact list

![Screenshot (1012)](https://github.com/shubhujeet/chatapp/assets/92719242/bcc8c265-eb6f-4866-8065-054c7800643d)
Sending message to contact

![Screenshot (1015)](https://github.com/shubhujeet/chatapp/assets/92719242/f608866f-4f08-4493-9cfe-ae7dfe95324a)
Right-Clcik to see avalable option on messages

![Screenshot (1016)](https://github.com/shubhujeet/chatapp/assets/92719242/88c8d8f2-9232-4a5d-b0c3-9deebefa3197)
Right-Click on the uses label to see user profile

![Screenshot (1017)](https://github.com/shubhujeet/chatapp/assets/92719242/dec4519d-3d9a-4c33-86da-d059bc5ebebd)
Successfully Profile icon change

![Screenshot (1019)](https://github.com/shubhujeet/chatapp/assets/92719242/85d1fe1e-7886-45c2-88e7-e18a908922a2)
Right-click to see contact person profile

![Screenshot (1020)](https://github.com/shubhujeet/chatapp/assets/92719242/11c24091-e400-462e-b3fb-60438768684a)
Message via another user account



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

At the time of password Restoration email will be send to registered email id but error handling if email id does not exist is not implemented yet

### .env
    email_sender  = <email_from_which_chat_app_will_send_emai>
    email_passwd  = <app_password_generated_from_above_gmail_ac>
    host_name     = <localhost> or <your_prefered_host>
    database_name = <database_name_where_chat_app_will_store_data>
    user_name     = <database_login_user_id>
    passwd_db     = <database_access_pwd>
