import time
import hashlib
import re

class Auth:
    def __init__(self, uname, passwd):
        self.uname = uname
        self.passwd = passwd
        self.banned = False
        self.rl = 0
        self.btime = 0
    
    def setpass(self, password):
        self.passwd = password

    def ban(self):
        self.btime = time.time()
        self.banned = True

    def unban(self):
        self.rl = 0
        self.banned = False

    def login(self, user, password):
        now = time.time()
        if(self.banned and (now - self.btime) >= 300):
            self.unban()
        if(user == ""):
            raise NameError("Username cannot be empty")
        if(password == ""):
            raise NameError("Password cannot be empty")
        hpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if(user == self.uname and hpassword == self.passwd):
            return
        if(user != self.uname or hpassword != self.passwd):
            if(self.rl >= 5 and self.banned == False):
                self.ban()
                raise NameError("5 invalid tries detected, account locked out. Try again in 5 minutes")
            self.rl += 1
            raise NameError("Invalid username or password")

    def change(self,oldpass, newpass, cnewpass,hashed):
        holdpass = hashlib.sha256(oldpass.encode('utf-8')).hexdigest()
        a = self.passwd
        if(oldpass == newpass):
            raise NameError("Old password cannot be the same as new password")
        if(oldpass == ""):
            raise NameError("Old password cannot be empty")
        if(newpass == ""):
            raise NameError("New password cannot be empty")
        if(cnewpass == ""):
            raise NameError("Confirm new password cannot be empty")
        if(holdpass != a):
            raise NameError("Incorrect old password")
        elif(newpass != cnewpass):
            raise NameError("Passwords do not match")
        elif(not (self.pol(newpass))):
            raise NameError("Password should be 6-20 chars long with upper and lower case characters and special characters")
        elif(holdpass == a):
            self.setpass(hashed)
            return
    
    def pol(self, password):
        return re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", password)
