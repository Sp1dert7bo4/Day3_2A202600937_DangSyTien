import os
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger


class ReActAgent:
    """
    A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Designed for OPTC Pirate Rumble strategy analysis.
    Implemented by Đặng Sỹ Tiến (2A202600937).
    """

    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 8):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        System prompt instructing the LLM to follow the ReAct format.
        Includes available tools and OPTC strategic context.
        """
        tool_descriptions = "\n".join(
            [f"  - {t['name']}: {t['description']}" for t in self.tools]
        )
        return f"""You are an expert OPTC (One Piece Treasure Cruise) Pirate Rumble strategist.
You help players build optimal PvP teams by analyzing enemies, finding counters, and maximizing synergy.

You have access to the following tools:
{tool_descriptions}

IMPORTANT RULES:
1. You MUST follow this EXACT format for every response:

Thought: <your strategic reasoning about what to do next>
Action: <tool_name>("<argument>")

2. After receiving an Observation, continue with another Thought/Action cycle.
3. When you have gathered enough information to give a final recommendation, respond with:

Thought: <your final reasoning>
Final Answer: <your complete team recommendation with explanation>

4. NEVER skip the Thought step. Always reason before acting.
5. Use tools strategically - analyze enemy first, then search for counters, then check synergy.
6. Do NOT make up information. Only use data from tool observations.
7. Always output in the EXACT format above. Do not add extra formatting around Action calls.

STRATEGIC PRIORITY ORDER:
1. Analyze enemy team composition and threats
2. Identify key debuffs to counter
3. Search for units with type advantage AND counter abilities
4. Check leader skill synergy before finalizing
5. Evaluate overall team plan"""

    def run(self, user_input: str) -> str:
        """
        Execute the ReAct loop:
        1. Generate Thought + Action from LLM.
        2. Parse Action and execute the corresponding Tool.
        3. Append Observation to conversation and repeat.
        4. Stop when Final Answer is found or max_steps reached.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})

        # Build conversation history as a growing prompt
        conversation = user_input
        steps = 0

        while steps < self.max_steps:
            # 1. Generate LLM response
            try:
                if steps > 0 and self.llm.__class__.__name__ == "GeminiProvider":
                    import time
                    time.sleep(12)  # Respect Gemini Free Tier 5 RPM rate limit
                result = self.llm.generate(conversation, system_prompt=self.get_system_prompt())
                response_text = result["content"]
            except Exception as e:
                logger.log_event("LLM_ERROR", {"step": steps, "error": str(e)})
                return f"Lỗi khi gọi LLM: {str(e)}"

            logger.log_event("LLM_RESPONSE", {
                "step": steps,
                "output": response_text[:500],
                "usage": result.get("usage", {}),
                "latency_ms": result.get("latency_ms", 0)
            })

            # Append LLM response to conversation
            conversation += f"\n{response_text}"

            # 2. Check for Final Answer → exit loop
            final_match = re.search(r"Final Answer:\s*(.+)", response_text, re.DOTALL)
            if final_match:
                answer = final_match.group(1).strip()
                logger.log_event("AGENT_FINAL_ANSWER", {"steps": steps + 1, "answer": answer[:300]})
                self.history.append({"input": user_input, "answer": answer, "steps": steps + 1})
                return answer

            # 3. Parse Action from LLM output
            # Support formats: Action: tool("arg") or Action: tool("arg1, arg2")
            action_match = re.search(r'Action:\s*(\w+)\(\s*"(.+?)"\s*\)', response_text)
            if not action_match:
                # Try without quotes: Action: tool(arg)
                action_match = re.search(r'Action:\s*(\w+)\(\s*(.+?)\s*\)', response_text)

            if action_match:
                tool_name = action_match.group(1)
                tool_args = action_match.group(2).strip().strip('"').strip("'")

                # 4. Execute the tool
                observation = self._execute_tool(tool_name, tool_args)
                logger.log_event("TOOL_CALL", {
                    "step": steps,
                    "tool": tool_name,
                    "args": tool_args,
                    "result_length": len(observation)
                })

                # 5. Append Observation to conversation for next iteration
                conversation += f"\nObservation: {observation}"
            else:
                # LLM didn't output a valid Action — prompt it to try again
                logger.log_event("PARSE_ERROR", {
                    "step": steps,
                    "output": response_text[:300]
                })
                conversation += "\nObservation: Error — could not parse your Action. Please use the exact format: Action: tool_name(\"argument\")"

            steps += 1

        # Max steps reached without Final Answer
        logger.log_event("AGENT_TIMEOUT", {"steps": steps})
        return "Đã đạt giới hạn bước suy luận. Agent không thể đưa ra kết luận trong số bước cho phép."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Execute a tool by name with the given arguments.
        Looks up the tool in the registry and calls its function.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                try:
                    return tool['function'](args)
                except Exception as e:
                    logger.log_event("TOOL_ERROR", {
                        "tool": tool_name,
                        "args": args,
                        "error": str(e)
                    })
                    return f"Lỗi khi chạy tool '{tool_name}': {str(e)}"
        return f"Tool '{tool_name}' không tồn tại. Các tools có sẵn: {', '.join(t['name'] for t in self.tools)}"
