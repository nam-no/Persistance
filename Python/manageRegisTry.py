import subprocess
from colorama import Fore,Style
def list_type_value():
    print("[+] what do you want typt data ? ")
    print("[-] 1.REG_SZ (String)")
    print("[-] 2.REG_EXPAND_SZ (Expandable String)")
    print("[-] 3.REG_DWORD (32-bit Integer)")
    print("[-] 4.REG_QWORD (64-bit Integer)")
    print("[-] 5.REG_BINARY (Binary Data)")
    print("[-] 6.REG_BINARY (Binary Data)")

def menu():
    print("[+] What do you want to do ?")
    print("[-] 1. Add the registry key .")
    print("[-] 2. Add the registry value .")
    print("[-] 3. Delete the registry key .")
    print("[-] 4. Delete the registry value .")

def get_value_type(choose):
    value_type = " "
    if(choose == 1):
        value_type = "REG_SZ"
    elif(choose == 2):
        value_type = "REG_EXPAND_SZ"
    elif(choose == 3):
        value_type = "REG_DWORD"
    elif(choose == 4):
        value_type = "REG_QWORD"
    elif(choose == 5):
        value_type = "REG_BINARY"
    elif(choose == 6):
        value_type = "REG_MULTI_SZ"
    else :
        print("[+] Please, Choose only from 1 to 6 .")
    return value_type
def check_registry_key_exists(key_path):
    command =["reg","query",key_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
def remove_registry_key(key_path):
    command = ["reg",'delete',key_path,"/f"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN + "[+] Removed registry key successfully."+ Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")
def remove_registry_value(key_path,value_name):
    command = ["reg", 'delete', key_path, "/v",value_name,"/f"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN + f"[+] Removed registry a value {value_name} of the  {key_path} successfully."+ Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")

def add_registry_key(key_path):
     command = ["reg", "add", key_path]
     try:
         result = subprocess.run(command, capture_output=True, text=True)
         if(check_registry_key_exists(key_path)==True):
             print(Fore.GREEN + "[+] Key added successfully." + Style.RESET_ALL)
         else:
             print(Fore.RED + "[+] Invalid key path." + Style.RESET_ALL)
     except subprocess.CalledProcessError as e:
         print(f"Error creating task: {e}")

def add_registry_value(key_path,value_name,value_data,value_type):
    command =["reg","add",key_path,"/v",value_name,"/t",value_type,"/d",value_data]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN +"[+] Key added successfully."+ Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error creating task: {e}")

def add():
    key_path = input("[+] Enter the key path : ")
    while (check_registry_key_exists(key_path) == True):
        print("[-] Key path already  exist.")
        key_path = input("[+] Enter the key path again : ")
    value_name = input("[+] Enter the name of the value : ")
    value_data = input("[+] Enter the data of the value : ")
    list_type_value()
    choose = int(input("Choose type value : "))
    value_type = get_value_type(choose)
    print(f"[+] Chose the type of the value is {value_type}")
    add_registry_value(key_path, value_name, value_data, value_type)
def delete():
    key_path = input("[+] Enter the key path need to create : ")
    while (check_registry_key_exists(key_path) == False):
        print(Fore.RED + "[-] Key path does not  exist."+ Style.RESET_ALL)
        key_path = input("[+] Enter the key path again : ")

def run():
    while (True):
        menu()
        chose = int(input("[+] Please, choose :"))
        if(chose ==1):
            print("[+] Chose mode 1. ")
            key_path = input("[+] Enter the key path : ")
            while (check_registry_key_exists(key_path) == True):
                print(Fore.RED + "[-] Key path already  exist." +Style.RESET_ALL )
                key_path = input("[+] Enter the key path again : ")
            add_registry_key(key_path)
        elif(chose==2):
            print("[+] Chose mode 2. ")
            key_path = input("[+] Enter the key path : ")
            while (check_registry_key_exists(key_path) == False):
                print(Fore.RED + "[-] Key path does not  exist."+ Style.RESET_ALL)
                key_path = input("[+] Enter the key path again : ")
            value_name = input("[+] Enter the name of the value : ")
            value_data = input("[+] Enter the data of the value : ")
            list_type_value()
            choose = int(input("Choose type value : "))
            value_type = get_value_type(choose)
            print(f"[+] Chose the type of the value is {value_type}")
            add_registry_value(key_path,value_name,value_data,value_type)
        elif(chose==3):
            print("[+] Chose mode 3. ")
            key_path = input("[+] Enter the key path need to delete : ")
            while (check_registry_key_exists(key_path) == False):
                print(Fore.RED+"[-] Key path does not  exist."+Style.RESET_ALL)
                key_path = input("[+] Enter the key path again : ")
            remove_registry_key(key_path)
        elif(chose==4):
            print("[+] Chose mode 4. ")
            key_path = input("[+] Enter the key path : ")
            while (check_registry_key_exists(key_path) == False):
                print(Fore.RED + "[-] Key path does not  exist."+Style.RESET_ALL)
                key_path = input("[+] Enter the key path again : ")
            value_name = input("[+] Enter the name of the value :")
            remove_registry_value(key_path,value_name)
        else:
            print("[+] Choose only form 1 --> 4 ")
        next = input(" Do you want to next (y/n) ?")
        if(next == "y"):
            continue
        else :
            print(" [->] Exit.")
            break
if __name__ == '__main__':
    run()
#C:\Users\Administrator\Desktop\Toolmalware\pestudio-9.59\pestudio\pestudio.exe
#HKCU\Software\Microsoft\Windows\CurrentVersion\Run