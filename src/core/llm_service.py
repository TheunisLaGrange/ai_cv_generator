import os
import json
import hashlib
from typing import Dict, List, Any
from pathlib import Path
from google import genai
from src.diagnostics.telemetry import StepTrace

# Import specialized atomic task components from your package folder
from src.core.workers.extractor import load_cv_source_data
from src.core.workers.optimizer import run_cognitive_pipeline
from src.core.workers.compiler import compile_document_package

class LLMService:
    """Central traffic coordinator directing conditional caching and live data pipelines."""
    
    def __init__(self, config: dict):
        self.config = config
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable is unassigned.")
        self.client = genai.Client(api_key=api_key)
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.cache_dir = self.base_dir / ".data_cache"

    def _calculate_content_hash(self, job_spec_text: str, cv_text: str) -> str:
        combined = (job_spec_text + cv_text).encode("utf-8")
        return hashlib.md5(combined).hexdigest()

    async def generate_plan(self, objective: str) -> List[str]:
        """🌟 UPDATED: Defines the fixed 3-stage execution plan to match our worker file architecture."""
        print(f"[Engine Core] Instantiating synchronized CV customization trajectory stages...")
        return [
            "Fetch and read local job_spec.txt and my_cv.json source files",
            "Process profile rewrite and extract technical skills via structured AI schemas",
            "Generate compiled target JSON dataset and compile tailored PDF application bundle"
        ]


    async def execute_step(self, step: str, trace: StepTrace) -> Dict[str, Any]:
        model_name = self.config["llm"]["worker_model"]
        self.cache_dir.mkdir(exist_ok=True)
        cache_enforced = self.config.get("enforce_local_cache", False)

        try:
            # 1. Extract dynamic metadata straight from your master CV database
            source_data = load_cv_source_data(self.base_dir)
            my_cv_data = source_data["my_cv"]
            raw_experience_only = my_cv_data.get("Professional Experience", [])

            # =====================================================================
            # 🛡️ LIFECYCLE CONDITIONAL DATA CACHE ROUTER
            # =====================================================================
            if cache_enforced:
                static_cache_path = self.cache_dir / "my_cache.json"
                data_source_label = f"STATIC CACHE ({static_cache_path.name})"
                print(f"🎯 Configuration Mandate: Local Cache Enforced. Loading: {static_cache_path.name}")
                with open(static_cache_path, "r", encoding="utf-8") as f:
                    ai_generated_payload = json.load(f)
            else:
                fingerprint = self._calculate_content_hash(source_data["job_spec"], json.dumps(my_cv_data))
                dynamic_cache_path = self.cache_dir / f"cache_{fingerprint}.json"
                
                if dynamic_cache_path.exists():
                    data_source_label = f"DYNAMIC DISK CACHE ({dynamic_cache_path.name})"
                    print(f"🎯 Dynamic Cache Hit! Loading text vectors: {dynamic_cache_path.name}")
                    with open(dynamic_cache_path, "r", encoding="utf-8") as f:
                        ai_generated_payload = json.load(f)
                else:
                    data_source_label = f"LIVE GEMINI API ({model_name})"
                    print(f"🌐 Dynamic Cache Miss. Dispatching requests to live endpoint: [{model_name}]...")
                    ai_generated_payload = await run_cognitive_pipeline(self.client, model_name, source_data)
                    with open(dynamic_cache_path, "w", encoding="utf-8") as f:
                        json.dump(ai_generated_payload, f, indent=4)
                    print("💾 Live AI response successfully cached to local disk.")

            # =====================================================================
            # 🧠 🛠️ CASE-INSENSITIVE & SPACE-NORMALIZED RESOLUTION LAYER
            # =====================================================================
            clean_payload = {k.lower().strip().replace(" ", "_"): v for k, v in ai_generated_payload.items()}
            
            # Strictly require AI/Cache arrays and fail loudly if missing
            if "professional_profile" not in clean_payload or not clean_payload["professional_profile"]:
                raise ValueError(f"Missing 'professional_profile' in payload keys: {list(clean_payload.keys())}")
            if "key_skills_and_technical_expertise" not in clean_payload or not clean_payload["key_skills_and_technical_expertise"]:
                raise ValueError(f"Missing 'key_skills_and_technical_expertise' in payload keys: {list(clean_payload.keys())}")

            profile_array = clean_payload["professional_profile"]
            skills_array = clean_payload["key_skills_and_technical_expertise"]

            # =====================================================================
            # 🔍 DIAGNOSTIC SOURCE LINEAGE REPORT
            # =====================================================================
            print("\n📊 [DIAGNOSTIC SOURCE REPORT]")
            print(f"   • Active Payload Origin : {data_source_label}")
            print(f"   • Professional Profile  : Loaded {len(profile_array)} items from [{data_source_label}]")
            print(f"   • Key Skills & Expertise: Loaded {len(skills_array)} items from [{data_source_label}]")
            print(f"   • Experience & Contact  : Loaded directly from [my_cv.json]\n")

            # Assemble unified structural target json dataset
            final_target_json = {
                "Contact Details": my_cv_data.get("Contact Details", {}),
                "Professional Profile": profile_array,
                "Key Skills and Technical Expertise": skills_array,
                "Professional Experience": raw_experience_only,
                "Education & Certifications": my_cv_data.get("Education & Certifications", []),
                "Core Competencies": my_cv_data.get("Core Competencies", []),
                "Languages": my_cv_data.get("Languages", [])
            }

            output_dir = self.base_dir / "Output"
            output_dir.mkdir(exist_ok=True)

            target_json_path = output_dir / "target.json"
            with open(target_json_path, 'w', encoding='utf-8') as f:
                json.dump(final_target_json, f, indent=4)
            print(f"   ✅ Dynamic target.json written cleanly to: {target_json_path}")

            # 4. Pass the compiled dataset and user profile metadata to the compiler
            compile_document_package(self.base_dir, final_target_json, source_data["user_profile"])

            
            trace.status = "SUCCESS"
            return {"status": "cv_twins_compiled_successfully"}

        except Exception as e:
            trace.status = "CRITICAL_ERROR"
            trace.diagnostic_msg = f"Orchestration pipeline failure: {str(e)}"
            return {}
