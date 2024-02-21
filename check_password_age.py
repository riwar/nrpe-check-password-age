#!/usr/bin/env python
import argparse
import subprocess
import datetime
import sys
import pwd

def main():
    args = parse_cmd_line()
    
    found,status,msg = check_user(args.user)
    
    if found:
        pwinfo = get_pw_info(args.user)
        last_pw_change_date = get_last_change(pwinfo)
        today = current_date()
        days_since_change = get_days_since_change(today,last_pw_change_date)
        status, msg = check_age(args.user,days_since_change,args.warning,args.critical)

    print(msg)
    sys.exit(status)

def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Check last time a user changed it's password")
    parser.add_argument('-c', '--critical',default=110,type=int)
    parser.add_argument('-w', '--warning',default=90,type=int)
    parser.add_argument('-u', '--user',default="root",type=str)

    args = parser.parse_args()
    check_args(args)
    return args

def check_args(args):
    if args.warning >= args.critical:
        msg = "INFO: waring {} is set higher then critical {}".format(args.warning,args.critical)
        print(msg,file=sys.stderr)

def check_user(user):
    found = user_exists(user)
    if not found:
        msg = "UNKNOWN: No user with name {} found on system".format(user)
        status = 3
    else:
        msg = ""
        status = 0

    return found,status,msg
    
def user_exists(user):
    try: 
        pwd.getpwnam(user)
        found = True
    except KeyError:
        found = False
    
    return found
        
def current_date():
    return datetime.datetime.today()

def get_pw_info(user):
    command = ["/usr/bin/passwd",user,"-S"] 
    output = subprocess.run(command,capture_output=True)
    output.check_returncode()
    return output.stdout

def get_last_change(pwinfo):
    pwinfo = pwinfo.decode("UTF-8")
    pwinfo = pwinfo.split(" ")
    last_change = pwinfo[2]
    return parse_last_change(last_change)

def parse_last_change(last_change):
    return datetime.datetime.strptime(last_change,"%Y-%m-%d")

def get_days_since_change(today,last_change):
    delta = today - last_change
    return delta.days

def check_age(user,days_since_change,warning,critical):
    if critical <= days_since_change:
        status = 2
        msg = "Critical: {} password not changed in {} days".format(user,critical)
    elif warning <= days_since_change:
        status = 1
        msg = "Warning: {} password not changed in {} days".format(user,warning)
    else: 
        status = 0
        msg = "OK!"

    return status,msg

if __name__ == "__main__":
    main()