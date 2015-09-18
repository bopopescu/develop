import os

account_file = "account.txt"
lock_file = "lock.txt"



def is_locked():
    flag_locked = False
    if os.path.exists(lock_file):
        fp = open(lock_file, "r")
        lock_list = fp.readlines().strip()
        fp.close()
        if username in lock_list:
            flag_locked = True
            print "Sorry, your username is already locked!"
    return flag_locked

def check_login(username):
    flag = False
    if os.path.exists(account_file):
        fp = open(account_file, "r")
        account_list = fp.readlines()
        fp.close()
        for each_line in account_list:
            each_line = each_line.strip()
            if username == each_line.split(" ")[0]:
                for i in xrange(3):
                    password = raw_input("password: ")
                    if password == each_line.split(" ")[1]:
                        flag = True
                        break
                    if i == 2:
                        print "locked"
                
            else:
                print "username is incorrent"
    return flag

            

def main():
    username = raw_input("username: ")
    flag_locked = is_locked()
    if flag_locked:
        return
    flag = check_login(username)
    if flag:
        print "login success"

if __name__ == "__main__":
    main()
