using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace TalentSource.Desktop.Services
{
    public class ProcessBridge
    {
        private Process? _backendProcess;
        private CancellationTokenSource? _cts;

        // Using safe default empty delegates eliminates initialization warnings
        public event Action<string>? OnLogReceived;
        public event Action<bool>? OnStateChanged;

        public async Task ExecutePipelineAsync(string pythonExePath, string mainScriptPath, string configPath)
        {
            OnStateChanged?.Invoke(true); 
            _cts = new CancellationTokenSource();

            if (!File.Exists(mainScriptPath))
            {
                OnLogReceived?.Invoke($"[CRITICAL ERROR] Core engine orchestrator not found at: {mainScriptPath}");
                OnStateChanged?.Invoke(false);
                return;
            }

            var token = _cts.Token;

            await Task.Run(async () =>
            {
                try
                {
                    var startInfo = new ProcessStartInfo
                    {
                        FileName = pythonExePath,
                        Arguments = $"-u \"{mainScriptPath}\" --config \"{configPath}\"",
                        WorkingDirectory = Path.GetDirectoryName(mainScriptPath) ?? string.Empty, 
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        StandardOutputEncoding = Encoding.UTF8,
                        StandardErrorEncoding = Encoding.UTF8
                    };

                    // 🔬 FORCE PYTHON TO RUN IN FULL UTF-8 MODE (Eliminates charmap crashes)
                    startInfo.EnvironmentVariables["PYTHONUTF8"] = "1";

                    _backendProcess = new Process { StartInfo = startInfo };
                    _backendProcess.Start();

                    // Run the streams concurrently to prevent buffer deadlocks
                    Task readOutput = ReadStreamAsync(_backendProcess.StandardOutput, token);
                    Task readError = ReadStreamAsync(_backendProcess.StandardError, token);

                    await Task.WhenAll(readOutput, readError);
                }
                catch (Exception ex)
                {
                    OnLogReceived?.Invoke($"[SYSTEM RUNTIME EXCEPTION] {ex.Message}");
                }
                finally
                {
                    TeardownProcess();
                }
            }, token);
        }

        private async Task ReadStreamAsync(StreamReader reader, CancellationToken token)
        {
            // peak/read loops safely handle async text lines without blocking CA2024 exceptions
            while (!token.IsCancellationRequested)
            {
                string? line = await reader.ReadLineAsync(token);
                if (line == null) break; 
                OnLogReceived?.Invoke(line);
            }
        }

        // Inside TalentSource.Desktop.Services.ProcessBridge class
        public async Task OpenTargetFileAsync(string pythonExePath, string mainScriptPath)
        {
            if (!File.Exists(mainScriptPath))
            {
                OnLogReceived?.Invoke($"[CRITICAL ERROR] Core engine orchestrator not found at: {mainScriptPath}");
                return;
            }

            await Task.Run(() =>
            {
                try
                {
                    var startInfo = new ProcessStartInfo
                    {
                        FileName = pythonExePath,
                        Arguments = $"-u \"{mainScriptPath}\" --edit-spec",
                        WorkingDirectory = Path.GetDirectoryName(mainScriptPath) ?? string.Empty,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        StandardOutputEncoding = Encoding.UTF8,
                        StandardErrorEncoding = Encoding.UTF8
                    };

                    using var process = new Process { StartInfo = startInfo };
                    process.Start();

                    // Read potential quick diagnostics inline
                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();
                    process.WaitForExit();

                    if (!string.IsNullOrWhiteSpace(output)) OnLogReceived?.Invoke(output.Trim());
                    if (!string.IsNullOrWhiteSpace(error)) OnLogReceived?.Invoke($"[ERROR] {error.Trim()}");
                }
                catch (Exception ex)
                {
                    OnLogReceived?.Invoke($"[SYSTEM RUNTIME EXCEPTION] File open failed: {ex.Message}");
                }
            });
        }


        public void TerminatePipeline()
        {
            OnLogReceived?.Invoke("\r\n[USER ACTION] Halting active customization pipeline forcibly...");
            _cts?.Cancel();
            TeardownProcess();
        }

        private void TeardownProcess()
        {
            try
            {
                if (_backendProcess != null && !_backendProcess.HasExited)
                {
                    _backendProcess.Kill(true); 
                }
            }
            catch { /* Catch race cleanup conditions */ }
            finally
            {
                _backendProcess?.Dispose();
                _backendProcess = null;
                OnStateChanged?.Invoke(false); 
            }
        }
    }
}
