function check_Service{
    param(
        [string]$NameService
    )

    $check = Get-Service -Name $NameService -ErrorAction SilentlyContinue
    if(-not $check)
    {
        return 0
    }
    return 1

}

function Add_Service{
    param(
    [string]$NameService,
    [string]$NameDisplay,
    [string]$BinaryPathName,
    [string]$DescriptionService,
    [string]$StartupType
    )

    New-Service -Name $NameService -DisplayName $NameDisplay -BinaryPathName $BinaryPathName -Description $DescriptionService -StartupType $StartupType
    
    if((check_Service -NameService $NameService) -eq 1){
        Write-Host "[-] Service created successfully."
        return
    }

}  

function list_StartupType{
    Write-Host "[+] Chose type data. 
    `n1. Automatic 
    `n2. Manual 
    `n3. Disabled 
    `n4. Boot 
    `n5. System "
}

$NameService = Read-Host -Prompt "[+] Enter the name service"
while((check_Service -NameService $NameService) -eq 1){
    Write-Host  "[-] Service $NameService already exist."
    $NameService = Read-Host -Prompt "[+] Enter the name service again"
}
$NameDisPlay = Read-Host -Prompt "[+] Enter the display name service"
$BinaryPathName = Read-Host -Prompt "[+] Enter the binary path name"
$DescriptionService = Read-Host -Prompt "[+] Enter the descripton for service"
$StartupType = Read-Host -Prompt "[+] Enter the startup type" 

Add_Service -NameService $NameService -NameDisplay $NameDisPlay -BinaryPathName $BinaryPathName -DescriptionService $DescriptionService -StartupType $StartupType