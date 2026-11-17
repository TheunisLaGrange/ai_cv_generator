# 📄 AI CV Generator

A modular Python pipeline powered by **Google Gemini** that tailors CVs to specific job specifications using evidence-based prompting, smart local caching, and automated ReportLab/PyPDF document compilation.

## ✨ Key Features

* **🔒 Strict Data & Logic Separation:** Keeps personal CV data, job specifications, and qualification certificates isolated inside `User_Data/` (ignored by Git) while storing generated artifacts in `Output/`.
* **🏗️ Refactored Architecture:** Clean separation of concerns with a standalone Python `Back_End/` engine and a Windows PowerShell `Front_End/` GUI wrapper.
* **🧠 Cognitive Templating:** Decouples prompt engineering from application code by routing text orchestration through configuration files (`config/cognitive_templates.yaml`).
* **🎯 Evidence-Based AI Tailoring:** Uses structured Pydantic schemas and anti-hallucination guardrails to filter, reorder, and rephrase your **Professional Profile** and **Key Skills** to match target job descriptions without fabricating experience.
* **⚡ Dual-Mode Local Caching:** Supports both static cache overrides (`enforce_local_cache: true`) and SHA-256 content-hashed dynamic disk caching to eliminate redundant API calls during testing.
* **📊 Integrated Telemetry & Diagnostics:** Embedded system tracking (`diagnostics/`) that runs runtime schema validations and telemetry traces to audit LLM pipeline execution.
* **📑 Automated Dual-PDF Compilation:** Generates a clean, ATS-friendly base CV via **ReportLab** (`*_without_qualifications.pdf`) and automatically merges supporting credential PDFs via **PyPDF** (`*_with_qualifications.pdf`).

## 🏗️ Project Structure

```text
ai_cv_generator/
├── Back_End/                   # 🐍 Python Pipeline Engine
│   ├── .data_cache/            # ⚡ Content-hashed dynamic disk cache
│   ├── config/
│   │   ├── agent_config.yaml       # ⚙️ Model selection, path settings, and cache flags
│   │   └── cognitive_templates.yaml # 🧠 Decoupled system prompts and LLM templates
│   ├── sandbox/
│   │   └── app_sandbox.py          # 🧪 Execution harness and pipeline sandbox
│   ├── src/
│   │   ├── core/
│   │   │   ├── llm_service.py      # 🧠 Cache router and core pipeline coordinator
│   │   │   └── workers/
│   │   │       ├── extractor.py    # 📥 Input loader (fixes cached path isolation bugs)
│   │   │       ├── optimizer.py    # 🤖 Asynchronous Gemini validation & Pydantic parsing
│   │   │       └── compiler.py     # 🖨️ ReportLab layout engine & PyPDF merger
│   │   └── diagnostics/            # 📊 Telemetry and Auditing Layer
│   │       ├── analyzer.py         # 🔍 Validation engine for structured data
│   │       └── telemetry.py        # 📋 System log and performance tracking
│   └── main.py                 # 🚀 Python backend entry point
├── Front_End/                  # 🖥️ User Interface Layer
│   └── generate_cv_gui.ps1     # 💎 WPF-based Windows PowerShell GUI wrapper
├── Sample_User_Data/           # 📋 Ready-to-use mock dataset for testing
│   ├── job_spec.txt
│   ├── my_cv.json
│   └── user_profile.json
├── User_Data/                  # 🔒 Private User Repository (Git Ignored)
│   ├── Qualifications/         # 🎓 Certificates and trade credentials
│   ├── job_spec.txt
│   ├── my_cv.json
│   └── user_profile.json
├── Output/                     # 📂 Production Outputs & Compiled PDF Artifacts
├── requirements.txt            # 📦 Python package dependencies
└── LICENSE                     # ⚖️ MIT License
```

## 🚀 Quick Start

### 1. 📦 Clone and Install Dependencies
```bash
git clone https://github.com
cd ai_cv_generator/Back_End
python -m venv .venv
.venv\Scripts\activate
pip install -r ../requirements.txt
```

### 2. 🔑 Configure Your Gemini API Key
Create a `.env` file inside `Back_End/` and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. 📂 Set Up Your User Data
Ensure your input documents match the directory setup:
* 📝 Edit `User_Data/my_cv.json` with your experience, custom JSON formats, and skills.
* 👤 Edit `User_Data/user_profile.json` with certificate names and PDF naming options.
* 🎓 Place supporting credential PDFs inside `User_Data/Qualifications/`.
* 📌 Paste the target job advertisement into `User_Data/job_spec.txt`.

### 4. ▶️ Run the Generator
Launch the standalone backend:
```bash
python main.py
```
Or execute the user interface from the root directory:
```powershell
./Front_End/generate_cv_gui.ps1
```

## ⚙️ Configuration (`Back_End/config/agent_config.yaml`)

* **`enforce_local_cache: false`** *(Default)*: Evaluates an active SHA-256 hash comparison across `job_spec.txt` + `my_cv.json`. Queries live Gemini endpoints only on cache misses.
* **`enforce_local_cache: true`**: Locks data loading to `.data_cache/my_cache.json` for rapid, offline layout changes, report validation, and PDF styling fixes.
