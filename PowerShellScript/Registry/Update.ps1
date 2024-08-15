function check_Path{
    param (
        [string]$Path,
        [string]$Name = " "
    )

    $isPath = Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue
    
    if(-not $isPath)
    {
        return 0
    }
    return 1
}

function Update_Registry{
    param(
        [string]$Path,
        [string]$Name,
        [string]$newValue
    )

    if((check_Path -Path $Path -Name $Name) -eq 1){
        Set-ItemProperty -Path $Path -Name $Name -Value $newValue 
        Write-Host "Value updated successfully."
    }else{
        Write-Host "Path $Path does not exist."
        return
    }

}
##HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
#UpdateValue.exe
$Path = Read-Host -Prompt "Enter the key path"
$Name = Read-Host -Prompt "Enter the name value"
$newValue = Read-Host -Prompt "Enter the new value"

Update_Registry -Path $Path -Name $Name -newValue $newValue