import subprocess

def menu():
    print("[-] What do you want to do ?")
    print("[+] 1. Create task schedule.")
    print("[+] 2. Remove task schedule.")
    print("[+] 3. Update task schedule.")
def menu_update():
    print("[-] What do you want to update ?")
    print("[+] 1. Execute path.")
    print("[+] 2. Start up time .")

def check_task_exists(task_name):
    try:
        # Thực hiện lệnh schtasks để kiểm tra task
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name],
            capture_output=True,#Đầu ra (stderr,stdout) vào đối tượng result
            text=True,# Đầu ra được sử lý dạng chuỗi thay vì dạng bytes
            check=True # Check lỗi
        )
        # Nếu lệnh thành công và có output, task tồn tại
        if task_name in result.stdout:
            return True
    except subprocess.CalledProcessError:
        # Nếu lệnh không thành công, task không tồn tại
        return False

    return False

def update_task_start_time(task_name, new_start_time):
    try:
        subprocess.run(
            ["schtasks", "/change",
             "/tn", task_name,
             "/st", new_start_time],
            check=True
        )
        print(f"Task '{task_name}' updated successfully to start at {new_start_time}.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating task: {e}")
def update_task_execute_path(task_name, new_command):
    try:
        subprocess.run(
            ["schtasks", "/change",
             "/tn", task_name,
             "/tr", new_command],
            check=True
        )
        print(f"Task '{task_name}' command updated successfully to '{new_command}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating task command: {e}")

def create_task(task_name,execute_path,script_args,schedules,startup_time):
    # Định nghĩa các đối số cho script Python
    #execute_path = "C:\\Windows\\System32\\notepad.exe"
    #script_args = ""  # Thay đổi tùy theo tham số của script

    # Xây dựng lệnh schtasks với các đối số
    command = [
        "schtasks", "/create",
        "/tn", f"{task_name}",  # Tên task
        "/tr", f"{execute_path} {script_args}",  # Đường dẫn tới script và đối số
        "/sc", f"{schedules}",  # Lịch trình: hàng ngày
        "/st", f"{startup_time}"  # Thời gian bắt đầu
#        "/f"  # Ghi đè nếu task đã tồn tại
    ]
    if (schedules == "daily"):
            try:
                # Thực thi lệnh
                subprocess.run(command, check=True)
                print("[+] Task created successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Error creating task: {e}")
    elif (schedules == "weekly"):
            days_of_week = input("[+] Enter the days of week (MON, TUE, WED, THU, FRI, SAT, SUN) : ")
            command.extend(["/d",days_of_week])
            print(command)
            try:
                # Thực thi lệnh
                subprocess.run(command, check=True)
                print(f"[+] Task '{task_name}' created successfully to run on {days_of_week} at {startup_time}.")
            except subprocess.CalledProcessError as e:
                print(f"[+]Error creating task: {e}")
    elif (schedules == "monthly"):
            days_of_month = input("[+] Enter the days of month (01 --> 31) : ")
            command.extend(["/d",days_of_month])
            try:
                # Thực thi lệnh
                subprocess.run(command, check=True)
                print(f"[+] Task '{task_name}' created successfully to run on days {days_of_month} of each month at {startup_time}.")
            except subprocess.CalledProcessError as e:
                print(f"Error creating task: {e}")
    else:return

def delete_task(task_name):
    try:
        # Xóa task bằng lệnh schtasks
        subprocess.run(
            ["schtasks", "/delete", "/tn", task_name, "/f"],
            check=True
        )
        print(f"Task '{task_name}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting task: {e}")

def main():
    #"C:\\Windows\\System32\\notepad.exe"
    while(True):
        menu()
        choose = int(input("[-] Please, choose : "))
        if(choose == 1) :
            task_name = input("[+] Enter the task name : ")
            while (check_task_exists(task_name) == True):
                print("[-] Task name already exist.")
                task_name = input("[+] Enter the task name again : ")
            execute_path = input("[+] Enter the excute path : ")
            execute_args = input("[+] Enter the excute argument : ")
            schedules = input("[+] Enter the schedule (daily , weekly, monthly) : ")
            startup_time = input("[+] Enter the time start (eg 00:00 --> 24:59):")
            create_task(task_name,execute_path,execute_args,schedules,startup_time)
        elif(choose == 2):
            task_name = input("[+] Enter the task name : ")
            while (check_task_exists(task_name) == False):
                print("[-] Task name does not exist.")
                task_name = input("[+] Enter the task name again  : ")
            delete_task(task_name)
        elif(choose == 3):
            menu_update()
            chon=int(input("Please, choose :"))
            task_name = input("[+] Enter the task name : ")
            while (check_task_exists(task_name) == False):
                print("[-] Task name does not exist.")
                task_name = input("[+] Enter the task name again  : ")
            if(chon==1):
                new_execute_path = input("[+] Enter the excute path : ")
                update_task_execute_path(task_name,new_execute_path)
            elif(chon==2):
                new_start_up_time = input("[+] Enter the time start (eg 00:00 --> 24:59) :")
                update_task_start_time(task_name,new_start_up_time)
            else:
                print("[+] Choose only form 1 --> 2 ")

        else:
            print("[+] Choose only form 1 --> 3 ")
        next = input(" Do you want to next (y/n) ?")
        if (next == "y"):
            continue
        else:
            print(" [->] Exit.")
            break

if __name__ == '__main__':
    main()
#C:\Windows\System32\cmd.exe