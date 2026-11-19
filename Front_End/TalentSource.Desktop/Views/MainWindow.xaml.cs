using System;
using System.Runtime.InteropServices; // 🔍 REQUIRED FOR WINDOWS DWM CALLS
using System.Windows;
using System.Windows.Interop;         // 🔍 REQUIRED FOR WINDOWS INTEROP
using System.Windows.Media;
using TalentSource.Desktop.Services;

namespace TalentSource.Desktop.Views
{
    public partial class MainWindow : Window
    {
        private readonly ProcessBridge _bridge;
        private bool _isPipelineRunning;

        // --- Native DWM Dark Mode Declarations ---
        [DllImport("dwmapi.dll")]
        private static extern int DwmSetWindowAttribute(IntPtr hwnd, int attr, ref int attrValue, int attrSize);

        private const int DWMWA_USE_IMMERSIVE_DARK_MODE = 20;
        // ----------------------------------------

        private const string PythonPath = @"C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe";
        private const string ScriptPath = @"C:\PC Programming\Python\src\AI\Agent\02_Python_Source\ai_cv_generator\Back_End\main.py";
        private const string ConfigPath = @"C:\PC Programming\Python\src\AI\Agent\02_Python_Source\ai_cv_generator\Back_End\config\agent_config.yaml";
        
        public MainWindow()
        {
            InitializeComponent();
            
            _bridge = new ProcessBridge();
            _bridge.OnLogReceived += UpdateTerminalLog;
            _bridge.OnStateChanged += UpdateInterfaceState;

            // 🎯 Enforce Native Windows Dark Mode on Window Loading
            SourceInitialized += MainWindow_SourceInitialized;
        }

        private void MainWindow_SourceInitialized(object? sender, EventArgs e)
        {
            var hwnd = new WindowInteropHelper(this).Handle;
            int useDarkMode = 1; // 1 = True (Enforce Dark Mode)
            DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ref useDarkMode, sizeof(int));
        }

        // ... Keep the rest of your existing click handlers and methods completely unchanged ...
        private async void PipelineButton_Click(object sender, RoutedEventArgs e)
        {
            if (_isPipelineRunning)
            {
                _bridge.TerminatePipeline();
                return;
            }

            TerminalLogBox.Clear();
            TerminalLogBox.AppendText("[System] Initializing asynchronous C# engine pipeline...\r\n");

            // Execute completely unblocked on its task thread
            await _bridge.ExecutePipelineAsync(PythonPath, ScriptPath, ConfigPath);
        }

        private async void OpenSpecButton_Click(object sender, RoutedEventArgs e)
        {
            // 🎯 FIX: Changed variable names to match your class constants
            await _bridge.OpenAssetFileAsync(PythonPath, ScriptPath, "--edit-spec");
        }

        private async void OpenCVButton_Click(object sender, RoutedEventArgs e)
        {
            // 🎯 FIX: Changed variable names to match your class constants
            await _bridge.OpenAssetFileAsync(PythonPath, ScriptPath, "--edit-cv");
        }


        private void UpdateTerminalLog(string logLine)
        {
            // Thread handshaking: Marshal the text payload back onto the UI thread safely
            Dispatcher.Invoke(() =>
            {
                TerminalLogBox.AppendText(logLine + Environment.NewLine);
                TerminalLogBox.ScrollToEnd();
            });
        }

        // Modify your existing UpdateInterfaceState layout to safely protect active processing run rules:
        private void UpdateInterfaceState(bool isRunning)
        {
            Dispatcher.Invoke(() =>
            {
                _isPipelineRunning = isRunning;
                if (_isPipelineRunning)
                {
                    PipelineButton.Content = "HALT PIPELINE PROCESS";
                    PipelineButton.Background = new SolidColorBrush(Color.FromRgb(180, 40, 40));
                    BypassCacheCheck.IsEnabled = false;
                    OpenSpecButton.IsEnabled = false; // 🔒 Guard from starting changes mid-generation run
                }
                else
                {
                    PipelineButton.Content = "RUN LIVE CUSTOMIZATION PIPELINE";
                    PipelineButton.Background = new SolidColorBrush(Color.FromRgb(42, 42, 42));
                    BypassCacheCheck.IsEnabled = true;
                    OpenSpecButton.IsEnabled = true;  // 🔓 Allow safe editing access again
                }
            });
        }

        protected override void OnClosed(EventArgs e)
        {
            // Wipes the process tree completely if the window shell is terminated abruptly
            _bridge.TerminatePipeline();
            base.OnClosed(e);
        }
    }
}
