# Changelog

All notable changes to the **AI CV Generator** project achieved during the decoupling, restructuring, and interface optimization sprints are documented below.

## [Unreleased] - 2026-11-19

### Added
- **Asynchronous CV Review Switch**: Implemented a new structural CLI argument switch `--edit-cv` inside the Python orchestrator engine (`main.py`) to launch local JSON profile data streams.
- **WPF Asset Integration Switch**: Added the interactive `OPEN MY CV JSON` flat control button into the desktop layout matrix (`MainWindow.xaml`) pointing directly to `my_cv.json` within the secure user profile repository.
- **Dynamic Character Refactoring Filter**: Integrated a robust regular expression markup filtering system (`clean_text_for_reportlab`) into the PDF production engine workflow (`compiler.py`) to catch, rewrite, and parse chemical formulas (like $CO_2$) and algebraic metrics (like $M^2$) seamlessly.

### Changed
- **Decoupled Bridge Interface**: Refactored the generic desktop background tasks infrastructure handler (`ProcessBridge.cs`) to dynamically pass structural asset-tracking flags (`--edit-spec`, `--edit-cv`) into background processes instead of binding rigid hardcoded paths locally.
- **Scope Initialization Bounds**: Cleaned up the cross-thread context layout at the top of the desktop view layer class file, linking runtime configuration keys to uniform shared static field bounds.
- **Data Scrubbing Order of Operations**: Adjusted document parsing loops inside `compiler.py` to ensure raw structural metadata configurations are applied securely to dynamic source fields before wrapping them inside layout flowable strings.

### Fixed
- **CLI Validation Fallback Loop**: Corrected a fallback exception route where omitting pipeline switches caused background routines to stall on text manuals inside the active terminal view.
- **Escaped XML String Corruption**: Eliminated a layout bug causing text labels like "Address", "Cell", and "Mail" to be stripped out as broken HTML code strings instead of rendering as clean, crisp bold fonts.

## [2026-11-18]

### Added
* **C# WPF Desktop Dashboard:** Engineered a high-performance, thread-safe presentation layer application to act as the primary structural interface for engine control loops.
* **Asynchronous Process Bridge:** Implemented an event-driven, non-blocking execution driver (`ProcessBridge.cs`) running concurrent `StreamReader` tasks to pipe real-time engine telemetry straight into UI terminal viewports.
* **Native Immersive Dark Mode:** Added direct interop bindings targeting the Windows kernel `dwmapi.dll` subsystem, transforming the standard white operating system title bar chrome into a charcoal aesthetic.
* **Pre-Processing Utility Worker:** Created a modular file execution framework (`src/utils/file_opener.py`) to decouple pre-run document modifications from generation run paths.
* **Embedded Resource Compilation:** Configured explicit assembly tracking patterns (`.csproj`) to inject profile branding items and icon resources directly into output binaries.
* **Unified CLI Configuration Switch:** Re-architected `main.py` into an argument-driven entry point controller supporting explicit route handling flags (`--edit-spec`, `--run-pipeline`, `--config`).

### Fixed
* **Terminal Redirection Character Crashes:** Eliminated cross-process encoding exceptions by forcing an explicit `PYTHONUTF8` system environment override and purging high-order emoji characters from console streams.
* **UI Thread Deadlocks:** Wrapped interprocess tasks into discrete `Task.Run` execution wrappers, using marshaled thread dispatchers (`Dispatcher.Invoke`) to update logging outputs safely without freezing user interactions.
* **XML Layout Balance Flaws:** Resolved a critical WPF build failure by ensuring proper closing balancing pairs across nested button template resource dictionaries.

## [2026-11-16]

### Added
* **Structural Modularization:** Refactored the repository root directory into explicit standalone spaces: `Back_End/` for core processing and `Front_End/` for user interfaces.
* **Cognitive Templates System:** Created `Back_End/config/cognitive_templates.yaml` to decouple system prompts, structured instructions, and behavioral goals from execution logic.
* **Diagnostics Suite:** Introduced an integrated monitoring layer under `src/diagnostics/` containing `analyzer.py` and `telemetry.py` to handle structural validation passes and pipeline logs.

### Fixed
* **Path Resolution Bug:** Resolved a critical cache routing flaw where `extractor.py` was pulling stale files from the `.data_cache/` folder instead of matching current workspace settings when `enforce_local_cache: false` was declared.
* **Hardcoded String Cleanup:** Eliminated rigid strings across code paths in favor of configuration files loaded out of `Back_End/config/`.
