import ctypes
from ctypes import wintypes
SERVICE_START = 0x0010
SERVICE_STOP = 0x0020
SERVICE_CONTROL_STOP = 0x00000001

SC_MANAGER_CONNECT = 0x0001
SERVICE_QUERY_STATUS = 0x0004

SC_MANAGER_CREATE_SERVICE = 0x0002
SERVICE_WIN32_OWN_PROCESS = 0x00000010
SERVICE_AUTO_START = 0x00000002
SERVICE_ERROR_NORMAL = 0x00000001
SERVICE_ALL_ACCESS = 0xF01FF

# class SERVICE_STATUS(ctypes.Structure):
#     _fields_ = [
#         ('dwServiceType', wintypes.DWORD),
#         ('dwCurrentState', wintypes.DWORD),
#         ('dwControlsAccepted', wintypes.DWORD),
#         ('dwWin32ExitCode', wintypes.DWORD),
#         ('dwServiceSpecificExitCode', wintypes.DWORD),
#         ('dwCheckPoint', wintypes.DWORD),
#         ('dwWaitHint', wintypes.DWORD),
#     ]

advapi32 = ctypes.WinDLL('Advapi32.dll')

#Hàm OpenScManager
OpenSCManager = advapi32.OpenSCManagerW
OpenSCManager.artypes = [wintypes.LPWSTR,wintypes.LPWSTR,wintypes.DWORD]
OpenSCManager.restype = wintypes.HANDLE

#Hàm CloseServiceHandle
CloseServiceHandle = advapi32.CloseServiceHandle
CloseServiceHandle.argtypes = [wintypes.HANDLE]
CloseServiceHandle.restype = wintypes.BOOL

#Hàm CreateService
CreateService = advapi32.CreateServiceW
CreateService.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR]
CreateService.restype = wintypes.HANDLE

#Hàm Openserviec
OpenService = advapi32.OpenServiceW
OpenService.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD]
OpenService.restype = wintypes.HANDLE

#Hàm StartService
StartService = advapi32.StartServiceW
StartService.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.LPWSTR)]
StartService.restype = wintypes.BOOL

# Hàm DeleteService
DeleteService = advapi32.DeleteService
DeleteService.argtypes = [wintypes.HANDLE]
DeleteService.restype = wintypes.BOOL

#Hàm ControlService
ControlService = advapi32.ControlService
ControlService.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(None)]
ControlService.restype = wintypes.BOOL
#Ham ChangeServiceConfig

ChangeServiceConfig = advapi32.ChangeServiceConfigW
ChangeServiceConfig.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR, wintypes.LPWSTR]
ChangeServiceConfig.restype = wintypes.BOOL
def menu():
    print("[+] 1. Create service ")
    print("[+] 2. Start service")
    print("[+] 3. Stop service")
    print("[+] 4. Delete service")


def service_exists(service_name):
    sc_manager = OpenSCManager(None, None, SC_MANAGER_CONNECT)
    if not sc_manager:
        raise Exception(f"OpenSCManager failed with error {ctypes.GetLastError()}")

    service = OpenService(sc_manager, service_name, SERVICE_QUERY_STATUS)
    if service:
        CloseServiceHandle(service)
        CloseServiceHandle(sc_manager)
        return True
    else:
        CloseServiceHandle(sc_manager)
        return False
def create_service(service_name, display_name,excutable_path):
    sc_manager = OpenSCManager(None,None,SC_MANAGER_CREATE_SERVICE)
    if not sc_manager:
         raise Exception(f"OpenSCManager failed with error {ctypes.GetLastError()}")
    service = CreateService(sc_manager,service_name,display_name,SERVICE_ALL_ACCESS,SERVICE_WIN32_OWN_PROCESS,SERVICE_AUTO_START,SERVICE_ERROR_NORMAL,excutable_path,None,None,None,None,None)
    if not service:
        raise Exception(f"CreateService failed with error {ctypes.GetLastError()}")
    print(f"Service '{service_name}' created successfully.")

    CloseServiceHandle(service)
    CloseServiceHandle(sc_manager)
def start_service(service_name):
    sc_manager = OpenSCManager(None, None, SC_MANAGER_CREATE_SERVICE)
    if not sc_manager:
        raise Exception(f"OpenSCManager failed with error {ctypes.GetLastError()}")

    service = OpenService(sc_manager, service_name, SERVICE_START)
    if not service:
        raise Exception(f"OpenService failed with error {ctypes.GetLastError()}")

    if not StartService(service, 0, None):
        raise Exception(f"StartService failed with error {ctypes.GetLastError()}")

    print(f"Service '{service_name}' started successfully.")

    CloseServiceHandle(service)
    CloseServiceHandle(sc_manager)
def stop_service(service_name):
    # Mở SCManager với quyền tạo dịch vụ
    sc_manager = OpenSCManager(None, None, SC_MANAGER_CREATE_SERVICE)
    if not sc_manager:
        raise Exception(f"OpenSCManager failed with error {ctypes.GetLastError()}")

    # Mở dịch vụ cần dừng
    service = OpenService(sc_manager, service_name, SERVICE_STOP)
    if not service:
        CloseServiceHandle(sc_manager)
        raise Exception(f"OpenService failed with error {ctypes.GetLastError()}")

    # Khởi tạo cấu trúc SERVICE_STATUS để nhận trạng thái dịch vụ
    #service_status = SERVICE_STATUS()
    # Gửi lệnh dừng dịch vụ
    if not ControlService(service, SERVICE_CONTROL_STOP, None):
        CloseServiceHandle(service)
        CloseServiceHandle(sc_manager)
        raise Exception(f"ControlService failed with error {ctypes.GetLastError()}")

    print(f"Service '{service_name}' stopped successfully.")

    # Đóng các handle
    CloseServiceHandle(service)
    CloseServiceHandle(sc_manager)
def delete_service(service_name):
    # Mở SCManager với quyền tạo dịch vụ
    sc_manager = OpenSCManager(None, None, SC_MANAGER_CREATE_SERVICE)
    if not sc_manager:
        raise Exception(f"OpenSCManager failed with error {ctypes.GetLastError()}")

    # Mở dịch vụ với tất cả quyền truy cập (SERVICE_ALL_ACCESS)
    service = OpenService(sc_manager, service_name, SERVICE_ALL_ACCESS)
    if not service:
        CloseServiceHandle(sc_manager)
        raise Exception(f"OpenService failed with error {ctypes.GetLastError()}")

    # Xóa dịch vụ
    if not DeleteService(service):
        CloseServiceHandle(service)
        CloseServiceHandle(sc_manager)
        raise Exception(f"DeleteService failed with error {ctypes.GetLastError()}")

    print(f"Service '{service_name}' deleted successfully.")

    # Đóng các handle
    CloseServiceHandle(service)
    CloseServiceHandle(sc_manager)
if __name__ == '__main__':
    while True :
        menu()
        choose = int(input("[+] Please, choose : "))
        if(choose == 1):
            service_name = input("[+] Enter the service name : ")
            while(service_exists(service_name) == True):
                input("[+] Service name already exist .")
                service_name = input("[+] Enter the service name : ")
            display_name = input("[+] Enter the display name : ")
            binPath = input("[+] Enter the excute path : ")
            create_service(service_name,display_name,binPath)
        elif(choose == 2 ):
            service_name = input("[+] Enter the service name : ")
            while (service_exists(service_name) == False):
                input("[+] Service name does not exist .")
                service_name = input("[+] Enter the service name : ")
            start_service(service_name)

        elif(choose == 3):
            service_name = input("[+] Enter the service name : ")
            while (service_exists(service_name) == False):
                input("[+] Service name does not exist .")
                service_name = input("[+] Enter the service name : ")
            stop_service(service_name)
        elif(choose == 4):
            service_name = input("[+] Enter the service name : ")
            while (service_exists(service_name) == False):
                input("[+] Service name does not exist .")
                service_name = input("[+] Enter the service name : ")
            delete_service(service_name)
        else:
            input("[+] Just only choose 1 --> 4")
            continue
        next = input("What do you want to next (y/n) ? ")
        if(next == 'n'):
            break
            print("[-->] Exit .")


