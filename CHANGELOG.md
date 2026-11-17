# Changelog

All notable changes to the **AI CV Generator** project achieved during today's restructuring and optimization sprints are documented below.

## [2026-11-16]

### Added
* **Structural Modularization:** Refactored the repository root directory into explicit standalone spaces: `Back_End/` for core processing and `Front_End/` for user interfaces.
* **Cognitive Templates System:** Created `Back_End/config/cognitive_templates.yaml` to decouple system prompts, structured instructions, and behavioral goals from execution logic.
* **Diagnostics Suite:** Introduced an integrated monitoring layer under `src/diagnostics/` containing `analyzer.py` and `telemetry.py` to handle structural validation passes and pipeline logs.
* **Front-End GUI Scaffolding:** Added `Front_End/generate_cv_gui.ps1` to serve as the application's primary visual wrapper, establishing cleaner integration points between Windows environments and backend engines.

### Fixed
* **Path Resolution Bug:** Resolved a critical cache routing flaw where `extractor.py` was pulling stale files from the `.data_cache/` folder instead of matching current workspace settings when `enforce_local_cache: false` was declared.
* **Hardcoded String Cleanup:** Eliminated rigid strings across code paths in favor of configuration files loaded out of `Back_End/config/`.
* **Worker Function Collisions:** Refactored initialization handshakes between `llm_service.py` and structural modules, removing duplicate file loading routines and enforcing singular file assignments.
