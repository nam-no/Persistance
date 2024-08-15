
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
function Remove_RegistryKey{
    param (
        [string]$Path
    )

    if((check_Path -Path $Path) -eq 0 ){
           Write-Host "Path $Path not exist."
    }else{
           Remove-Item -Path $Path -Recurse
           Write-Host "Removed successfully $Path "
   }
}

function Remove_RegistryValue{
    param(
        [string]$Path,
        [string] $Name
    )
    if((check_Path -Path $Path) -eq 0 ){
           Write-Host "Path $Path not exist."
    }else{
           Remove-ItemProperty -Path $Path -Name $Name
           Write-Host "Removed successfully a value from $Path "
    }
}
##HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
Write-Host "What do you want to  remove? `n 1. Remove Key in Registry `n 2. Remove value in Registry"
$choose = Read-Host -Prompt "[+] Please, Chose"
if($choose -eq 1){
    $Path = Read-Host -Prompt "[+] Enter the Path need to remove"
    Remove_RegistryKey -Path $Path
}elseif($choose -eq 2){
    $Path = Read-Host -Prompt "[+] Enter the Path need to remove"
    $Name = Read-Host -Prompt "[+] Enter the value name"
    Remove_RegistryValue -Path $Path -Name $Name
}else{return}

