function Add-TaskSchedule {
    param (
        [string]$TaskName,
        [string]$Execute_Path,
        [string]$Argument =" ",
        [string]$StartUpTime
        
    )
    if($Argument -eq " "){
    # Tạo Action
        $action = New-ScheduledTaskAction -Execute $Execute_Path 
    }else{
        $action = New-ScheduledTaskAction -Execute $Execute_Path -Argument $Argument
    }


    # Tạo Trigger
    $trigger = New-ScheduledTaskTrigger -Daily -At $StartUpTime

    # Tạo Task Schedule
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger
}
#Ham check task schedule da ton tai hay chua 
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

#C:\Windows\System32\notepad.exe
#-Execute: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe


[string]$taskName = Read-Host -Prompt "[+] Enter the task name"
while((Check-TaskSchedule -TaskName $taskName) -eq 1){
    Write-Host "Task $taskName already exits."
   [string]$taskName = Read-Host -Prompt "[+] Enter the task name again"
}
[string]$execute_path = Read-Host -Prompt "[+] Enter the excutable path"
[string]$chose = Read-Host -Prompt "[+] Do you want to enter argument (y/n)"
if($chose -eq "y"){
[string]$argument = Read-Host -Prompt "[+] Enter the Argument (optional)"
}else{
    $argument=" "
}
[string]$StartUpTime = Read-Host -Prompt "[+] Enter the Trigger Time (e.g., 12:00PM)"
Add-TaskSchedule -TaskName $taskName -Execute_Path $execute_path -Argument $argument -StartUpTime $StartUpTime

#Add-TaskSchedule -TaskName "MyTask" -ActionArg "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument "C:\Windows\System32\notepad.exe" -TriggerTime "9:34AM"