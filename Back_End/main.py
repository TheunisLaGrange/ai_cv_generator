import argparse
import asyncio
import os
import platform
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
import yaml

# =====================================================================
# 🔬 DETERMINISTIC TIERS WORKSPACE ANCHORING
# =====================================================================
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

# Inject paths into runtime lookups to allow seamless cross-tier package visibility
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(1, str(BACKEND_DIR))

# Securely bind local environment credentials
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# =====================================================================
# 📦 UNIFIED ROOT MODULE IMPORTS
# =====================================================================
from src.core.llm_service import LLMService
from src.diagnostics.telemetry import StepTrace
from src.utils.file_opener import open_target_file


async def run_pipeline_orchestration(config_path_override=None):
    """Executes the automated extraction and customization pipeline."""
    print("🔬 Engine Environment: Spawning core system orchestrator...")
    
    # Use C# custom config path if provided, fallback to default configuration
    if config_path_override:
        absolute_config_path = Path(config_path_override).resolve()
    else:
        absolute_config_path = BACKEND_DIR / "config" / "agent_config.yaml"

    print(f"🎯 Loading configuration blueprint from: {absolute_config_path}")
    
    if not absolute_config_path.exists():
        print(f"❌ CRITICAL CONFIG CONFIGURATION NOT FOUND: {absolute_config_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(absolute_config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    # Instantiate the core coordinator cleanly
    service = LLMService(config=config)
    
    # Create the standalone tracer context node
    trace_node = StepTrace(step_name="Compile tailored PDF bundle", step_index=0)
    
    # Dispatches execution flow downstream to the orchestration matrix loop
    print("🚀 Triggering execute_step loop...")
    result = await service.execute_step("Process and compile final PDF bundle", trace_node)
    
    if trace_node.status == "SUCCESS":
        print("\n🎉 PIPELINE TASK VERIFICATION CLEARED SUCCESSFULLY!")
    else:
        # Check if the diagnostic message contains the 503 or UNAVAILABLE error
        diag_str = str(trace_node.diagnostic_msg)
        if "503" in diag_str or "UNAVAILABLE" in diag_str:
            print("\n⚠️  API SERVER ERROR: The live Gemini AI model is experiencing high demand.", file=sys.stderr)
            print("👉 [Free Tier Rate Limit]: This spike is temporary. Please wait a minute and try again.\n", file=sys.stderr)
        else:
            print(f"\n❌ Pipeline Step Failed: {trace_node.diagnostic_msg}", file=sys.stderr)
            
        sys.exit(69)


def main():
    # Build a robust CLI interface using Python's standard argument library
    parser = argparse.ArgumentParser(
        description="TalentSource Process Orchestration Engine Backend"
    )

    # Core workflow state toggle switches
    parser.add_argument(
        "--edit-spec",
        action="store_true",
        help="Open the job specification text asset for manual verification/modification",
    )
    parser.add_argument(
        "--run-pipeline",
        action="store_true",
        help="Execute automated extraction and customization matrix pipelines",
    )
    
    # Dynamic configuration parameter input
    parser.add_argument(
        "--config",
        type=str,
        help="Explicit physical path to a target configuration layout profile yaml",
    )

    args = parser.parse_args()

    # Pre-processing Step: Open file for editing
    if args.edit_spec:
        # Safely anchor to your isolated User_Data block relative to the project root
        target_job_spec = PROJECT_ROOT / "User_Data" / "job_spec.txt"
        
        # 🎯 CHANGED: Replaced the folder emoji with a safe bracket label [File]
        print(f"[File] Requesting OS application handler for: {target_job_spec}")
        
        try:
            open_target_file(str(target_job_spec))
            print("Handshake Success: File successfully launched for manual preparation.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error during manual file deployment: {e}", file=sys.stderr)
            sys.exit(1)

    # Core Operational Step: Run the AI pipeline
    elif args.run_pipeline:
        asyncio.run(run_pipeline_orchestration(config_path_override=args.config))
        
    # Boundary Exception: No matching command parameters provided
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
