# 📄 AI CV Generator

A modular Python pipeline powered by **Google Gemini** that tailors CVs to specific job specifications using evidence-based prompting, smart local caching, and automated ReportLab/PyPDF document compilation.

## ✨ Key Features

* **🔒 Strict Data & Logic Separation:** Keeps personal CV data, job specifications, and qualification certificates isolated inside `User_Data/` (ignored by Git) while storing generated artifacts in `Output/`.
* **🎯 Evidence-Based AI Tailoring:** Uses structured Pydantic schemas and anti-hallucination guardrails to filter, reorder, and rephrase your **Professional Profile** and **Key Skills** to match target job descriptions without fabricating experience.
* **⚡ Dual-Mode Local Caching:** Supports both static cache overrides (`enforce_local_cache: true`) and SHA-256 content-hashed dynamic disk caching to eliminate redundant API calls during testing.
* **📑 Automated Dual-PDF Compilation:** Generates a clean, ATS-friendly base CV via **ReportLab** (`*_without_qualifications.pdf`) and automatically merges supporting credential PDFs via **PyPDF** (`*_with_qualifications.pdf`).

## 🏗️ Project Structure

```text
ai_cv_generator/
├── config/
│   └── agent_config.yaml       # ⚙️ Model selection and caching behavior flags
├── sandbox/
│   └── app_sandbox.py          # 🧪 Execution harness and step verification
├── Sample_User_Data/           # 📋 Ready-to-use mock dataset for testing
│   ├── job_spec.txt
│   ├── my_cv.json
│   └── user_profile.json
├── src/
│   └── core/
│       ├── llm_service.py      # 🧠 Cache router, key normalization, and pipeline orchestration
│       └── workers/
│           ├── extractor.py    # 📥 Loads and validates input JSON/text files
│           ├── optimizer.py    # 🤖 Asynchronous Gemini prompting & Pydantic parsing
│           └── compiler.py     # 🖨️ ReportLab layout engine & PyPDF certificate merger
├── main.py                     # 🚀 Application entry point
├── requirements.txt            # 🐍 Python package dependencies
├── LICENSE                     # ⚖️ MIT License
└── .gitignore                  # 🙈 Excludes .env, User_Data/, Output/, and .data_cache/
```

## 🚀 Quick Start

### 1. 📦 Clone and Install Dependencies
```bash
git clone https://github.com
cd ai_cv_generator
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 🔑 Configure Your Gemini API Key
Create a `.env` file in the project root and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. 📂 Set Up Your User Data
Copy the contents of `Sample_User_Data/` into a new `User_Data/` folder in the project root:
```powershell
Copy-Item -Path "Sample_User_Data" -Destination "User_Data" -Recurse
```
* 📝 Edit `User_Data/my_cv.json` with your personal details, experience, and skills.
* 👤 Edit `User_Data/user_profile.json` with your desired output filename prefix and certificate PDF filenames.
* 🎓 Place any supporting certificate PDFs inside `User_Data/Qualifications/`.
* 📌 Paste the target job advertisement into `User_Data/job_spec.txt`.

### 4. ▶️ Run the Generator
```bash
python main.py
```
Generated outputs (`target.json`, `<Name>_without_qualifications.pdf`, and `<Name>_with_qualifications.pdf`) will be written to the `Output/` directory.

## ⚙️ Configuration (`config/agent_config.yaml`)

* **`enforce_local_cache: false`** *(Default)*: Checks `.data_cache/` for a matching hash of `job_spec.txt` + `my_cv.json`. Calls the live Gemini endpoint on a cache miss and saves the response for future runs.
* **`enforce_local_cache: true`**: Bypasses live API calls and loads `.data_cache/my_cache.json` directly for offline layout and PDF testing.
