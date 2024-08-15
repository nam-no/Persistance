function check_Path{
    param(
        [string]$Path
    )

    $check = Test-Path $Path
    if(-not $check)
    {
        return 0
    }
    return 1

}

function Add_RegistryKey{
    param(
        [string]$Path
    )
        if((check_Path -Path $Path) -eq 1){
            Write-Host "Path $Path alredy exist."
        }else{
            New-Item -Path $Path
        }

}

function Add_RegistryValue{
    param(
    [string]$Path,
    [string]$Name,
    [string]$Value,
    [string]$TypeData
    )

    New-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType  $TypeData
}

function list_TypeData{
    Write-Host "[+] Chose type data. 
    `n1. String 
    `n2. ExpanString 
    `n3. MultiString 
    `n4. DWord 
    `n5. QWord 
    `n6 .Binary "
}

#HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
#C:\Users\Administrator\Desktop\Toolmalware\peid-0-95\PEiD.exe
Push-Location  HKCU:

$E_Path = Read-Host -Prompt "[+] Enter the Key Path "
if((check_Path -Path $E_Path) -eq 1){
    $Name = Read-Host -Prompt "[+] Enter the value name "
    $Value = Read-Host -Prompt "[+] Enter the value "
    $type_Data = Read-Host -Prompt "[+] Enter the type data"

Add_RegistryValue -Path $E_Path -Name $Name -Value $Value -TypeData $type_Data
}else{
    $Path = Add_RegistryKey -Path $E_Path
    Write-Host "[-] Path created successfully"
    $Name = Read-Host -Prompt "[+] Enter the value name"
    $Value = Read-Host -Prompt "[+] Enter the value"
    $type_Data = Read-Host -Prompt "[+] Enter the type data"
    Add_RegistryValue -Path $E_Path -Name $Name -Value $Value -TypeData $type_Data
}
Pop-Location
Pop-Location
