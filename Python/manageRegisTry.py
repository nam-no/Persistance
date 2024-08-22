import ctypes
from ctypes import wintypes

# Khai báo các hằng số cần thiết
HKEY_CURRENT_USER = 0x80000001
KEY_READ = 0x20019
HKEY_LOCAL_MACHINE = 0x80000002
KEY_WRITE = 0x20006
REG_OPTION_NON_VOLATILE = 0x00000000
REG_SZ = 1
KEY_WOW64_64KEY = 0x0100

# Load thư viện advapi32.dll để làm việc với registry
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

#Hàm RegOpenKeyEx
RegOpenKeyEx = advapi32.RegOpenKeyExW
RegOpenKeyEx.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR,     # lpSubKey
    wintypes.DWORD,       # ulOptions
    wintypes.DWORD,      # samDesired
    ctypes.POINTER(wintypes.HKEY)  # phkResult
]
#Hàm RegQueryValueEx
RegQueryValueEx = advapi32.RegQueryValueExW
RegQueryValueEx.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR,     # lpValueName
    wintypes.LPVOID,      # lpReserved
    ctypes.POINTER(wintypes.DWORD), # lpType
    wintypes.LPBYTE,      # lpData
    ctypes.POINTER(wintypes.DWORD)  # lpcbData
]
# Định nghĩa các hàm cần thiết từ advapi32.dll
RegCreateKeyEx = advapi32.RegCreateKeyExW
RegSetValueEx = advapi32.RegSetValueExW
RegCloseKey = advapi32.RegCloseKey


# Định nghĩa kiểu dữ liệu cho các hàm
RegCreateKeyEx.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR,     # lpSubKey
    wintypes.DWORD,       # Reserved
    wintypes.LPWSTR,      # lpClass
    wintypes.DWORD,       # dwOptions
    wintypes.DWORD,        # samDesired
    wintypes.LPVOID,      # lpSecurityAttributes
    wintypes.PHANDLE,     # phkResult
    wintypes.LPDWORD      # lpdwDisposition
]

RegSetValueEx.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR,     # lpValueName
    wintypes.DWORD,       # Reserved
    wintypes.DWORD,       # dwType
    wintypes.LPCWSTR,     # lpData
    wintypes.DWORD        # cbData
]
# Định nghĩa kiểu dữ liệu cho hàm RegDeleteKeyEx
RegDeleteKeyEx = advapi32.RegDeleteKeyExW
RegDeleteKeyEx.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR,     # lpSubKey
    wintypes.DWORD,      # samDesired
    wintypes.DWORD        # Reserved
]
# Định nghĩa kiểu dữ liệu cho hàm RegDeleValue
RegDeleteValue = advapi32.RegDeleteValueW
RegDeleteValue.argtypes = [
    wintypes.HKEY,        # hKey
    wintypes.LPCWSTR      # lpValueName
]
RegCloseKey.argtypes = [
    wintypes.HKEY         # hKey
]
# Hàm kiểm tra sự tồn tại của một khóa Registry
def check_registry_key(hkey, subkey):
    handle = wintypes.HKEY()
    result = RegOpenKeyEx(hkey, subkey, 0, KEY_READ, ctypes.byref(handle))

    if result == 0:  # ERROR_SUCCESS
        RegCloseKey(handle)
        return True
    else:
        return False
# Hàm kiểm tra sự tồn tại của một giá trị trong khóa Registry
def check_registry_value(hkey, subkey, value_name):
    handle = wintypes.HKEY()
    result = RegOpenKeyEx(hkey, subkey, 0, KEY_READ, ctypes.byref(handle))
    if result != 0:  # Khóa không tồn tại
        return False
    data_type = wintypes.DWORD()
    data_size = wintypes.DWORD()
    result = RegQueryValueEx(handle, value_name, None, ctypes.byref(data_type), None, ctypes.byref(data_size))
    RegCloseKey(handle)
    if result == 0:  # ERROR_SUCCESS
        return True
    else:
        return False


def create_registry_key(hkey, subkey):
    handle = wintypes.HKEY()
    disposition = wintypes.DWORD()

    result = RegCreateKeyEx(
        hkey,
        subkey,
        0,
        None,
        REG_OPTION_NON_VOLATILE,
        KEY_WRITE,
        None,
        ctypes.byref(handle),
        ctypes.byref(disposition)
    )
    if result == 0:  # ERROR_SUCCESS
        print(f"[+] Created '{subkey}' successfully.")
        RegCloseKey(handle)
        return True
    else:
        print(f"[+] Error {result}")
        return False

# Hàm để tạo một registry key
def create_registry_value(key, subkey, value_name, value_data):
    hkey = wintypes.HKEY()
    disposition = wintypes.DWORD()
    # Tạo hoặc mở registry key
    result = RegCreateKeyEx(
        key,
        subkey,
        0,
        None,
        REG_OPTION_NON_VOLATILE,
        KEY_WRITE,
        None,
        ctypes.byref(hkey),
        ctypes.byref(disposition)
    )

    if result != 0:
        raise ctypes.WinError(ctypes.get_last_error())

    # Đặt giá trị cho registry key
    result = RegSetValueEx(
        hkey,
        value_name,
        0,
        REG_SZ,
        value_data,
        (len(value_data) + 1) * ctypes.sizeof(wintypes.WCHAR)
    )
    if result != 0:
        raise ctypes.WinError(ctypes.get_last_error())

    # Đóng registry key
    RegCloseKey(hkey)
    print(f"[+] Registry key '{subkey}' created/updated successfully.")
#Hàm xóa một key
def delete_registry_key(hkey, subkey):
    result = RegDeleteKeyEx(hkey, subkey, KEY_WOW64_64KEY, 0)
    return result == 0  # ERROR_SUCCESS
# Hàm xóa giá trị trong Registry
def delete_registry_value(hkey, subkey, value_name):
    handle = wintypes.HKEY()
    result = RegOpenKeyEx(hkey, subkey, 0, KEY_WRITE, ctypes.byref(handle))
    if result != 0:  # ERROR_SUCCESS
        return False
    result = RegDeleteValue(handle, value_name)
    RegCloseKey(handle)
    return result == 0  # ERROR_SUCCESS
def menu():
    print("[+] 1.Created value. ")
    print("[+] 2.Created key. ")
    print("[+] 3.Delete key.")
    print("[+] 4.Delete value. ")
def get_hkey():
    print("[+] 1.HKEY_CURRENT_USER ")
    print("[+] 2.HKEY_LOCAL_MACHINE ")
    chose = int(input("[+] Chosse hkey : "))
    if(chose == 1):
        hkey = HKEY_CURRENT_USER
    elif(chose == 2):
        hkey = HKEY_LOCAL_MACHINE
    return hkey
if __name__ == '__main__':
    while True:
        menu()
        choose = int(input("Please, choose :"))
        if(choose == 1):
            print("[+] You chose to create key ")
            hkey = get_hkey()
            subkey = input("[+] Enter subkey : ")
            while(check_registry_key(hkey,subkey) == False):
                print("[+] Subkey does not exist.")
                subkey = input("[+] Enter subkey again  : ")
            value_name = input("[+] Enter value name :")
            while(check_registry_value(hkey,subkey,value_name) == True):
                print("[+] Value already exist.")
                value_name = input("[+] Enter value name again :")
            value_data = input("[+] Enter value data :")
            create_registry_value(hkey,subkey,value_name,value_data)
        elif(choose==2):
            print("[+] You chose to create key ")
            hkey = get_hkey()
            subkey = input("[+] Enter subkey : ")
            while (check_registry_key(hkey, subkey) == True):
                print("[+] Subkey already exist.")
                subkey = input("[+] Enter subkey again  : ")
            create_registry_key(hkey,subkey)
        elif(choose==3):
            print("[+] You chose to delete key ")
            hkey = get_hkey()
            subkey = input("[+] Enter subkey need to delete : ")
            while (check_registry_key(hkey, subkey) == False):
                print("[+] Subkey does not exist.")
                subkey = input("[+] Enter subkey again  : ")
            delete_registry_key(hkey,subkey)
            print("[+] Deleted key")
        elif(choose==4):
            print("[+] You chose to delete value ")
            hkey = get_hkey()
            subkey = input("[+] Enter subkey : ")
            while (check_registry_key(hkey, subkey) == False):
                print("[+] Subkey does not exist.")
                subkey = input("[+] Enter subkey again  : ")
            value_name = input("[+] Enter value name :")
            while (check_registry_value(hkey, subkey, value_name) == False):
                print("[+] Value does not exist.")
                value_name = input("[+] Enter value name again :")
            delete_registry_value(hkey,subkey, value_name)
            print("[+] Deleted value")
        else:print("Choose 1 --> 4")
        next = input("[+] What do you want to next (y/n) ? ")
        if(next == 'n'):
            break
