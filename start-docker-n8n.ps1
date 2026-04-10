# Start script for Docker compose stack (Windows PowerShell)
# Usage: .\start-docker-n8n.ps1  (ensure Docker Desktop is running)

param(
    [switch]$Rebuild
)

Set-StrictMode -Version Latest

function Check-Docker {
    try {
        docker version | Out-Null
        return $true
    } catch {
        Write-Error "Docker does not appear to be installed or running. Please install/start Docker Desktop."
        return $false
    }
}

if (-not (Check-Docker)) { exit 1 }

if ($Rebuild) {
    Write-Host "Rebuilding images..."
    docker compose build --no-cache
}

Write-Host "Starting containers..."
docker compose up -d

# Wait for services to be healthy
$max = 60
$elapsed = 0
while ($elapsed -lt $max) {
    $status = docker inspect --format='{{json .State.Health.Status}}' patientcare_n8n 2>$null | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($status -eq 'healthy') { Write-Host "n8n is healthy"; break }
    Start-Sleep -Seconds 2
    $elapsed += 2
}

Write-Host "Showing container status..."
docker ps --filter "name=patientcare_" --format "table {{.Names}}\t{{.Status}}"

Write-Host "You can open n8n at http://localhost:5678 and the app at http://localhost:5000"
