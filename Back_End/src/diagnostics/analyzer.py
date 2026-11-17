from typing import List, Dict, Any

class TraceAnalyzer:
    """Responsible solely for visual rendering and diagnostics post-mortems."""
    @staticmethod
    def print_post_mortem(session_id: str, trace_history: List[Dict[str, Any]]):
        print("\n" + "="*60)
        print(f"🕵️ AGENT RUNTIME POST-MORTEM TRACE [Session: {session_id}]")
        print("="*60)
        for entry in trace_history:
            status_symbol = "✅" if entry['status'] == "SUCCESS" else "🚨"
            print(f"{status_symbol} Step {entry['step_index']}: '{entry['step_name']}' -> {entry['status']}")
            if entry['error_code']:
                print(f"   ├─ Error Class:  [{entry['error_code']}]")
                print(f"   └─ Diagnostics:  {entry['diagnostic_msg']}")
        print("="*60 + "\n")
