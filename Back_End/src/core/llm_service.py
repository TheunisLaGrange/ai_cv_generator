import os
import json
import hashlib
from typing import Dict, List, Any
from pathlib import Path
from groq import AsyncGroq  # 🔄 Swapped from google.genai
from src.diagnostics.telemetry import StepTrace

from src.core.workers.extractor import load_cv_source_data
from src.core.workers.optimizer import run_cognitive_pipeline
from src.core.workers.compiler import compile_document_package

class LLMService:
    """Central traffic coordinator directing conditional caching and live Groq data pipelines."""
    
    def __init__(self, config: dict):
        self.config = config
        
        # 🔑 Authenticate via Groq standard environment keys
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GROQ_API_KEY environment variable is unassigned.")
        self.client = AsyncGroq(api_key=api_key)
        
        self.backend_dir = Path(__file__).resolve().parent.parent.parent
        self.base_dir = self.backend_dir.parent 
        
        self.input_dir = self.base_dir / "User_Data"
        self.output_dir = self.base_dir / "Output"
        self.cache_dir = self.backend_dir / ".data_cache" / "cache"

        templates_path = self.backend_dir / "config" / "cognitive_templates.yaml"
        if not templates_path.exists():
            raise FileNotFoundError(f"Missing required engine templates file: {templates_path}")
            
        with open(templates_path, "r", encoding="utf-8") as f:
            import yaml
            self.cognitive_templates = yaml.safe_load(f)

    def _calculate_content_hash(self, job_spec_text: str, cv_text: str) -> str:
        combined = (job_spec_text + cv_text).encode("utf-8")
        return hashlib.md5(combined).hexdigest()

    async def generate_plan(self, objective: str) -> List[str]:
        return [
            "Fetch and read local source files",
            "Process profile rewrite and extract technical skills via structured AI templates",
            "Generate compiled target JSON dataset and compile tailored PDF application bundle"
        ]

    async def execute_step(self, step: str, trace: StepTrace) -> Dict[str, Any]:
        model_name = self.config["llm"]["worker_model"]
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_enforced = self.config.get("enforce_local_cache", False)

        try:
            source_data = load_cv_source_data(self.base_dir)
            my_cv_data = source_data["my_cv"]
            raw_experience_only = my_cv_data.get("Professional Experience", [])

            # 🛠️ QUICK FIX: Initialize with a safe default fallback string
            data_source_label = "UNKNOWN_SOURCE"

            if cache_enforced:
                static_cache_path = self.cache_dir.parent / "my_cache.json"
                print(f"🎯 Configuration Mandate: Local Cache Enforced. Loading: {static_cache_path.name}")
                with open(static_cache_path, "r", encoding="utf-8") as f:
                    ai_generated_payload = json.load(f)
            else:
                fingerprint = self._calculate_content_hash(source_data["job_spec"], json.dumps(my_cv_data))
                dynamic_cache_path = self.cache_dir / f"cache_{fingerprint}.json"
                
                if dynamic_cache_path.exists():
                    data_source_label = f"DYNAMIC DISK CACHE ({dynamic_cache_path.name})"
                    with open(dynamic_cache_path, "r", encoding="utf-8") as f:
                        ai_generated_payload = json.load(f)
                else:
                    data_source_label = f"LIVE GROQ API ({model_name})"
                    print(f"🌐 Dynamic Cache Miss. Dispatching requests to Groq endpoint: [{model_name}]...")
                    
                    source_data["cognitive_templates"] = self.cognitive_templates
                    
                    # 🚀 Run the single-pass optimized pipeline
                    ai_generated_payload = await run_cognitive_pipeline(
                        self.client, 
                        model_name, 
                        source_data
                    )
                    with open(dynamic_cache_path, "w", encoding="utf-8") as f:
                        json.dump(ai_generated_payload, f, indent=4)
                    print("💾 Live AI response successfully cached to local disk.")

            # =====================================================================
            # 🛡️ UNICODE ARTIFACT SANITIZATION LAYER (Fixes the black block issue)
            # =====================================================================
            def sanitize_text(text: Any) -> Any:
                if isinstance(text, str):
                    # Replace non-breaking hyphens (\u2011) with standard hyphens
                    text = text.replace("\u2011", "-").replace("‑", "-")
                    # Replace narrow non-breaking spaces (\u202f) or generic non-breaking spaces (\u00a0)
                    text = text.replace("\u202f", " ").replace("\u00a0", " ")
                    return text
                elif isinstance(text, list):
                    return [sanitize_text(item) for item in text]
                elif isinstance(text, dict):
                    return {k: sanitize_text(v) for k, v in text.items()}
                return text

            # Sanitize the entire raw AI payload before processing keys
            ai_generated_payload = sanitize_text(ai_generated_payload)
            # =====================================================================

            clean_payload = {k.lower().strip().replace(" ", "_"): v for k, v in ai_generated_payload.items()}
            
            if "professional_profile" not in clean_payload or not clean_payload["professional_profile"]:
                raise ValueError("Missing 'professional_profile' in payload keys.")
            if "key_skills_and_technical_expertise" not in clean_payload or not clean_payload["key_skills_and_technical_expertise"]:
                raise ValueError("Missing 'key_skills_and_technical_expertise' in payload keys.")

            profile_array = clean_payload["professional_profile"]
            skills_array = clean_payload["key_skills_and_technical_expertise"]

            print("\n📊 [DIAGNOSTIC SOURCE REPORT]")
            print(f"   • Active Payload Origin : {data_source_label}")
            print(f"   • Professional Profile  : Loaded {len(profile_array)} items")
            print(f"   • Key Skills & Expertise: Loaded {len(skills_array)} items\n")

            final_target_json = {
                "Contact Details": my_cv_data.get("Contact Details", {}),
                "Professional Profile": profile_array,
                "Key Skills and Technical Expertise": skills_array,
                "Professional Experience": raw_experience_only,
                "Education & Certifications": my_cv_data.get("Education & Certifications", []),
                "Core Competencies": my_cv_data.get("Core Competencies", []),
                "Languages": my_cv_data.get("Languages", [])
            }

            self.output_dir.mkdir(exist_ok=True)
            target_json_path = self.output_dir / "target.json"
            with open(target_json_path, 'w', encoding='utf-8') as f:
                json.dump(final_target_json, f, indent=4)
            print(f"   ✅ Dynamic target.json written cleanly to: {target_json_path}")

            compile_document_package(
                self.base_dir, 
                final_target_json, 
                self.config.get("pdf_preferences", {})
            )
            
            trace.status = "SUCCESS"
            return {"status": "cv_twins_compiled_successfully"}

        except Exception as e:
            trace.status = "CRITICAL_ERROR"
            trace.diagnostic_msg = f"Orchestration pipeline failure: {str(e)}"
            return {"status": "failed", "error": str(e)}
