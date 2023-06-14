import re

class Email_Authentication:

    def __init__(self,email):
        self.email = email
        self.ret_opt = ["match","invalid_email","invalid_domain_add","invalid_local_add"]

    def check_validity(self)-> str:
        email_val = self.email.split("@")
        if len(email_val)== 2:
            local_add, domain_add = email_val
            
            # checks local address not start with "." nor end with "." it could have
            # there should no ".." two continuous sequence of "." dot
            # any special character from the given character set as [!#$%&'*+/=?`{|}~^-]
            
            local_add_pat = "\A([\w\d!#$%&'*+/=?`{|}~^-])+(?:\.[\w\d!#$%&'*+/=?`{|}~^-]+)*"
            
            # checks domain should not start with "-" nor end with "-"
            # ending domain name should have atleast 2-6 characters only
            # from the english alphabet
            # there is no special character allowed in domin other than "-","."

            domain_add_pat = "((\A([a-zA-Z0-9])+(?:-[a-zA-Z0-9]+)*)+\.)+[A-Za-z]{2,6}\Z"

            if re.fullmatch(local_add_pat,local_add): 
                if re.fullmatch(domain_add_pat,domain_add):
                    return "match"
                    
                else:
                    return "invalid_domain_add"
            else:
                return "invalid_local_add"
                
        else:
            return "invalid_email"


class Password_Authentication:

    def __init__(self,passwd):
        self.passwd = passwd
        self.opt = [{"very_weak":"5-7"},{"weak":"8-10"},{"good":"11-13"},{"excellent":"14-20"},{"large":"more than 20"},{"short":"less than 5"}]
    
    def check_safety(self)-> str:

        self.passwd_len = len(self.passwd)

        if self.passwd_len == 5 or ( self.passwd_len > 5 and self.passwd_len < 8):
            return "very_weak"

        elif self.passwd_len == 8 or (self.passwd_len > 8 and self.passwd_len < 11):
            return "weak"
        
        elif self.passwd_len == 11 or (self.passwd_len > 11 and self.passwd_len <14):
            return "good"
        
        elif self.passwd_len == 14 or (self.passwd_len > 14 and self.passwd_len <=20):
            return "excellent"
        
        elif self.passwd_len > 20:
            return "large"
        
        else:
            return "short"

    def available_opt(self)-> list:
        return self.opt