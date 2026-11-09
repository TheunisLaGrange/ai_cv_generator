# =====================================================================
# 🧪 PRISTINE APPLICATION SANDBOX ENTRY POINT
# =====================================================================
import yaml
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent

# Inject project root path into python system search records
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.chdir(PROJECT_ROOT)
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Import your unified Traffic-Cop Orchestration Class directly
from src.core.llm_service import LLMService
from src.diagnostics.telemetry import StepTrace

async def run_sandbox_validation():
    print("🔬 Sandbox Environment: Spawning core system orchestrator...")
    
    # 1. Load your local agent configuration matrix rules
    import yaml
    with open(PROJECT_ROOT / "config" / "agent_config.yaml", "r") as f:
        config = yaml.safe_load(f)
        
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
