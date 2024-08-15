import subprocess
from colorama import Fore,Style

def menu():
    print("[-] What do you want to do ?")
    print("[+] 1. Create task service.")
    print("[+] 2. Remove task service.")
    print("[+] 3. Config task service.")
def check_service_exist(service_name):
    command = ["sc","query",service_name]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def create_service(service_name,execute_path):
    command = ["sc", "create",service_name,f"binPath={execute_path}"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN + "[+] Service created successfully." + Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error creating service: {e}")
def delete_service(service_name):
    command = ["sc","delete",service_name]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN + "[+] Removed  service successfully."+ Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")

def config_service(service_name,auto):
    command=["sc","config",service_name,f"start={auto}"]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(Fore.GREEN + f"[+] Config mode {auto} successlly."+ Style.RESET_ALL)
    except subprocess.CalledProcessError as e:
        print(f"Error : {e}")

def run() :
    while(True):
        menu()
        chose = int(input("[+] Please, choose :"))
        if (chose == 1):
            print("[+] Chose mode 1. ")
            service_name = input("[+] Enter the service name  : ")
            while (check_service_exist(service_name) == True):
                print(Fore.RED + "[-] Service name already  exist." + Style.RESET_ALL)
                service_name = input("[+] Enter the service name again : ")
            binPath = input("[+] Enter the binPath :")
            create_service(service_name,binPath)
        elif (chose == 2):
            print("[+] Chose mode 2. ")
            service_name = input("[+] Enter the service name  : ")
            while (check_service_exist(service_name) == False):
                print(Fore.RED + "[-] Service name does not exist." + Style.RESET_ALL)
                service_name = input("[+] Enter the service name again : ")
            delete_service(service_name)
        elif (chose == 3):
            print("[+] Chose mode 3. ")
            service_name = input("[+] Enter the service name  : ")
            while (check_service_exist(service_name) == False):
                print(Fore.RED + "[-] Service name does not exist." + Style.RESET_ALL)
                service_name = input("[+] Enter the service name again : ")
            mode_auto = input("[+] Enter mode auto (auto, disabled, ...) : ")
            config_service(service_name,mode_auto)
        else:
            print("[+] Choose only form 1 --> 3 ")
        next = input(" [+] Do you want to next (y/n) ? :")
        if (next == "y"):
            continue
        else:
            print(" [->] Exit.")
            break
if __name__ == '__main__':
    run()
