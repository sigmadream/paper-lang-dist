$env:PATH = "$PSScriptRoot/../.tools/gcc/bin;$PSScriptRoot/../.tools/R/bin/x64;" + $env:PATH
$env:UV_CACHE_DIR = "$PSScriptRoot/../.uv-cache"
$env:PYTHONUTF8 = '1'

# Load local secrets from .env (git-ignored) into this shell process.
# Only NAME=value lines are read; comments and blank lines are ignored.
$envFile = Join-Path $PSScriptRoot '../.env'
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$') {
            $name = $matches[1]
            $value = $matches[2].Trim('"').Trim("'")
            if ($value) { [Environment]::SetEnvironmentVariable($name, $value, 'Process') }
        }
    }
}
