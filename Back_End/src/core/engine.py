import asyncio
import time
import sys
import traceback
from src.core.state import AgentState
from src.core.llm_service import LLMService
from src.diagnostics.telemetry import StepTrace

class AutonomousAgentRuntime:
    def __init__(self, state: AgentState, config: dict):
        self.state = state
        self.config = config
        self.llm = LLMService(config=config)

    async def step_engine(self) -> bool:
        """Executes one state cycle asynchronously. Returns False to pause/terminate."""
        # 1. Non-blocking guard against active sleep schedules
        if self.state.status == "SLEEPING":
            if time.time() < self.state.wake_time:
                return False 
            self.state.status = "RUNNING"

        # 2. Lazy Planning Phase Initialization (Awaiting the async plan)
        if not self.state.plan:
            self.state.status = "RUNNING"
            self.state.plan = await self.llm.generate_plan(self.state.objective)
            self.state.save_checkpoint()
            return True

        # 3. Successful Goal Target Check
        if self.state.current_step_index >= len(self.state.plan):
            self.state.status = "COMPLETED"
            print("🎉 Objective achieved successfully.")
            self.state.save_checkpoint()
            return False

        current_step = self.state.plan[self.state.current_step_index]
        trace_node = StepTrace(step_name=current_step, step_index=self.state.current_step_index)
        
        try:
            # 4. Await the tool execution asynchronously (Non-blocking)
            result = await self.llm.execute_step(current_step, trace_node)
            trace_node.payload = result
            
            if trace_node.status == "CRITICAL_ERROR":
                raise ValueError(trace_node.diagnostic_msg)
                
            self.state.current_step_index += 1
            if self.state.current_step_index < len(self.state.plan):
                self.state.status = "SLEEPING"
                delay = self.config["throttling"].get("self_scheduling_delay", 2)
                self.state.wake_time = time.time() + delay
            
            self.state.trace_history.append(trace_node.to_dict())
            self.state.save_checkpoint()
            return True

        except Exception as e:
            self.state.status = "FAILED"
            if trace_node.status != "CRITICAL_ERROR":
                trace_node.status = "CRITICAL_ERROR"
                trace_node.error_code = type(e).__name__
                trace_node.diagnostic_msg = "".join(traceback.format_exception(*sys.exc_info()))
            
            self.state.trace_history.append(trace_node.to_dict())
            print(f"❌ Trajectory broken at step {self.state.current_step_index}.")
            self.state.save_checkpoint()
            return False
