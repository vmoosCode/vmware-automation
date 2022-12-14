import os
import paramiko as pm
from getpass import getpass
import argparse
from  tabulate import tabulate
import json

os.system('clear')


"""
script that make you control vms power directly from ESXi host through SSH connecton using paramiko
This could be usefull to power lab vms, .. etc
this usefull for learning and for home use.
"""


def getargs():
    parser = argparse.ArgumentParser(description="Just an example",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--esxi")
    parser.add_argument("-u", "--username")
    args = parser.parse_args()

    # password = getpass('password: ')
    # config['password'] = password
    config = vars(args)
    config['password'] = 'P@ssw0rd'
    return config

def load_profiles():
    with open('profiles.json','r') as f:
        read = f.read()
        profiles = json.loads(read)
    f.close()
    return profiles

def loadvmsfromfile():
    pass

def connect(ip,user,password):
    port= 22
    ssh = pm.SSHClient()
    ssh.set_missing_host_key_policy(pm.AutoAddPolicy())
    ssh.connect(ip,port,user, password)
    return ssh
    
def getallvms(conn):
    stding, stdout, stderr = conn.exec_command('vim-cmd vmsvc/getallvms')
    lines = stdout.readlines()
    # vms dict keys represebt vm name, and the value represent vm ID 
    vms = {} 
    for line in lines:
        l = line.split()
        vms[l[1]] = l[0]
    with open('vms.txt','w') as f:
        f.write(json.dumps(vms))
    return vms

def toggleProfile(conn,profile_name):
    profiles = load_profiles()
     
def select_profile():
    profiles = load_profiles()
    for index, profile in enumerate(profiles):
        print(index, profile)

def profile_creator(list_of_vms_ids, profile_name):
    # load vms 
    with open('vms.txt','r') as f:
        vms = f.read()
        stored_json = json.loads(vms)
    f.close()

    profiles = {}
    validated_ids = []
    for vm in list_of_vms_ids:
        if vm in stored_json.values():
            validated_ids.append(vm)
        else:
            return f"this ID is not valid {vm}"
    with open('profiles.json','r') as j:
        loaded_profiles = j.read()
        profiles_json = json.loads(loaded_profiles)
        j.close()
    profiles[profile_name] = validated_ids
    p = [profile_name,validated_ids]
    profiles_json.update(p)
    with open('profiles.json','a') as f:
        f.write(json.dumps(profiles))
    f.close()
    return 1 

if __name__=="__main__":
    load_profiles()
    args = getargs()
    # print(args['esxi'])
    # print(args['username'])
    # print(args['password'])
    conn = connect(args['esxi'],args['username'],args['password'])
    allvms = getallvms(conn)
    print('Discovered VMs \n')
    vms_table=  []
    for vm in allvms:
        if vm != 'Name':
            vms_table.append([vm,allvms[vm]])
    print(tabulate(vms_table, headers=['Name', 'ID']))
    print('---------------------------------------')
    print('\n 1- Create new environment \n 2- Toggle Environment \n 3-Exit \n ')
    selection = input('Selection: ')

    if selection == "1":
        print('Lets Create new Environment, write down VM id and seperate with comma: ')
        ids = input('IDs seperated by ",": ')
        profile_name = input('Profile name: ')
        ids = ids.replace(" ","")
        ids_list = ids.split(',')
        create_profile = profile_creator(ids_list, profile_name)
        if create_profile == 1 :
            print('Would you like to toggle this profile:  y/n')
        else:
            print(create_profile)
    if selection == "2":
        select_profile()
    if selection == "3":
        exit()






