 $RepoDir = $PSScriptRoot
Start-Transcript -Path (Join-Path $RepoDir "pipeline.log") -Append | Out-Null
Write-Output ("[{0}] Pipeline run started" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Set-Location (Join-Path $RepoDir "code\deployment")
docker compose up -d --build --force-recreate
Write-Output ("[{0}] Pipeline run finished (exit {1})" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $LASTEXITCODE)
Stop-Transcript