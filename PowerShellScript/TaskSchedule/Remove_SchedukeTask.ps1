function Remove-TaskSchedule {
    param (
        [string]$TaskName
    )

    # Xóa Task Schedule
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

function Check-TaskSchedule{
    param (
    [string]$TaskName
    )
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $task) {
        return 0
    
    }else{
        return 1
    }
}

[string]$taskName = Read-Host -Prompt "[+] Enter the task name you want to delete"
while((Check-TaskSchedule -TaskName $taskName) -eq 0){
    Write-Host "[+] Task $taskName does not exist."
   [string]$taskName = Read-Host -Prompt "[+] Enter the task name again."
}

Remove-TaskSchedule -TaskName $taskName
if((Check-TaskSchedule -TaskName $taskName) -eq 0){
    Write-Host "[+] Deleted $taskName successfully."
}