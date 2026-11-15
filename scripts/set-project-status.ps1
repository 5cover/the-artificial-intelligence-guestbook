# Sets the Status of issues on the project board (https://github.com/users/5cover/projects/23).
# Usage: ./scripts/set-project-status.ps1 -Status 'In Progress' -Issue 13, 14
param(
    [Parameter(Mandatory)] [ValidateSet('Idea', 'Ready', 'In Progress', 'Pending', 'Nope', 'Done')] [string] $Status,
    [Parameter(Mandatory)] [int[]] $Issue
)
$ErrorActionPreference = 'Stop'
$projectId = 'PVT_kwHOAmiDks4Brvf4'
$statusField = 'PVTSSF_lAHOAmiDks4Brvf4zhqAwAU'
$options = @{ 'Idea' = 'bbb88861'; 'Ready' = 'd3a117a4'; 'In Progress' = '5f1f2975'; 'Pending' = 'd0737c61'; 'Nope' = '44eead8b'; 'Done' = '4cf59bb6' }

function Invoke-WithRetry([scriptblock] $Action) {
    for ($attempt = 1; ; $attempt++) {
        $result = & $Action
        if ($LASTEXITCODE -eq 0) { return $result }
        if ($attempt -ge 3) { throw "gh failed after $attempt attempts" }
    }
}

$items = (Invoke-WithRetry { gh project item-list 23 --owner 5cover --limit 500 --format json } | ConvertFrom-Json).items
foreach ($n in $Issue) {
    $item = $items | Where-Object { $_.content.number -eq $n }
    if (-not $item) { Write-Warning "#$n is not on the board"; continue }
    Invoke-WithRetry { gh project item-edit --id $item.id --project-id $projectId --field-id $statusField --single-select-option-id $options[$Status] } | Out-Null
    Write-Output "#$n -> $Status"
}
