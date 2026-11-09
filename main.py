import os
import sys
import asyncio
import yaml
from pathlib import Path
from dotenv import load_dotenv

# =====================================================================
# 🔬 CORRECTED ABSOLUTE PATH ANCHORING FOR YOUR PROJECT WORKSPACE
# =====================================================================
# Path(__file__).resolve() targets this exact main.py file.
# .parent gives you C:\PC Programming\Python\src\AI\Agent\ai_cv_generator
PROJECT_ROOT = Path(__file__).resolve().parent

# Inject local project root into system path for clean imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load local environment variables dynamically
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Import system workflow services cleanly
from src.core.llm_service import LLMService
from src.diagnostics.telemetry import StepTrace

async def run_sandbox_validation():
    print("🔬 Sandbox Environment: Spawning core system orchestrator...")
    
    # Target the configuration folder sitting EXACTLY inside this application workspace
    absolute_config_path = PROJECT_ROOT / "config" / "agent_config.yaml"
    print(f"🔍 Loading configuration from: {absolute_config_path}")
    
    with open(absolute_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    service = LLMService(config=config)
    # ... rest of your trajectory execution loop remains untouched ...


    # Now config is loaded cleanly, independent of terminal state or background thread swaps!
    service = LLMService(config=config)

        
    # 2. Instantiate your traffic cop orchestration service engine
    service = LLMService(config=config)
    
    # 3. Simulate and test a live execution step directly through the class
    trace_node = StepTrace(step_name="Compile tailored PDF bundle", step_index=0)
    
    # Trigger the centralized orchestrator to run the entire pipeline
    result = await service.execute_step("Process and compile final PDF bundle", trace_node)
    
    if trace_node.status == "SUCCESS":
        print("\n🎉 SANDBOX TASK VERIFICATION CLEARED SUCCESSFULLY!")
    else:
        print(f"\n❌ Sandbox Step Failed: {trace_node.diagnostic_msg}")

if __name__ == "__main__":
    asyncio.run(run_sandbox_validation())
    input("\n[Sandbox Concluded] Press Enter to exit terminal...")
