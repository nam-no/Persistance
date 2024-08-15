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

function menu{
    Write-Host "What do you want to do ?"
    Write-Host "1. Update Action ."
    Write-Host "2. Update Trigger."
    Write-Host "3. Update Task ."
}
function Update_TaskSchedul_Action{
    param(
        [string]$TaskName,
        [string]$Execute,
        [string]$Argument = " "
    )

    $action = New-ScheduledTaskAction -Execute $Execute -Argument $Argument

    Set-ScheduledTask -TaskName $TaskName -Action $action 
    
}
function Update_TaskSchedul_Trigger{
    param(
        [string]$TaskName,
        [string]$startUpTime
    )
    $trigger = New-ScheduledTaskTrigger -Daily -At $startUpTime
    Set-ScheduledTask -TaskName $TaskName -Trigger $trigger 
    
}

function Update_TaskSchedule
{
    param(
        [string]$TaskName,
        [string]$Execute,
        [string]$Argument = " ",
        [string]$startUpTime
    )
     $action = New-ScheduledTaskAction -Execute $Execute -Argument $Argument
     $trigger = New-ScheduledTaskTrigger -Daily -At $startUpTime
     Set-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger
}

menu 
$choose = Read-Host -Prompt "[+] Please, Choose"
if($choose -eq 1){  
    [string]$taskName = Read-Host -Prompt "[+] Enter the task name want to update "
    while((Check-TaskSchedule -TaskName $taskName) -eq 0){
        Write-Host "[+] Task $taskName does not exits."
       [string]$taskName = Read-Host -Prompt "[+] Enter the task name again"
    }
    [string]$execute = Read-Host -Prompt "[+] Enter the new excutable path"
    [string]$argument = Read-Host -Prompt "[+] Enter the new Argument (optional)"
    Update_TaskSchedul_Action -TaskName $taskName -Execute $execute -Argument $argument
}elseif($choose -eq 2){
    [string]$taskName = Read-Host -Prompt "[+]Enter the task name want to update "
    while((Check-TaskSchedule -TaskName $taskName) -eq 0){
        Write-Host "[+] Task $taskName does not exits."
       [string]$taskName = Read-Host -Prompt "[+] Enter the task name again"
    }

    [string]$startUpTime = Read-Host -Prompt "[+] Enter the new start up time (e.g., 12:00PM)"
    Update_TaskSchedul_Trigger -TaskName $taskName -startUpTime $startUpTime
}elseif($choose -eq 3){
    [string]$taskName = Read-Host -Prompt "[+] Enter the task name want to update "
    while((Check-TaskSchedule -TaskName $taskName) -eq 0){
        Write-Host "[+] Task $taskName does not exits."
       [string]$taskName = Read-Host -Prompt "[+] Enter the task name again"
    }
    [string]$execute = Read-Host -Prompt "[+] Enter the new (excutable path)"
    [string]$argument = Read-Host -Prompt "[+] Enter the new Argument (optional)"
    [string]$startUpTime = Read-Host -Prompt "[+] Enter the new start up time (e.g., 12:00PM)"
    Update_TaskSchedule -TaskName $taskName -Execute $execute -Argument $argument -startUpTime $startUpTime
}else {return}
#C:\Users\Administrator\Desktop\Toolmalware\peid-0-95\PEiD.exe