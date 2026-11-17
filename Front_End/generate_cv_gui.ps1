Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# =====================================================================
# 🔬 DETERMINISTIC ROOT GROUNDING
# =====================================================================
# =====================================================================
# 🔬 DECOUPLED TIERS PATH ANCHORING
# =====================================================================
$FRONTEND_DIR = $PSScriptRoot
$ROOT_DIR     = Split-Path -Parent $FRONTEND_DIR

# Map explicitly to the sibling project tiers
$BACKEND_DIR  = Join-Path $ROOT_DIR "Back_End"
$MAIN_SCRIPT  = Join-Path $BACKEND_DIR "main.py"
$CONFIG_FILE  = Join-Path $BACKEND_DIR "config\agent_config.yaml"

# Safe validation checkpoint to prevent background thread hangs
if (-not (Test-Path $MAIN_SCRIPT)) {
    [System.Windows.Forms.MessageBox]::Show("CRITICAL PATH ERROR:`nCore engine orchestrator not found at targeted location:`n$MAIN_SCRIPT", "Pipeline Fault", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    exit
}

# =====================================================================
# 🎨 MINIMAL DESKTOP CANVAS CONTROL
# =====================================================================
$Form = New-Object System.Windows.Forms.Form
$Form.Text = "AI Engine - Production Deployment Dashboard"
$Form.Size = New-Object System.Drawing.Size(460, 320)
$Form.StartPosition = "CenterScreen"
$Form.FormBorderStyle = "FixedDialog"
$Form.MaximizeBox = $false

$TitleLabel = New-Object System.Windows.Forms.Label
$TitleLabel.Text = "Execute AI CV Customization Blueprint"
$TitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$TitleLabel.Location = New-Object System.Drawing.Point(25, 20)
$TitleLabel.Size = New-Object System.Drawing.Size(400, 25)
$Form.Controls.Add($TitleLabel)

# Cache Lifecycle Interactive Override Mode
$CacheCheckbox = New-Object System.Windows.Forms.CheckBox
$CacheCheckbox.Text = "Force Live API Request Execution Bypass (Ignore Cache Mode)"
$CacheCheckbox.Location = New-Object System.Drawing.Point(30, 65)
$CacheCheckbox.Size = New-Object System.Drawing.Size(400, 20)
$CacheCheckbox.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$Form.Controls.Add($CacheCheckbox)

# Inline Terminal Status Monitor Display 
$OutputBox = New-Object System.Windows.Forms.TextBox
$OutputBox.Multiline = $true
$OutputBox.ReadOnly = $true
$OutputBox.BackColor = "Black"
$OutputBox.ForeColor = "LightGreen"
$OutputBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$OutputBox.Location = New-Object System.Drawing.Point(25, 105)
$OutputBox.Size = New-Object System.Drawing.Size(395, 90)
$OutputBox.Text = "READY: Awaiting deployment execution directive..."
$Form.Controls.Add($OutputBox)

# Process Trigger Action Component
$LaunchButton = New-Object System.Windows.Forms.Button
$LaunchButton.Text = "🚀 RUN LIVE CUSTOMIZATION PIPELINE"
$LaunchButton.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$LaunchButton.Location = New-Object System.Drawing.Point(25, 215)
$LaunchButton.Size = New-Object System.Drawing.Size(395, 40)
$Form.Controls.Add($LaunchButton)

# =====================================================================
# ⚡ APPLICATION RUNTIME LIFECYCLE ROUTER
# =====================================================================
$LaunchButton.Add_Click({
    $LaunchButton.Enabled = $false
    $OutputBox.ForeColor = "LightGreen"
    $OutputBox.Text = "[Orchestrator] Preparing background stream handshakes...`r`n"
    $Form.Refresh()

    # Conditionally modify configuration file values based on checkbox state
    if ($CacheCheckbox.Checked) {
        $OutputBox.AppendText("[Config Matrix] Update directive detected: Setting ignore_dynamic_cache=True`r`n")
        # Perform clean modification inline to force live pipeline runs
        (Get-Content $CONFIG_FILE) -replace 'ignore_dynamic_cache:.*', 'ignore_dynamic_cache: true' | Set-Content $CONFIG_FILE
    } else {
        (Get-Content $CONFIG_FILE) -replace 'ignore_dynamic_cache:.*', 'ignore_dynamic_cache: false' | Set-Content $CONFIG_FILE
    }
    $Form.Refresh()

    # Spawning Subprocess with clean environment boundaries
    $pInfo = New-Object System.Diagnostics.ProcessStartInfo
    $pInfo.FileName = "python"
    $pInfo.Arguments = "`"$MAIN_SCRIPT`""
    $pInfo.RedirectStandardOutput = $true
    $pInfo.RedirectStandardError = $true
    $pInfo.UseShellExecute = $false
    $pInfo.CreateNoWindow = $true

    # 🌟 INJECT ENCODING FIXES HERE: Mandate UTF-8 streams for background pipe channels
    $pInfo.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8"
    $pInfo.EnvironmentVariables["PYTHONUTF8"] = "1"

    $OutputBox.AppendText("[Process Shell] Spawning core system orchestrator main.py...`r`n")
    $Form.Refresh()

    try {
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $pInfo
        [void]$process.Start()

        # Fix the unassigned variable scan warning cleanly
        [void]$process.StandardOutput.ReadToEnd()
        [void]$process.StandardError.ReadToEnd()
        $process.WaitForExit()


        if ($process.ExitCode -eq 0) {
            $OutputBox.AppendText("🎉 SUCCESS: Document customization execution concluded smoothly!")
        } else {
            $OutputBox.ForeColor = "Red"
            $OutputBox.Text = "❌ PROCESS EXCEPTION DETECTED (`$($process.ExitCode)`):`r`n$stderr"
        }
    }
    catch {
        $OutputBox.ForeColor = "Red"
        $OutputBox.Text = "❌ RUNTIME ERROR SPAWNING BACKEND: $_"
    }

    $LaunchButton.Enabled = $true
})

[void]$Form.ShowDialog()
