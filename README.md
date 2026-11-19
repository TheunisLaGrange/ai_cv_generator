# 📄 AI CV Generator & Optimization Matrix

A highly modular, decoupled cross-platform pipeline that tailors professional CVs to target job specifications using evidence-based prompt engineering, content-hashed disk caching, and automated ReportLab document compilation. The system interfaces with a high-performance C# desktop control deck.

## ⚙️ Core Architecture Matrix

- **Frontend Desktop Tier**: Implemented with C# / .NET / WPF, providing a dark-themed control surface utilizing native DWM immersive design characteristics. It hooks into background process streams asynchronously using dynamic process bridge handlers.
- **Cognitive Execution Layer**: Powered by ultra-low latency Groq API cloud infrastructure running single-pass contextual mappings. It processes data using highly optimized schemas defined in local configuration templates.
- **Document Compiling Engine**: Constructed with ReportLab and PyPDF, mapping customized data vectors cleanly to dynamic PDF flowables while automatically bundling verified certification files found on local disk.

## ✨ Key Features

* **🔒 Strict Data & Logic Separation:** Personal background metrics, target specifications, and certificate documents are strictly containerized inside `User_Data/` (fully ignored by source control tracking).
* **🏗️ Production-Grade Architecture:** Clean separation of concerns featuring an independent Python `Back_End/` runtime engine and a native C# WPF desktop control layout (`Front_End/`) running an asynchronous interprocess execution bridge.
* **🖥️ Immersive Dark-Mode Interface:** A thread-safe WPF dashboard window utilizing direct Windows DWM interop to enforce dark-themed system title bars and custom profile icon embeddings.
* **🧠 Cognitive Templating:** Decouples prompt orchestration from core application code by moving structural instructions, personas, and targets out into dedicated layout configuration profiles (`config/cognitive_templates.yaml`).
* **⚡ Content-Hashed Local Caching:** Combines static data-cache locks (`enforce_local_cache: true`) with automated SHA-256 validation comparisons over raw text arrays to entirely eliminate redundant remote AI API call metrics during document styling passes.
* **📂 Fluid Workflow Utilities:** Standalone internal processing tools (`src/utils/file_opener.py`) that trigger safe, non-blocking OS kernel level handshakes to initialize document modification windows directly from front-end control buttons.
* **📑 Automated Dual-PDF Compilation:** Synthesizes an ATS-compliant base document via **ReportLab** (`*_without_qualifications.pdf`) and leverages **PyPDF** to intelligently bind verified credential portfolios (`*_with_qualifications.pdf`) instantly.

## 🏗️ Project Structure

```text
ai_cv_generator/
├── Back_End/                       # 🐍 Python Core Pipeline Engine
│   ├── .data_cache/                # ⚡ Content-hashed dynamic disk cache
│   ├── config/
│   │   ├── agent_config.yaml       # ⚙️ Model runtime selection, tracking paths, and flags
│   │   └── cognitive_templates.yaml # 🧠 Decoupled system prompts and LLM templates
│   ├── sandbox/
│   │   └── app_sandbox.py          # 🧪 Execution harness and pipeline validation sandbox
│   ├── src/
│   │   ├── core/
│   │   │   ├── workers/
│   │   │   │   ├── compiler.py     # 🖨️ ReportLab layout engine & PyPDF merger
│   │   │   │   ├── extractor.py    # 📥 Input loader (resolves workspace path mappings)
│   │   │   │   └── optimizer.py    # 🤖 Asynchronous Gemini validation & Pydantic parsing
│   │   │   ├── engine.py
│   │   │   ├── llm_service.py      # 🧠 Cache router and pipeline execution coordinator
│   │   │   └── state.py
│   │   ├── diagnostics/            # 📊 Telemetry and Auditing Layer
│   │   │   ├── analyzer.py         # 🔍 Validation engine for structured datasets
│   │   │   └── telemetry.py        # 📋 System log tracking and runtime metrics
│   │   └── utils/                  # 🛠️ Independent Shared Utility Packages
│   │       └── file_opener.py      # 📂 Native OS application wrapper utility
│   └── main.py                     # 🚀 Central Traffic Cop & Command Line Router
├── Front_End/                      # 🖥️ Client User Interface Tiers
│   └── TalentSource.Desktop/       # 💻 Native C# WPF Desktop Control Deck Application
│       ├── Assets/                 # 🎨 Embedded application graphics and branding resources
│       ├── Services/
│       │   └── ProcessBridge.cs    # 🌉 Asynchronous thread-safe interprocess execution engine
│       ├── Views/
│       │   ├── MainWindow.xaml     # 🎨 Layout definitions and custom element components
│       │   └── MainWindow.xaml.cs  # 🧠 UI business logic and DWM platform interop
│       └── TalentSource.Desktop.csproj
├── pipeline/                       # ⚙️ DevOps Automation & Continuous Integration Framework
│   ├── build_release.ps1           # 📦 Automation script for compilation assets
│   ├── step_4_preflight_audit.ps1  # 🔍 Pre-release code evaluation pass script
│   └── step_5_push_project.ps1     # 🚀 Core system configuration sync script
├── User_Data/                      # 🔒 Private User Repository (Git Ignored Context)
│   ├── Qualifications/             # 🎓 Trade credentials and certificate documents
│   └── job_spec.txt                # 📌 Target job description advertisement text asset
├── Output/                         # 📂 Production Outputs & Compiled PDF Artifacts
└── requirements.txt                # 📦 Python package dependency manifests
```

## 🚀 Quick Start

### 1. 📦 Set Up the Python Environment
```powershell
cd ai_cv_generator/Back_End
python -m venv .venv
.venv\Scripts\activate
pip install -r ../requirements.txt
```

### 2. 🔑 Configure Environment Settings
Create a `.env` file inside `Back_End/` to store your credentials safely:
```env
GROQ_API_KEY=your_grok_gemini_api_key_here
```

### 3. 🖥️ Launch the Desktop Control Deck
Navigate into your front-end view directory path and fire up the interface controller:
```powershell
cd ../Front_End/TalentSource.Desktop
dotnet run
```

## 🚀 Execution & Command Line Interfaces

The backend engine parses runtime tasks using Python's standard argument libraries to enforce strict separation of program logic and configuration boundaries:

```bash
# Display core operational manual text
python main.py -h

# Execute automated extraction and customization matrix pipelines
python main.py --run-pipeline --config "path/to/config.yaml"

# Open the job specification text asset for manual preparation
python main.py --edit-spec

# Open the profile JSON asset for manual verification
python main.py --edit-cv
```

## 🛠️ Environmental Settings

To maintain stability across modern system architectures, the execution engine forces internal pipelines into absolute UTF-8 operating modes (`PYTHONUTF8=1`), neutralizing common character-map conversion crashes when processing complex engineering characters like $CO_2$ or custom hyphens.