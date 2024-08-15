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

function Remove_Service{
    param (
        [string]$NameService
    )

    if((check_Service -NameService $NameService) -eq 0 ){
           Write-Host "Service $NameService not exist."
    }else{
           sc.exe delete $NameService
           Write-Host "Removed successfully $NameService "
   }
}


$NameService = Read-Host -Prompt "[+] Enter the name service"



while((check_Service -NameService $NameService) -eq 0){
    Write-Host  "[-] Service $NameService does not exist."
    $NameService = Read-Host -Prompt "[+] Enter the name service again"
}
Remove_Service -NameService $NameService
if((check_Service -NameService $NameService) -eq 0 ){
    Write-Host  "[-] Deleted $NameService successfully."
}
